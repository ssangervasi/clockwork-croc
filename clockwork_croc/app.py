from clockwork_croc.util import get_logger
from clockwork_croc.config import load_secrets
from clockwork_croc.croc import Croc

logger = get_logger('app', level='INFO')

##
# main
def main():
    logger.info('Starting main.')
    secrets = load_secrets()
    logger.info('Secrets all good.')
    croc = Croc()
    croc.authorize(secrets['discord'])
    croc.get_me()
    croc.get_my_guild()
    croc.get_my_general_channel()
    croc.say_hello()
    logger.info('Done.')

if  __name__ == '__main__':
    main()
