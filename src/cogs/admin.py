import discord
import pandas as pd
import settings, syscommands, permissions
import asyncio
import random
from discord.ext import commands

class admin(commands.Cog, description='Administration commands'):

    def __init__(self, bot):
        self.bot = bot

    # Variable that is set equal to the output from the bot so that it can be deleted after the cog is invoked
    msg = None

    @commands.command(description='Updates the mod role ID')
    @commands.check(permissions.is_admin)
    async def updateperms(self, ctx, roleID):
        await settings.modifyConfig('adminRoleID', roleID)

    @commands.command(description='Purges chat')
    @commands.check(permissions.is_mod)
    async def purge(self, ctx, amount: int):
        async for message in ctx.channel.history(limit=amount):
            delay = random.random()
            await asyncio.sleep(delay)
            await message.delete()

    @commands.command(description='Reboots the bot')
    @commands.check(permissions.is_mod)
    async def reboot(self, ctx):
        await ctx.send('```ini\nRebooting...\n```')
        syscommands.reboot()

    @commands.command(description='Sends the users .csv file')
    @commands.check(permissions.is_mod)
    async def getusersdb(self, ctx):
        await ctx.send(file=discord.File(r'./dataframes/users.csv'))

    @commands.command(description='Force adds a new user to the users database')
    @commands.check(permissions.is_mod)
    async def fadd(self, ctx, member, *name: str):
        df = pd.read_csv('./dataframes/users.csv')
        if (member in df['uuid'].unique()):
            await ctx.send('```ini\nThis user has already signed up.\n```')
            return
        df.loc[len(df.index)] = [' '.join(name), member]
        df.to_csv('./dataframes/users.csv', index=False)
        await ctx.send('```ini\nThe user has been added.\n```')

    @commands.command(description='Changes the name of the user in the users database')
    @commands.check(permissions.is_mod)
    async def changename(self, ctx, member: int, *name:str):
        df = pd.read_csv('./dataframes/users.csv')
        df.loc[df[df['uuid'] == member].index[0], 'name'] = ' '.join(name)
        df.to_csv('./dataframes/users.csv', index=False)
        await ctx.send('```ini\nThe user\'s name has been updated.\n```')

    @commands.command(description='Creates an event')
    @commands.check(permissions.is_mod)
    async def startevent(self, ctx):
        pass

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
    await bot.add_cog(admin(bot))