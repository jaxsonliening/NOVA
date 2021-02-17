import discord
import random
import humanize
import asyncio
import datetime
import string
import json
import time
from discord.ext import tasks, commands

commando = open("command_counter.json", "r")
counter = json.load(commando)


class miscellaneous(commands.Cog):
    """Helpful commands that don't quite fit in a certain category"""

    def __init__(self, client):
        self.client = client
        self.commands_and_messages.start()

    @commands.command()
    async def invite(self, ctx):
        """Invite NOVA to your own server"""
        embed = discord.Embed(title='Invite links for NOVA',
                              description='[<:news:730866149109137520> Required Permissions](https://discord.com/api/'
                                          'oauth2/authorize?client_id=709922850953494598&permissions=1573252215&scope='
                                          'bot)\n'
                                          '[<:news:730866149109137520> No Permissions]'
                                          '(https://discord.com/api/oauth2/authorize?client_id=709922850953494598&permi'
                                          'ssions=0&scope=bot)\n[<:news:730866149109137520> All Permissions (admin)]'
                                          '(https://discord.com/api/oauth2/authorize?client_id=709922850953494598&perm'
                                          'issions=8&scope=bot)', color=0x5643fd)
        embed.set_footer(text='Developed by YeetVegetabales', icon_url='https://cdn.discordapp.com/avatars'
                                                                       '/569374429218603019'
                                                                       '/a_6dac6946906e498650f6c2466aa82200.gif?size'
                                                                       '=256&f=.gif')
        embed.set_thumbnail(url='https://images-ext-2.discordapp.net/external/54Mim4lahztGCP4hgmpy4lOdEUc4'
                                '-dOeNA_x6hVHMlc/%3Fsize%3D4096/https/cdn.discordapp.com/avatars/709922850953494598'
                                '/f78ed19924e8c95abc30f406d47670d7.png')
        await ctx.send(embed=embed)

    @commands.command()
    async def discord(self, ctx):
        """Generate a link to join NOVA's discord server!"""
        embed = discord.Embed(title='Join the discord today!', color=0x5643fd, description="This server is where "
                                                                                           "all of "
                                                                                           "NOVA's updates and "
                                                                                           "important "
                                                                                           "announcements will pass "
                                                                                           "through. The creator of "
                                                                                           "this "
                                                                                           "bot, YeetVegetabales#5313, "
                                                                                           "will also be there testing "
                                                                                           "and letting the communtiy "
                                                                                           "in "
                                                                                           "on things first hand!")
        embed.set_thumbnail(url='https://images-ext-2.discordapp.net/external/AQCEqCF4Yl_PWAfuA-GReZoDify6'
                                '--y4hXOJVkqaDHo/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/709922850953494598'
                                '/f78ed19924e8c95abc30f406d47670d7.png')
        embed.add_field(name='Server Invite', value='<:news:730866149109137520> '
                                                    '[Join here](https://discord.gg/Uqh9NXY)')
        await ctx.send(embed=embed)

    @commands.command()
    async def ping(self, ctx):
        """Calculate bot latency"""
        ping = round(self.client.latency, 5)
        await ctx.send(f"<a:loading:743537226503421973> ``{ping * 1000} milliseconds`` <a:loading:743537226503421973>")

    @commands.command(aliases=['dev'])
    async def developer(self, ctx):
        """Get some basic info about this bot's creator."""
        embed = discord.Embed(title='Developer - YeetVegetabales', color=0x5643fd, timestamp=ctx.message.created_at,
                              description="The developer of this bot is YeetVegetabales. He is 15 years old and"
                                          " made NOVA in order to learn how to code. DM him on discord to get any "
                                          "information on this bot or if you just want to chat about anything :)\n\n"
                                          "<:Discord:735530547992068146>  -   "
                                          "**[YeetVegetabales#5313](https://discord.gg/Uqh9NXY)**\n\n"
                                          "<:reddit:749433072549625897>  -   **[u/YeetVegetabales]"
                                          "(https://reddit.com/user/YeetVegetabales)**\n\n"
                                          "<:github:734999696845832252>  -   **[YeetVegetabales]"
                                          "(https://github.com/YeetVegetabales/)**\n\n"
                                          "<:steamsquare512:770389717342224465>  -   **[Vendetta]("
                                          "https://steamcommunity.com/profiles/76561199089966378)**")
        await ctx.send(embed=embed)

    # Command Counter
    @commands.Cog.listener()
    async def on_command(self, ctx):
        counter['total_commands_run'] += 1
        commando.close()

    # Messages Seen
    @commands.Cog.listener()
    async def on_message(self, message):
        counter['messages_seen'] += 1
        commando.close()

    @tasks.loop(seconds=60.0)
    async def commands_and_messages(self):
        json.dump(counter, open('command_counter.json', 'w'))
        return


def setup(client):
    client.add_cog(miscellaneous(client))
