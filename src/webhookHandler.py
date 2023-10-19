from discord import Webhook
import aiohttp

# Function that sends a message to a webhook link
async def webhook(url, embed):
    async with aiohttp.ClientSession() as session:
        webhook = Webhook.from_url(url, session=session)
        await webhook.send(embed=embed)