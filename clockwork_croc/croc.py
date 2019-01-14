from disco.bot import Plugin, Config

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

    @Plugin.listen('MessageCreate')
    def on_message_create(self, event):
        message = event.message
        logger.info(f'On MessageCreate message: {message}')
        should_reply = self.croc.should_reply(message)
        logger.info(f'Message {message.id} | Should_reply: {should_reply}')
        if not should_reply: return

        messag
        e.reply('Snap snap!')

class Croc:
    my_channel_name = 'clockwork-croc'

    def __init__(self, client):
        self.client = client
        self.guild_id_list = []

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
    def guilds(self):
        guilds = [
            self.client.api.guilds_get(guild_id)
            for guild_id in self.guild_id_list
        ]
        logger.debug(f'Guild dict {guilds[0].to_dict()}')
        self.summarize_guilds(guilds)
        return guilds
    
    @property
    def my_guild(self):
        return self.guilds[0]

    @property
    @memoize
    def channels(self):
        return self.client.api.guilds_channels_list(self.my_guild.id)

    @property
    @memoize
    def my_channel(self):
        self.summarize_channels(self.channels)
        my_channels = [
            channel
            for channel in self.channels
            if channel.name == self.my_channel_name
        ]
        return my_channels[0] if len(my_channels) > 0 else None

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