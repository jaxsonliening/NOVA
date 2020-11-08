import discord
from discord.ext import commands
import json
import os


async def get_data():
    with open('econ.json', 'r') as f:
        await json.load(f)


class Economy(commands.Cog):
    """Economy commands for NOVA"""

    def __init__(self, client):
        self.client = client

    os.chdir('/Users/jaxson/PycharmProjects/NOVABOT/')


def setup(client):
    client.add_cog(Economy(client))
