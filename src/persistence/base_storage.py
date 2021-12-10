import logging
from abc import ABC, abstractmethod

logger = logging.getLogger()


class Storage(ABC):
    @abstractmethod
    def store(self, *args, **kwargs):
        pass


class BaseUserStage(ABC):
    def save(self, profile_id, user_dtls):
        logger.info('saving profile details: %d', profile_id)
        self.save_profile_dtls(user_dtls['profile'])

        logger.info('saving friends for user: %d', profile_id)
        friends = user_dtls['friends']
        list(map(lambda friend: self.save_friend(friend), friends))

        logger.info('saving posts for user: %d', profile_id)
        posts = user_dtls['posts']
        list(map(lambda post: self.save_post(post)), posts)

    def save_profile_dtls(self, profile_dtls):
        storage = self.get_profile_storage()
        storage.store(profile_dtls)

        logger.info('saved profile details.')

    @abstractmethod
    def save_friend(self, friend):
        storage = self.get_profile_storage()
        profile_id = friend['id']
        storage.store(friend)

        logger.info('saved friend details with id: %d.', profile_id)

    @abstractmethod
    def save_post(self, post):
        storage = self.get_posts_storage()
        storage_id = post['post_id']
        storage.store(storage_id)

        logger.info('saved post details with id: %d', storage_id)

    @abstractmethod
    def get_profile_storage(self):
        pass

    @abstractmethod
    def get_friend_storage(self):
        pass

    @abstractmethod
    def get_posts_storage(self):
        pass
