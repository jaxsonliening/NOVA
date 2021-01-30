import discord
import aiohttp
import random
import asyncio
import io
import re
import wikipedia
from aiotrivia import TriviaClient, AiotriviaException
from discord.ext import commands
from secrets import *
from random import randint, choice, sample
from big_lists import *

ZALGO_DEFAULT_AMT = 3
ZALGO_MAX_AMT = 7


class fun(commands.Cog):
    """Use NOVA to have a little fun on your server"""

    def __init__(self, client):
        self.client = client
        self.trivia = TriviaClient()

    @commands.group(invoke_without_command=True)
    async def animal(self, ctx):
        """Get a picture of various animals."""
        embed = discord.Embed(title="Animal Subcommands", color=0x5643fd, timestamp=ctx.message.created_at,
                              description=f"Use `{ctx.prefix}animal <dog/cat/bird/panda/fox>` to get a wonderful "
                                          f"animal picture"
                                          f"\n\n**» n.animal dog**\n"
                                          f"**» n.animal cat**\n"
                                          f"**» n.animal bird**\n"
                                          f"**» n.animal panda**\n"
                                          f"**» n.animal fox**")
        embed.set_image(url="https://imgur.com/oUDiZJK.jpg")
        await ctx.send(embed=embed)

    @animal.command(aliases=['pupper', 'doggo'])
    async def dog(self, ctx):
        # all credit to R.Danny for this command
        """Get a nice dog to brighten your day"""
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://random.dog/woof") as resp:
                if resp.status != 200:
                    return await ctx.send('<:RedX:707949835960975411> No dog found')

                filename = await resp.text()
                url = f'https://random.dog/{filename}'
                filesize = ctx.guild.filesize_limit if ctx.guild else 8388608
                if filename.endswith(('.mp4', '.webm')):
                    async with ctx.typing():
                        async with cs.get(url) as other:
                            if other.status != 200:
                                return await ctx.send('Could not download dog video :/')

                            if int(other.headers['Content-Length']) >= filesize:
                                return await ctx.send(f'Video was too big to upload... See it here: {url} instead.')

                            fp = io.BytesIO(await other.read())
                            await ctx.send(file=discord.File(fp, filename=filename))
                else:
                    await ctx.send(embed=discord.Embed(color=0x5643fd,
                                                       description=f"<:github:734999696845832252> "
                                                                   f"[Source Code]"
                                                                   f"(https://github.com/Rapptz/RoboDanny/blob/rewrite/"
                                                                   f"cogs/funhouse.py#L44-L66)").set_image(url=url)
                                   .set_footer(text='https://random.dog/woof'))

    @animal.command(aliases=['catto', 'kitty'])
    async def cat(self, ctx):
        """Waste time with some cat images"""
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://api.thecatapi.com/v1/images/search") as resp:
                if resp.status != 200:
                    return await ctx.send('<:RedX:707949835960975411> No cat found')
                js = await resp.json()
                await ctx.send(embed=discord.Embed(color=0x5643fd,
                                                   description=f"<:github:734999696845832252> "
                                                               f"[Source Code]"
                                                               f"(https://github.com/DevilJamJar"
                                                               f"/DevilBot/blob/master/cogs/fun."
                                                               f"py)").set_image(
                    url=js[0]['url']).set_footer(text='https://api.thecatapi.com/v1/images/search'))

    @animal.command()
    async def panda(self, ctx):
        """Cute panda images."""
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://some-random-api.ml/img/panda") as resp:
                if resp.status != 200:
                    return await ctx.send('<:RedX:707949835960975411> No panda found.')
                js = await resp.json()
                embed = discord.Embed(color=0x5643fd, timestamp=ctx.message.created_at)
                embed.set_image(url=js['link'])
                await ctx.send(embed=embed)

    @animal.command(aliases=['birb'])
    async def bird(self, ctx):
        """Cute birb images."""
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://some-random-api.ml/img/birb") as resp:
                if resp.status != 200:
                    return await ctx.send('<:RedX:707949835960975411> No birb found.')
                js = await resp.json()
                embed = discord.Embed(color=0x5643fd, timestamp=ctx.message.created_at)
                embed.set_image(url=js['link'])
                await ctx.send(embed=embed)

    @animal.command()
    async def fox(self, ctx):
        """Cute fox images."""
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://some-random-api.ml/img/fox") as resp:
                if resp.status != 200:
                    return await ctx.send('<:RedX:707949835960975411> No fox found.')
                js = await resp.json()
                embed = discord.Embed(color=0x5643fd, timestamp=ctx.message.created_at)
                embed.set_image(url=js['link'])
                await ctx.send(embed=embed)

    @commands.command(name='8ball')
    async def _8ball(self, ctx, *, question):
        """Allow the mystical NOVA to answer all of life's important questions"""
        responses = ['It is certain', 'It is decidedly so', 'Without a doubt', 'Yes, definitely', 'You may rely on it',
                     'As I see it, yes', 'Most likely', 'Outlook good', 'Yes', 'Signs point to yes',
                     'Reply hazy, try again', 'Ask again later', 'Better not tell you now', 'Cannot predict now',
                     'Concentrate and ask again', 'Do not count on it', 'My reply is no', 'My sources say no',
                     'The outlook is not so good', 'Very doubtful']
        embed = discord.Embed(title='Magic 8ball says', color=0x5643fd, timestamp=ctx.message.created_at)
        embed.add_field(name='Question:', value=question, inline=False)
        embed.add_field(name='Answer:', value=random.choice(responses), inline=False)
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/726475732569555014/747266621512614009/8-Ball-'
                                'Pool-Transparent-PNG.png')
        await ctx.send(embed=embed)

    @commands.command(aliases=["bigemote"])
    async def bigmote(self, ctx, *emoji: discord.Emoji):
        """Emotes, but B I G (only works from the bot's cache)"""
        a = []
        y = ""
        for item in emoji:
            a.append(self.client.get_emoji(item.id))
        emote = a[0]
        x = emote.id
        if emote.animated is True:
            y += 'gif'
        else:
            y += 'png'
        await ctx.send(f"https://cdn.discordapp.com/emojis/{x}.{y}")

    @commands.command(aliases=['dankvid', 'video'])
    async def dankvideo(self, ctx):
        """Randomly generate a funny video."""
        m = random.choice(dank_links)
        await ctx.send(f"Video **{dank_links.index(m) + 1}** of **{len(dank_links)}**\n{m}")

    # credit some random github page https://github.com/calebj/calebj-cogs/blob/master/zalgo/zalgo.py
    @commands.command()
    async def zalgo(self, ctx, *, text: str):
        """Make your text look like it came from the scary side of town."""
        fw = text.split()[0]
        try:
            amount = min(int(fw), ZALGO_MAX_AMT)
            text = text[len(fw):].strip()
        except ValueError:
            amount = ZALGO_DEFAULT_AMT
        text = self.zalgoify(text.upper(), amount)
        await ctx.send(text)

    def zalgoify(self, text, amount=3):
        zalgo_text = ''
        for c in text:
            zalgo_text += c
            if c != ' ':
                for t, range in ZALGO_PARAMS.items():
                    range = (round(x * amount / 5) for x in range)
                    n = min(randint(*range), len(ZALGO_CHARS[t]))
                    zalgo_text += ''.join(sample(ZALGO_CHARS[t], n))
        return zalgo_text

    @commands.command()
    async def topic(self, ctx):
        """Send a random topic into chat to jump-start a conversation."""
        topic = random.choice(topics)
        embed = discord.Embed(title="💬 Topic", timestamp=ctx.message.created_at, color=0x5643fd, description=topic)
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(fun(client))
