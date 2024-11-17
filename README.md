# Discord-Sukuna-Bot-Grinder


GRINDER FOR SUKUNA BOT (Beta)

MADE USING [Discord.py-self](https://github.com/dolfies/discord.py-self)

IF YOU ARE DOWNLOADING Discord.py-self USE THE FOLLOWING COMMAND (NOT `pip install discord.py-self`)!

`pip install -U --force-reinstall git+https://github.com/dolfies/discord.py-self.git`


Features: Auto-battler, Track Aces, feel free to suggest any additions

HOW TO USE:

1. Download Project
2. Input your **discord token** as well as **user ID** in `config.json` (Rest all can be configured using bot commands)
3. Use `prefix settle` in any channel first, followed by `prefix help` command to get started (bot prefix followed by space and 'help')


Hi! This bot is made by a bad programmer but it happens to work (by using this bot you are accepting Manami as our lord and saviour) 
Here is a breakdown of all the features and commands in the bot so far.
1. An auto-battler, simply use `prefix battle, amount_of_battle_tokens` and watch the bot fight for you! It does get interrupted by lag sometimes so it might break but I can do very little to fix that.
You can also use `prefix stop` while battling which stops the auto-battler at any moment
2. A tracker for your aces! I found that working towards larger aces is a pain in the ass so I added an ace tracker, the command is `prefix track, card_id, ace_number` and this will keep track of your ace in a text file! (comes into use when pulling)
You can use `prefix untrack, card_id, ace_number` to untrack the ace
3. A pull logger! This is why I added the tracker, use `prefix log` before you start pulling and the bot will tell you when you get a shard you need!
You can also use `prefix sacrifice` at any time to see how many non-important shards you have pulled so you can sacrifice them! Use `prefix unlog` to stop the logger

**How is this better than autosac?** 

Simple, no limit on how much you can work towards...unlike the limit of 20 cards on autosac wishlish, plus you have a clear idea of what you are working towards!
