import logging
from abc import ABC, abstractmethod

logger = logging.getLogger(__file__)


class Scrapper(ABC):
    @abstractmethod
    def scrape(self):
        pass


class CredentialsMixin:
    _credentials = None

    @property
    def credentials(self):
        return self._credentials

    @credentials.setter
    def credentials(self, credentials):
        self._credentials = credentials


class UserDataScrapeMixin(ABC):
    @abstractmethod
    def get_profile_scrapper(self, credentials):
        pass

    @abstractmethod
    def get_friends_scrapper(self, credentials):
        pass

    @abstractmethod
    def get_posts_scrapper(self, credentials):
        pass


class UserDataScrapperBase(CredentialsMixin, Scrapper):
    def __init__(self, user_id, credentials, fetch_range=None):
        self._user_id = user_id
        self._orig_credentials = credentials
        self._credentials = credentials
        self._fetch_range = fetch_range

    def scrape(self):
        logger.info("Scrapping data for user: %s started.", self._user_id)
        scrapped_data = self.scrape_users_data()

        logger.info('Scrapping data for user: %s completed', self._user_id)

        return scrapped_data

    def scrape_users_data(self):
        scrapped_data = {}
        logger.info('Scrapping profile details for user %s', self._user_id)
        profile_scrapper = self.get_profile_scrapper(self.credentials)
        scrapped_data['profile'] = profile_scrapper.scrape()

        logger.info('Querying friends-list for user %s', self._user_id)
        friends_scrapper = self.get_friends_scrapper(profile_scrapper.credentials)
        scrapped_data['friends'] = list(friends_scrapper.scrape())
        logger.info('User %s has %d friends.', self._user_id, len(scrapped_data['friends']))

        logger.info('Querying list of posts for user %s', self._user_id)
        posts_scrapper = self.get_posts_scrapper(friends_scrapper.credentials)
        scrapped_data['posts'] = list(posts_scrapper.scrape())
        logger.info('User %s has %d posts.', self._user_id, len(scrapped_data['posts']))

        return scrapped_data


class UserDataScrapper(UserDataScrapeMixin, UserDataScrapperBase):
    pass
