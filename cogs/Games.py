import discord
import aiohttp
import random
import asyncio
import json
import io
import re
import akinator
from aiotrivia import TriviaClient, AiotriviaException
from discord.ext import commands
from secrets import *
from contextlib import suppress
from async_timeout import timeout

quiplash_questions = ["What two words would passengers never want to hear a pilot say?",
                      "You would never go on a roller coaster called _____",
                      "The secret to a happy life",
                      "If a winning coach gets Gatorade dumped on his head, what should get dumped on the losing coach?",
                      "Name a candle scent designed specifically for Kim Kardashian",
                      "You should never give alcohol to ______",
                      "Everyone knows that monkeys hate ______",
                      "The biggest downside to living in Hell",
                      "Jesus's REAL last words",
                      "The worst thing for an evil witch to turn you into",
                      "The Skittles flavor that just missed the cut",
                      "On your wedding night, it would be horrible to find out that the person you married is ____",
                      "A name for a really bad Broadway musical",
                      "The first thing you would do after winning the lottery",
                      "Why ducks really fly south in the winter",
                      "America's energy crisis would be over if we made cars that ran on ______",
                      "It's incredibly rude to ____ with your mouth open"
                      "What's actually causing global warming?",
                      "A name for a brand of designer adult diapers",
                      "Name a TV drama that's about a vampire doctor",
                      "Something squirrels probably do when no one is looking",
                      "The crime you would commit if you could get away with it",
                      "Come up with a great title for the next awkward teen sex movie",
                      "What's the Mona Lisa smiling about?",
                      "A terrible name for a cruise ship",
                      "What FDR meant to say was We have nothing to fear, but _____",
                      "Come up with a title for an adult version of any classic video game",
                      "The name of a font nobody would ever use",
                      "Something you should never put on an open wound"
                      "Scientists say erosion, but we all know the Grand Canyon was actually made by _____",
                      "The real reason the dinosaurs died"
                      "Come up with the name of a country that doesn't exist",
                      "The best way to keep warm on a cold winter night",
                      "A college major you don't see at many universities",
                      "What would make baseball more entertaining to watch?",
                      "The best thing about going to prison",
                      "The best title for a new national anthem for the USA",
                      "Come up with the name of book that would sell a million copies, immediately",
                      "What would you do if you were left alone in the White House for an hour?",
                      "Invent a family-friendly replacement word that you could say instead of an actual curse word",
                      "A better name for testicles",
                      "The name of the reindeer Santa didn't pick to pull his sleigh",
                      "What's the first thing you would do if you could time travel?",
                      "The name of a pizza place you should never order from",
                      "A not-very-scary name for a pirate",
                      "Come up with a name for a beer made especially for monkeys",
                      "The best thing about living in an igloo",
                      "The worst way to be murdered",
                      "Something you shouldn't get your significant other for Valentine's Day",
                      "A dangerous thing to do while driving",
                      "Something you shouldn't wear to a job interview",
                      "The #1 reason penguins can't fly",
                      "Using only two words, a new state motto for Texas",
                      "The hardest thing about being Batman",
                      "A great way to kill time at work",
                      "Come up with a really bad TV show that starts with Baby",
                      "Why does the Tower of Pisa lean?",
                      "What's wrong with these kids today?",
                      "A great new invention that starts with Automatic",
                      "Come up with a really bad football penalty that begins with Intentional",
                      "A Starbucks coffee that should never exist",
                      "There's Gryffindor, Ravenclaw, Slytherin, and Hufflepuff, but what's the Hogwarts house few "
                      "have ever heard of?",
                      "The worst words to say for the opening of a eulogy at a funeral",
                      "Something you should never use as a scarf",
                      "Invent a holiday that you think everyone would enjoy",
                      "The best news you could get today",
                      "Usually, it's bacon,lettuce and tomato, but come up with a BLT you wouldn't want to eat",
                      "The worst thing you could stuff a bed mattress with",
                      "A great opening line to start a conversation with a stranger at a party",
                      "Something you would like to fill a swimming pool with",
                      "Miley Cyrus' Wi-Fi password, possibly",
                      "If you were allowed to name someone else's baby any weird thing you wanted, "
                      "what would you name it?",
                      "A fun thing to think about during mediocre sex",
                      "You know you're in for a bad taxi ride when _____",
                      "Where do babies come from?",
                      "The terrible fate of the snowman Olaf in a director's cut of 'Frozen'",
                      "Sometimes, after a long day, you just need to ______",
                      "The worst way to spell Mississippi",
                      "Give me one good reason why I shouldn't spank you right now",
                      "The best pick-up line for an elderly singles mixer",
                      "A good stage name for a chimpanzee stripper",
                      "The best place to bury all those bodies",
                      "One place a finger shouldn't go",
                      "Come up with a name for the most difficult yoga pose known to mankind",
                      "What's lurking under your bed when you sleep?",
                      "The name of a canine comedy club with puppy stand-up comedians",
                      "A great name for a nude beach in Alaska",
                      "Make up the title of a movie that is based on the first time you had sex",
                      "A vanity license plate a jerk in an expensive car would get",
                      "A good fake name to use when checking into a hotel",
                      "A good catchphrase to yell every time you finish pooping",
                      "Your personal catchphrase if you were on one of those 'Real Housewives' shows",
                      "The Katy Perry Super Bowl halftime show would have been better with _____",
                      "Okay... fine! What do YOU want to talk about then?!!!",
                      "Miller Lite beer would make a lot of money if they came up with a beer called Miller Lite _____",
                      "Something you should never stick up your butt",
                      "A terrible name for a clown",
                      "An inappropriate thing to do at a cemetery"]


class Games(commands.Cog):
    """Play games in your server"""

    def __init__(self, client):
        self.client = client
        self.trivia = TriviaClient()
        self.aki = akinator.Akinator()

    @commands.command()
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

    @commands.command(aliases=['ql'])
    async def quiplash(self, ctx):
        """Play the popular jakcbox game quiplash (extreme help from nizcomix)"""
        msg = await ctx.send('**QUIPLASH** - Send `join` into chat now to reserve a spot!')
        users = []
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
                        if len(users) == 8:
                            break
                        continue
            finally:
                await ctx.send("Starting the game, answer the prompt in your DMs")
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
                        await msg.author.send("Your response has been recorded! Check back in the original"
                                              " channel to vote.")
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
                    await ctx.send(ques)
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


def setup(client):
    client.add_cog(Games(client))
