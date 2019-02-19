from itertools import cycle, islice

import gevent
from gevent import monkey
monkey.patch_all()

from disco.client import Client, ClientConfig
from disco.bot import Bot, BotConfig
from disco.voice.client import VoiceClient, VoiceState
from disco.voice.player import Player
from disco.voice.playable import BasePlayable

from clockwork_croc.util import get_logger, chain

logger = get_logger(__name__, level='DEBUG')


class DiscoBooter:
    def __init__(self, secrets, plugins=[]):
        self.secrets = secrets
        self.plugins = plugins

    @chain
    def boot(self):
        (self
            .build_client_config()
            .build_client()
            .build_bot()
            .run_forever()
        )

    def run_forever(self):
        return gevent.spawn(self.bot.run_forever).join()

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

    @chain
    def build_voice_client(self):
        server_id = self.secrets['server']['id']
        self.voice_client = VoiceClient(self.client, server_id)
