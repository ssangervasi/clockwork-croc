import re
from itertools import cycle, islice, tee, repeat, chain
from collections import namedtuple
from textwrap import dedent as dd

import gevent
from disco.bot import Plugin, Config
from disco.types.message import (
    MessageEmbed,
    MessageEmbedAuthor,
    MessageEmbedField,
    MessageEmbedFooter,
    MessageEmbedImage,
    MessageEmbedThumbnail,
    MessageEmbedVideo,
)

from clockwork_croc.util import get_logger, memoize

logger = get_logger('croc', level='DEBUG')


class CrocPlugin(Plugin):
    guild_id_list = []

    def __init__(self, *args, **kwargs):
        logger.info(f'Constructed CrocPlugin(args={args}, kwargs={kwargs})')
        super(self.__class__, self).__init__(*args, **kwargs)
        self.croc = Croc(self.client)

    @Plugin.command('ping')
    def command_ping(self, event):
        event.msg.reply('Pong!')

    @Plugin.listen('Ready')
    def on_ready(self, event):
        logger.info(f'On Ready event: {event}')
        self.croc.summarize_guilds(event.guilds)
        self.croc.guild_id_list = [guild.id for guild in event.guilds]
        self.croc.my_channel

    @Plugin.listen('MessageCreate')
    def on_message_create(self, event):
        message = event.message
        logger.info(f'On MessageCreate message: {message}')

        self.client.gw.events.emit('SnapSnap')
        self.croc.handle_message(message)

class Croc:
    my_channel_name = 'clockwork-croc'
    my_voice_channel_name = 'snap-snap'

    def __init__(self, client):
        self.client = client
        self.voice_client = None


    def handle_message(self, message):
        logger.info(f'Message {message.id}')

        handlers = [
            self.handle_ignore_self,
            self.handle_greeting,
            self.handle_fancy,
            self.handle_speak,
            self.handle_shut_up,
            self.handle_make_noise,
        ]

        result = message
        for handler in handlers:
            if result is None:
                break

            result = handler(result)

    def handle_ignore_self(self, message):
        should_ignore = not all([
            message.channel.id == self.my_channel.id,
            message.author.id != self.me.id
        ])
        return None if should_ignore else message
    
    def handle_greeting(self, message):
        if re.match(r'yo|hello|hi', message.content, re.I):
            message.reply('Snap snap!')
            return None
        return message

    def handle_fancy(self, message):
        if re.match(r'fancy', message.content, re.I):
            message.reply(embed=self.fancy_embed())
            return None
        return message

    def handle_speak(self, message):
        if re.match(r'speak|talk|join', message.content, re.I):
            self.voice_client = self.my_voice_channel.connect()
            logger.info(f'Joined with voice client {self.voice_client}')
            return None
        return message

    def handle_shut_up(self, message):
        if re.match(r'shut up|quiet|go away', message.content, re.I):
            self.voice_client.disconnect()
            return None
        return message

    def handle_make_noise(self, message):
        if not re.match(r'make noise', message.content, re.I):
            return message

        gevent.spawn(self.send_noise)

    def send_noise(self):
        logger.info('send_noise')
        if not self.voice_client:
            logger.info('send_noise no client')
            return

        self.voice_client.set_speaking(voice=True)
        # frames = repeat(bytearray(islice(cycle(range(100, 200)), 1_000)), 100)
        frames = repeat(bytearray(islice(cycle(chain(range(0, 200), range(200, 0))), 500)), 1_000)

        i = 0
        while self.voice_client:
            try:
                frame = next(frames)
            except StopIteration:
                break
            self.voice_client.send_frame(frame)
            self.voice_client.increment_timestamp(480)
            gevent.sleep(1.0/480)
            i += 1

        logger.info(f'send_noise loop done after {i} frames')

    @property
    @memoize
    def me(self):
        return self.client.api.users_me_get()

    @property
    def id_to_guild(self):
        return self.client.api.users_me_guilds_list()

    @property
    def my_guild(self):
        self.summarize_guilds(self.id_to_guild.values())
        return next(iter(self.id_to_guild.values()))

    @property
    @memoize
    def id_to_channel(self):
        return self.client.api.guilds_channels_list(self.my_guild.id)

    @property
    @memoize
    def my_channel(self):
        # self.summarize_channels(self.id_to_channel.values())
        my_channels = [
            channel
            for channel in self.id_to_channel.values()
            if channel.name == self.my_channel_name
        ]
        return my_channels[0] if len(my_channels) > 0 else None

    @property
    @memoize
    def my_voice_channel(self):
        my_voice_channels = [
            channel
            for channel in self.id_to_channel.values()
            if channel.name == self.my_voice_channel_name
        ]
        return my_voice_channels[0] if len(my_voice_channels) > 0 else None

    def fancy_embed(self):
        return MessageEmbed(
            title='Heck yes.',
            description=dd('''
                h1. Ho dang it's markdown 
                > ~ - ~ - ~ - ~ - 😎 ~ - ~ - ~ - ~ - 
            '''),
            url='https://caniuse.com/#search=marquee',
            # timestamp
            color=69_69_69,
            footer=dict(
                text=dd('''
                    *Markdown is my jam*
                    **JAAAAAAAAAAMMMMMMMM**
                ''')
            ),
            image=dict(url='https://cdn.discordapp.com/app-icons/530605657699909643/10496f03af9dbbd6e3669b50f7fc5cb4.png?size=512'),
            thumbnail=dict(url='https://cdn.discordapp.com/app-icons/530605657699909643/10496f03af9dbbd6e3669b50f7fc5cb4.png?size=64'),
            video=dict(url='https://youtu.be/sn8KYD1Vco0'),
            author=dict(name='Crock Daddy'),
            fields=[
                dict(
                    name='How we do',
                    value=dd('''
                        Things:
                            1. Like this
                            2. Like that
                            3. Like this
                    ''')
                ),
                dict(
                    name="Sometimes it's not markdown tho",
                    value=dd('''
                        ```python
                            def py():
                                raise 'Am I highlighted?'
                        ```

                        > Notice me, markdown
                    ''')
                )
            ]
        )

    def summarize_channels(self, channels):
        def summarize(channel):
            return f'''
                Channel "{channel.name}"
                    Id: {channel.id}
                    Type code: {channel.type.value}
                    Type name: {channel.type.name}
            '''

        summary = '\n'.join(map(summarize, channels))
        logger.info(f'Channels summary:\n{summary}')

    def summarize_guilds(self, guilds):
        def summarize(guild):
            return f'''
                Guild "{guild.name}"
                    Id: {guild.id}
                    Owner Id: {guild.owner_id}
                    # Channels: {len(guild.channels)}
            '''

        summary = '\n'.join(map(summarize, guilds))
        logger.info(f'Guilds summary:\n{summary}')
