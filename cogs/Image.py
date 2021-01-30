import discord
from discord.ext import commands


class image(commands.Cog):
    """Image manipulation commands to spice up your profile picture."""

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def glass(self, ctx, member: discord.Member = None):
        """Add a glass filter to a profile picture."""
        user = member or ctx.message.author
        av = str(user.avatar_url_as(format='png'))
        url = f'https://some-random-api.ml/canvas/glass?avatar={av}'
        embed = discord.Embed(color=0x5643fd, timestamp=ctx.message.created_at)
        embed.set_image(url=url)
        await ctx.send(embed=embed)

    @commands.command()
    async def gay(self, ctx, member: discord.Member = None):
        """Add a rainbow filter to a profile picture."""
        user = member or ctx.message.author
        av = str(user.avatar_url_as(format='png'))
        url = f'https://some-random-api.ml/canvas/gay?avatar={av}'
        embed = discord.Embed(color=0x5643fd, timestamp=ctx.message.created_at)
        embed.set_image(url=url)
        await ctx.send(embed=embed)

    @commands.command()
    async def invert(self, ctx, member: discord.Member = None):
        """Add an inverted filter to a profile picture."""
        user = member or ctx.message.author
        av = str(user.avatar_url_as(format='png'))
        url = f'https://some-random-api.ml/canvas/invert?avatar={av}'
        embed = discord.Embed(color=0x5643fd, timestamp=ctx.message.created_at)
        embed.set_image(url=url)
        await ctx.send(embed=embed)

    @commands.command()
    async def wasted(self, ctx, member: discord.Member = None):
        """Add a GTA V wasted filter to a profile picture."""
        user = member or ctx.message.author
        av = str(user.avatar_url_as(format='png'))
        url = f'https://some-random-api.ml/canvas/wasted?avatar={av}'
        embed = discord.Embed(color=0x5643fd, timestamp=ctx.message.created_at)
        embed.set_image(url=url)
        await ctx.send(embed=embed)

    @commands.command(aliases=['trigger'])
    async def triggered(self, ctx, member: discord.Member = None):
        """Add a triggered filter to a profile picture."""
        user = member or ctx.message.author
        av = str(user.avatar_url_as(format='png'))
        url = f'https://some-random-api.ml/canvas/triggered?avatar={av}'
        embed = discord.Embed(color=0x5643fd, timestamp=ctx.message.created_at)
        embed.set_image(url=url)
        await ctx.send(embed=embed)

    @commands.command()
    async def greyscale(self, ctx, member: discord.Member = None):
        """Add a greyscale filter to a profile picture."""
        user = member or ctx.message.author
        av = str(user.avatar_url_as(format='png'))
        url = f'https://some-random-api.ml/canvas/greyscale?avatar={av}'
        embed = discord.Embed(color=0x5643fd, timestamp=ctx.message.created_at)
        embed.set_image(url=url)
        await ctx.send(embed=embed)

    @commands.command()
    async def invertgreyscale(self, ctx, member: discord.Member = None):
        """Add an inverted and greyscaled filter to a profile picture."""
        user = member or ctx.message.author
        av = str(user.avatar_url_as(format='png'))
        url = f'https://some-random-api.ml/canvas/invertgreyscale?avatar={av}'
        embed = discord.Embed(color=0x5643fd, timestamp=ctx.message.created_at)
        embed.set_image(url=url)
        await ctx.send(embed=embed)

    @commands.command(aliases=['brightness'])
    async def bright(self, ctx, member: discord.Member = None):
        """Add a bright filter to a profile picture."""
        user = member or ctx.message.author
        av = str(user.avatar_url_as(format='png'))
        url = f'https://some-random-api.ml/canvas/brightness?avatar={av}'
        embed = discord.Embed(color=0x5643fd, timestamp=ctx.message.created_at)
        embed.set_image(url=url)
        await ctx.send(embed=embed)

    @commands.command()
    async def sepia(self, ctx, member: discord.Member = None):
        """Add a sepia filter to a profile picture."""
        user = member or ctx.message.author
        av = str(user.avatar_url_as(format='png'))
        url = f'https://some-random-api.ml/canvas/sepia?avatar={av}'
        embed = discord.Embed(color=0x5643fd, timestamp=ctx.message.created_at)
        embed.set_image(url=url)
        await ctx.send(embed=embed)

    @commands.command()
    async def threshold(self, ctx, member: discord.Member = None):
        """Add a black and white filter to a profile picture."""
        user = member or ctx.message.author
        av = str(user.avatar_url_as(format='png'))
        url = f'https://some-random-api.ml/canvas/threshold?avatar={av}'
        embed = discord.Embed(color=0x5643fd, timestamp=ctx.message.created_at)
        embed.set_image(url=url)
        await ctx.send(embed=embed)

    @commands.command()
    async def red(self, ctx, member: discord.Member = None):
        """Add a red filter to a profile picture."""
        user = member or ctx.message.author
        av = str(user.avatar_url_as(format='png'))
        url = f'https://some-random-api.ml/canvas/red?avatar={av}'
        embed = discord.Embed(color=0x5643fd, timestamp=ctx.message.created_at)
        embed.set_image(url=url)
        await ctx.send(embed=embed)

    @commands.command()
    async def green(self, ctx, member: discord.Member = None):
        """Add a green filter to a profile picture."""
        user = member or ctx.message.author
        av = str(user.avatar_url_as(format='png'))
        url = f'https://some-random-api.ml/canvas/green?avatar={av}'
        embed = discord.Embed(color=0x5643fd, timestamp=ctx.message.created_at)
        embed.set_image(url=url)
        await ctx.send(embed=embed)

    @commands.command()
    async def blue(self, ctx, member: discord.Member = None):
        """Add a blue filter to a profile picture."""
        user = member or ctx.message.author
        av = str(user.avatar_url_as(format='png'))
        url = f'https://some-random-api.ml/canvas/blue?avatar={av}'
        embed = discord.Embed(color=0x5643fd, timestamp=ctx.message.created_at)
        embed.set_image(url=url)
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(image(client))