from textwrap import dedent as dd

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

# from clockwork_croc.secrets import secrets


# class CrocPluginConfig(Config):
#     token = secrets['bot']['token']
# @Plugin.with_config(CrocPluginConfig)


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
        should_reply = self.croc.should_reply(message)
        logger.info(f'Message {message.id} | Should_reply: {should_reply}')
        if not should_reply:
            return

        message.reply('Snap snap!', embed=self.croc.fancy_embed())


class Croc:
    my_channel_name = 'clockwork-croc'

    def __init__(self, client):
        self.client = client

    def should_reply(self, message):
        return all([
            message.channel.id == self.my_channel.id,
            message.author.id != self.me.id
        ])

    @property
    @memoize
    def me(self):
        return self.client.api.users_me_get()

    @property
    def id_to_guild(self):
        return self.client.api.users_me_guilds_list()
        # guilds = [
        #     self.client.api.guilds_get(guild_id)
        #     for guild_id in self.guild_id_list
        # ]
        # logger.debug(f'Guild dict {guilds[0].to_dict()}')
        # self.summarize_guilds(guilds)
        # return guilds

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
        self.summarize_channels(self.id_to_channel.values())
        my_channels = [
            channel
            for channel in self.id_to_channel.values()
            if channel.name == self.my_channel_name
        ]
        return my_channels[0] if len(my_channels) > 0 else None

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
        '''
        MessageEmbed,
        MessageEmbedAuthor,
        MessageEmbedField,
        MessageEmbedFooter,
        MessageEmbedImage,
        MessageEmbedThumbnail,
        MessageEmbedVideo,
        '''
        """
        return MessageEmbed(
            title='Heck yes.',
            description=dd('''
                <blink>Does outdated HTML Work?</blink>
                <marquee>~ - ~ - ~ - ~ - 😎 ~ - ~ - ~ - ~ - </marquee>
            '''),
            url='https://caniuse.com/#search=marquee',
            # timestamp
            color=69_69_69,
            footer=MessageEmbedFooter(
                text=dd('''
                    <strong>I've got to left feet</stong>
                    <div style="background: pink">
                        And I'm all out of bublegum...
                    </div>
                ''')
            ),
            image=MessageEmbedImage(url='https://cdn.discordapp.com/app-icons/530605657699909643/10496f03af9dbbd6e3669b50f7fc5cb4.png?size=512'),
            thumbnail=MessageEmbedThumbnail(url='https://cdn.discordapp.com/app-icons/530605657699909643/10496f03af9dbbd6e3669b50f7fc5cb4.png?size=64'),
            video=MessageEmbedVideo(url='https://youtu.be/sn8KYD1Vco0'),
            author=MessageEmbedAuthor(name='Crock Daddy'),
            fields=[
                MessageEmbedField(
                    name='How we do',
                    value=dd('''
                        <ol>
                            <li>Like this</li>
                            <li>Like that</li>
                            <li>Like this</li>
                        </ol>
                    ''')
                )
            ]
        )
        """

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
