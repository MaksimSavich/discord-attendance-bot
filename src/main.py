import os
import discord
import settings, customHelp
import asyncio
import pandas as pd
from pathlib import Path
from discord.ext import commands
from dotenv import load_dotenv

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=settings.prefix, help_command=customHelp.customHelp() , intents=intents)

async def generate_dataframe_files():
    Path("./dataframes/").mkdir(parents=True, exist_ok=True)
    if not os.path.isfile('./dataframes/users.csv'):
        dfUsers = pd.DataFrame(columns=['name','uuid'])
        dfUsers.to_csv('./dataframes/users.csv', index=False)
    if not os.path.isfile('./dataframes/eventlist.csv'):
        dfEvents = pd.DataFrame(columns=['event_name','event_end_time'])
        dfEvents.to_csv('./dataframes/eventlist.csv', index=False)

# Function to load cogs dynamically
async def load_cogs():
    for cog_file in settings.COGS_DIR.glob('*.py'):
        if cog_file.name != '__init__.py':
            cog_module = f'cogs.{cog_file.stem}'
            try:
                await bot.load_extension(cog_module)
                print(f"Loaded cog: {cog_module}")
            except Exception as e:
                print(f"Failed to load cog {cog_module}. Error: {e}")

# Command to reload cogs
@bot.command()
async def reload(ctx, extension):
    await ctx.message.delete()
    await bot.unload_extension(f'cogs.{extension}')
    await bot.load_extension(f'cogs.{extension}')
    msg = await ctx.send(f'```ini\n[{extension}]: Reloaded\n```')
    await asyncio.sleep(settings.autoDeleteDelay)
    try:
        await msg.delete()
    except:
        pass

@bot.event
async def on_ready():
    await generate_dataframe_files()
    await load_cogs()
    print(f'We have logged in as {bot.user}')

# custom bot event that handles command errors
@bot.event
async def on_command_error(ctx, error):
    await ctx.message.delete()
    if(error):
        msg = await ctx.send(f'```ini\n[Error]\n\n{error}\n```')
    elif(ctx.invoked_with.lower() != 'help'):
        msg = await ctx.send(f'```ini\n[Error]\n\nCommand \"{ctx.invoked_with}\" was not found\n```')
    
    await asyncio.sleep(settings.autoDeleteDelay)
    try:
        await msg.delete()
    except:
        pass

load_dotenv()
bot.run(os.getenv('TOKEN'))