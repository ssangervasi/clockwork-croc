from gevent import monkey

monkey.patch_all()

from disco.client       import Client, ClientConfig
from disco.bot          import Bot, BotConfig

from clockwork_croc.util import get_logger, chain

logger = get_logger(__name__, level='DEBUG')


class DiscoBooter:
    
    def __init__(self, secrets, plugins=[]):
        self.secrets = secrets
        self.plugins = plugins

    @chain
    def boot(self):
        self.build_client_config()
        self.build_client()
        self.build_bot()
        self.run_forever()

    @chain
    def build_client_config(self):
        logger.info('TODO: Add specific configs instead of using default.')

        token = self.secrets['bot']['token']
        config = ClientConfig({'token': token})

        self.config = config

    @chain
    def build_client(self):
        self.client = Client(self.config)

    @chain
    def build_bot(self):
        self.build_bot_config()
        self.bot = Bot(self.client, self.bot_config)
        map(self.bot.add_plugin, [
            plugin(self.bot, None)
            for plugin in self.plugins
        ])

    @chain
    def build_bot_config(self):
        self.bot_config = BotConfig()

    def run_forever(self):
        self.bot.run_forever()
        # self.client.run_forever()

    def auto_shard(self):
        from disco.gateway.sharder import AutoSharder
        
        AutoSharder(self.config)


