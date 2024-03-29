from clockwork_croc.util import get_logger
from clockwork_croc.config import load_secrets
from clockwork_croc.croc import Croc
from clockwork_croc.disco_booter import DiscoBooter

logger = get_logger('app', level='INFO')


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

    booter = DiscoBooter(secrets)
    input


    croc = Croc()
    croc.authorize(secrets['discord'])
    croc.go_online()
    croc.get_my_guild()
    croc.get_my_channel()
    croc.say_hello()
    logger.info('Done.')


if __name__ == '__main__':
    main()
