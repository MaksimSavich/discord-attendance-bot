import discord
import os
import settings
import asyncio
import pandas as pd
from discord.ext import commands

class general(commands.Cog, description='General commands'):

    def __init__(self, bot):
        self.bot = bot

    # Variable that is set equal to the output from the bot so that it can be deleted after the cog is invoked
    msg = None

    # test command
    # @commands.command(description='test')
    # async def generate(self, ctx):
    #     data1 = [['Maksim Savich', 653440672069845003]]
    #     df = pd.DataFrame(data1, columns=['name','UUID'])
    #     df.to_csv('users.csv', index=False)

    @commands.command(description='test')
    async def signup(self, ctx, *name: str):
        df = pd.read_csv('./dataframes/users.csv')
        if (ctx.message.author.id in df['uuid'].unique()):
            await ctx.send('```ini\nYou have already signed up.\n```')
            return
        df.loc[len(df.index)] = [name, ctx.message.author.id]
        df.to_csv('./dataframes/users.csv', index=False)
        await ctx.send('```ini\nYou have signed up.\n```')

    @commands.command(description='test')
    async def read(self, ctx):
        df = pd.read_csv('./dataframes/users.csv')
        await ctx.send(df)

    # Deletes the command sent by the user
    async def cog_before_invoke(self, ctx):
        await ctx.message.delete()

    # Deletes the output from the bot after a certain amount of time
    async def cog_after_invoke(self, ctx):
        if self.msg != None:
            await asyncio.sleep(settings.autoDeleteDelay)
            try:
                await self.msg.delete()
            except:
                pass
            self.msg = None

# Registers the cog
async def setup(bot):
    await bot.add_cog(general(bot))