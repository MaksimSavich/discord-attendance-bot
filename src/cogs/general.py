import discord
import os
import time
import math
import settings
import pandas as pd
from discord.ext import commands, tasks
from discord import app_commands

class general(commands.Cog, description='General commands'):

    def __init__(self, bot):
        self.bot = bot
        self.auto_event_end.start()

    # Variable that is set equal to the output from the bot so that it can be deleted after the cog is invoked
    msg = None

    # Loop that checks for the end of an event and processes the DB upon the end of an event
    @tasks.loop(minutes=5.0)
    async def auto_event_end(self):
        channel = self.bot.get_channel(settings.attendanceOutputChannel)
        df = pd.read_csv('./dataframes/eventlist.csv')
        for index, row in df.iterrows():
            if row['event_end_time_unix'] < math.floor(time.time()):
                if channel:
                    try:
                        filename = df.loc[index, 'filename']
                        embed = discord.Embed(color=0xFDFD96, description=f'Event DB Dump: {filename}')
                        await channel.send(embed=embed, file=discord.File(rf'./dataframes/{filename}.csv'))
                        df.drop(index, inplace=True)
                        df.to_csv('./dataframes/eventlist.csv', index=False)
                        os.remove(f'./dataframes/{filename}.csv')
                    except Exception as e:
                        embed = discord.Embed(color=0xFDFD96, title='Automated Response',description=f'Error: Attendance file not found!\nERROR:\n{e}')
                        await channel.send(embed=embed)
                else:
                    print('Auto Event End Error Response: Channel not found!')

    @app_commands.command(name="signup",description="Signs a user up for the attendance bot")
    async def signup(self, interaction: discord.Interaction, name: str):
        df = pd.read_csv('./dataframes/users.csv')
        if (interaction.user.id in df['uuid'].unique()):
            embed = discord.Embed(color=0xFDFD96, description='You have already signed up.')
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        embed = discord.Embed(color=0xFDFD96, description='You have successfully signed up to use the attendance bot!')
        df.loc[len(df.index)] = [name, interaction.user.id]
        df.to_csv('./dataframes/users.csv', index=False)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="attend",description="Allows user to attend an event")
    async def attend(self, interaction: discord.Interaction, code:str):
        code = code.split(' ')[0].lower()
        if interaction.channel_id == settings.attendanceChannel:
            dfUser = pd.read_csv('./dataframes/users.csv')
            if (interaction.user.id in dfUser['uuid'].unique()):
                dfEventCheck = pd.read_csv('./dataframes/eventlist.csv')
                if (code in dfEventCheck['code'].unique()):
                        filename = dfEventCheck.loc[dfEventCheck[dfEventCheck['code'] == code].index[0], 'filename']
                        name = dfUser.loc[dfUser[dfUser['uuid'] == interaction.user.id].index[0], 'name']
                        dfEvent = pd.read_csv(f'./dataframes/{filename}.csv')
                        if (interaction.user.id in dfEvent['uuid'].unique()):
                            embed = discord.Embed(color=0xFDFD96, description='Your attendance has already been marked.')
                            await interaction.response.send_message(embed=embed, ephemeral=True)
                            return
                        dfEvent.loc[len(dfEvent.index)] = [name,interaction.user.id]
                        dfEvent.to_csv(f'./dataframes/{filename}.csv', index=False)
                        embed = discord.Embed(color=0xFDFD96, description='Your attendance has been recorded.')
                        await interaction.response.send_message(embed=embed, ephemeral=True)
                else:
                    embed = discord.Embed(color=0xFDFD96, description='That code doesn\'t exist! Make sure you have typed the correct code.')
                    await interaction.response.send_message(embed=embed, ephemeral=True)

# Registers the cog
async def setup(bot):
    await bot.add_cog(general(bot) ,guilds = [discord.Object(id=settings.guildID)])