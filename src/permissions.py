import discord
import settings
import pandas as pd
from discord.ext import commands

async def is_admin_or_mod(interaction: discord.Interaction):
    # Load admin users list
    admin_users = pd.read_csv(f'{settings.BASE_DIR}/dataframes/admin_users.csv')

    # Check if the user is an admin
    if interaction.user.id in admin_users['user_id'].values:
        return True

    # Check if the user is a mod by checking their roles
    # Ensure the interaction.user.roles attribute is accessible as expected; 
    # if this code is in a context where interaction.user does not have roles (like in a DM),
    # or if you're using discord.Interaction which does not have a .roles attribute directly,
    # you may need to adjust how you access the user's roles.
    elif hasattr(interaction.user, 'roles') and settings.modRoleID in [role.id for role in interaction.user.roles]:
        return True
    else:
        return False