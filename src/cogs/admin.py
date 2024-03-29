import os
import discord
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

    @app_commands.command(name="setguildid",description="Updates the guild ID")
    @app_commands.check(permissions.is_admin_or_mod)
    async def setguildid(self, interaction: discord.Interaction, guild_id: str):
        await settings.modifyConfig('guildID', guild_id)
        importlib.reload(settings)
        embed = discord.Embed(color=0xFDFD96, description=f'Guild ID updated.')
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="setmodrole",description="Updates the mod role ID")
    @app_commands.check(permissions.is_admin_or_mod)
    async def setmodrole(self, interaction: discord.Interaction, role_id: str):
        await settings.modifyConfig('modRoleID', role_id)
        importlib.reload(settings)
        embed = discord.Embed(color=0xFDFD96, description=f'Mod role ID updated.')
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="setattendancechannel",description="Updates the attendance channel ID")
    @app_commands.check(permissions.is_admin_or_mod)
    async def setattendancechannel(self, interaction: discord.Interaction, channel_id: str):
        await settings.modifyConfig('attendanceChannel', channel_id)
        importlib.reload(settings)
        embed = discord.Embed(color=0xFDFD96, description=f'Attendance channel updated.')
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="setoutputchannel",description="Updates the attendance output channel ID")
    @app_commands.check(permissions.is_admin_or_mod)
    async def setoutputchannel(self, interaction: discord.Interaction, channel_id: str):
        await settings.modifyConfig('attendanceOutputChannel', channel_id)
        importlib.reload(settings)
        embed = discord.Embed(color=0xFDFD96, description=f'Attendance output channel updated.')
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="purge",description="Purges chat")
    @app_commands.check(permissions.is_admin_or_mod) 
    async def purge(self, interaction: discord.Interaction, amount: int):
        embed = discord.Embed(color=0xFDFD96, description=f'Purging {amount} messages.')
        await interaction.response.send_message(embed=embed, ephemeral=True)
        async for message in interaction.channel.history(limit=amount):
            delay = random.random()
            await asyncio.sleep(delay)
            await message.delete()

    @app_commands.command(name="reboot",description="Reboots the bot")
    @app_commands.check(permissions.is_admin_or_mod) 
    async def reboot(self, interaction: discord.Interaction):
        embed = discord.Embed(color=0xFDFD96, description=f'Rebooting...')
        await interaction.response.send_message(embed=embed)
        syscommands.reboot()

    @app_commands.command(name="getusersdb",description="Sends the users .csv file")
    @app_commands.check(permissions.is_admin_or_mod)
    async def getusersdb(self, interaction: discord.Interaction):
        await interaction.response.send_message(file=discord.File(rf'{settings.BASE_DIR}/dataframes/users.csv'))

    @app_commands.command(name="fadd",description="Force adds a new user to the users database")
    @app_commands.check(permissions.is_admin_or_mod)
    async def fadd(self, interaction: discord.Interaction, user_id: str, name: str):
        df = pd.read_csv(f'{settings.BASE_DIR}/dataframes/users.csv')
        if (int(user_id) in df['uuid'].unique()):
            embed = discord.Embed(color=0xFDFD96, description=f'This user has already signed up.')
            await interaction.response.send_message(embed=embed ,ephemeral=True)
            return
        df.loc[len(df.index)] = [name, int(user_id)]
        df.to_csv(f'{settings.BASE_DIR}/dataframes/users.csv', index=False)
        embed = discord.Embed(color=0xFDFD96, description=f'The user has been added to the DB.')
        await interaction.response.send_message(embed=embed ,ephemeral=True)

    @app_commands.command(name="changename",description="Changes the name of the user in the users database")
    @app_commands.check(permissions.is_admin_or_mod)
    async def changename(self, interaction: discord.Interaction, user_id: str, name:str):
        df = pd.read_csv(f'{settings.BASE_DIR}/dataframes/users.csv')
        df.loc[df[df['uuid'] == int(user_id)].index[0], 'name'] = name
        df.to_csv(f'{settings.BASE_DIR}/dataframes/users.csv', index=False)
        embed = discord.Embed(color=0xFDFD96, description=f'The user\'s name has been updated.')
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="checkattendance",description="Lists all people who have attended an active event")
    @app_commands.check(permissions.is_admin_or_mod)
    async def checkattendance(self, interaction: discord.Interaction, code:str):
        df = pd.read_csv(f'{settings.BASE_DIR}/dataframes/eventlist.csv')
        index = df.loc[df['code'] == code].index[0]
        filename = df.loc[index, "filename"]
        dfevent = pd.read_csv(f'{settings.BASE_DIR}/dataframes/{filename}.csv')
        users = dfevent['name'].tolist()
        name_list = ''

        embed = discord.Embed(color=0xFDFD96, title=f'{filename} Attendance')
        for i in range (len(dfevent.index)):
            name_list = name_list + users[i] + '\n'
        embed.add_field(name='Users', value=name_list, inline=True)

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="events",description="Outputs a list of active events")
    @app_commands.check(permissions.is_admin_or_mod)
    async def events(self, interaction: discord.Interaction):
        df = pd.read_csv(f'{settings.BASE_DIR}/dataframes/eventlist.csv')
        event_names = df['event_name'].tolist()
        codes = df['code'].tolist()
        event_end_times_unix = df['event_end_time_unix'].tolist()

        embed = discord.Embed(color=0xFDFD96, title='Event List')
        for i in range (len(df.index)):
            embed.add_field(name='Event Name', value=event_names[i], inline=True)
            embed.add_field(name='Code', value=codes[i], inline=True)
            embed.add_field(name='Time Remaining (H:M:S)', value=time.strftime("%H:%M:%S", time.gmtime(abs(event_end_times_unix[i]-math.floor(time.time())))), inline=True)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="endevent",description="Ends an event")
    @app_commands.check(permissions.is_admin_or_mod)
    async def endevent(self, interaction: discord.Interaction, code:str):
        code = code.split(' ')[0].lower()
        channel = self.bot.get_channel(settings.attendanceOutputChannel)
        df = pd.read_csv(f'{settings.BASE_DIR}/dataframes/eventlist.csv')
        if channel:
            try:
                index = df.loc[df['code'] == code].index[0]
                filename = df.loc[index, "filename"]
                df.drop(index, inplace=True)
                df.to_csv(f'{settings.BASE_DIR}/dataframes/eventlist.csv', index=False)
                embed = discord.Embed(color=0xFDFD96, description=f'Event DB Dump: {filename}')
                await channel.send(embed=embed, file=discord.File(rf'{settings.BASE_DIR}/dataframes/{filename}.csv'))
                os.remove(f'{settings.BASE_DIR}/dataframes/{filename}.csv')
                embed2 = discord.Embed(color=0xFDFD96, description=f'Succesfully ended the event {filename}')
                await interaction.response.send_message(embed=embed2)
            except Exception as e:
                embed = discord.Embed(color=0xFDFD96, title='Automated Response', description=f'Error: Attendance file not found! Did you enter the correct code? If not, please contact an admin.\n{e}')
                await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(color=0xFDFD96, title='Automated Response', description=f'Error: Attendance output channel not found! Please contact an admin.')
            await interaction.response.send_message(embed=embed)

    @app_commands.command(name="startevent",description="Creates an event")
    @app_commands.check(permissions.is_admin_or_mod)
    async def startevent(self, interaction: discord.Interaction, event_name:str, code:str, hours:int):
        df = pd.read_csv(f'{settings.BASE_DIR}/dataframes/eventlist.csv')
        code = code.split(' ')[0].lower()
        if not all(char.isalnum() or char.isspace() for char in event_name):
            embed = discord.Embed(color=0xFDFD96, description='Please only use alphanumeric characters!\nOnly Aa-Zz 0-9 and spaces are allowed.\nDON\'T USE SLASHES! ')
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        event_name = event_name.replace(' ','_').lower()
        if (code in df['code'].unique()):
            embed = discord.Embed(color=0xFDFD96, description=f'Event already exists with that code!')
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        if (event_name in df['event_name'].unique()):
            embed = discord.Embed(color=0xFDFD96, description=f'Event already exists with that name!')
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        epoch = math.floor(time.time())
        timestamp = datetime.fromtimestamp(epoch)
        epoch = epoch + (3600 * hours)
        endtime = datetime.fromtimestamp(epoch)
        filename = f'{event_name}_{str(timestamp).split(" ")[0]}'
        df.loc[len(df.index)] = [event_name,code,timestamp,endtime,epoch,filename]
        df.to_csv(f'{settings.BASE_DIR}/dataframes/eventlist.csv', index=False)
        dfNewEvent = pd.DataFrame(columns=['name','uuid'])
        dfNewEvent.to_csv(f'{settings.BASE_DIR}/dataframes/{filename}.csv', index=False)
        embed = discord.Embed(color=0xFDFD96, description=f'Event \'{event_name}\' created')
        await interaction.response.send_message(embed=embed)
        
# Registers the cog
async def setup(bot):
    await bot.add_cog(admin(bot), guilds = [discord.Object(id=settings.guildID)]  )