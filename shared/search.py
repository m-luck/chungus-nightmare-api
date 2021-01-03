import discord
import tweepy
import sys
from shared import secrets
import cryptocompare
import cronus.beat as beat
from gptreplyguy.gpt_helpers import char_swap, randomize_capitalization

auth = tweepy.AppAuthHandler(secrets.twitter_api_key, secrets.twitter_api_secret)
api = tweepy.API(auth)

class TwitterMonitor(discord.Client):

    def clean_input(self, message):
        uni_ = ''.join([i if ord(i) < 128 else '' for i in str(message.content)])
        prompt = " ".join(uni_.split())
        return prompt
        
    def search(self, term, count=10):
        results = [
            tweet.full_text
            for tweet 
            in tweepy.Cursor(api.search, q=term, tweet_mode="extended").items(count)
        ]
        return results
    
    def strip_extra(self, text, mentions=True, links=True, hash=True, rt=True):
        if mentions: 
            word_list = text.split(' ')
            text = ' '.join([word for word in word_list if not word.startswith('@')])
        if links:
            word_list = text.split(' ')
            text = ' '.join([word for word in word_list if not word.startswith('http') and not word.startswith('\nhttp')])
        if hash:
            word_list = text.split(' ')
            text = ' '.join([word for word in word_list if not word.startswith('#')])
        if rt:
            word_list = text.split(' ')
            text = ' '.join([word for word in word_list if not word.startswith('RT')])
        word_list = text.split(' ')
        text = ' '.join([word for word in word_list if not word.endswith('…') and not word.startswith('&')])
        return text

    def get_human_search_results(self, term, count=1):
        res = self.search(term, count)
        if res:
            return char_swap(
                randomize_capitalization(
                    '\n----------------------------\n'.join(
                        [self.strip_extra(seq) for seq in res]
                    )
                )
            )
        else: 
            return " .."

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    async def on_message(self, message):
        if (
            message.author.id == self.user.id or 
            not message.channel.name.startswith('chungus')
        ):
            return

        prompt = self.clean_input(message)
        print("PROMPT:", prompt)
        async with message.channel.typing():
            response = self.get_human_search_results(prompt)
            print("RESPONSE:", response)
            if not response: 
                response = ".."
            await message.channel.send(response)


class CryptoMonitor(discord.Client):

    alarm_threshold = 1.2 * 6  # 1% in 20 minutes is yuge.
    alarm_emoji = '💥' 
    tickers = [
        'BTC',
        'ETH',
    ]

    def get_human_search_results(self, old_vals=None):
        prices = cryptocompare.get_price(self.tickers, curr='USD', full=False)

        price_perc_diff = None
        if old_vals:
            price_perc_diff = [
                (
                    (val['USD'] / old_vals[name]['USD']) * 100
                ) - 100
                for name, val 
                in prices.items()
            ] 
        price_strs = [
            f"{name}: ${val['USD']}"
            for name, val 
            in prices.items()
        ] 

        suffixes = []
        if price_perc_diff:
            prefixes = ['+' if diff > 0 else '' for diff in price_perc_diff] 
            suffixes = [
                self.alarm_emoji if abs(diff) > self.alarm_threshold else ''
                for diff in price_perc_diff
            ] 
            price_strs = [
                f"{s} ({prefixes[i]}{price_perc_diff[i]:.5f}%) {suffixes[i]}"
                for i, s
                in enumerate(price_strs)
            ] 
        return (
            '\n'.join(price_strs) + '\n-------\n',
            prices,
            self.alarm_emoji in suffixes
        )

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

        for guild in self.guilds:
            for channel in guild.text_channels:
                if channel.name == 'shitcoins-hyperchin-x':
                    with channel.typing():
                        await channel.send('I have been told it is nighttime. Shortening update interval to every 2 hours.')
        old_vals = await self.act()
        every_n_seconds = 20 * 60 * 6
        beat.set_rate(1/every_n_seconds)
        while beat.true():
            new_vals = await self.act(old_vals=old_vals)
            old_vals = new_vals
            beat.sleep() 

    async def act(self, old_vals=None):
        prices, old_vals, in_alarm = self.get_human_search_results(old_vals)
        text_channel_list = []
        for guild in self.guilds:
            for channel in guild.text_channels:
                if channel.name == 'shitcoins-hyperchin-x':
                    with channel.typing():
                        await channel.send(prices)
                        return old_vals
    
    # async def on_message(self, message):
    #     if (
    #         message.author.id == self.user.id or 
    #         not message.channel.name.startswith('marmot')
    #     ):
    #         return

    #     prompt = self.clean_input(message)
    #     print("PROMPT:", prompt)
    #     async with message.channel.typing():
    #         response = self.get_human_search_results(prompt)
    #         print("RESPONSE:", response)
    #         if not response: 
    #             response = ".."
    #         await message.channel.send(response)