import discord
import discord.utils
import subprocess, json
from bot import Selfbot, SUKUNA_ID

# pip install -U --force-reinstall git+https://github.com/dolfies/discord.py-self.git (FOR LIBRARY)

def install():
    subprocess.run([ "pip", "install", "-U", "--force-reinstall", "git+https://github.com/dolfies/discord.py-self.git"])

json_file = json.load(open("config.json"))
token, base_channel, prefix, install_needed = json_file["token"], json_file["base_channel_id"], json_file["prefix"], json_file["install_needed"]
if install_needed: install()
client = Selfbot(base_channel, prefix)
client.run(token)