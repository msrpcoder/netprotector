# bootstrapper
import sys
import logging
from logging.handlers import RotatingFileHandler
from credentials import get_credentials
from scrapper import FBUserDataScrapper

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(stream=sys.stdout))
logger.addHandler(RotatingFileHandler('logs/logs.txt', maxBytes=1000000))

credentials = get_credentials()
scrapper = FBUserDataScrapper('100054383195035', credentials)

scrapped_results = scrapper.scrape()
