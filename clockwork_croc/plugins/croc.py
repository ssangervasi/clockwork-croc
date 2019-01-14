from disco.bot import Plugin, Config

from clockwork_croc.util import get_logger, memoize

logger = get_logger('croc', level='DEBUG')

# from clockwork_croc.secrets import secrets


# class CrocPluginConfig(Config):
#     token = secrets['bot']['token']
# @Plugin.with_config(CrocPluginConfig)


class CrocPlugin(Plugin):
    guild_list = None

    @Plugin.command('ping')
    def command_ping(self, event):
        event.msg.reply('Pong!')

    @Plugin.listen('Ready')
    def on_ready(self, event):
        self.guild_list = event.guilds

    @Plugin.listen('MessageCreate')
    def on_message_create(self, event):
        message = event.message
        if message.channel.name != 'clockwork-croc':
            return

        message.reply('Snap snap!')

    @property
    def guild(self):
        guild_list = self.guild_list
        return guild_list[0] if guild_list else None

    @property
    def channel_list(self):
        return self.guild.channels if self.guild else []

    @property
    def my_channel(self):
        def summarize(channel):
            return f'''
                Channel "{channel.name}"
                    Id: {channel.id}
                    Type code: {channel.type.value}
                    Type name: {channel.type.name}
            '''

        summary = '\n'.join(map(summarize, self.channel_list))
        print(summary)
        logger.info(f'All channels:\n{summary}')

        my_channel_name = 'clockwork-croc'
        my_channel_list = [
            channel
            for channel in self.channel_list
            if channel.name == my_channel_name
        ]
        return my_channel_list[0] if len(my_channel_list) > 0 else None
