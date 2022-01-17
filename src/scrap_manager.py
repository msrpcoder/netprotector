import datetime
from typing import Dict

from persistence.fb import Profile
from scrapper import FBUserDataScrapper


class UserScrapeManager(object):
    """
    Responsibilities:
        1. Scrap details for user.
        2. Filter details by timestamp
        2. Store details for user.
        3. Update sync timings details for user.
        4. For each friend
            publish friend details to kafka consumer
    """
    def __init__(self, profile_id: str, credentials: Dict):
        self._profile_id = profile_id
        self._credentials = credentials

    def _filter_results(self, profile: Profile, scraped_results: Dict) -> Dict:
        if not profile:
            return scraped_results

        filtered_scrapped_results = scraped_results
        if profile.last_posts_sync:
            last_sync_date = datetime.datetime.strptime(profile.last_posts_sync, '%Y-%m-%d %H:%M:%S.%f')
            posts = scraped_results['posts']
            filtered_posts = list(filter(lambda post: post['time'] > last_sync_date, posts))
            for post in filtered_posts:
                post['time'] = str(post['time'])

            filtered_scrapped_results['posts'] = filtered_posts

        if profile.last_friends_sync:
            START FROM HERE(Fetch from ES, already saved_friends and filter out new friends)

    def start_sync_operation(self):
        # get last_sync details(if present)
        profile = Profile.get_by_id(self._profile_id)

        # start sync operation
        scrapper = FBUserDataScrapper('100054383195035', self._credentials)
        scrapped_results = scrapper.scrape()

        # filter results by last_sync operation details.
        filtered_scrapped_results = self._filter_results(profile)

        # store filtered results
        # update last_sync details
        # for each new friend:
        #   publish new message in kafka
        pass