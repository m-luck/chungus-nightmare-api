import random
import time
import discord
import gptreplyguy.gpt_helpers as gpt_helpers

one_in = 10

class GPTReplyGuy(discord.Client):
    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    def clean(self, message):
        return prompt

    async def on_message(self, message):
        if message.author.id == self.user.id:
            return

        async with message.channel.typing():
            chance = one_in
            if one_in == chance:
                uni_ = ''.join([i if ord(i) < 128 else '' for i in str(message.content)])
                prompt = " ".join(uni_.split())
                print("PROMPT:", prompt)
                response = gpt_helpers.generate_response(prompt)
                print("RESPONSE:", response)
                await message.channel.send(response)