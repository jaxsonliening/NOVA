import discord
import os
import asyncio
import requests
import json
from secrets import token
from discord.ext import tasks, commands
from itertools import cycle

intents = discord.Intents.all()
client = commands.Bot(command_prefix=commands.when_mentioned_or("n.", "N."), case_insensitive=True, intents=intents)
client.remove_command('help')
status = [f'n.help | {"{:,}".format(len(client.users))} users']


@client.event
async def on_ready():
    print('NOVA is online')
    member_counts.start()


errorurl = 'https://media.discordapp.net/attachments/726475732569555014/745738546660245664/vsPV_ipxVKfJKE3xJGvJZeX' \
           'wrxKUqqkJGBFdIgwpWWE3X7CIJrZ6kElRSJ4Mdvw5cC7wMPYLTKFNnBBv-2K4WP344DoO6Al7RQB4.png'
errorcolor = 0xFF0000


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title='Warning!',
                              description='This command is on a cooldown.\n '
                                          'Please try again in ``{:.2f}`` seconds'.format(error.retry_after),
                              color=errorcolor, timestamp=ctx.message.created_at)
        embed.set_thumbnail(url=errorurl)
        await ctx.send(embed=embed)

    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"⚠ {ctx.message.author.mention}, you are missing a required argument. "
                       f"Please make sure to include ``{error.param}`` in your command.")

    if isinstance(error, commands.NSFWChannelRequired):
        embed = discord.Embed(title='Warning!', color=errorcolor, timestamp=ctx.message.created_at,
                              description=f'{ctx.message.author.mention},  '
                                          f'an NSFW channel is required. Go to horny jail.')
        embed.set_image(url='https://i.kym-cdn.com/entries/icons/facebook/000/033/758/Screen_Shot_2020-04-28_at_12.21'
                            '.48_PM.jpg')
        await ctx.send(embed=embed)

    if isinstance(error, commands.BotMissingPermissions):
        embed = discord.Embed(title='Warning!', color=errorcolor, timestamp=ctx.message.created_at,
                              description=f'{ctx.message.author.mention},  '
                                          f'NOVA is missing the required permissions to use the command. In order for '
                                          f'NOVA to use this command, ``{error.missing_perms}``'
                                          f'must be enabled in role settings.')
        embed.set_thumbnail(url=errorurl)
        await ctx.send(embed=embed)

    if isinstance(error, commands.MissingPermissions):
        y = str(error.missing_perms)
        x = str(y.strip("['_]"))
        await ctx.send(f"⚠ You are not allowed to use this command. You must have ``{x}`` "
                       f"permissions in order to do so.")

    if isinstance(error, commands.UserNotFound):
        embed = discord.Embed(title='Warning!', color=errorcolor, timestamp=ctx.message.created_at,
                              description=f'{ctx.message.author.mention},  '
                                          f'that user could not be found.')
        embed.set_thumbnail(url=errorurl)
        await ctx.send(embed=embed)

    if isinstance(error, commands.CommandInvokeError):
        embed = discord.Embed(title='Warning!', color=errorcolor, timestamp=ctx.message.created_at,
                              description=f'{ctx.message.author.mention},  '
                                          f'there was an error with this command. If you would like to report this '
                                          f'issue to the creator of this bot, join the support server.\n'
                                          f'🔗  [Link](https://discord.gg/Uqh9NXY)')
        embed.add_field(name='Error:', value=f'```py\n{error}```')
        embed.set_thumbnail(url=errorurl)
        await ctx.send(embed=embed)
        raise error


@tasks.loop(seconds=300.0)
async def member_counts():
    total_members = 0
    for guild in client.guilds:
        total_members += guild.member_count
    await client.change_presence(activity=discord.Game(name=f'n.help | {"{:,}".format(total_members)} users'))


for filename in os.listdir('cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')
client.run(token)
