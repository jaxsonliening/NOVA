import discord
import aiohttp
import random
import asyncio
import json
import io
import re
import akinator
import time
import asyncpraw
import requests
import urllib3
import urllib
import itertools
import time
import textwrap
from time import perf_counter
from aiotrivia import TriviaClient, AiotriviaException
from discord.ext import commands
from secrets import *
from contextlib import suppress
from async_timeout import timeout
from big_lists import *
from PIL import Image, ImageDraw, ImageSequence, ImageFont


class games(commands.Cog):
    """Play games in your server"""

    def __init__(self, client, reddit):
        self.client = client
        self.trivia = TriviaClient()
        self.aki = akinator.Akinator()
        self.coin = "<:coin:781367758612725780>"
        self.reddit = reddit

    reddit = asyncpraw.Reddit(client_id=reddit_client_id,
                              client_secret=reddit_client_secret,
                              username=reddit_username,
                              password=reddit_password,
                              user_agent=reddit_user_agent)

    @commands.command(aliases=['mm'])
    async def mastermind(self, ctx):
        """You have 5 tries to guess a 4 digit code. Can you do it?"""
        part = random.sample(list(map(str, list(range(9)))), 4)
        code = [int(x) for x in part]
        human_code = "".join(str(x) for x in code)
        embed = discord.Embed(title='Welcome to Mastermind', color=0x5643fd, timestamp=ctx.message.created_at,
                              description='Mastermind is a logic and guessing game where you have to find a four-digit '
                                          'code in only five tries. Type out four numbers to begin guessing!\n\n'
                                          '<:redx:732660210132451369> ``The number you guessed is incorrect``\n'
                                          '<:ticknull:732660186057015317> ``The number you guessed is in the code, '
                                          'but not '
                                          'in the right spot``\n'
                                          '<:tickgreen:732660186560462958> ``You have the right digit and in the '
                                          'correct spot``')
        await ctx.send(embed=embed)
        i = 0
        while i < 5:
            try:
                result = ""
                msg = await self.client.wait_for('message', timeout=60, check=lambda m: m.author == ctx.author)
                r = [int(x) for x in msg.content]
                if len(msg.content) != 4:
                    await ctx.send('Please only guess four-digit numbers.')
                    continue
                for element in r:
                    if element in code:
                        if r.index(element) == code.index(element):
                            result += "<:tickgreen:732660186560462958>"
                        else:
                            result += "<:ticknull:732660186057015317>"
                    else:
                        result += "<:redx:732660210132451369>"
                await ctx.send(result)
                if r == code:
                    await ctx.send(f"<a:party:773063086109753365> That's the right code. You win! "
                                   f"<a:party:773063086109753365>\nYou cracked the code in **{i + 1}** tries.")
                    break
                i += 1
            except ValueError:
                await ctx.send(f'{ctx.message.author.mention}, that is not a valid code! Please try again '
                               f'with actual numbers.')
                continue
            except asyncio.TimeoutError:
                await ctx.send(f'{ctx.message.author.mention},'
                               f' you took too long to guess! The correct code was **{human_code}**.')
                break
        else:
            await ctx.send(f"{ctx.message.author.mention}, you ran out of tries! The correct code was "
                           f"**{human_code}**.")

    @commands.command()
    async def fight(self, ctx, member: discord.Member = None):
        """Fight other members to the death."""
        if member is None:
            return await ctx.send('<:redx:732660210132451369> You must have someone '
                                  'to fight in order to run this command!')
        user_mention = member
        user = member.display_name
        auth_mention = ctx.message.author.mention
        auth = ctx.message.author.display_name
        weapon_list = ['Russian AK-47', 'revolver', 'crossbow', 'Sniper-AWP', 'SCAR-20', 'sword', 'knife', 'shotgun',
                       'spear',
                       'desert eagle', 'steel axe', 'trebuchet', 'Marksmen rifle', 'Hunting rifle', 'slingshot',
                       'nuclear bomb', 'trident', 'torpedo', 'cannon', 'catapult', 'nerf gun', 'land mine',
                       'grenade', 'M-16', 'lead-pipe', 'Glock-17', 'Burst-AUG', 'P-90', 'double-barrel shotgun',
                       'sawed-off shotgun', 'FAMAS', '.22 caliber rifle', 'hammer', 'bottle of bleach', 'tide-pod']
        healing_list = ['band-aid', 'first aid kit', 'bottle of alcohol', 'bottle of essential oils', 'flu vaccine',
                        'plague mask',
                        'gas mask', 'magic potion', "witch's spell", 'bottle of cough syrup']
        try:
            await ctx.send(f"**{auth}** has entered the arena and challenged **{user}** to a duel.\n"
                           f"{user_mention.mention} do you accept?\n``yes|no``")
            msg = await self.client.wait_for('message', check=lambda m: m.author == user_mention, timeout=15)
            if msg.content.lower() == 'yes':
                await ctx.send(f'Fight has begun!')
                auth_health = 100
                user_health = 100
                await ctx.send(embed=discord.Embed(description=f'{auth}: <:heart:775889971931512842>'
                                                               f'{auth_health}\n'
                                                               f'{user}: <:heart:775889971931512842>{user_health}',
                                                   color=0x5643fd))
                while user_health > 0 and auth_health > 0:
                    try:
                        await asyncio.sleep(2)
                        await ctx.send(f"{user_mention.mention} it is now your turn. Would you like to ``attack``, "
                                       f"``heal``, or ``end``?")
                        msg = await self.client.wait_for('message', check=lambda m: m.author == user_mention,
                                                         timeout=15)
                        if msg.content.lower() == 'attack':
                            weapon = random.choice(weapon_list)
                            damage = random.randint(25, 50)
                            after = auth_health - damage
                            auth_health -= damage
                            await ctx.send(f"{user_mention.mention} did **{damage}** "
                                           f"damage to {auth} with a "
                                           f"{weapon}.\n{auth} has <:heart:775889971931512842>{after} health"
                                           f" remaining.")
                        elif msg.content.lower() == 'heal':
                            if user_health > 99:
                                await ctx.send("Well that did nothing, "
                                               "you can't heal if you already have full health.")
                            else:
                                heal = random.choice(healing_list)
                                points = random.randint(25, 50)
                                after = user_health + points
                                user_health += points
                                await ctx.send(f"After deciding to heal, {user} gained **{points}** health by "
                                               f"using a {heal}. \nTheir total health is now "
                                               f"<:heart:775889971931512842>{after}")
                        elif msg.content.lower() == 'end':
                            await ctx.send(f'{user} has ended the match. <:owner:730864906429136907>{auth}'
                                           f'<:owner:730864906429136907> is the winner!')
                            await ctx.send(embed=discord.Embed(description=f'{auth}: <:heart:775889971931512842>'
                                                                           f'{auth_health}\n'
                                                                           f'{user}: <:heart:775889971931512842>'
                                                                           f'{user_health}',
                                                               color=0x5643fd))
                            break
                        if auth_health < 1:
                            await asyncio.sleep(2)
                            await ctx.send(f'{auth} has lost all of their health. <:owner:730864906429136907>'
                                           f'{user_mention.mention}<:owner:730864906429136907> wins!')
                            await ctx.send(embed=discord.Embed(description=f'{auth}: <:heart:775889971931512842>'
                                                                           f'0\n'
                                                                           f'{user}: <:heart:775889971931512842>'
                                                                           f'{user_health}',
                                                               color=0x5643fd))
                            break
                        await asyncio.sleep(2)
                        await ctx.send(f"{auth_mention} now it's your turn. Would you like to `attack`, `heal`, or"
                                       f" `end`?")
                        msg = await self.client.wait_for('message', check=lambda m: m.author == ctx.message.author,
                                                         timeout=15)
                        if msg.content.lower() == 'attack':
                            weapon = random.choice(weapon_list)
                            damage = random.randint(25, 50)
                            after = user_health - damage
                            user_health -= damage
                            await ctx.send(f"{auth_mention} did **{damage}** "
                                           f"damage to {user} with a "
                                           f"{weapon}.\n{user} has <:heart:775889971931512842>{after} health"
                                           f" remaining.")
                        elif msg.content.lower() == 'heal':
                            if auth_health > 99:
                                await ctx.send("Well that did nothing, "
                                               "you can't heal if you already have full health.")
                            else:
                                heal = random.choice(healing_list)
                                points = random.randint(25, 50)
                                after = auth_health + points
                                auth_health += points
                                await ctx.send(f"After deciding to heal, {auth} gained **{points}** health by "
                                               f"using a {heal}. \nTheir total health is now "
                                               f"<:heart:775889971931512842>{after}")
                        elif msg.content.lower() == 'end':
                            await ctx.send(f'{auth} has ended the match. <:owner:730864906429136907>{user}'
                                           f'<:owner:730864906429136907> is the winner!')
                            await ctx.send(embed=discord.Embed(description=f'{auth}: <:heart:775889971931512842>'
                                                                           f'{auth_health}\n'
                                                                           f'{user}: <:heart:775889971931512842>'
                                                                           f'{user_health}',
                                                               color=0x5643fd))
                            break
                        if user_health < 1:
                            await asyncio.sleep(2)
                            await ctx.send(f'{user} has lost all of their health. <:owner:730864906429136907>'
                                           f'{auth_mention}<:owner:730864906429136907> wins!')
                            await ctx.send(embed=discord.Embed(description=f'{auth}: <:heart:775889971931512842>'
                                                                           f'{auth_health}\n'
                                                                           f'{user}: <:heart:775889971931512842>'
                                                                           f'0',
                                                               color=0x5643fd))
                            break
                        continue
                    except asyncio.TimeoutError:
                        await ctx.send('<:redx:732660210132451369> You took too long to respond! '
                                       'The fight was abandoned.')
            elif msg.content.lower() == 'no':
                return await ctx.send(f'**{user}** has declined the match. Better luck next time :/')
            else:
                return await ctx.send(f"<:redx:732660210132451369> {user_mention.mention}, "
                                      f"you didn't respond with yes or no so the match "
                                      f"was cancelled.")
        except asyncio.TimeoutError:
            await ctx.send('<:redx:732660210132451369> You took too long to respond! The fight was abandoned.')

    @commands.command()
    async def trivia(self, ctx, difficulty: str = None):
        """Test out your knowledge with trivia questions from nizcomix#7532"""
        difficulty = difficulty or random.choice(['easy', 'medium', 'hard'])
        try:
            question = await self.trivia.get_random_question(difficulty)
        except AiotriviaException:
            return await ctx.send(embed=discord.Embed(title='That is not a valid sort.',
                                                      description='Valid sorts are ``easy``, ``medium``, and ``hard``.',
                                                      color=0xFF0000))
        answers = question.responses
        d = difficulty.capitalize()
        random.shuffle(answers)
        final_answers = '\n'.join([f"{index}. {value}" for index, value in enumerate(answers, 1)])
        await ctx.send(embed=discord.Embed(
            title=f"{question.question}", description=f"\n{final_answers}\n\nQuestion about: **{question.category}"
                                                      f"**\nDifficulty: **{d}**",
            color=0x5643fd))
        answer = answers.index(question.answer) + 1
        try:
            while True:
                msg = await self.client.wait_for('message', timeout=15, check=lambda m: m.author == ctx.message.author)
                if str(answer) in msg.content:
                    return await ctx.send(embed=discord.Embed(description=f"{answer} was correct ({question.answer})",
                                                              color=0x32CD32, title='Correct!'))
                if str(answer) not in msg.content:
                    return await ctx.send(embed=discord.Embed(description=f"Unfortunately **{msg.content}** was wrong. "
                                                                          f"The "
                                                                          f"correct answer was ``{question.answer}``.",
                                                              title='Incorrect', color=0xFF0000))
        except asyncio.TimeoutError:
            embed = discord.Embed(title='Time expired', color=0xFF0000,
                                  description=f"The correct answer was {question.answer}")
            await ctx.send(embed=embed)

    @commands.command(aliases=['aki'])
    async def akinator(self, ctx):
        """Let NOVA guess a person of your choice."""
        answers = ["y", "yes", "n", "no", "0", "1", "2", "3", "4", "i", "idk", "i dont know",
                   "i don't know", "pn", "probably not", "probably", "p"]
        embed = discord.Embed(title="Welcome to Akinator",
                              description="""Think of any character, they can be fictional or a real person. 
                                          You will be asked questions about this character and it is your job 
                                          to respond with one of the five acceptable answers:\n
                                           **• yes**
                                           **• no**
                                           **• idk**
                                           **• probably** 
                                           **• probably not**\n
                                           Reply with **stop** to end the game.""",
                              color=0x5643fd,
                              timestamp=ctx.message.created_at)
        embed.set_thumbnail(url="https://imgur.com/Hkny5Fz.jpg")
        await ctx.send(embed=embed)
        try:
            self.aki.start_game()
            await ctx.send(self.aki.answer("idk"))
            questions = 0
            while self.aki.progression <= 80:
                ms = await self.client.wait_for("message", check=lambda m: m.author == ctx.author, timeout=60)
                if ms.content.lower() in answers:
                    ques = self.aki.answer(ms.content)
                    await ctx.send(f"**{ctx.message.author.display_name}:**\n{ques}")
                    questions += 1
                    continue
                elif ms.content.lower() == "stop":
                    await ctx.send("The game has ended. Thanks for playing!")
                    return
                else:
                    continue
            self.aki.win()
            embed = discord.Embed(title=f"It's {self.aki.first_guess['name']}", color=0x5643fd,
                                  timestamp=ctx.message.created_at,
                                  description=f"**Description:** {self.aki.first_guess['description']}\n\n"
                                              f"I made this guess in **{questions}** tries.\n\n"
                                              f"**Was I correct?**\nyes/no")
            embed.set_image(url=self.aki.first_guess['absolute_picture_path'])
            await ctx.send(embed=embed)
            try:
                correct = await self.client.wait_for('message', check=lambda c: c.author == ctx.author, timeout=60)
                if correct.content.lower() == "yes" or correct.content.lower() == "y" or correct.content == ":flushed:":
                    await ctx.send("<a:party:773063086109753365> Congratulations <a:party:773063086109753365>")
                elif correct.content.lower() == "no" or correct.content.lower() == "n":
                    try:
                        second_guess = self.aki.guesses[1]
                        embed = discord.Embed(title=f"My second guess is {second_guess['name']}", color=0x5643fd,
                                              timestamp=ctx.message.created_at,
                                              description=f"**Description:** {second_guess['description']}\n\n"
                                                          f"I made this guess in **{questions}** tries.\n\n"
                                                          f"**Was I correct?**\nyes/no")
                        embed.set_image(url=second_guess['absolute_picture_path'])
                        await ctx.send(embed=embed)
                        m = await self.client.wait_for('message', check=lambda c: c.author == ctx.author, timeout=60)
                        if m.content.lower() == "yes" or m.content.lower() == "y" or m.content == ":flushed:":
                            await ctx.send("<a:party:773063086109753365> Congratulations <a:party:773063086109753365>")
                        else:
                            await ctx.send("Welp, better luck next time.")
                    except IndexError:
                        await ctx.send("Welp, better luck next time.")
            except asyncio.TimeoutError:
                await ctx.send("You took too long to respond so the game was abandoned")
        except asyncio.TimeoutError:
            await ctx.send("You took too long to respond so the game was abandoned")

    @commands.command(aliases=['type'])
    async def typing(self, ctx):
        """Test your typing skills with this fun and interactive game."""
        sentence = random.choice(sentences)
        word_count = len(sentence.split())
        embed = discord.Embed(title="Welcome to Typing Test", color=0x5643fd, timestamp=ctx.message.created_at,
                              description="The game will be starting in `5` seconds. Get ready!")
        embed.add_field(name="Directions", value="You will be sent a random sentence and it is yo"
                                                 "ur duty to type back the "
                                                 "sentence as quick as possible with as few mistakes as possible.",
                        inline=False)
        embed.add_field(name="Rules", value="Be warned: punctuation, capitalization, and spelling DO matter.",
                        inline=False)
        await ctx.send(embed=embed)
        await asyncio.sleep(5)
        await ctx.send("**3...**")
        await asyncio.sleep(1)
        await ctx.send("**2...**")
        await asyncio.sleep(1)
        await ctx.send("**1...**")
        await asyncio.sleep(1)
        await ctx.send("**GO**")
        await asyncio.sleep(1)
        await ctx.send(sentence)
        try:
            start = perf_counter()
            msg = await self.client.wait_for('message', timeout=60, check=lambda x: x.author == ctx.author)
            user_characters = list(msg.content)
            characters = list(sentence)
            maximum = range(0, len(characters))
            correct = 0
            for indexer in maximum:
                try:
                    if user_characters[indexer] == characters[indexer]:
                        correct += 1
                except IndexError:
                    pass
            accuracy = correct / len(characters) * 100
            stop = perf_counter()
            total = round(stop - start)
            part_of_minute = total / 60
            await ctx.send(f"<:clock:738186842343735387> Time: `{total}` seconds\n"
                           f"<:star:737736250718421032> Speed: `{round(word_count / part_of_minute)}` WPM\n"
                           f"<:license:738176207895658507> Accuracy: `{round(accuracy)}`%")
        except asyncio.TimeoutError:
            await ctx.send("You took over a minute to send your sentence back so the process was abandoned.")
        except ZeroDivisionError:
            await ctx.send("Lmao you are so bad at typing that you got a zero percent accuracy.")

    @commands.command(aliases=['gr'])
    async def guessreddit(self, ctx, subreddit=None):
        """Look at two reddit posts and decide which one got more upvotes"""
        try:
            subreddit_list = ["holup", "dankmemes", "memes"]
            listed = ", ".join(str(sub) for sub in subreddit_list)
            if subreddit is None:
                await ctx.send(f"Here is the list of currently available subs you can choose to play from:\n\n"
                               f"`{listed}`\n\nSend which subreddit you would like to use into chat.")
                msg = await self.client.wait_for("message", check=lambda x: x.author == ctx.message.author, timeout=60)
                if msg.content in subreddit_list:
                    subreddit = msg.content
                else:
                    return await ctx.send("That subreddit is not available for this game.\n"
                                          "Try again with a different sub.")
            if subreddit not in subreddit_list:
                return await ctx.send(f"That subreddit is not available for this game. "
                                      f"\nThe current available subreddits are `{listed}`.")
            ms = await ctx.send("<a:loading:743537226503421973> Please wait while the game is loading... "
                                "<a:loading:743537226503421973>")
            posts = []
            emojis = ["1️⃣", "2️⃣"]
            sub = await self.reddit.subreddit(subreddit, fetch=True)
            async for submission in sub.top("day", limit=50):
                if not submission.stickied:
                    posts.append(str(submission.id))
            random.shuffle(posts)
            final_ids = random.sample(posts, 2)
            post1 = await self.reddit.submission(id=final_ids[0])
            post2 = await self.reddit.submission(id=final_ids[1])
            await ms.delete()
            embed1 = discord.Embed(title="Image 1", color=0x5643fd)
            embed1.set_image(url=post1.url)
            embed1.set_footer(text=f"r/{subreddit}")
            await ctx.send(embed=embed1)
            embed2 = discord.Embed(title="Image 2", color=0x5643fd)
            embed2.set_image(url=post2.url)
            embed2.set_footer(text=f"r/{subreddit}")
            await ctx.send(embed=embed2)
            msg = await ctx.send("Can you figure out which post got more upvotes?\n"
                                 "React with 1️⃣ or 2️⃣ to make your guess.")
            await msg.add_reaction("1️⃣")
            await msg.add_reaction("2️⃣")
            score1 = "{:,}".format(post1.score)
            score2 = "{:,}".format(post2.score)
            reaction, user = await self.client.wait_for('reaction_add', check=lambda r, u: str(
                r.emoji) in emojis and u.id == ctx.author.id and r.message.id == msg.id,
                                                  timeout=60)
            if int(post1.score) > int(post2.score) and str(reaction.emoji) == emojis[0]:
                await ctx.send(f"Congratulations! `1` was the correct answer with <:upvote:751314607808839803>"
                               f" `{score1}` upvotes.\nImage 2 "
                               f"only had <:upvote:751314607808839803> `{score2}` upvotes.")
            elif int(post1.score) < int(post2.score) and str(reaction.emoji) == emojis[1]:
                await ctx.send(f"Congratulations! `2` was the correct answer with <:upvote:751314607808839803> "
                               f"`{score2}` upvotes.\nImage 1 "
                               f"only had <:upvote:751314607808839803> `{score1}` upvotes.")
            elif int(post1.score) > int(post2.score) and str(reaction.emoji) == emojis[1]:
                await ctx.send(f"Unfortunately, `2` was the incorrect answer.\nImage 1 had <:upvote:751314607808839803>"
                               f" `{score1}` upvotes "
                               f"while Image 2 had <:upvote:751314607808839803> `{score2}` upvotes.")
            elif int(post1.score) < int(post2.score) and str(reaction.emoji) == emojis[0]:
                await ctx.send(f"Unfortunately, `1` was the incorrect answer.\n"
                               f"Image 2 had <:upvote:751314607808839803> `{score2}` upvotes "
                               f"while Image 1 only had <:upvote:751314607808839803> `{score1}` upvotes.")
            else:
                await ctx.send("You did not react with the correct emojis so the game was cancelled.")
        except asyncio.TimeoutError:
            await ctx.send("You never reacted with a guess so the game was cancelled.")

    @commands.command()
    async def captionary(self, ctx):
        """A fun game based on captioning different gifs."""
        game_master = ctx.message.author.id
        random.shuffle(gif_links)
        random.shuffle(inspiration)
        gifs = gif_links[:20]
        embed = discord.Embed(title="Captionary", color=0x5643fd, timestamp=ctx.message.created_at,
                              description="Captionary is a fun game based on submitting captions for different gifs."
                                          "There are anywhere between 5 and 20 rounds and players submit their best"
                                          "captions to be voted on.")
        embed.add_field(name='**Commands**',
                        value='➤ `caption` - submit your caption\n'
                              '➤ `!inspire` - get a free caption idea\n'
                              '➤ `!stop` - used by the game master to end the game', inline=False)
        embed.add_field(name='**Game Master**',
                        value=f'{ctx.message.author.mention} is the game master for this match! '
                              f'This user holds the power to end the game at any time using the `!stop` command.')
        embed.set_image(url='https://imgur.com/qUPbXKI.jpg')
        await ctx.send(embed=embed)
        await ctx.send(f"{ctx.message.author.mention} as the game master, you get to choose the round length."
                       f"\nYou can choose any number between **30** and **120**.")
        try:
            waiter = await self.client.wait_for("message", check=lambda x: x.author.id == game_master, timeout=30)
            if 29 < int(waiter.content) < 121:
                round_time = int(waiter.content)
                await ctx.send(f"Round time has been set at **{round_time}**")
            elif 30 > int(waiter.content) or 120 < int(waiter.content):
                round_time = 60
                await ctx.send(
                    f"That is not a number between 30 and 120 so the round time has been set at `60`.")
            else:
                round_time = 60
                await ctx.send(f"That is not a number between 30 and 120 so the round time has been set at `60`.")
        except asyncio.TimeoutError:
            round_time = 60
            await ctx.send(f"{ctx.message.author.display_name} never responded so the round time has been set at `60`.")
            pass
        except ValueError:
            round_time = 60
            await ctx.send(f"You did not respond with a number so the round "
                           f"time has been set at `60`.")
            pass
        await ctx.send(f"{ctx.message.author.mention} additionally, you get to choose how many rounds will be played.\n"
                       f"You may choose any number between **5** and **20**.")
        try:
            waiter = await self.client.wait_for("message", check=lambda x: x.author.id == game_master, timeout=30)
            if 4 < int(waiter.content) < 20:
                total_rounds = int(waiter.content) + 1
                await ctx.send(f"The number of rounds has been set at **{total_rounds}**")
            elif 5 > int(waiter.content) or 20 < int(waiter.content):
                total_rounds = 11
                await ctx.send(f"That is not a number between **5** and **20** so the number of rounds "
                               f"has been set at `10`.")
            else:
                total_rounds = 11
                await ctx.send(f"That is not a number between **5** and **20** so the number of rounds "
                               f"has been set at `10`.")
        except asyncio.TimeoutError:
            total_rounds = 11
            await ctx.send(f"{ctx.message.author.display_name}"
                           f" never responded so the number of rounds has been set at `10`.")
            pass
        await asyncio.sleep(2)
        await ctx.send("Get Ready! The game will start in **15 seconds**.")
        await asyncio.sleep(15)
        rounds = 1
        gif_index = 0
        players = []
        # game loop
        while rounds < total_rounds:
            end_time = time.time() + round_time
            await ctx.send(f"**ROUND {rounds}/{total_rounds}**")
            gif_link = await ctx.send(gifs[gif_index])
            if rounds == 1:
                pass
            elif len(players) == 0 and rounds != 1:
                await ctx.send("There were no players for this round so the game has ended.")
                break
            else:
                await ctx.send(" ".join(player.mention for player in players))
            try:
                round_players = []
                round_answers = []
                # round loop

                while time.time() < end_time:
                    msg = await self.client.wait_for("message", check=lambda x: x.author != ctx.bot, timeout=120)
                    if "!caption" in msg.content:
                        if msg.author.id in round_players:
                            await ctx.send("You've already given a caption for this round!")
                        if msg.author not in players:
                            players.append(msg.author)
                        if msg.author.id not in round_players:
                            await msg.add_reaction('<:tickgreen:732660186560462958>')
                            round_players.append(msg.author)
                            round_answers.append(msg.content)
                        else:
                            continue
                    elif "!inspire" in msg.content:
                        await ctx.send(random.choice(inspiration))
                        continue
                    elif "!stop" == msg.content and msg.author.id == game_master:
                        return await ctx.send("Thanks for playing, this game has ended!")
            except asyncio.TimeoutError:
                pass
            # end loop here
            rounds += 1
            gif_index += 1
        await ctx.send("Thanks for playing!")

    @commands.command()
    async def race(self, ctx, member: discord.Member = None):
        """See who can be the fastest in this quick-paced game."""
        progress = "<:loading_filled:730823516059992204>"
        if member is None:
            return await ctx.send('<:redx:732660210132451369> You must mention someone to play against!')
        player_1 = "🐕 |  "
        player_2 = "🐈 |  "
        accept_or_decline = ["<:tickgreen:732660186560462958>", "<:redx:732660210132451369>"]
        emojis = ["🐕", "🐈"]
        msg = await ctx.send(f"{member.mention}\n\n{ctx.message.author.display_name} wants to race!\n"
                             f"React with <:tickgreen:732660186560462958> or <:redx:732660210132451369>"
                             f"to accept or decline.")
        await msg.add_reaction("<:tickgreen:732660186560462958>")
        await msg.add_reaction("<:redx:732660210132451369>")
        try:
            reaction, user = await self.client.wait_for("reaction_add", timeout=60, check=lambda r, u: str(r.emoji) in accept_or_decline and u.id == member.id and r.message.id == msg.id)
            if str(reaction.emoji) == accept_or_decline[0]:
                delete_dis = await ctx.send(f"{member.mention} has accepted! The game will begin in **5** seconds.")
                await asyncio.sleep(5)
                await msg.delete()
                await delete_dis.delete()
                await ctx.send(f"**Player 1 - {ctx.message.author.display_name}**")
                player_1_progression = await ctx.send(player_1)
                await ctx.send(f"**Player 2 - {member.display_name}**")
                player_2_progression = await ctx.send(player_2)
                msg2 = await ctx.send("GO! React with your animal to win.")
                await msg2.add_reaction("🐕")
                await msg2.add_reaction("🐈")
                while len(player_1) < 156 and len(player_2) < 156:
                    reaction, user = await self.client.wait_for("reaction_add", timeout=60, check=lambda r, u: str(
                        r.emoji) in emojis and u.id == ctx.message.author.id or member.id and r.message.id == msg.id)
                    if str(reaction.emoji) == emojis[0] and user.id == ctx.message.author.id:
                        player_1 += progress
                        await player_1_progression.edit(content=player_1)
                        await asyncio.sleep(1)
                    elif str(reaction.emoji) == emojis[1] and user.id == member.id:
                        player_2 += progress
                        await player_2_progression.edit(content=player_2)
                        await asyncio.sleep(1)
                if len(player_1) > len(player_2):
                    return await ctx.send(f"<:owner:730864906429136907>{ctx.message.author.display_name} "
                                          f"is the winner!\n"
                                          f"Thanks to {member.display_name} for playing.")
                if len(player_1) < len(player_2):
                    return await ctx.send(f"<:owner:730864906429136907>{member.display_name} is the winner!\n"
                                          f"Thanks to {ctx.message.author.display_name} for playing.")
            elif str(reaction.emoji) == accept_or_decline[1]:
                return await ctx.send(f"{member.mention} has declined. Better luck next time!")
        except asyncio.TimeoutError:
            return await ctx.send(f"The game has timed out due to inactivity.")


def setup(client):
    client.add_cog(games(client, reddit=asyncpraw.Reddit(client_id=reddit_client_id,
                                                         client_secret=reddit_client_secret,
                                                         username=reddit_username,
                                                         password=reddit_password,
                                                         user_agent=reddit_user_agent)))
