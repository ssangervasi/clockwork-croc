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
            .build_voice_client()
            .build_crocky_talky()
            .run_forever()
        )

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
    
    @chain
    def build_crocky_talky(self):
        voice_channel_id = self.secrets['server']['voice_channel_id']
        self.crocky_talky = CrockyTalky(self.voice_client, voice_channel_id)

    def run_forever(self):
        bot_thread = gevent.spawn(self.bot.run_forever)
        crocky_talky_thread = gevent.spawn(self.crocky_talky.run_forever)
        gevent.joinall([bot_thread, crocky_talky_thread])
        # gevent.joinall([crocky_talky_thread])


class CrockyTalky:
    def __init__(self, voice_client, voice_channel_id):
        self.voice_client = voice_client
        self.client = voice_client.client
        self.voice_channel_id = voice_channel_id
        self.speaking = False

    def run_forever(self):
        logger.info('CrockyTalky running')
        self.client.gw.events.on('SnapSnap', self.on_snap_snap)
        self.client.gw.events.on('VoiceSpeaking', self.on_voice_speaking)
        while True:
            if self.voice_client.state == VoiceState.CONNECTED:
                logger.info('Connected')
            else:
                logger.info('Not connected')
            gevent.sleep(1)

    def on_snap_snap(self):
        logger.info(f'Snap snap')
        if self.voice_client.state != VoiceState.CONNECTED:
            self.voice_client.connect(self.voice_channel_id)
            return

        self.speaking = not self.speaking
        self.voice_client.set_speaking(voice=self.speaking)

    def on_voice_speaking(self, event):
        logger.info(f'Speaking: {event}')
        # self.voice_client.connect(self.voice_channel_id)
