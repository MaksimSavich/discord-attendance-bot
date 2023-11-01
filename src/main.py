import os
import discord
import settings, permissions
import pandas as pd
from pathlib import Path
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=settings.prefix, intents=intents)

async def generate_dataframe_files():
    Path("./dataframes/").mkdir(parents=True, exist_ok=True)
    if not os.path.isfile('./dataframes/users.csv'):
        dfUsers = pd.DataFrame(columns=['name','uuid'])
        dfUsers.to_csv('./dataframes/users.csv', index=False)
    if not os.path.isfile('./dataframes/eventlist.csv'):
        dfEvents = pd.DataFrame(columns=['event_name','code','event_creation_date','event_end_time','event_end_time_unix','filename'])
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

async def reload_autocomplete(
    interaction: discord.Interaction,
    current: str,
) -> list[app_commands.Choice[str]]:
    cogs = ['general', 'admin']
    return [
        app_commands.Choice(name=cog, value=cog)
        for cog in cogs if current.lower() in cog.lower()
    ]

@bot.tree.command(name="reloads",description="Reloads cogs", guild=discord.Object(id=settings.guildID))
@app_commands.check(permissions.is_admin)
@app_commands.autocomplete(extension=reload_autocomplete)
async def reloads(interaction: discord.Interaction, extension: str):
    await bot.unload_extension(f'cogs.{extension}')
    await bot.load_extension(f'cogs.{extension}')
    embed = discord.Embed(color=0xFDFD96, description=f'{extension}: Reloaded.')
    await interaction.response.send_message(embed=embed)

@bot.event
async def on_ready():
    await generate_dataframe_files()
    await load_cogs()
    await bot.tree.sync(guild=discord.Object(id=settings.guildID))
    print(f'We have logged in as {bot.user}')

# custom bot event that handles command errors
# currently not working since I switched to slash commands
# @bot.event
# async def on_command_error(ctx, error):
#     await ctx.message.delete()
#     if(error):
#         msg = await ctx.send(f'```ini\n[Error]\n\n{error}\n```')
#     elif(ctx.invoked_with.lower() != 'help'):
#         msg = await ctx.send(f'```ini\n[Error]\n\nCommand \"{ctx.invoked_with}\" was not found\n```')
    
#     await asyncio.sleep(settings.autoDeleteDelay)
#     try:
#         await msg.delete()
#     except:
#         pass

load_dotenv()
bot.run(os.getenv('TOKEN'))