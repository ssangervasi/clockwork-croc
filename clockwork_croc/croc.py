from disco import client

from clockwork_croc.util import get_logger, memoize

logger = get_logger('croc', level='DEBUG')

class Croc:
    api_root = furl('https://discordapp.com/api/v6')

    def authorize(self, discord_secrets):
        assert discord_secrets is not None

        client.ClientConfig(
            token=discord_secrets['bot']['token']
        )

        bot_username = discord_secrets['bot']['username']
        bot_token = discord_secrets['bot']['token']
        self.token = bot_token
        client_id = discord_secrets['client']['id']
        client_secret = discord_secrets['client']['secret']

        logger.info(f'Local stored username: {bot_username}')

        session = requests.Session()
        session.headers.update({
            'Authorization': f'Bot {bot_token}',
            'User-Agent': 'DiscordBot (www.example.com, 1)'
        })

        self.session = session

    def get(self, api_path):
        url = self.api_root.copy().join(api_path).url
        r = self.session.get(url)

        import json
        def pretty_json(d):
            return json.dumps(dict(d.items()), sort_keys=True, indent=4)

        logger.debug(f'Request Headers:\n{pretty_json(r.request.headers)}')
        logger.debug(f'Response Headers:\n{pretty_json(r.headers)}')
        r.raise_for_status()
        return r.json()

    @memoize
    def get_me(self):
        me_dict = self.get('users/@me')
        username = me_dict['username']
        logger.info(f'Authenticated username: {username}')
        return me_dict

    @memoize
    def get_my_guild(self):
        guild_list = self.get('users/@me/guilds')
        guild_name_list = [guild['name'] for guild in guild_list]
        logger.info(f'Guild names: {guild_name_list}')
        assert len(guild_list) > 0
        return guild_list[0]

    @memoize
    def get_my_general_channel(self):
        guild = self.get_my_guild()
        guild_id = guild['id']
        channel_list = self.get(f'guilds/{guild_id}/channels')
        
        from enum import Enum
        class ChannelType(Enum):
            GUILD_TEXT = 0
            DM = 1
            GUILD_VOICE = 2
            GROUP_DM = 3
            GUILD_CATEGORY = 4

        def summarize(channel):
            channel_type = ChannelType(channel['type'])
            return f'''
                Channel "{channel['name']}"
                    Type code: {channel_type.value}
                    Type name: {channel_type.name}
            '''

        summary = '\n'.join(map(summarize, channel_list))
        logger.info(f'All channels:\n{summary}')
        
        general_channel_list = [
            channel
            for channel in channel_list
            if (channel['name'] == 'general'
                and ChannelType(channel['type']) is ChannelType.GUILD_TEXT)
        ]
        assert len(general_channel_list) > 0
        return general_channel_list[0]

    @memoize
    def get_gateway(self):
        gateway_dict = self.get('gateway/bot')
        identify_dict = {
            2
        }
        {
          'token': self.token,
          'properties': {
            '$os': 'macos',
            '$browser': 'clockwork_crock',
            '$device': 'clockwork_crock'
          },
          'presence': {
            'status': 'online',
            'afk': False
          }
        }
        return gateway_dict

    def say_hello(self):
        self.get_gateway()
        general_channel = self.get_my_general_channel()
        channel_id = general_channel['id']
        url = self.api_root.copy().join(f'channels/{channel_id}/messages').url
        
        payload = {
            'content': 'Snap snap, muthafucka.',
            'nonce': 1, # Hard-coding this so I don't keep sending this message
            'tts': False
        }

        r = self.session.post(url, json=payload)
        r.raise_for_status()

