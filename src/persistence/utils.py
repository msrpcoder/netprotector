import os

from numpy.random.mtrand import randint


class ImproperlyConfiguredDataStoreError(Exception):
    pass


def get_pg_db_url(raise_error=False):
    pg_username = os.environ.get('PG_USERNAME', 'postgres')
    pg_password = os.environ.get('PG_PASSWORD', 'postgres')
    pg_host = os.environ.get('PG_HOST', 'localhost')
    pg_port = os.environ.get('PG_PORT', 5432)
    pg_db = os.environ.get('PG_DATABASE', 'postgres')

    if not (pg_username and pg_password) and raise_error:
        raise ImproperlyConfiguredDataStoreError('PG_USERNAME and PG_PASSWORD are not passed.')

    return f'postgresql://{pg_username}:{pg_password}@{pg_host}:{pg_port}/{pg_db}'


def get_safe_file_path(dir_name: str, file_name: str, ext: str, max_value: int = 10) -> str:
    file_path = os.path.join(dir_name, f'{file_name}.{ext}')
    if not os.path.exists(file_path):
        return file_path

    counter = 1
    while counter < max_value:
        file_path = os.path.join(dir_name, f'{file_name}-{counter}.{ext}')
        if not os.path.exists(file_path):
            break

        counter += 1

    random_counter = randint(1, max_value)
    file_path = os.path.join(dir_name, f'{file_name}-{random_counter}.{ext}')

    return file_path
