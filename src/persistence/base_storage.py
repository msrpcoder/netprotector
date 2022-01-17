import logging
import os
import shutil

import requests
from sqlalchemy.orm import Session
from abc import ABC, abstractmethod
from typing import Dict, List
from .fb import engine, Profile, es_client
from .utils import get_safe_file_path

logger = logging.getLogger()


class Storage(ABC):
    @abstractmethod
    def store(self, *args, **kwargs):
        pass


class BaseUserStorage(ABC):
    def store(self, profile_id, user_dtls):
        logger.info('saving profile details: %s', profile_id)
        self.save_profile_dtls(user_dtls['profile'])

        logger.info('saving friends for user: %s', profile_id)
        friends = user_dtls['friends']
        list(map(lambda friend: self.save_friend(profile_id, friend), friends))

        logger.info('saving posts for user: %s', profile_id)
        posts = user_dtls['posts']
        list(map(lambda post: self.save_post(profile_id, post), posts))

    def save_profile_dtls(self, profile_dtls):
        storage = self.get_profile_storage()
        storage.store(profile_dtls)

        logger.info('saved profile details.')

    def save_friend(self, profile_id: str, friends: List[Dict]):
        storage = self.get_friend_storage()
        storage.store(profile_id, friends)

        logger.info('saved friend details for profile id: %s.', profile_id)

    def save_post(self, profile_id: str, post: Dict):
        storage = self.get_posts_storage()
        post_id = post['post_id']
        storage.store(profile_id, post)

        logger.info('saved post details with id: %s, for profile: %s', post_id, profile_id)

    @staticmethod
    def get_profile_storage():
        return PostgresProfileStorage()

    @staticmethod
    def get_friend_storage():
        return ElasticSearchFriendsStorage()

    @staticmethod
    def get_posts_storage():
        return ElasticSearchPostsStorage()


class PostgresProfileStorage(Storage):
    def store(self, profile_dtls):
        with Session(engine) as session, session.begin():
            # check if profile object exists
            profile = session.query(Profile).where(Profile.id == profile_dtls['id']).first()
            if not profile:
                profile = Profile()
                profile.id = profile_dtls['id']

            profile.name = profile_dtls['Name']
            # add profile job details in postgres
            session.add(profile)
            # add profile in es
            es_client.index(index='profile', id=profile.id, document=profile_dtls)
            # download profile images
            image_store = ImageStorage()
            image_store.store(profile_id=profile.id, image_type='profile', url=profile_dtls['profile_picture'])

        logger.info('Persisted profile with id %s', profile_dtls['id'])


class ElasticSearchPostsStorage(Storage):
    def store(self, profile_id: str, posts_dtls: Dict):
        post_id = posts_dtls['post_id']
        es_client.index(index='posts', id=post_id, document=posts_dtls)

        images = posts_dtls['images']
        # download profile images
        image_store = ImageStorage()

        for image_url in images:
            image_store.store(profile_id=profile_id, image_type='posts', url=image_url)

        logger.info('Persisted %d posts with profile_id: %s', len(images), post_id)


class ElasticSearchFriendsStorage(Storage):
    def store(self, profile_id: str, friend: Dict):
        friend_id = friend['id']
        relationship_id = f'{profile_id}-{friend_id}'
        friend['source_profile'] = profile_id
        es_client.index(index='friends', id=relationship_id, document=friend)

        url = friend['profile_picture']
        image_storage = FriendsImageStorage()
        image_storage.store(profile_id=friend_id, image_type='friends', url=url)

        logger.info('Persisted friends for user: %s', relationship_id)


class ImageStorage(Storage):
    def store(self, profile_id: str, image_type: str, url: str):
        logger.info('Downloading image type: %s for profile: %s at url: %s', image_type, profile_id, url)

        resp_stream = requests.get(url, stream=True).raw
        base_dir = os.environ.get('IMAGE_STORE_DIR', '/home/pcs/images')
        image_type_dir = os.path.join(base_dir, profile_id, image_type)
        os.makedirs(image_type_dir, exist_ok=True)

        max_copies = 10000 if image_type == 'posts' else 10
        file_path = get_safe_file_path(image_type_dir, 'image', 'png', max_copies)

        with open(file_path, 'wb') as fp:
            shutil.copyfileobj(resp_stream, fp)

        logger.info('Persisted image type: %s for profile: %s at %s', image_type, profile_id, file_path)


class FriendsImageStorage(Storage):
    def store(self, profile_id: str, image_type: str, url: str):
        logger.info('Downloading friend"s image type: %s for profile: %s at url: %s', image_type, profile_id, url)

        resp_stream = requests.get(url, stream=True).raw
        base_dir = os.environ.get('IMAGE_STORE_DIR', '/home/pcs/images')
        image_type_dir = os.path.join(base_dir, image_type)
        os.makedirs(image_type_dir, exist_ok=True)

        file_path = get_safe_file_path(image_type_dir, f'image-f{profile_id}', 'png', 10)

        with open(file_path, 'wb') as fp:
            shutil.copyfileobj(resp_stream, fp)

        logger.info('Persisted friends" image type: %s for profile: %s at %s', image_type, profile_id, file_path)
