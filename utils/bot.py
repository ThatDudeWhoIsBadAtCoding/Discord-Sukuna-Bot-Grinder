import discord
import asyncio
from utils.battler import Battler
from utils.fetch_cards import Card_Tree
import json
from utils.logger import Logger

# pip install -U --force-reinstall git+https://github.com/dolfies/discord.py-self.git

SUKUNA_ID = 1251024513487863921

class Selfbot(discord.Client):
    def __init__(self, base_channel, id, prefix):
        super().__init__()
        self.id = id
        self.activate_channel_id = base_channel
        self.prefix = prefix
        self.battler = None
        self.logger = None
    
    def settle(self, id):
        with open("config.json", "r") as file:
            data = json.load(file)
        data["base_channel_id"] = id
        with open("config.json", "w") as file:
            json.dump(data, file, indent=4)
        self.activate_channel_id = id
    
    def change_prefix(self, new_prefix):
        with open("config.json", "r") as file:
            data = json.load(file)
        data["prefix"] = new_prefix
        with open("config.json", "w") as file:
            json.dump(data, file, indent=4)
        self.prefix = new_prefix

    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message_edit(self, m1, m2):
        if m2.author.id == SUKUNA_ID and "lost" in m2.content and m2.channel.id == self.activate_channel_id and str(self.id) in m2.content:
            await asyncio.sleep(2)
            self.battler.losses += 1
            await self.battler.fight_battle(True)

    
    async def on_message(self, message):
        if ("switch" not in message.content and "settle" not in message.content) and  message.channel.id != self.activate_channel_id: return
        try:
            if message.author.id == SUKUNA_ID and self.battler.battling and message.embeds:
                await asyncio.sleep(2)
                self.battler.wins += 1
                await self.battler.fight_battle(True)
        except AttributeError:
            pass
        try:
            if message.author.id == SUKUNA_ID and message.flags.ephemeral and self.battler.active and not self.battler.battling:
                await message.channel.send("Seems like you forgot to use `/reset battle` you silly goose, fine...i'll do it for you smh")
                await asyncio.sleep(2)
                await self.battler.fight_battle(True)
        except AttributeError:
            pass
        try:
            if message.author.id == SUKUNA_ID and self.logger.logging and "Looks like you already own this card" in message.content and message.channel.id == self.activate_channel_id:
                c = message.content.split("**")[-2].split("> ")[-1]
                amount = message.content.split("`")[-2].split(": ")[-1]
                parent_card = self.logger.log(c, amount)
                if parent_card:
                    await message.channel.send(f"Oh, it seems like you needed this shard for {parent_card} Ace, cool....these are the sacrifices so far `{self.logger.sacrifices if self.logger.sacrifices else "Nothing lol"}`")
        except AttributeError:
            pass

        if not self.check_if_me(message): return

        if not message.content.startswith(self.prefix): return

        command_ = "".join(message.content.split(" ")[1:])
        command_ = command_.split(",")
        command, inputs = command_[0], command_[1:]
        # prefix command, input1, input2....

        match command:
            case "switch":
                self.activate_channel_id = message.channel.id
                await message.channel.send(f"Successfully swtiched to {message.channel.name}")
            case "battle":
                channel = await self.fetch_channel(self.activate_channel_id)
                self.battler = Battler(channel, int(inputs[0]))
                await self.battler.activate()
            case "stop":
                await message.channel.send(f"Stopped battles at {self.battler.battle_tokens} tokens, {self.battler.wins} wins and {self.battler.losses} losses")
                self.battler.active = False
            case "help":
                await message.channel.send(f"Hello, thank you for using this bot! Made by....actually let's not disclose that yet i'm gonna get banned. \nHere is how you can configure the bot to your needs without having to open the config file \n 1.`{self.prefix} switch` to switch the bot to the current channel, `{self.prefix} settle` to permanently change the bots default channel \n 2. `{self.prefix} prefix, new_prefix` to change prefix \n ")
            case "tree":
                tree = Card_Tree(inputs[0], inputs[1])
                # \u2014
                await message.channel.send(f"```{tree.get_card_tree()}```")
            case "settle":
                self.settle(message.channel.id)
                await message.channel.send(f"Successfully altered base ID to `{message.channel.name}` (ID = `{message.channel.id}`)")
            case "track":
                tree = Card_Tree(inputs[0], inputs[1])
                res = tree.track_ace()
                if res == -1:
                    await message.channel.send(f"{tree.name} Ace {tree.ace} is already being tracked  directly or in another ace!")
                else:
                    await message.channel.send(f"You are now tracking {tree.name} Ace {tree.ace}") 
            case "untrack":      
                tree = Card_Tree(inputs[0], inputs[1])
                tree.untrack_ace()
                await message.channel.send(f"Untracked {tree.name} Ace {tree.ace}") 
            case "log":
                self.logger = Logger(inputs[0] if len(inputs) else 9)
                await message.channel.send(f"Now logging pulls, Pulls: {self.logger.pulls}")
            case "sacrifice":
                if self.logger:
                    await message.channel.send(f"Here are the sacrifices `{self.logger.sacrifices}`")
            case "unlog":
                if self.logger:
                    await message.channel.send(f"DONE LOGGING, here are the final sacrifices `{self.logger.sacrifices}`")
                    del self.logger
            case "prefix":
                old_prefix = self.prefix
                self.change_prefix(inputs[0])
                await message.channel.send(f"Successfully chaged from {old_prefix} to {self.prefix}")

        
    def check_if_me(self, message):
        return message.author.id == self.id

