import discord
import asyncio
from battler import Battler

# pip install -U --force-reinstall git+https://github.com/dolfies/discord.py-self.git

SUKUNA_ID = 1251024513487863921

class Selfbot(discord.Client):
    def __init__(self, base_channel, prefix):
        super().__init__()
        self.id = 1214908731180191758
        self.activate_channel_id = base_channel
        self.prefix = prefix
        self.battler = None

    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message_edit(self, m1, m2):
        if m2.author.id == SUKUNA_ID and "lost" in m2.content and self.battler:
            await asyncio.sleep(2)
            self.battler.losses += 1
            await self.battler.fight_battle(True)

    
    async def on_message(self, message):
        if "switch" not in message.content and  message.channel.id != self.activate_channel_id: return

        if message.author.id == SUKUNA_ID and self.battler.battling and message.embeds:
            await asyncio.sleep(2)
            self.battler.wins += 1
            await self.battler.fight_battle(True)

        if not self.check_if_me(message): return

        if not message.content.startswith(self.prefix): return

        command_ = "".join(message.content.split(" ")[1:])
        command_ = command_.split(",")
        command, inputs = command_[0], command_[1:]

        match command:
            case "switch":
                self.activate_channel_id = message.channel.id
                await message.channel.send(f"Successfully swtiched to {message.channel.name}")
            case "battle":
                channel = await self.fetch_channel(self.activate_channel_id)
                self.battler = Battler(channel, int(inputs[0]))
                await self.battler.activate()
            case "help":
                await message.channel.send(f"Hi! Thanks for using this bot (By activating you consider Manami our lord and savior). The basic format for the battle auto_grinder is `{self.prefix} battle, amount of tokens` ...amount of reset tokens is 1 more thna the amount of battle fought. Be sure to use `/battle reset` before activating the command")

                
    def check_if_me(self, message):
        return message.author.id == self.id

