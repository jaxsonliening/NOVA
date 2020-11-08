import ast
import discord
import praw

from discord.ext import commands
from secrets import *


def insert_returns(body):
    # insert return stmt if the last expression is a expression statement
    if isinstance(body[-1], ast.Expr):
        body[-1] = ast.Return(body[-1].value)
        ast.fix_missing_locations(body[-1])

    # for if statements, we insert returns into the body and the orelse
    if isinstance(body[-1], ast.If):
        insert_returns(body[-1].body)
        insert_returns(body[-1].orelse)

    # for with blocks, again we insert returns into the body
    if isinstance(body[-1], ast.With):
        insert_returns(body[-1].body)


class Dev(commands.Cog):
    """Commands for the creator of this bot, YeetVegetabales."""

    def __init__(self, client, reddit):
        self.client = client
        self.reddit = reddit

    reddit = praw.Reddit(client_id=reddit_client_id,
                         client_secret=reddit_client_secret,
                         username=reddit_username,
                         password=reddit_password,
                         user_agent=reddit_user_agent)

    @commands.command()
    @commands.is_owner()
    async def eval(self, ctx, *, cmd):
        """Evaluates expressions (owner only)
        """
        fn_name = "_eval_expr"

        cmd = cmd.strip("` ")

        # add a layer of indentation
        cmd = "\n".join(f"    {i}" for i in cmd.splitlines())

        # wrap in async def body
        body = f"async def {fn_name}():\n{cmd}"

        parsed = ast.parse(body)
        body = parsed.body[0].body

        insert_returns(body)

        env = {
            'bot': ctx.bot,
            'discord': discord,
            'commands': commands,
            'ctx': ctx,
            '__import__': __import__
        }
        exec(compile(parsed, filename="<ast>", mode="exec"), env)

        result = (await eval(f"{fn_name}()", env))
        await ctx.send(result)

    @commands.command()
    @commands.is_owner()
    async def modq(self, ctx, sub):
        """This isn't for you to use"""
        posts = []
        commentt = []
        embedd = discord.Embed(
            colour=0x5643fd, title="Counting items in the modqueue...", timestamp=ctx.message.created_at)
        embedd.set_footer(text=f'Requested by {ctx.message.author}', icon_url=ctx.message.author.avatar_url)
        embedd.set_image(
            url='https://i.imgur.com/gVX3yPJ.gif?noredirect')
        message = await ctx.send(embed=embedd)
        for post in self.reddit.subreddit(sub).mod.modqueue(limit=None, only="submissions"):
            posts.append(post)
        for comment in self.reddit.subreddit(sub).mod.modqueue(limit=None, only="comments"):
            commentt.append(comment)
        total_count = len(posts) + len(commentt)
        embed = discord.Embed(title=f'r/{sub} modqueue', color=0x5643fd, timestamp=ctx.message.created_at,
                              description=f'I found ``{total_count}`` total items in the r/{sub} modqueue.')
        embed.add_field(name='Posts', value=len(posts), inline=True)
        embed.add_field(name='Comments', value=len(commentt), inline=True)
        embedd.set_footer(text=f'Requested by {ctx.message.author}', icon_url=ctx.message.author.avatar_url)
        await message.edit(embed=embed)


def setup(client):
    client.add_cog(Dev(client, reddit=praw.Reddit(client_id=reddit_client_id,
                                                  client_secret=reddit_client_secret,
                                                  username=reddit_username,
                                                  password=reddit_password,
                                                  user_agent=reddit_user_agent
                                                  )))
