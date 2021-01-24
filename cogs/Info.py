import discord
import platform
import json
import os
import inspect
import asyncio
from discord.ext import commands


def lines_of_code():
    """
    I did not write this code.
    This code was taken off of a tag in discord.gg/dpy owned by Dutchy#6127
    I don't know if this is licensed
    but alas
    :return:
    """
    import pathlib
    p = pathlib.Path('./')
    cm = cr = fn = cl = ls = fc = 0
    for f in p.rglob('*.py'):
        if str(f).startswith("venv"):
            continue
        fc += 1
        with f.open() as of:
            for l in of.readlines():
                l = l.strip()
                if l.startswith('class'):
                    cl += 1
                if l.startswith('def'):
                    fn += 1
                if l.startswith('async def'):
                    cr += 1
                if '#' in l:
                    cm += 1
                ls += 1
    return {
        "comments": cm,
        "coroutine": cr,
        "functions": fn,
        "classes": cl,
        "lines": ls,
        "files": fc
    }


lines = lines_of_code()


class Info(commands.Cog):
    """Gain some info on users or servers"""

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["av"])
    async def avatar(self, ctx, *, member: discord.Member = None):
        """See the profile picture for a user"""
        member = member or ctx.message.author
        embed = discord.Embed(
            color=0x5643fd, title=f"{member}", timestamp=ctx.message.created_at)
        url = str(member.avatar_url).replace(".webp", ".png")
        embed.set_image(url=url)
        await ctx.send(embed=embed)

    @commands.command(aliases=['ui'])
    async def userinfo(self, ctx, member: discord.Member = None):
        """See info on a member in the server"""
        status_list = {
            "online": "<:online:726127263401246832> -  ``Online``",
            "offline": "<:offline:726127263203983440> -  ``Offline``",
            "idle": "<:idle:726127192165187594> -  ``Idle``",
            "dnd": "<:dnd:726127192001478746> -  ``Do not disturb``"}
        member = member or ctx.message.author
        roles = [role for role in member.roles]
        servers = len([g for g in self.client.guilds if g.get_member(member.id)])
        embed = discord.Embed(color=0x5643fd, timestamp=ctx.message.created_at)
        embed.set_author(name=f'User Info  -  {member}')
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text=f'Requested by {ctx.message.author}', icon_url=ctx.message.author.avatar_url)

        embed.add_field(name='ID:', value=f"<:author:734991429843157042> ``{member.id}``", inline=False)

        embed.add_field(name='Account Created:',
                        value=f"🕒 ``{member.created_at.strftime('%a, %B %d %Y, %I:%M %p UTC')}``",
                        inline=False)
        embed.add_field(name='Joined Server:',
                        value=f"<:member:731190477927219231> "
                              f"``{member.joined_at.strftime('%a, %B %d %Y, %I:%M %p UTC')}``",
                        inline=False)
        embed.add_field(name='Status:', value=f"{status_list[str(member.status)]}", inline=False)
        embed.add_field(name='Shared Servers with NOVA:', value=f"<:wumpus:742965982640865311> ``{servers}``")
        embed.add_field(name=f"Top Roles ({len(roles)} total):",
                        value=" ".join([role.mention for role in roles[::-1][:5]]), inline=False)
        await ctx.send(embed=embed)

    @commands.command(aliases=['si'], usage='')
    @commands.guild_only()
    async def serverinfo(self, ctx, *, guild_id: int = None):
        """Get info on a server"""

        if guild_id is not None and await self.client.is_owner(ctx.author):
            guild = self.client.get_guild(guild_id)
            if guild is None:
                return await ctx.send(f'<:redx:732660210132451369> NOVA is not in this guild '
                                      f'or this guild ID is invalid.')
        else:
            guild = ctx.guild

        roles = [role for role in guild.roles]

        class Secret:
            pass

        secret_member = Secret()
        secret_member.id = 0
        secret_member.roles = [guild.default_role]
        region = str(guild.region)
        r = region.capitalize()
        emojis = [emoji for emoji in guild.emojis]
        channels = [channel for channel in guild.channels]
        vc = [voice_channel for voice_channel in guild.voice_channels]
        folders = [category for category in guild.categories]
        bots = len([bot for bot in guild.members if bot.bot])
        humans = len(guild.members) - bots

        e = discord.Embed(title=f'<:Discord:735530547992068146> '
                                f'  Server Info  -  {guild.name}', color=0x5643fd, timestamp=ctx.message.created_at,
                          description=guild.description)
        e.add_field(name='ID:', value=f"<:author:734991429843157042> ``{guild.id}``", inline=False)
        e.add_field(name='Owner:', value=f"<:owner:730864906429136907>``{guild.owner}``", inline=False)
        e.add_field(name='Region:', value=f"📌 ``{r}``", inline=False)
        if guild.icon:
            e.set_thumbnail(url=guild.icon_url)
        e.add_field(name='Members:', value=f"<:member:731190477927219231> ``{guild.member_count}`` **•**"
                                           f"   <:bot:703728026512392312> ``{bots}`` **•**"
                                           f"   👨 ``{humans}``",
                    inline=False)
        e.add_field(name='Roles:', value=f'<:roles:734232012730138744> ``{len(roles)}``', inline=False)
        e.add_field(name='Emojis:', value=f"<:emoji:734231060069613638> ``{len(emojis)}``", inline=False)
        e.add_field(name='Channels:', value=f"<:category:716057680548200468> ``{len(folders)}`` **•** "
                                            f"<:text_channel:703726554018086912> ``{len(channels)}`` **•** "
                                            f"<:voice_channel:703726554068418560> ``{len(vc)}``")
        e.add_field(name='Server Created:', inline=False,
                    value=f"🕒  "
                          f"``{guild.created_at.strftime('%a, %B %d %Y, %I:%M %p UTC')}``")
        e.set_footer(text=f'Requested by {ctx.message.author}', icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=e)

    @commands.command(aliases=['ab'])
    async def about(self, ctx):
        """Get basic information about NOVA"""
        pre = ctx.prefix
        emojis = len(self.client.emojis)
        y = '{:,}'.format(emojis)
        total_members = 0
        total_unique = len(self.client.users)
        unique = '{:,}'.format(total_unique)
        text = 0
        voice = 0
        guilds = 0
        for guild in self.client.guilds:
            guilds += 1
            total_members += guild.member_count
            for channel in guild.channels:
                if isinstance(channel, discord.TextChannel):
                    text += 1
                elif isinstance(channel, discord.VoiceChannel):
                    voice += 1
        members = '{:,}'.format(total_members)
        channels = text + voice
        parsed_channels = '{:,}'.format(channels)
        a_file = open("command_counter.json", "r")
        json_object = json.load(a_file)
        a_file.close()
        parsed_commands_run = '{:,}'.format(json_object['total_commands_run'] + 1)
        embed = discord.Embed(title='About NOVA', color=0x5643fd, timestamp=ctx.message.created_at,
                              description=f'My prefix for {ctx.guild.name} is ``{pre}``\nDo ``'
                                          f'{pre}help`` for a list of commands')
        embed.set_thumbnail(url='https://cdn.discordapp.com/avatars/709922850953494598/f78ed19924e8c95abc30f406d47670d7'
                                '.png?size=1024')
        embed.set_author(name='Developed by YeetVegetabales#5313',
                         icon_url='https://imgur.com/FfnuDFH.png')
        embed.add_field(inline=False, name='Info',
                        value='NOVA is a general purpose discord bot that has tools to help you better moderate your '
                              'server as well as have a little fun')
        embed.add_field(name='Stats',
                        value=f'**•** ``{guilds}`` servers with ``{members}``'
                              f' total users (`{unique}` unique)\n'
                              f'**•** ``{y}`` available emojis\n'
                              f'**•** ``{parsed_channels}`` channels\n'
                              f'**•** ``{parsed_commands_run}`` commands run', inline=False)
        embed.add_field(name='Code', value=f'**•** ``{len(self.client.commands)}`` commands with '
                                           f'``{len(self.client.cogs)}`` cogs\n'
                                           f"**•** `{lines.get('lines'):,}` lines of code with "
                                           f"`{lines.get('files'):,}` "
                                           f"files\n"
                                           f"**•** <:python:726515814861242519> `{platform.python_version()}`\n"
                                           f"**•** <:discordpy:708801596431007845> `{discord.__version__}`"

                        , inline=False)
        embed.add_field(name='Other', value='<:news:730866149109137520> [Discord Server](https://discord.gg/Uqh9NXY)\n'
                                            '<:news:730866149109137520> [Invite Link](https://discor'
                                            'd.com/api/oauth2/authorize?client_id=709922850953494598&permissions=470150'
                                            '214&scope=bot)', inline=True)
        await ctx.send(embed=embed)

    @commands.command()
    async def cogs(self, ctx):
        """Shows all of NOVA's cogs"""
        cogs = []
        for cog in self.client.cogs:
            cogs.append(
                f"`{cog}` • {self.client.cogs[cog].__doc__}")
            # adds cogs and their description to list. if the cog doesnt have a description it will return as "None"
        await ctx.send(embed=discord.Embed(colour=0x5643fd, title=f"All Cogs ({len(self.client.cogs)})",
                                           description=f"Do `{ctx.prefix}help <cog>` to show info for any cog!"
                                                       + "\n\n" + "\n".join(
                                               cogs)))

    @commands.command(aliases=['src'])
    async def source(self, ctx, *, command: str = None):
        """Find the full source code for a command."""
        # https://github.com/Rapptz/RoboDanny/blob/rewrite/cogs/meta.py#L328-L366
        # Copyright (c) 2015 Rapptz
        # Copyright (c) 2020 niztg
        # https://github.com/niztg/CyberTron5000
        if not command:
            embed = discord.Embed(color=0x5643fd,
                                  description="All source code can be found on NOVA's personal"
                                              " GitHub repository",
                                  url="https://github.com/YeetVegetabales/NOVA", title="Source Code")
            embed.add_field(name="<:staff:730846674775179394> LICENSE",
                            value=f"[MIT](https://opensource.org/licenses/MIT)\n"
                                  f"https://github.com/YeetVegetabales/NOVA")
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_image(url="https://imgur.com/ykrkpNd.jpg")
            return await ctx.send(embed=embed)
        elif command in ("help", "?"):
            embed = discord.Embed(colour=0x5643fd,
                                  title=f"<:github:734999696845832252> Sourcecode for help",
                                  url="https://github.com/YeetVegetabales/NOVA/blob/master/cogs/Help.py#L13-L125",
                                  description="\n<:staff:730846674775179394> "
                                              "[LICENSE](https://opensource.org/licenses/MIT)\n\n"
                                              "https://github.com/YeetVegetabales/NOVA")
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_image(url='https://imgur.com/ykrkpNd.jpg')
            await ctx.send(embed=embed)
        else:
            cmd = self.client.get_command(command)
            if not cmd:
                return await ctx.send("<:redx:732660210132451369> Command not found.")
            file = cmd.callback.__code__.co_filename
            location = os.path.relpath(file)
            total, fl = __import__('inspect').getsourcelines(cmd.callback)
            ll = fl + (len(total) - 1)
            url = f"https://github.com/YeetVegetabales/NOVA/blob/master/{location}#L{fl}-L{ll}"
            if not cmd.aliases:
                char = '\u200b'
            else:
                char = '/'
            embed = discord.Embed(color=0x5643fd,
                                  title=f"<:github:734999696845832252> "
                                        f"Sourcecode for {cmd.name}{char}{'/'.join(cmd.aliases)}",
                                  url=url,
                                  description="\n<:staff:730846674775179394> "
                                              "[LICENSE](https://opensource.org/licenses/MIT)\n\n"
                                              "https://github.com/YeetVegetabales/NOVA")
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_image(url="https://imgur.com/ykrkpNd.jpg")
            await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Info(client))
