from clockwork_croc.util import get_logger
from clockwork_croc.config import load_secrets
from clockwork_croc.croc import Croc

logger = get_logger('app', level='INFO')


def main():
    logger.info('Starting main.')
    secrets = load_secrets()
    logger.info('Secrets all good.')
    croc = Croc()
    croc.authorize(secrets['discord'])
    croc.go_online()
    croc.get_my_guild()
    croc.get_my_channel()
    croc.say_hello()
    logger.info('Done.')


if __name__ == '__main__':
    main()

class DiscoBooter:
    import argparse

    from disco.client       import Client, ClientConfig
    from disco.bot          import Bot, BotConfig
    from disco.util.logging import setup_logging

    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.args = self.parser.parse_args()

    def main(self):
        self.build_client_config()
        
        if self.auto_shard(): return
        
        self.build_client()
        self.build_bot()        
        return self

    def build_client_config(self):
        logger.INFO('TODO: Add specific configs instead of using default.')

        config = ClientConfig()

        args = self.args
        for arg_key, config_key in six.iteritems(CONFIG_OVERRIDE_MAPPING):
            if getattr(args, arg_key) is not None:
                setattr(config, config_key, getattr(args, arg_key))

        self.config = config
        return self

    def build_client(self):
        self.client = Client(self.config)

    def build_bot(self):
        bot = None
        if args.run_bot or hasattr(config, 'bot'):
            bot_config = BotConfig(config.bot) if hasattr(config, 'bot') else BotConfig()
            if not hasattr(bot_config, 'plugins'):
                bot_config.plugins = args.plugin
            else:
                bot_config.plugins += args.plugin

            bot = Bot(client, bot_config)

        self.bot = bot
        return self

    def run(self):
        runner = (self.bot or self.client)
        runner.run_forever()

    def auto_shard(self):
        from disco.gateway.sharder import AutoSharder
        
        AutoSharder(self.config)


