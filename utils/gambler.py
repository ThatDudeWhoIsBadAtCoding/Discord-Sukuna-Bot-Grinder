import asyncio

class Gambler():
    def __init__(self, channel, amount):
        self.gamble_command_id = 1270476097745584148
        self.gamble_amount = amount
        self.channel = channel
        self.gamble_command = None

    async def activate(self):
        if self.gamble_amount <= 0:
            await self.channel.send("You must run the gambler more than once atleast")
            del self
            return
        commands = await self.channel.application_commands()
        for command in commands:
            if command.id == self.gamble_command_id:
                self.gamble_command = command
        await self.channel.send(f"Successfully activated in {self.channel.name}, going to gamble {self.gamble_amount} times...which is {self.gamble_amount*3000} cursed energy")
        await asyncio.sleep(1)
        await self.gamble()
    

    async def gamble(self):
        if self.gamble_amount <= 0 or self.gamble_command is None: return
        self.gamble_amount -= 1
        await self.gamble_command.__call__()
        await asyncio.sleep(5)
        if self.gamble_amount != 0:
            await self.channel.send(f"Gambling frfr, got {self.gamble_amount} more gambles to go")
        else:
            await self.channel.send("We done gambling bois")
        await self.gamble()

