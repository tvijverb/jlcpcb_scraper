import unittest
from jlcpcb_scraper.scraper import JlcpcbScraper

class TestJlcpcbScraper(unittest.TestCase):
    def setUp(self):
        self.scraper = JlcpcbScraper()

    def test_get_parts(self):
        # TODO
        pass

if __name__ == '__main__':
    unittest.main()