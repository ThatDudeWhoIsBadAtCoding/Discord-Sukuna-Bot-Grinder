import asyncio


class Battler():
    def __init__(self, channel, tokens):
        print(tokens)
        self.battle_command = 1255451462989774858
        self.battle_reset_command = 1255855746952724573
        self.channel = channel
        self.battling = False
        self.wins = 0
        self.losses = 0
        self.battle_tokens = tokens
        self.active = True
    

    async def activate(self):
        self.active = True
        if self.battle_tokens <= 0:
            await self.channel.send("You must input more than one token to use")
            del self
            return
        commands = await self.channel.application_commands()
        for command in commands:
            if command.id == self.battle_reset_command:
                for c in command.children:
                    if c.name == "battle":
                        self.battle_reset_command = c
            if command.id == self.battle_command:
                self.battle_command = command
        await self.channel.send(f"Successfully activated in {self.channel.name} with {self.battle_tokens} tokens....Initiating Battle")
        await asyncio.sleep(1)
        await self.fight_battle(False)


    
    async def battles_over(self):
        winrate = self.wins/(self.wins + self.losses)
        await self.channel.send(f"Successfully played all battles....Wins = {self.wins}, Losses = {self.losses}, Win rate = {round(winrate*100, 1)}%")
        self.active = False
    
    async def fight_battle(self, reset):
        if not self.active:
            print("battler inactive now")
            return
        if reset and self.battle_tokens >= 1:
            self.battle_tokens -= 1
            self.battling = False
            await self.battle_reset_command.__call__()
            await asyncio.sleep(4)
            bat = "battles" if self.battle_tokens > 0 else "battle"
            await self.channel.send(f"{self.battle_tokens + 1} more {bat} to go!")
            await self.fight_battle(False)
            await asyncio.sleep(4)
            return
        
        elif not self.battling: 
            await asyncio.sleep(4)
            await self.battle_command.__call__()
            self.battling = True
            return
        
        if self.battle_tokens <= 0:
            await self.battles_over()