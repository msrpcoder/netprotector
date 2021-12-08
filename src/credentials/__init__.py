import os
import json
import logging

logger = logging.getLogger(__file__)
credentials = None

with open(os.path.join(os.path.dirname(__file__), 'credentials.json')) as fp:
    credentials = json.load(fp)

logger.info("Loaded %d credentials.", len(credentials))


def lock_credential(current_credential):
    def credential_comparator(credential):
        return (credential['username'] == current_credential.get('username') or
                credential['password'] == current_credential.get('password'))

    current_credential = list(filter(credential_comparator, credentials))[0]
    current_credential['locked'] = True

    logger.info('Credential %s locked.', current_credential)


def get_credentials(current_credential={}):
    def credential_comparator(credential):
        return (credential['username'] != current_credential.get('username') or
                credential['password'] != current_credential.get('password')) and \
               not credential['locked']

    if current_credential:
        lock_credential(current_credential)

    available_credentials = filter(credential_comparator, credentials)
    return next(available_credentials)


__all__ = ('get_credentials', 'lock_credential', )
