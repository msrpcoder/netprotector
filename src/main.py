# bootstrapper
import sys
import logging
from logging.handlers import RotatingFileHandler
from credentials import get_credentials
from scrapper import FBUserDataScrapper
from persistence import BaseUserStorage

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(stream=sys.stdout))
logger.addHandler(RotatingFileHandler('logs/logs.txt', maxBytes=1000000))

credentials = get_credentials()
scrapper = FBUserDataScrapper('100054383195035', credentials)

if False:
    scrapped_results = scrapper.scrape()
else:
    import json
    with open('/home/pcs/data.json', 'r') as fp:
        scrapped_results = json.load(fp)

dao = BaseUserStorage()
dao.store(profile_id='100054383195035', user_dtls=scrapped_results)
