import os
import logging
import time
from datetime import datetime, timedelta
from dataclasses import dataclass, field

import requests
from requests.adapters import HTTPAdapter
from fake_useragent import UserAgent
from bs4 import BeautifulSoup, SoupStrainer

from models import Part, Category, create_or_update_category, create_or_update_part

logger = logging.getLogger(__name__)


JLCPCB_KEY = os.environ.get("JLCPCB_KEY")
JLCPCB_SECRET = os.environ.get("JLCPCB_SECRET")


class JlcpcbScraper:
    def __init__(self, base_url='https://jlcpcb.com/parts', categories: list[Category] = []):
        self.session = requests.Session()
        ua = UserAgent()
        self.session.headers.update({
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate",
            "Host": "jlcpcb.com",
            "User-Agent": str(ua.chrome),
        })
        self.session.mount('https://', HTTPAdapter(max_retries=3))
        self.base_url = base_url
        self.session.get(self.base_url)
        self.all_links = []
        self.categories: list[Category] = categories
        self.token: str | None = None
        self.token_expires: datetime | None = None
        self.key = JLCPCB_KEY
        self.secret = JLCPCB_SECRET
        self._obtain_token()
        logger.info('JlcpcbScraper initialized')

    def _obtain_token(self) -> None:
        if not self.key or not self.secret:
            raise RuntimeError("JLCPCB_KEY and JLCPCB_SECRET environment variables must be set")
        body = {
            "appKey": self.key,
            "appSecret": self.secret
        }
        headers = {
            "Content-Type": "application/json",
        }
        resp = requests.post("https://jlcpcb.com/external/genToken",
            json=body, headers=headers)
        if resp.status_code != 200:
            raise RuntimeError(f"Cannot obtain token {resp.json()}")
        data = resp.json()
        if data["code"] != 200:
            raise RuntimeError(f"Cannot obtain token {data}")
        self.token = data["data"]
        self.session.headers.update({
            "externalApiToken": self.token,
        })
        self.token_expires = datetime.now() + timedelta(seconds=1800)

    def get_all_links(self):
        response = self.session.get(self.base_url+'/all-electronic-components')
        soup = BeautifulSoup(response.text, 'html.parser')
        for link in soup.find_all('a', href=True):
            if '/parts/1st/' in link['href'] or '/parts/2nd/' in link['href']:
                self.all_links.append(link['href'])
        logger.info('All links fetched')
    
    def extract_categories(self, session, response):
        new_categories = []
        for component in response.get('data', {}).get('componentInfos', []):
            category_name = component.get('firstCategory')
            subcategory_name = component.get('secondCategory')
            if not self.category_exists(subcategory_name):
                new_category = Category(name=category_name, subcategory_name=subcategory_name)
                category = create_or_update_category(session, new_category)
                if category not in self.categories:
                    new_categories.append(new_category)
                    self.categories.append(new_category)
        yield [], new_categories

    def get_parts(self, session):
        # first query
        response = self.session.post('https://jlcpcb.com/external/component/getComponentInfos')
        if response.status_code != 200:
            logger.error(f"Cannot obtain parts {response.json()}")
            raise RuntimeError(f"Cannot obtain parts {response.json()}")
        response = response.json()
        if not response.get("code") == 200:
            logger.error(f"Cannot obtain parts {response}")
            raise RuntimeError(f"Cannot obtain parts {response}")
        if not response.get('data', {}).get('componentInfos', []):
            yield None, None
            return
        yield from self.extract_categories(session, response)
        self.parse_pagination(response)
        yield from self.parse_parts(session, response)
        # subsequent page queries
        request_count = 1
        while response['data']['componentInfos']:
            time.sleep(0.2)
            logger.info(f'Fetching page {request_count}')
            request_count + 1
            response = self.session.post('https://jlcpcb.com/external/component/getComponentInfos', data={"lastKey": self.last_key})
            if response.status_code != 200:
                logger.error(f"Cannot obtain parts, status code not 200: {response}")
                yield None, None
                return
            response = response.json()
            if not response.get("code") == 200:
                logger.error(f"Cannot obtain parts, internal status code not 200: {response}")
                yield None, None
                return
            if response.get('data', {}).get('componentInfos', []) is None:
                yield None, None
                logger.info('No more parts to fetch')
            yield from self.extract_categories(session, response)
            self.parse_pagination(response)
            yield from self.parse_parts(session, response)
            if self.token_expires < datetime.now():
                self._obtain_token()

    def parse_parts(self, session, response):
        parts = response['data']['componentInfos']
        all_categories = []
        all_parts = []
        for part in parts:
            if  part['stock'] == 0:
                continue
            part_subcategory = part['secondCategory']
            if not self.category_exists(part_subcategory):
                new_category = Category(name=part['firstCategory'], subcategory_name=part_subcategory)
                category = create_or_update_category(session, new_category)
                if category not in self.categories:
                    all_categories.append(new_category)
                    self.categories.append(new_category)
            subcategory_id = self.get_category(part_subcategory).id
            part_price = self.get_part_price(part['price'])
            part_instance = Part(
                lcsc=part['lcscPart'],
                category_id=subcategory_id,
                mfr=part['mfrPart'],
                package=part['package'],
                joints=int(part['solderJoint']),
                manufacturer=part['manufacturer'],
                basic=part['libraryType'] == 'base',
                description=part['description'],
                datasheet=part['datasheet'],
                stock=int(part['stock']),
                price=part_price,
                last_update=datetime.now()  # Replace with the actual value based on your logic
            )
            all_parts.append(part_instance)
            create_or_update_part(session, part_instance)

        # Add parts to subcategories
        yield all_parts, all_categories

    def parse_pagination(self, response):
        self.last_key = response.get('data', {}).get('lastKey', None)
        if not self.last_key:
            raise RuntimeError("Cannot obtain last key")
        
    def get_part_price(self, price: str) -> float | None:
        '''
        string input example: "'20-180:0.004285714,200-780:0.003485714,1600-9580:0.002771429,800-1580:0.003042857,9600-19980:0.002542857,20000-:0.002414286'"
        output example: 0.004285714
        '''
        try:
            if not price:
                return None
            price = price.split(',')
            price = price[0].split(':')
            return float(price[1])
        except Exception as e:
            logger.error(f'Error parsing price: {e}')
            return None
    
    def category_exists(self, subcategory_name: str) -> bool:
        return any([category.subcategory_name == subcategory_name for category in self.categories])
    
    def get_category(self, subcategory_name: str) -> Category | None:
        return next((category for category in self.categories if category.subcategory_name == subcategory_name), None)
    
    def get_category_by_id(self, category_id: int) -> Category | None:
        return next((category for category in self.categories if category.id == category_id), None)


if __name__ == '__main__':
    scraper = JlcpcbScraper()
    scraper.get_parts()
    # save to pkl file
    import pickle
    with open('jlcpcb.pkl', 'wb') as f:
        pickle.dump(scraper.categories, f)