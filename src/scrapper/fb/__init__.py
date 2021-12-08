import logging
from datetime import datetime
from facebook_scraper import _scraper, exceptions, get_posts

from credentials import get_credentials
from scrapper.base import UserDataScrapper, Scrapper, CredentialsMixin, UserDataScrapperBase

logger = logging.getLogger(__file__)


class FBLoginMixin:
    def login(self):
        credentials = self.credentials
        while True:
            try:
                logger.info("Trying to login using credentials %s", credentials)
                _scraper.login(credentials['username'], credentials['password'])
            except exceptions.LoginError as err:
                logger.exception(err)
                try:
                    credentials = get_credentials(credentials)
                    self.credentials = credentials
                except StopIteration:
                    logger.error('All credentials locked.')
                    raise err
            else:
                logger.info("Logged in successfully using %s", credentials)
                break


class FBProfileDataScrapper(FBLoginMixin, UserDataScrapperBase):
    def scrape(self):
        self.login()
        profile = _scraper.get_profile(self._user_id)

        return profile


class FBFriendsListScraper(FBLoginMixin, UserDataScrapperBase):
    def scrape(self):
        self.login()
        friends = _scraper.get_friends(self._user_id)

        return friends


class FBPostsScraper(FBLoginMixin, UserDataScrapperBase):
    def scrape(self):
        self.login()
        posts = get_posts(self._user_id, page_limit=1000)

        if self._fetch_range:
            start_time = self._fetch_range.get('start_time')
            end_time = self._fetch_range.get('end_time')

            filtered_posts = []
            for post in posts:
                allow_posts = True
                if start_time:
                    allow_posts = post['time'] > datetime.utcfromtimestamp(start_time)

                if end_time:
                    allow_posts = post['time'] < datetime.utcfromtimestamp(end_time)

                if allow_posts:
                    filtered_posts.append(post)

            logger.info('Filtered %d/%d posts', len(filtered_posts), len(posts))
            return filtered_posts
        return posts


class FBUserDataScrapper(UserDataScrapper):
    def get_profile_scrapper(self, credentials):
        return FBProfileDataScrapper(self._user_id, credentials)

    def get_friends_scrapper(self, credentials):
        return FBFriendsListScraper(self._user_id, credentials)

    def get_posts_scrapper(self, credentials):
        return FBPostsScraper(self._user_id, credentials)
