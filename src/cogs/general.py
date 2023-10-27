import discord
import time
import math
import settings
import pandas as pd
from discord.ext import commands, tasks
from discord import app_commands

class general(commands.Cog, description='General commands'):

    def __init__(self, bot):
        self.bot = bot
        # self.index = 0
        # self.printer.start()

    # Variable that is set equal to the output from the bot so that it can be deleted after the cog is invoked
    msg = None

    @tasks.loop(seconds=5.0)
    async def printer(self):
        df = pd.read_csv('./dataframes/users.csv')
        for i in len(df.index):
            df.loc[df[df['event_end_time_unix'] == math.floor(time.time())].index[0], 'name']


    @app_commands.command(name="signup",description="Signs a user up for the attendance bot")
    async def signup(self, interaction: discord.Interaction, name: str):
        df = pd.read_csv('./dataframes/users.csv')
        if (interaction.user.id in df['uuid'].unique()):
            await interaction.response.send_message('```ini\nYou have already signed up.\n```')
            return
        df.loc[len(df.index)] = [name, interaction.user.id]
        df.to_csv('./dataframes/users.csv', index=False)
        await interaction.response.send_message('```ini\nYou have signed up.\n```')

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
                            await interaction.response.send_message('```ini\nYour attendance has already been marked.\n```')
                            return
                        dfEvent.loc[len(dfEvent.index)] = [name,interaction.user.id]
                        dfEvent.to_csv(f'./dataframes/{filename}.csv', index=False)
                        await interaction.response.send_message('```ini\nYour attendance has been recorded.\n```')
                else:
                    await interaction.response.send_message('```ini\nWrong code!\n```')

        
                        

    # Deletes the command sent by the user
    # async def cog_before_invoke(self, ctx):
    #     await ctx.message.delete()

    # Deletes the output from the bot after a certain amount of time
    # async def cog_after_invoke(self, ctx):
    #     if self.msg != None:
    #         await asyncio.sleep(settings.autoDeleteDelay)
    #         try:
    #             await self.msg.delete()
    #         except:
    #             pass
    #         self.msg = None

# Registers the cog
async def setup(bot):
    await bot.add_cog(general(bot) ,guilds = [discord.Object(id=settings.guildID)])