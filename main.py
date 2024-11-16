import discord
import discord.utils
import subprocess, json
from utils.bot import Selfbot, SUKUNA_ID

json_file = json.load(open("config.json"))
token, base_channel, prefix, id = json_file["token"], json_file["base_channel_id"], json_file["prefix"], json_file["user_id"]
client = Selfbot(base_channel, id, prefix)
client.run(token)