from gevent import monkey

monkey.patch_all()

from clockwork_croc.util import get_logger
from clockwork_croc.secrets import load_secrets
from clockwork_croc.croc import CrocPlugin

from clockwork_croc.disco_booter import DiscoBooter

logger = get_logger(__name__, level='DEBUG')


# def main():
#     logger.info('Starting main.')
#     secrets = load_secrets()
#     logger.info('Secrets all good.')
#     croc = Croc()
#     croc.authorize(secrets['discord'])
#     croc.go_online()
#     croc.get_my_guild()
#     croc.get_my_channel()
#     croc.say_hello()
#     logger.info('Done.')

def main():
    logger.info('Starting main.')
    
    secrets = load_secrets()['discord']
    logger.info('Secrets all good.')

    booter = DiscoBooter(
        secrets=secrets,
        plugins=[
            CrocPlugin
        ]
    )

    booter.boot()
    


    # croc = Croc()
    # croc.authorize(secrets['discord'])
    # croc.go_online()
    # croc.get_my_guild()
    # croc.get_my_channel()
    # croc.say_hello()
    # logger.info('Done.')


if __name__ == '__main__':
    main()
