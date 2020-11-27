import discord
import aiohttp
import random
import asyncio
import io
import re
from aiotrivia import TriviaClient, AiotriviaException
from discord.ext import commands
from secrets import *


class Games(commands.Cog):
    """Play games in your server"""

    def __init__(self, client):
        self.client = client
        self.trivia = TriviaClient()

    @commands.command()
    async def mastermind(self, ctx):
        """You have 10 tries to guess a 4 digit code. Can you do it?"""
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

    @commands.command()
    async def magic(self, ctx):
        """The first time a bot can do a magic trick."""
        num1 = random.randint(10, 30)
        num2 = random.randint(10, 30)
        num3 = random.randint(10, 30)
        final = num1 - num2 + num3
        embed = discord.Embed(title='Discord Magic', color=0x5643fd, timestamp=ctx.message.created_at,
                              description="NOVA has recently ascended the human race and can now read minds. To begin, "
                                          "think of a number and make sure to remember it. Once you have"
                                          " done that type `ok` into chat.")
        embed.set_thumbnail(url='https://imgur.com/Gc8aiyG.png')
        await ctx.send(embed=embed)
        try:
            while True:
                msg = await self.client.wait_for('message', timeout=30, check=lambda m: m.author == ctx.author)
                if msg.content.lower() == 'ok':
                    await ctx.send(f'Good, like I said you should remember that. The next step is to **add** {num1}'
                                   f' to your original number. Remember this one too. Reply with `ok` once you have '
                                   f' figured it out.')
                    msg = await self.client.wait_for('message', timeout=30, check=lambda m: m.author == ctx.author)
                    if msg.content.lower() == 'ok':
                        await ctx.send(f'Now that you added {num1} to your original number, take the new number and'
                                       f' **subtract** {num2}. After doing this, reply with `ok`.')
                        msg = await self.client.wait_for('message', timeout=30, check=lambda m: m.author == ctx.author)
                        if msg.content.lower() == 'ok':
                            await ctx.send(
                                f'Now you need to **add** {num3} to the previous number. Once again reply with `ok` '
                                f'to continue the magic.')
                            msg = await self.client.wait_for('message', timeout=30,
                                                             check=lambda m: m.author == ctx.author)
                            await asyncio.sleep(2)
                            if msg.content.lower() == 'ok':
                                await ctx.send(
                                    f'Finally, subtract the number you thought of in the beginning. '
                                    f'See, you were supposed to remember it. Reply with one last `ok` to complete the '
                                    f'magic.')
                                msg = await self.client.wait_for('message', timeout=30,
                                                                 check=lambda m: m.author == ctx.author)
                                x = await ctx.send('<a:loading:743537226503421973> Calculating '
                                                   '<a:loading:743537226503421973>')
                                await asyncio.sleep(2)
                                await x.delete()
                                if msg.content.lower() == 'ok':
                                    await ctx.send(
                                        f'I have found that the final number you came up with was **{final}**!\n'
                                        f'If this was not your number, then you suck at math lol')
                                    break
                                else:
                                    await ctx.send("You didn't respond with `ok` so the trick was abandoned.")
                                    break
                            else:
                                await ctx.send("You didn't respond with `ok` so the trick was abandoned.")
                                break
                        else:
                            await ctx.send("You didn't respond with `ok` so the trick was abandoned.")
                            break
                    else:
                        await ctx.send("You didn't respond with `ok` so the trick was abandoned.")
                        break
                else:
                    await ctx.send("You didn't respond with `ok` so the trick was abandoned.")
                    break
        except asyncio.TimeoutError:
            embed = discord.Embed(title='Time Expired', color=0x56433fd, timestamp=ctx.message.created_at,
                                  description='You either suck at math or you left. If you want to try again just run'
                                              '`n.magic` again.')
            await ctx.send(embed=embed)

    @commands.command(aliases=['twenty-one', '21'])
    async def blackjack(self, ctx):
        deck = []
        suits = ['Hearts', 'Diamonds', 'Spades', 'Clubs']
        ranks = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 7, 'Nine': 10, 'Jack': 10,
                 'Queen': 10, 'King': 10, 'Ace': 11}
        for x in suits:
            for y in ranks:
                card = f"{y} of {x}"
                deck.append(card)
        cards = random.sample(deck, 2)
        await ctx.send(cards)


def setup(client):
    client.add_cog(Games(client))
