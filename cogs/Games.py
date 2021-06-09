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
from time import perf_counter
from aiotrivia import TriviaClient, AiotriviaException
from discord.ext import commands
from secrets import *
from contextlib import suppress
from async_timeout import timeout
from big_lists import *


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
        econ_data = open("economy.json", "r")
        money = json.load(econ_data)
        econ_data.close()
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
                    if str(ctx.message.author.id) in money.keys():
                        money[str(ctx.message.author.id)]['wallet'] += 100
                        econ_data = open("economy.json", "w")
                        json.dump(money, econ_data)
                        econ_data.close()
                        await ctx.send(f"You also gained {self.coin}`100` for winning.")
                    break
                i += 1
            except ValueError:
                await ctx.send(f'{ctx.message.author.mention}, that is not a valid code! Please try again '
                               f'with actual numbers.')
                continue
            except asyncio.TimeoutError:
                await ctx.send(f'{ctx.message.author.mention},'
                               f' you took too long to guess! The correct code was **{human_code}**.')
                if ctx.message.author.id in money.keys():
                    money[str(ctx.message.author.id)]['wallet'] -= 100
                    econ_data = open("economy.json", "w")
                    json.dump(money, econ_data)
                    econ_data.close()
                    await ctx.send(f"You also lost {self.coin}`100` for losing.")
                break
        else:
            await ctx.send(f"{ctx.message.author.mention}, you ran out of tries! The correct code was "
                           f"**{human_code}**.")
            if str(ctx.message.author.id) in money.keys():
                money[str(ctx.message.author.id)]['wallet'] -= 100
                econ_data = open("economy.json", "w")
                json.dump(money, econ_data)
                econ_data.close()
                await ctx.send(f"You also lost {self.coin}`100` for losing.")

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

    @commands.command(aliases=['ql'])
    async def quiplash(self, ctx):
        """Play the popular jackbox game quiplash (extreme help from nizcomix)"""
        users = []
        msg = await ctx.send('**QUIPLASH** - Send `join` into chat now to reserve a spot!')
        msg2 = await ctx.send(f"{len(users)}/8")
        await ctx.send(file=discord.File("/Users/jaxson/PycharmProjects/NOVABOT/quiplash.png"))
        local_quips = quiplash_questions
        with suppress(asyncio.TimeoutError):
            try:
                async with timeout(30):
                    while True:
                        app = await self.client.wait_for('message', check=lambda
                            x: x.channel == ctx.channel and x.author not in users and not x.author.bot
                               and x.content.lower() == "join")
                        await app.add_reaction('<:tickgreen:732660186560462958>')
                        content = msg.content + f"\n➤ {app.author.display_name}"
                        users.append(app.author)
                        await msg.edit(content=content)
                        await msg2.edit(content=f"{len(users)}/8")
                        if len(users) == 8:
                            break
                        continue
            finally:
                linked_message = await ctx.send("Starting the game, answer the prompt in your DMs")
        quip = random.choice(local_quips)
        local_quips.remove(quip)
        for user in users:
            await user.send('**The prompt for this round is:** \n{}'.format(quip))
        finals = []
        answerers = []
        with suppress(asyncio.TimeoutError):
            try:
                while True:
                    async with timeout(20):
                        msg = await self.client.wait_for('message',
                                                         check=lambda x: isinstance(x.channel, discord.DMChannel)
                                                                         and x.author not in answerers and x.author
                                                                         in users)
                        finals.append(msg.content)
                        answerers.append(msg.author)
                        await msg.add_reaction('<:tickgreen:732660186560462958>')
                        await msg.author.send(embed=discord.Embed(title=f"Your response has been recorded!\n"
                                                                        f"Check back in the original"
                                              f" channel to vote.", color=0x5643fd,
                                              description=f"[<:share:730823872265584680> "
                                                          f"Jump to message]({linked_message.jump_url})"))
                        if len(finals) == len(users):
                            break
                        continue
            finally:
                await ctx.send("Send the number of the quip you would like to vote for into chat")
        if not finals:
            return await ctx.send('There are no quips :/')
        await ctx.send(f"**The Prompt:** {quip}\n**The answers:**"
                       f":\n" + "\n".join([f"{i}. {v}" for i, v in enumerate(finals, 1)]))
        vote = {}
        for number in range(1, len(finals) + 1):
            vote[str(number)] = 0
        a = 0
        with suppress(asyncio.TimeoutError):
            while True:
                async with timeout(20):
                    msg = await self.client.wait_for('message', check=lambda
                        x: x.content.isdigit() and x.content in vote.keys() and x.author in users and x.channel == ctx.channel)
                    vote[msg.content] += 1
                    a += 1
                    if a == len(users):
                        break
                    continue
        winner = max(vote.items(), key=lambda m: m[1])
        quip = finals[int(winner[0]) - 1]
        user = answerers[int(winner[0]) - 1]
        return await ctx.send(f"Option {winner[0]} is the winner!\n`{quip}`\nWritten by "
                              f"<:owner:730864906429136907>**{user}**")

    @commands.command(aliases=['hm', 'guessword', 'wordguess'])
    async def hangman(self, ctx):
        """The classic word guessing game, hangman."""
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://www.randomlists.com/data/words.json") as resp:
                if resp.status != 200:
                    return await ctx.send('<:RedX:707949835960975411> Could not pick a word.')
                js = await resp.json()
                index = random.choice(range(0, 2465))
                word = js['data'][index]
                print(word)
                await ctx.send(f'Solve your word letter by letter or type out the full word into chat to complete.\n'
                               f'Send the letter you want to guess into chat now!')
                split_word = [str(x) for x in word]
                blanks = []
                tries = 7
                correct = 0
                for x in split_word:
                    blanks.append('\_ ')
                await ctx.send(f'You have **7** tries to start.')
                try:
                    while tries > 0:
                        blank_strings = "".join(str(char) for char in blanks)
                        await ctx.send(blank_strings)
                        if correct == len(word):
                            await ctx.send(f'<a:party:773063086109753365> '
                                           f'**{word}** is correct.'
                                           f'<a:party:773063086109753365>')
                            break
                        else:
                            pass
                        msg = await self.client.wait_for('message', timeout=60, check=lambda x: x.author == ctx.author)
                        if msg.content == word:
                            await ctx.send(f'<a:party:773063086109753365> '
                                           f'**{word}** is correct.'
                                           f'<a:party:773063086109753365>')
                            break
                        elif msg.content in split_word:
                            await ctx.send('<:tickgreen:732660186560462958>')
                            term_number = split_word.index(msg.content)
                            if blanks[term_number] == '\_ ':
                                blanks[term_number] = f"{msg.content} "
                            correct += 1
                            continue
                        else:
                            await ctx.send('<:redx:732660210132451369>')
                            tries -= 1
                            await ctx.send(f'You have **{tries}** tries left.')
                            continue
                    else:
                        await ctx.send(f'You ran out of tries!\n'
                                       f'The correct word was **{word}**')
                except asyncio.TimeoutError:
                    await ctx.send(f'You abandoned the game so the process was stopped. \nYour word was **{word}**.')

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

    @commands.group(invoke_without_command=True)
    async def case(self, ctx, *, case_name: str = None):
        """Open a CSGO case."""
        case_list = ['danger zone', 'prisma', 'fracture', 'operation broken fang', 'prisma 2', 'glove', 'cs20',
                     'spectrum']
        if not case_name:
            embed = discord.Embed(title="CSGO CASES", color=0x5643fd, timestamp=ctx.message.created_at,
                                  description="Here is a list of all available cases to open at the moment. "
                                              "I plan on adding more in the future but just enjoy these for "
                                              "the time being. Run `n.case <case_name>` to open one yourself!")
            embed.set_image(url="https://i.imgur.com/igOWNRL.gif")
            embed.set_thumbnail(url="https://imgur.com/INmWt3O.png")
            embed.add_field(name="Stats", inline=False, value="Run `n.case stats` to see the stats for each rarity\n"
                                                              "Run `n.case inventory` to see your personal inventory")
            embed.add_field(name="Cases", inline=False,
                            value="➤ random\n"
                                  "➤ danger zone\n"
                                  "➤ prisma\n"
                                  "➤ prisma 2\n"
                                  "➤ fracture\n"
                                  "➤ operation broken fang\n"
                                  "➤ glove\n"
                                  "➤ cs20\n"
                                  "➤ spectrum")
            embed.add_field(name="Chances", inline=False,
                            value="➤ Mil-Spec (Blue) - 79.92%\n"
                                  "➤ Restricted (Purple) - 15.96%\n"
                                  "➤ Classified (Pink) - 3.66%\n"
                                  "➤ Covert (Red) - 0.91%\n"
                                  "➤ Legendary (Gold) - 0.31%\n\nAll weapons have a 10% chance of being StatTrak:tm:")
            await ctx.send(embed=embed)
        else:
            try:
                # working on banking and filtering
                econ_data = open("economy.json", "r")
                money = json.load(econ_data)
                econ_data.close()
                if str(ctx.message.author.id) not in money.keys():
                    return await ctx.send("You cannot open a case because you haven't created a bank account yet!\n"
                                          "Run `n.create` in order to begin.")
                wallet_amount = money[str(ctx.message.author.id)]['wallet']
                if wallet_amount < 100:
                    return await ctx.send(f"You do not have enough money in your wallet to open a case!\n"
                                          f"You must have at least {self.coin}`100` in order to do so.")
                # writing in inventory
                inv = open("user_inv.json", "r")
                inventories = json.load(inv)
                if str(ctx.message.author.id) not in inventories.keys():
                    inventories[str(ctx.message.author.id)] = {"mil-spec": 0, "restricted": 0, "classified": 0,
                                                               "covert": 0, "rare legendary item": 0}
                    final = open("user_inv.json", "w")
                    json.dump(inventories, final)
                    final.close()
                # picking the case if it was random
                if case_name.lower() == "random":
                    case_name = random.choice(case_list)
                rarity = ''
                grade = ''
                # opening stats
                a_file = open("cases_stats.json", "r")
                case_stats = json.load(a_file)
                # take their money
                money[str(ctx.message.author.id)]['wallet'] -= 100
                econ_data = open("economy.json", "w")
                json.dump(money, econ_data)
                econ_data.close()
                # determine rarity
                out_number = random.randint(0, 1000000)
                if 0 <= out_number <= 799200:
                    rarity += "Mil-Spec"
                    rarity_color = 0x4b68fb
                    case_stats['mil-spec'] += 1
                    b_file = open("cases_stats.json", "w")
                    json.dump(case_stats, b_file)
                    b_file.close()
                    inventories[str(ctx.message.author.id)]['mil-spec'] += 1
                    final = open("user_inv.json", "w")
                    json.dump(inventories, final)
                    final.close()
                    back = 50
                elif 799201 <= out_number <= 959000:
                    rarity += "Restricted"
                    rarity_color = 0x8952fc
                    case_stats['restricted'] += 1
                    b_file = open("cases_stats.json", "w")
                    json.dump(case_stats, b_file)
                    b_file.close()
                    inventories[str(ctx.message.author.id)]['restricted'] += 1
                    final = open("user_inv.json", "w")
                    json.dump(inventories, final)
                    final.close()
                    back = 150
                elif 959001 <= out_number <= 991000:
                    rarity += "Classified"
                    rarity_color = 0xd55ae6
                    case_stats['classified'] += 1
                    b_file = open("cases_stats.json", "w")
                    json.dump(case_stats, b_file)
                    b_file.close()
                    inventories[str(ctx.message.author.id)]['classified'] += 1
                    final = open("user_inv.json", "w")
                    json.dump(inventories, final)
                    final.close()
                    back = 1000
                elif 991001 <= out_number <= 997400:
                    rarity += "Covert"
                    rarity_color = 0xc44546
                    case_stats['covert'] += 1
                    b_file = open("cases_stats.json", "w")
                    json.dump(case_stats, b_file)
                    b_file.close()
                    inventories[str(ctx.message.author.id)]['covert'] += 1
                    final = open("user_inv.json", "w")
                    json.dump(inventories, final)
                    final.close()
                    back = 5000
                else:
                    rarity += "Rare Legendary Item"
                    rarity_color = 0xFFD700
                    case_stats['rare legendary item'] += 1
                    b_file = open("cases_stats.json", "w")
                    json.dump(case_stats, b_file)
                    b_file.close()
                    inventories[str(ctx.message.author.id)]['rare legendary item'] += 1
                    final = open("user_inv.json", "w")
                    json.dump(inventories, final)
                    final.close()
                    back = 10000
                # determine grade
                out = random.randint(0, 10000)
                if 0 <= out <= 792:
                    grade += "Well-Worn"
                    multiplier = 1.05
                elif 793 <= out <= 1785:
                    grade += "Battle-Scarred"
                    multiplier = 1
                elif 1786 <= out <= 6103:
                    grade += "Field-Tested"
                    multiplier = 1.1
                elif 6104 <= out <= 8572:
                    grade += "Minimal Wear"
                    multiplier = 1.25
                else:
                    grade += "Factory New"
                    multiplier = 1.5
                number = random.randint(0, 10000)
                # decide stat trak
                if 0 <= number <= 1009:
                    StatTrak = True
                    multiplier += .5
                else:
                    StatTrak = False
                # load the cases
                a_file = open("cases.json", "r")
                cases = json.load(a_file)
                # pick a random skin from the rarity
                maxi = len(cases['cases'][case_name.lower()][rarity.lower()])
                indexer = random.randint(0, int(maxi))
                if indexer == maxi:
                    indexer = -1
                skin_name = cases['cases'][case_name.lower()][rarity.lower()][indexer]
                # pick out the image url
                image = cases['cases'][case_name.lower()][rarity.lower()][indexer][str(list(skin_name.keys())[0])][
                    'img_url']
                new_wallet_amount = back * multiplier
                rounded = round(new_wallet_amount)
                money[str(ctx.message.author.id)]['wallet'] += rounded
                econ_data = open("economy.json", "w")
                json.dump(money, econ_data)
                econ_data.close()
                description = f""
                percentage1 = multiplier - 1
                percentage = round(percentage1 * 100)
                if StatTrak is True:
                    description += f"StatTrak:tm: {rarity} \n{str(list(skin_name.keys())[0])} \n{grade}\n\n" \
                                   f"You spent {self.coin}`100` to open this case." \
                                   f"\nYour skin was {rarity} so you received {self.coin}`{back:,}` back.\n" \
                                   f"Your skin was also {grade} and StatTrak:tm:, which added a `{percentage}`% " \
                                   f"multiplier bringing your total money back to {self.coin}`{rounded:,}`."
                else:
                    description += f"{rarity} \n{str(list(skin_name.keys())[0])} \n{grade}\n\n" \
                                   f"You spent {self.coin}`100` to open this case." \
                                   f"\nYour skin was {rarity} so you received {self.coin}`{back:,}` back.\n" \
                                   f"Your skin was also {grade} so you received a `{percentage}`% multiplier " \
                                   f"bringing your total money back to {self.coin}`{rounded:,}`."
                embed = discord.Embed(color=0xF5F5F5)
                embed.set_image(url="https://i.imgur.com/igOWNRL.gif")
                msg = await ctx.send(embed=embed)
                await asyncio.sleep(2)
                embed = discord.Embed(title=f"{case_name.title()} Case", color=rarity_color, description=description)
                embed.set_image(url=image)
                embed.set_footer(text=f'Opened by {ctx.message.author}', icon_url=ctx.message.author.avatar_url)
                await msg.edit(embed=embed)
            except KeyError:
                embed = discord.Embed(title="CSGO CASES", color=0xFF0000, timestamp=ctx.message.created_at,
                                      description="The case you entered was not a valid case! There is a limited "
                                                  "number of cases you can open as more are being added. Below are a"
                                                  " list of the cases you can currently open. Use `n.case <case_name>`"
                                                  " to open them.")
                embed.set_thumbnail(url="https://imgur.com/INmWt3O.png")
                embed.add_field(name="Available Cases", inline=False,
                                value="➤ `random`\n"
                                      "➤ `danger zone`\n"
                                      "➤ `prisma`\n"
                                      "➤ `prisma 2`\n"
                                      "➤ `fracture`\n"
                                      "➤ `operation broken fang`\n"
                                      "➤ `glove`\n"
                                      "➤ `cs20`\n"
                                      "➤ `spectrum`")
                await ctx.send(embed=embed)

    @case.command()
    async def stats(self, ctx):
        """Shows the global stats for case openings."""
        a_file = open("cases_stats.json", "r")
        case_stats = json.load(a_file)
        total = case_stats['mil-spec'] + case_stats['restricted'] + case_stats['classified'] + case_stats['covert'] + \
                case_stats['rare legendary item']
        mil = case_stats['mil-spec'] * 50
        res = case_stats['restricted'] * 150
        cla = case_stats['classified'] * 1000
        cov = case_stats['covert'] * 5000
        rar = case_stats['rare legendary item'] * 10000
        money_earned = mil + res + cla + cov + rar
        percentage = round(((money_earned / (total * 100)) * 100) - 100)
        embed = discord.Embed(color=0x5643fd, title="CSGO Case Stats", timestamp=ctx.message.created_at)
        embed.set_thumbnail(url="https://imgur.com/INmWt3O.png")
        embed.add_field(name="Spending Stats", inline=False, value=f"➤ Money Spent: {self.coin}`{total * 100:,}`\n"
                                                                   f"➤ Money Earned: {self.coin}`{money_earned:,}`\n"
                                                                   f"➤ Profit Margin: `{percentage}%`")
        embed.add_field(name="Total Cases Opened", inline=False, value=f"➤ `{total:,}`")
        embed.add_field(name="Mil-Spec", inline=False, value=f"➤ `{case_stats['mil-spec']:,}`")
        embed.add_field(name="Restricted", inline=False, value=f"➤ `{case_stats['restricted']:,}`")
        embed.add_field(name="Classified", inline=False, value=f"➤ `{case_stats['classified']:,}`")
        embed.add_field(name="Covert", inline=False, value=f"➤ `{case_stats['covert']:,}`")
        embed.add_field(name="Rare Legendary Item", inline=False, value=f"➤ `{case_stats['rare legendary item']:,}`")
        await ctx.send(embed=embed)

    @case.command(aliases=['inv'])
    async def inventory(self, ctx, user: discord.Member = None):
        """Shows the global stats for case openings."""
        member = user or ctx.message.author
        a_file = open("user_inv.json", "r")
        case_stats = json.load(a_file)
        if str(ctx.message.author.id) not in case_stats.keys():
            return await ctx.send("You have no items in your inventory! Open some cases with `n.case` "
                                  "to gain some items.")
        elif str(member.id) not in case_stats.keys() and member.id != ctx.message.author.id:
            return await ctx.send("This user does not have any items in their inventory!")
        total = case_stats[str(member.id)]['mil-spec'] + \
                case_stats[str(member.id)]['restricted'] + \
                case_stats[str(member.id)]['classified'] + \
                case_stats[str(member.id)]['covert'] + \
                case_stats[str(member.id)]['rare legendary item']
        mil = case_stats[str(member.id)]['mil-spec'] * 50
        res = case_stats[str(member.id)]['restricted'] * 150
        cla = case_stats[str(member.id)]['classified'] * 1000
        cov = case_stats[str(member.id)]['covert'] * 5000
        rar = case_stats[str(member.id)]['rare legendary item'] * 10000
        money_earned = mil + res + cla + cov + rar
        percentage = round(((money_earned / (total * 100)) * 100) - 100)
        embed = discord.Embed(color=0x5643fd, title=f"{member.display_name}'s Inventory",
                              timestamp=ctx.message.created_at)
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name="Inventory Value", inline=False, value=f"➤ Money Spent: {self.coin}`{total * 100:,}`\n"
                                                                    f"➤ Money Earned: {self.coin}`{money_earned:,}`\n"
                                                                    f"➤ Profit Margin: `{percentage}%`")
        embed.add_field(name="Total Cases Opened", inline=False, value=f"➤ `{total:,}`")
        embed.add_field(name="Mil-Spec", inline=False,
                        value=f"➤ `{case_stats[str(member.id)]['mil-spec']:,}`")
        embed.add_field(name="Restricted", inline=False,
                        value=f"➤ `{case_stats[str(member.id)]['restricted']:,}`")
        embed.add_field(name="Classified", inline=False,
                        value=f"➤ `{case_stats[str(member.id)]['classified']:,}`")
        embed.add_field(name="Covert", inline=False,
                        value=f"➤ `{case_stats[str(member.id)]['covert']:,}`")
        embed.add_field(name="Rare Legendary Item", inline=False,
                        value=f"➤ `{case_stats[str(member.id)]['rare legendary item']:,}`")
        await ctx.send(embed=embed)

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
        embed.add_field(name="Rules", value="Be warned: punctuation, capitalization, and spelling DO matter.", inline=False)
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
            accuracy = correct/len(characters) * 100
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

    case_json_template = """
     "mil-spec": [{"": {"img_url": ""}},
                       {"": {"img_url": ""}},
                       {"": {"img_url": ""}},
                       {"": {"img_url": ""}},
                       {"": {"img_url": ""}},
                       {"": {"img_url": ""}},
                       {"": {"img_url": ""}}],
          "restricted": [{"": {"img_url": ""}},
                         {"": {"img_url": ""}},
                         {"": {"img_url": ""}},
                         {"": {"img_url": ""}},
                         {"": {"img_url": ""}}],
          "classified": [{"": {"img_url": ""}},
                         {"": {"img_url": ""}},
                         {"": {"img_url": ""}}],
          "covert": [{"": {"img_url": ""}},
                     {"": {"img_url": ""}}],
          "rare legendary item": [{"": {"img_url": ""}},
                                  {"": {"img_url": ""}},
                                  {"": {"img_url": ""}}]
    """

    @commands.command()
    async def guessreddit(self, ctx, subreddit):
        try:
            subreddit_list = ["holup", "dankmemes"]
            listed = ", ".join(str(sub) for sub in subreddit_list)
            if subreddit not in subreddit_list:
                return await ctx.send(f"That subreddit is not available for this game. "
                                      f"\nThe current available subreddits are `{listed}`.")
            ms = await ctx.send("<a:loading:743537226503421973> Please wait while the game is loading... "
                                "<a:loading:743537226503421973>")
            posts = []
            sub = await self.reddit.subreddit(subreddit, fetch=True)
            async for submission in sub.top("day", limit=50):
                if not submission.stickied:
                    posts.append(str(submission.id))
            random.shuffle(posts)
            final_ids = random.sample(posts, 2)
            post1 = await self.reddit.submission(id=final_ids[0])
            post2 = await self.reddit.submission(id=final_ids[1])
            await ms.delete()
            await ctx.send("Can you figure out which post got more upvotes? Look at each image and send "
                           "`1` or `2` in chat"
                           " to confirm your guess.")
            embed1 = discord.Embed(title="Image 1", color=0x5643fd)
            embed1.set_image(url=post1.url)
            await ctx.send(embed=embed1)
            embed2 = discord.Embed(title="Image 2", color=0x5643fd)
            embed2.set_image(url=post2.url)
            await ctx.send(embed=embed2)
            score1 = "{:,}".format(post1.score)
            score2 = "{:,}".format(post2.score)
            message = await self.client.wait_for('message', check=lambda x: x.author == ctx.message.author, timeout=60)
            if int(post1.score) > int(post2.score) and message.content == '1':
                await ctx.send(f"Congratulations! `1` was the correct answer with <:upvote:751314607808839803>"
                               f" {score1} upvotes. Image 2 "
                               f"only had <:upvote:751314607808839803> {score2} upvotes.")
            elif int(post1.score) < int(post2.score) and message.content == '2':
                await ctx.send(f"Congratulations! `2` was the correct answer with <:upvote:751314607808839803> "
                               f"{score2} upvotes. Image 1 " 
                               f"only had <:upvote:751314607808839803> {score1} upvotes.")
            elif int(post1.score) > int(post2.score) and message.content == '2':
                await ctx.send(f"Unfortunately, `2` was the incorrect answer. Image 1 had <:upvote:751314607808839803>"
                               f" {score1} upvotes "
                               f"while Image 2 had <:upvote:751314607808839803> {score2} upvotes.")
            elif int(post1.score) < int(post2.score) and message.content == '1':
                await ctx.send(f"Unfortunately, `1` was the incorrect answer. "
                               f"Image 2 had <:upvote:751314607808839803> {score2} upvotes "
                               f"while Image 1 only had <:upvote:751314607808839803> {score1} upvotes.")
            else:
                await ctx.send("You did not respond with `1` or `2` so the game was cancelled.")
        except asyncio.TimeoutError:
            await ctx.send("You never responded with a guess so the game was cancelled.")


def setup(client):
    client.add_cog(games(client, reddit=asyncpraw.Reddit(client_id=reddit_client_id,
                                                         client_secret=reddit_client_secret,
                                                         username=reddit_username,
                                                         password=reddit_password,
                                                         user_agent=reddit_user_agent)))
