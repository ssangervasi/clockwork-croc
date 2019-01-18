from clockwork_croc.disco_booter import DiscoBooter
from clockwork_croc.util import get_logger
from clockwork_croc.secrets import load_secrets
from clockwork_croc.croc import CrocPlugin


logger = get_logger(__name__, level='DEBUG')


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

if __name__ == '__main__':
    main()
