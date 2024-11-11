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
    

    async def activate(self):
        if self.battle_tokens <= 0:
            await self.channel.send("You must input more than one token to use")
            del self
            return
        commands = await self.channel.application_commands()
        for command in commands:
            if command.id == self.battle_reset_command:
                print('reset command found')
                for c in command.children:
                    if c.name == "battle":
                        self.battle_reset_command = c
            if command.id == self.battle_command:
                print('battle command found')
                self.battle_command = command
        await self.channel.send(f"Successfully activated in {self.channel.name} with {self.battle_tokens} tokens....Initiating Battle")
        await asyncio.sleep(1)
        await self.fight_battle(False)


    
    async def battles_over(self):
        winrate = self.wins/(self.wins + self.losses)
        await self.channel.send(f"Successfully played all battles....Wins = {self.wins}, Losses = {self.losses}, Win rate = {round(winrate*100, 1)}%")
        del self
    
    async def fight_battle(self, reset):
        commands = await self.channel.application_commands()
        if reset and self.battle_tokens >= 1:
            self.battle_tokens -= 1
            self.battling = False
            await self.battle_reset_command.__call__()
            await asyncio.sleep(2)
            bat = "battles" if self.battle_tokens > 0 else "battle"
            await self.channel.send(f"{self.battle_tokens + 1} more {bat} to go!")
            await self.fight_battle(False)
            await asyncio.sleep(1)
            return
        
        elif not self.battling:
            await self.battle_command.__call__()
            self.battling = True
            return
        
        if self.battle_tokens <= 0:
            await self.battles_over()

        # for command in commands:
        #     if reset and self.battle_tokens >= 1:
        #         if command.id == self.battle_reset_command_id:
        #             self.battle_tokens -= 1
        #             print('command found')
        #             for c in command.children:
        #                 if c.name == "battle":
        #                     await c.__call__()
        #                     self.busy = False
        #                     await asyncio.sleep(2)
        #                     await self.channel.send(f"{self.battle_tokens + 1} more battles to go!")
        #                     await self.fight_battle(False)
        #                     if self.battle_tokens == 0:
        #                         await self.battles_over()
        #                     return
        #     if command.id == self.battle_command_id and not self.battling:
        #         await command.__call__()
        #         self.busy = True
        #         break

