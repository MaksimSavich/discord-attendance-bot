import discord
import settings
import asyncio
import random
from discord.ext import commands

class general(commands.Cog, description='General commands'):

    def __init__(self, bot):
        self.bot = bot

    # Variable that is set equal to the output from the bot so that it can be deleted after the cog is invoked
    msg = None

    # test command
    @commands.command(description='test')
    async def test(self, ctx):
        pass

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