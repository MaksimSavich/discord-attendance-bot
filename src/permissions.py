import discord
import settings
from discord.ext import commands

def is_admin(interaction: discord.Interaction):
    # Check if the user invoking the command has admin permissions
    return interaction.user.guild_permissions.manage_guild

def is_mod(interaction: discord.Interaction):
    # Check if the user invoking the command has a specific role ID
    return settings.modRoleID in [role.id for role in interaction.user.roles]