import discord
import praw
import random
import datetime
import aiohttp
import humanize
from discord.ext import commands
from secrets import *


class Reddit(commands.Cog):
    """Gather info and posts from many places on reddit"""

    def __init__(self, client, reddit):
        self.client = client
        self.reddit = reddit

    reddit = praw.Reddit(client_id=reddit_client_id,
                         client_secret=reddit_client_secret,
                         username=reddit_username,
                         password=reddit_password,
                         user_agent=reddit_user_agent)

    errorurl = 'https://media.discordapp.net/attachments/726475732569555014/745738546660245664/vsPV_' \
               'ipxVKfJKE3xJGvJZeX' \
               'wrxKUqqkJGBFdIgwpWWE3X7CIJrZ6kElRSJ4Mdvw5cC7wMPYLTKFNnBBv-2K4WP344DoO6Al7RQB4.png'

    @commands.command(aliases=['rs'])
    async def redditstats(self, ctx, user=None):
        """Gather the reddit stats for a user"""
        user = user or ctx.message.author.name
        thing = discord.Embed(title='Loading...', color=0x5643fd,
                              description='Please stand by this process should be over shortly',
                              timestamp=ctx.message.created_at)
        thing.set_image(url='https://i.imgur.com/gVX3yPJ.gif?noredirect')
        thing.set_footer(text=f'Requested by {ctx.message.author}', icon_url=ctx.message.author.avatar_url)
        message = await ctx.send(embed=thing)
        redditor = self.reddit.redditor(user)
        week_posts = self.reddit.redditor(user).top("week")
        posts = self.reddit.redditor(user).top("month")
        year_posts = self.reddit.redditor(user).top("year")
        weeks = []
        months = []
        years = []
        upvotes_week = 0
        for x in week_posts:
            weeks.append(x.score)
            upvotes_week += x.score
        upvotes_month = 0
        for submission in posts:
            months.append(submission.score)
            upvotes_month += submission.score
        upvotes_year = 0
        for s in year_posts:
            years.append(s.score)
            upvotes_year += s.score
        ts = int(redditor.created_utc)
        name = redditor.name
        upvote_week = '{:,}'.format(upvotes_week)
        upvote_month = '{:,}'.format(upvotes_month)
        upvote_year = '{:,}'.format(upvotes_year)
        week_num = str(len(weeks))
        month_num = str(len(months))
        year_num = str(len(years))
        if week_num == '100':
            week_num += '+'
        if month_num == '100':
            month_num += '+'
        if year_num == '100':
            year_num += '+'
        try:
            embed = discord.Embed(color=0x5643fd, timestamp=ctx.message.created_at,
                                  title=f'Reddit Info  -  u/{redditor.name}', url=f'https://reddit.com/user/{name}/')
            embed.set_thumbnail(url=redditor.icon_img)
            embed.set_footer(text=f'Requested by {ctx.message.author}', icon_url=ctx.message.author.avatar_url)

            embed.add_field(name='Total Karma', value=f"{redditor.link_karma + redditor.comment_karma:,}", inline=True)
            embed.add_field(name='Link Karma', value=f"{redditor.link_karma:,}", inline=False)
            embed.add_field(name='Comment Karma', value=f"{redditor.comment_karma:,}", inline=False)
            embed.add_field(name='Account Created', inline=False, value='{}'.format(
                datetime.datetime.fromtimestamp(ts).strftime('%B %d, %Y')))
            embed.add_field(name='Upvote Statistics', inline=False,
                            value=f'Total upvotes in the past week: `{upvote_week}` | `{week_num}` posts\n'
                                  f'Total upvotes in the past month: `{upvote_month}` | `{month_num}` posts\n'
                                  f'Total upvotes in the past year: `{upvote_year}` | `{year_num}` posts')
            await message.edit(embed=embed)
        except Exception:
            await ctx.send('That redditor could not be found.')

    @commands.command(aliases=['ms'])
    async def modstats(self, ctx, user=None):
        """Gather the mod stats for a user"""
        user = user or ctx.message.author.name
        thing = discord.Embed(title='Loading...', color=0x5643fd,
                              description='Please stand by this process should be over shortly',
                              timestamp=ctx.message.created_at)
        thing.set_image(url='https://i.imgur.com/gVX3yPJ.gif?noredirect')
        thing.set_footer(text=f'Requested by {ctx.message.author}', icon_url=ctx.message.author.avatar_url)
        message = await ctx.send(embed=thing)
        reddits = []
        numbas = []
        modstats = []
        user = self.reddit.redditor(user)
        try:
            async with aiohttp.ClientSession() as cs:
                async with cs.get(f"https://www.reddit.com/user/{user}/moderated_subreddits/.json") as r:
                    res = await r.json()
                subreddits = res['data']
                for subreddit in subreddits:
                    reddits.append(
                        f"[{subreddit['sr_display_name_prefixed']}](https://reddit.com{subreddit['url']}) • "
                        f"<:member:716339965771907099> **{subreddit['subscribers']:,}**")
                    numbas.append(subreddit['subscribers'])
                if len(reddits) > 10:
                    rs = reddits[:10]
                else:
                    rs = reddits

                for index, sr in enumerate(rs, 1):
                    modstats.append(f"{index}. {sr}")

                final_ms = "\n".join(modstats)
                embed = discord.Embed(color=0x5643fd,
                                      timestamp=ctx.message.created_at, title=f'Mod Stats for u/{user}',
                                      url=f'https://reddit.com/user/{user}')
                embed.set_thumbnail(url=user.icon_img)
                embed.set_footer(text=f'Requested by {ctx.message.author}', icon_url=ctx.message.author.avatar_url)
                embed.add_field(name='Sub Count', value=len(subreddits), inline=True)
                embed.add_field(name='Total Subscribers', value=humanize.intcomma(sum(numbas)), inline=True)
                embed.add_field(name="Avg. Subsribers per Sub",
                                value=f"{humanize.intcomma(round(sum(numbas) / len(numbas)))}", inline=True)
                embed.add_field(name='Top Subreddits', value=final_ms, inline=False)
            await message.edit(embed=embed)
        except Exception as error:
            embed = discord.Embed(title=
                                  "Moderator not found, try again with a valid username.", color=0xFF0000,
                                  description=error)
            await ctx.send(embed=embed)

    @commands.command()
    async def meme(self, ctx):
        """Grab a meme from reddit's dankest subreddit"""
        thing = discord.Embed(title='Loading...', color=0x5643fd,
                              description='<a:loading:743537226503421973> One dank meme coming right up '
                                          '<a:loading:743537226503421973>',
                              timestamp=ctx.message.created_at)
        thing.set_image(url='https://i.imgur.com/gVX3yPJ.gif?noredirect')
        thing.set_footer(text=f'Requested by {ctx.message.author}', icon_url=ctx.message.author.avatar_url)
        message = await ctx.send(embed=thing)
        posts = []
        for submission in self.reddit.subreddit('dankmemes').top('day', limit=100):
            if not submission.stickied:
                posts.append(submission)
        submission = random.choice(posts)
        embed = discord.Embed(title=submission.title, color=0x5643fd, timestamp=ctx.message.created_at)
        embed.set_author(name=f'u/{submission.author}', icon_url=submission.author.icon_img)
        embed.set_image(url=submission.url)
        embed.set_footer(text='r/dankmemes', icon_url='https://images-ext-1.discordapp.net/external/RBgvzfKtRRBs51Gj'
                                                      'dfLcuQhU6kjF_ycIzTW8LVXvsJg/https/b.thumbs.redditmedia.com/qLE'
                                                      '6RUF_ARSgCZ854L5Hq4iKd1GqzuW2A5k6xf2kEFs.png')
        embed.add_field(name='Score', value=f'<:upvote:751314607808839803> {submission.score}')
        embed.add_field(name='Comments', value=f'💬 {submission.num_comments}')
        await message.edit(embed=embed)

    @commands.command(aliases=['ask'])
    async def askreddit(self, ctx):
        """Get a random askreddit thread with a comment"""
        embedd = discord.Embed(
            colour=0x5643fd, title="<a:loading:743537226503421973> Loading... <a:loading:743537226503421973>",
            timestamp=ctx.message.created_at
        )
        embedd.set_footer(text=f'Requested by {ctx.message.author}', icon_url=ctx.message.author.avatar_url)
        embedd.set_image(
            url='https://i.imgur.com/gVX3yPJ.gif?noredirect')
        message = await ctx.send(embed=embedd)
        try:
            posts = []
            comments = []
            for submission in self.reddit.subreddit("AskReddit").top('day', limit=15):
                posts.append(submission)
            final_post = random.choice(posts)
            if final_post.is_self:
                embed = discord.Embed(title=final_post.title,
                                      description=final_post.selftext + f"\n<:upvote:751314607808839803> "
                                                                        f"**{final_post.score}**     "
                                                                        f"**💬 {final_post.num_comments}**",
                                      colour=0x5643fd, timestamp=ctx.message.created_at)
                embed.set_author(name=final_post.author, icon_url=final_post.author.icon_img)
                for top_level_comment in final_post.comments:
                    comments.append(top_level_comment)
                final_comment = random.choice(comments)
                embed.add_field(
                    name=f"{final_comment.author} | <:upvote:751314607808839803> **{final_comment.score:,}**   **"
                         f"💬 {len(final_comment.replies):,}**",
                    value=final_comment.body)
                embed.set_footer(text=f'Requested by {ctx.message.author}', icon_url=ctx.message.author.avatar_url)
                await message.edit(embed=embed)
        except Exception as error:
            embed = discord.Embed(title='Error Occurred', color=0xFF0000, description=error)
            await ctx.send(embed=embed) if not final_post.over_18 or final_comment.over_18 and ctx.channel.is_nsfw() \
                else await ctx.send(
                f"⚠️:underage: **{ctx.author.mention}**, NSFW channel required!")

    @commands.command()
    async def post(self, ctx, subreddit, sort='hot'):
        """Get a random post from anywhere on reddit"""
        try:
            embedd = discord.Embed(
                colour=0x5643fd, title="<a:loading:743537226503421973> Loading... <a:loading:743537226503421973>",
                timestamp=ctx.message.created_at
            )
            embedd.set_footer(text=f'Requested by {ctx.message.author}', icon_url=ctx.message.author.avatar_url)
            embedd.set_image(
                url='https://i.imgur.com/gVX3yPJ.gif?noredirect')
            message = await ctx.send(embed=embedd)
            reddit = self.reddit.subreddit(subreddit)
            sorts = ['new', 'controversial', 'rising', 'top', 'topever', 'hot', 'controversialever']
            reddits = [reddit.new(limit=50), reddit.controversial(limit=50), reddit.rising(limit=50),
                       reddit.top(limit=150), reddit.top(limit=1), reddit.hot(limit=80), reddit.controversial(limit=1)]
            if sort in sorts:
                posts = [x for x in reddits[sorts.index(sort)] if not x.stickied]
            else:
                return await ctx.send(
                    f"⚠️**{ctx.author.mention}**, that isn't a valid sort! Valid sorts include {', '.join(sorts)}.")
            submission = random.choice(posts)
            if submission.is_self:
                embed = discord.Embed(title=submission.title,
                                      colour=0x5643fd,
                                      description=submission.selftext, timestamp=ctx.message.created_at)
            else:
                embed = discord.Embed(title=submission.title,
                                      colour=0x5643fd,
                                      timestamp=ctx.message.created_at)
                embed.set_image(url=submission.url)

            embed.set_author(name=f"u/{submission.author.name}", icon_url=submission.author.icon_img)
            embed.set_footer(text=f'r/{submission.subreddit}',
                             icon_url=submission.subreddit.icon_img)
            embed.set_thumbnail(url=submission.subreddit.icon_img)
            embed.add_field(name='Score', value=f'<:upvote:751314607808839803> {submission.score}')
            embed.add_field(name='Comments', value=f'💬 {submission.num_comments}')
            await message.edit(
                embed=embed) if not submission.over_18 or submission.over_18 and ctx.channel.is_nsfw() \
                else await message.edit(embed=discord.Embed(title='Warning!',
                                                            description=f"⚠️:underage: **{ctx.author.mention}**, "
                                                                        f"NSFW channel required!", color=0xFF0000,
                                                            timestamp=ctx.message.created_at)
                                        .set_image(url='https://i.kym-cdn.com/entries/icons/facebook/000/033/758/Screen'
                                                       '_Sh'
                                                       'ot_2020-04-28_at_12.21.48_PM.jpg'))
        except NameError:
            embed = discord.Embed(title='Error', description=
            'That is not a valid subreddit. Please try again using a different name.',
                                  color=0xFF0000, timestamp=ctx.message.created_at)
            embed.set_thumbnail(url=self.errorurl)
            await ctx.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(title='Error', description=e, color=0xFF0000, timestamp=ctx.message.created_at)
            await ctx.send(embed=embed)

    @commands.command()
    async def votes(self, ctx, link):
        """See the number of upvotes on a post before two hours."""
        thing = discord.Embed(title='Loading...', color=0x5643fd,
                              description='<a:loading:743537226503421973> '
                                          'Gathering stats <a:loading:743537226503421973>',
                              timestamp=ctx.message.created_at)
        thing.set_image(url='https://i.imgur.com/gVX3yPJ.gif?noredirect')
        thing.set_footer(text=f'Requested by {ctx.message.author}', icon_url=ctx.message.author.avatar_url)
        message = await ctx.send(embed=thing)
        post = self.reddit.submission(url=link)
        if post.is_self:
            embed = discord.Embed(title=post.title,
                                  colour=0x5643fd,
                                  description=post.selftext, timestamp=ctx.message.created_at, url=link)
            embed.add_field(name='Metrics', value=f"The linked post currently has ``{post.score}`` upvotes and "
                                                  f"``{post.num_comments}`` comments.")
        else:
            embed = discord.Embed(title=post.title,
                                  colour=0x5643fd,
                                  timestamp=ctx.message.created_at,
                                  description=f"The linked post currently has ``{post.score}`` upvotes and "
                                              f"``{post.num_comments}`` comments.", url=link)
            embed.set_image(url=post.url)
        embed.set_author(name=f"u/{post.author.name}", icon_url=post.author.icon_img)
        await message.edit(embed=embed)


def setup(client):
    client.add_cog(Reddit(client, reddit=praw.Reddit(client_id=reddit_client_id,
                                                     client_secret=reddit_client_secret,
                                                     username=reddit_username,
                                                     password=reddit_password,
                                                     user_agent=reddit_user_agent
                                                     )))
