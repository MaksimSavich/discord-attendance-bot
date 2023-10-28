import discord
import os
import pandas as pd
import settings, syscommands, permissions
import asyncio
import random
import importlib
import time
import math
from datetime import datetime
from discord.ext import commands
from discord import app_commands

class admin(commands.Cog, description='Administration commands'):

    def __init__(self, bot):
        self.bot = bot

    # Variable that is set equal to the output from the bot so that it can be deleted after the cog is invoked
    msg = None

    @app_commands.command(name="updatemodrole",description="Updates the mod role ID")
    @app_commands.check(permissions.is_admin)
    async def updatemodrole(self, interaction: discord.Interaction, role_id: str):
        await settings.modifyConfig('modRoleID', role_id)
        importlib.reload(settings)
        embed = discord.Embed(color=0xFDFD96, description=f'Mod role ID updated.')
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="setattendancechannel",description="Updates the attendance channel ID")
    @app_commands.check(permissions.is_admin)
    async def setattendancechannel(self, interaction: discord.Interaction, channel_id: str):
        await settings.modifyConfig('attendanceChannel', channel_id)
        importlib.reload(settings)
        embed = discord.Embed(color=0xFDFD96, description=f'Attendance channel updated.')
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="setoutput",description="Updates the attendance output channel ID")
    @app_commands.check(permissions.is_admin)
    async def setoutput(self, interaction: discord.Interaction, channel_id: str):
        await settings.modifyConfig('attendanceOutputChannel', channel_id)
        importlib.reload(settings)
        embed = discord.Embed(color=0xFDFD96, description=f'Attendance output channel updated.')
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="purge",description="Purges chat")
    @app_commands.check(permissions.is_mod)
    async def purge(self, interaction: discord.Interaction, amount: int):
        embed = discord.Embed(color=0xFDFD96, description=f'Purging {amount} messages.')
        await interaction.response.send_message(embed=embed, ephemeral=True)
        async for message in interaction.channel.history(limit=amount):
            delay = random.random()
            await asyncio.sleep(delay)
            await message.delete()

    @app_commands.command(name="reboot",description="Reboots the bot")
    @app_commands.check(permissions.is_mod)
    async def reboot(self, interaction: discord.Interaction):
        embed = discord.Embed(color=0xFDFD96, description=f'Rebooting...')
        await interaction.response.send_message(embed=embed, ephemeral=True)
        syscommands.reboot()

    @app_commands.command(name="getusersdb",description="Sends the users .csv file")
    @app_commands.check(permissions.is_mod)
    async def getusersdb(self, interaction: discord.Interaction):
        await interaction.response.send_message(file=discord.File(r'./dataframes/users.csv'))

    @app_commands.command(name="fadd",description="Force adds a new user to the users database")
    @app_commands.check(permissions.is_mod)
    async def fadd(self, interaction: discord.Interaction, user_id: str, name: str):
        df = pd.read_csv('./dataframes/users.csv')
        if (int(user_id) in df['uuid'].unique()):
            embed = discord.Embed(color=0xFDFD96, description=f'This user has already signed up.')
            await interaction.response.send_message(embed=embed ,ephemeral=True)
            return
        df.loc[len(df.index)] = [name, int(user_id)]
        df.to_csv('./dataframes/users.csv', index=False)
        embed = discord.Embed(color=0xFDFD96, description=f'The user has been added to the DB.')
        await interaction.response.send_message(embed=embed ,ephemeral=True)

    @app_commands.command(name="changename",description="Changes the name of the user in the users database")
    @app_commands.check(permissions.is_mod)
    async def changename(self, interaction: discord.Interaction, user_id: str, name:str):
        df = pd.read_csv('./dataframes/users.csv')
        df.loc[df[df['uuid'] == int(user_id)].index[0], 'name'] = name
        df.to_csv('./dataframes/users.csv', index=False)
        embed = discord.Embed(color=0xFDFD96, description=f'The user\'s name has been updated.')
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="endevent",description="Ends an event")
    @app_commands.check(permissions.is_mod)
    async def endevent(self, interaction: discord.Interaction, code:str):
        code = code.split(' ')[0].lower()
        channel = self.bot.get_channel(settings.attendanceOutputChannel)
        df = pd.read_csv('./dataframes/eventlist.csv')
        index = df.loc[df['code'] == code].index[0]
        if channel:
            try:
                filename = df.loc[index, "filename"]
                df.drop(index, inplace=True)
                df.to_csv('./dataframes/eventlist.csv', index=False)
                embed = discord.Embed(color=0xFDFD96, description=f'Event DB Dump: {filename}')
                await channel.send(embed=embed, file=discord.File(rf'./dataframes/{filename}.csv'))
                os.remove(f'./dataframes/{filename}.csv')
                embed2 = discord.Embed(color=0xFDFD96, description=f'Succesfully ended the event {filename}')
                await interaction.response.send_message(embed=embed2)
            except Exception as e:
                embed = discord.Embed(color=0xFDFD96, title='Automated Response', description=f'Error: Attendance file not found! Please contact an admin.')
                await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(color=0xFDFD96, title='Automated Response', description=f'Error: Attendance output channel not found! Please contact an admin.')
            await interaction.response.send_message(embed=embed)

    @app_commands.command(name="startevent",description="Creates an event")
    @app_commands.check(permissions.is_mod)
    async def startevent(self, interaction: discord.Interaction, event_name:str, code:str, hours:int):
        df = pd.read_csv('./dataframes/eventlist.csv')
        code = code.split(' ')[0].lower()
        event_name = event_name.replace(' ','_').lower()
        if (code in df['code'].unique()):
            embed = discord.Embed(color=0xFDFD96, description=f'Event already exists with that code!')
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        if (code in df['event_name'].unique()):
            embed = discord.Embed(color=0xFDFD96, description=f'Event already exists with that name!')
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        epoch = math.floor(time.time())
        timestamp = datetime.fromtimestamp(epoch)
        epoch = epoch + (3600 * hours)
        endtime = datetime.fromtimestamp(epoch)
        filename = f'{event_name}_{str(timestamp).split(" ")[0]}'
        df.loc[len(df.index)] = [event_name,code,timestamp,endtime,epoch,filename]
        df.to_csv('./dataframes/eventlist.csv', index=False)
        dfNewEvent = pd.DataFrame(columns=['name','uuid'])
        dfNewEvent.to_csv(f'./dataframes/{filename}.csv', index=False)
        embed = discord.Embed(color=0xFDFD96, description=f'Event \'{event_name}\' created')
        await interaction.response.send_message(embed=embed)
        
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
    await bot.add_cog(admin(bot), guilds = [discord.Object(id=settings.guildID)]  )