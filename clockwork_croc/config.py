from os import path

import yaml
from hamcrest import assert_that, has_entries, instance_of

##
# Secrets

def load_secrets():
    app_dir_path = path.dirname(__file__)
    secrets_path = path.abspath(path.join(app_dir_path, '../.secrets.yaml'))
    if not path.exists(secrets_path):
        raise Exception(f'Cannot locate secrets! Expected "{secrets_path}" to exist.')

    with open(secrets_path, 'r') as secrets_file:
        parsed_secrets = yaml.load(secrets_file)

    assert_required_secrets_are_included(parsed_secrets)
    return parsed_secrets

def assert_required_secrets_are_included(secrets_dict):
    assert_that(
        secrets_dict,
        has_entries({
            'discord': has_entries({
                'client': has_entries({
                    'id': instance_of(str),
                    'secret': instance_of(str)
                }),
                'bot': has_entries({
                    'username': instance_of(str),
                    'token': instance_of(str)
                })
            })
        })
    )
