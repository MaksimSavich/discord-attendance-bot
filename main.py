import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(command_prefix='!',intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.command()
async def test(ctx):
    await ctx.send('Hello!')

load_dotenv()
client.run(os.getenv('TOKEN'))