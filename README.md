# JLCPCB Scraper

This is a Python module to scrape parts information from jlcpcb.com/parts.

## Installation

To install the dependencies, run:

```bash
pip install -r requirements.txt
```

## Usage


Create a Postgres DB and make sure it is reachable by the pc that will execute this script.
Set environment variable SQLALCHEMY_DATABASE_URI, JLCPCB_KEY and JLCPCB_SECRET
```
export SQLALCHEMY_DATABASE_URI=postgres://YourUserName:YourPassword@YourHostname:5432/YourDatabaseName
export JLCPCB_KEY=<KEY>
export JLCPCB_SECRET=<SECRET>
```

Execute main.py
```
python3 jlcpcb_scraper/main.py
``` 


## Testing TODO, INCOMPLETE

To run the tests, use the following command:

```bash
pytest tests
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)