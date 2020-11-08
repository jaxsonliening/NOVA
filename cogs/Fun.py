
import discord
import aiohttp
import random
import asyncio
import io
from aiotrivia import TriviaClient, AiotriviaException
from discord.ext import commands
from secrets import *


class Fun(commands.Cog):
    """Use NOVA to have a little fun on your server"""

    def __init__(self, client):
        self.client = client
        self.trivia = TriviaClient()

    @commands.command(aliases=['pupper', 'doggo'])
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

    @commands.command(aliases=['catto', 'kitty'])
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

    @commands.command()
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

    @commands.command(aliases=['birb'])
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

    @commands.command()
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

    @commands.group(invoke_without_command=True, aliases=['astronomy'])
    async def apod(self, ctx):
        # APOD command group
        """Astronomy Picture of the Day"""
        p = ctx.prefix
        async with aiohttp.ClientSession() as cs, ctx.typing():
            async with cs.get(f"https://api.nasa.gov/planetary/apod?api_key={nasa_key}") \
                    as resp:
                if resp.status != 200:
                    return await ctx.send('<:RedX:707949835960975411> No image could be found')
                else:
                    js = await resp.json()
                    embed = discord.Embed(color=0x5643fd, title=js['title'],
                                          timestamp=ctx.message.created_at)
                    embed.set_image(url=js['url'])
                    embed.add_field(name='Date', value=js['date'], inline=True)
                    embed.add_field(name='Sub Commands',
                                    value=f"``{p}apod hd``\n``{p}apod description``\n``{p}apod date``",
                                    inline=True)
                    embed.set_footer(text=f"Copyright {js['copyright']}")
                    await ctx.send(embed=embed)

    @apod.command()
    async def date(self, ctx, date):
        """Show the astronomy picture of the day for a given date (YYYY-MM-DD)"""
        link = f"https://api.nasa.gov/planetary/apod?date={date}&api_key={nasa_key}"
        async with aiohttp.ClientSession() as cs, ctx.typing():
            async with cs.get(link) as resp:
                if resp.status != 200:
                    return await ctx.send('<:RedX:707949835960975411> No image could be found')
                else:
                    js = await resp.json()
                    embed = discord.Embed(color=0x5643fd, title=js['title'],
                                          timestamp=ctx.message.created_at)
                    embed.set_image(url=js['url'])
                    embed.add_field(name='Date', value=js['date'], inline=True)
                    embed.add_field(name='HD Version', value=f"<:asset:734531316741046283> [Link]({js['hdurl']})",
                                    inline=True)
                    embed.set_footer(text=f"Copyright {js['copyright']}")
                    await ctx.send(embed=embed)

    @apod.command()
    async def hd(self, ctx):
        """HD version for the astronomy picture of the day"""
        async with aiohttp.ClientSession() as cs, ctx.typing():
            async with cs.get(f"https://api.nasa.gov/planetary/apod?api_key={nasa_key}") \
                    as resp:
                if resp.status != 200:
                    return await ctx.send('<:RedX:707949835960975411> No image could be found')
                else:
                    js = await resp.json()
                    embed = discord.Embed(color=0x5643fd, title=f"{js['title']} (HD)",
                                          timestamp=ctx.message.created_at)
                    embed.set_image(url=js['hdurl'])
                    embed.set_footer(text=f"Copyright {js['copyright']}")
                    await ctx.send(embed=embed)

    @apod.command()
    async def description(self, ctx):
        """Explanation for the astronomy picture of the day"""
        async with aiohttp.ClientSession() as cs, ctx.typing():
            async with cs.get(f"https://api.nasa.gov/planetary/apod?api_key={nasa_key}") \
                    as resp:
                if resp.status != 200:
                    return await ctx.send('<:RedX:707949835960975411> No description could be found')
                else:
                    js = await resp.json()
                    embed = discord.Embed(color=0x5643fd, title=js['title'], description=js['explanation'],
                                          timestamp=ctx.message.created_at)
                    embed.set_footer(text=f"Copyright {js['copyright']}")
                    await ctx.send(embed=embed)

    @commands.command()
    async def inspiro(self, ctx):
        """Look at beautiful auto-generated quotes"""
        url = 'https://inspirobot.me/api?generate=true'
        async with aiohttp.ClientSession() as cs, ctx.typing():
            async with cs.get(url) as r:
                data = await r.text()
        embed = discord.Embed(color=0x5643fd,
                              description="<:github:734999696845832252> [Source Code](https://github.com/DevilJamJar/"
                                          "DevilBot/blob/master/cogs/fun.py)", timestamp=ctx.message.created_at)
        embed.set_image(url=data)
        embed.set_footer(text='Copyright 2020 Deviljamjar')
        await ctx.send(embed=embed)

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

    @commands.command()
    async def motivation(self, ctx):
        """Need motivation? NOVA has you covered."""
        responses = ['https://youtu.be/kGOQfLFzJj8', 'https://youtu.be/kYfM5uKBKKg', 'https://youtu.be/VV_zfO3HmTQ',
                     'https://youtu.be/fLeJJPxua3E', 'https://youtu.be/5aPntFAyRts', 'https://youtu.be/M2NDQOgGycg',
                     'https://youtu.be/FDDLCeVwhx0', 'https://youtu.be/P10hDp6mUG0', 'https://youtu.be/K8S8OvPhMDg',
                     'https://youtu.be/zzfREEPbUsA', 'https://youtu.be/mgmVOuLgFB0', 'https://youtu.be/t8ApMdi24LI',
                     'https://youtu.be/JXQN7W9y_Tw', 'https://youtu.be/fKtmM_45Dno', 'https://youtu.be/k9zTr2MAFRg',
                     'https://youtu.be/bm-cCn0uRXQ', 'https://youtu.be/9bXWNeqKpjk', 'https://youtu.be/ChF3_Zbuems',
                     'https://youtu.be/BmIM8Hx6yh8', 'https://youtu.be/oNYKDM4_ZC4', 'https://youtu.be/vdMOmeljTvA',
                     'https://youtu.be/YPTuw5R7NKk', 'https://youtu.be/jnT29dd7LWM', 'https://youtu.be/7XzxDIJKXlk']
        await ctx.send(random.choice(responses))

    @commands.command()
    async def hex(self, ctx, code):
        """Explore hex colors"""
        color = discord.Colour(int(code, 16))
        thumbnail = f'https://some-random-api.ml/canvas/colorviewer?hex={code}'
        async with aiohttp.ClientSession() as cs, ctx.typing():
            async with cs.get(f"https://www.thecolorapi.com/id?hex={code}") \
                    as resp:
                if resp.status != 200:
                    return await ctx.send('<:RedX:707949835960975411> No hex code could be found.')
                else:
                    js = await resp.json()
                    name = js['name']
                    image = js['image']
                    rgb = js['rgb']
                    hsl = js['hsl']
                    hsv = js['hsv']
                    cmyk = js['cmyk']
                    xyz = js['XYZ']
                    try:
                        embed = discord.Embed(title=f"Showing hex code ``#{code}``", color=color,
                                              timestamp=ctx.message.created_at)
                        embed.set_thumbnail(url=thumbnail)
                        embed.add_field(name='Name', value=f"{name['value']}")
                        embed.add_field(name='Exact name?', value=f"``{name['exact_match_name']}``")
                        embed.add_field(name='Closest named hex', value=f"``{name['closest_named_hex']}``")
                        embed.add_field(name='🔗 Image Links',
                                        value=f"<:asset:734531316741046283> [Bare]({image['bare']})\n"
                                              f"<:asset:734531316741046283> [Labeled]({image['named']})",
                                        inline=False)
                        embed.add_field(name='Other Codes',
                                        value=f"**rgb**({rgb['r']}, {rgb['g']}, {rgb['b']})\n"
                                              f"**hsl**({hsl['h']}, {hsl['s']}, {hsl['l']})\n"
                                              f"**hsv**({hsv['h']}, {hsv['s']}, {hsv['v']})\n"
                                              f"**cmyk**({cmyk['c']}, {cmyk['m']}, {cmyk['y']}, {cmyk['k']})\n"
                                              f"**XYZ**({xyz['X']}, {xyz['Y']}, {xyz['Z']})", inline=False)
                        await ctx.send(embed=embed)
                    except ValueError:
                        await ctx.send("<:redx:732660210132451369> "
                                       "That is not a valid hex code, please try again with a different value.")
                    except BaseException:
                        await ctx.send("<:redx:732660210132451369> "
                                       "Could not process that hex code, please try again with a different value.")

    @commands.command()
    @commands.cooldown(1, 59, commands.BucketType.member)
    async def poke(self, ctx, member: discord.Member, *, message):
        """This command shows up in the dictionary under the definition of annoying."""
        member = member or ctx.message.author
        await ctx.send(f'<a:a_check:742966013930373151> Message successfully sent to ``{member}``')
        embed = discord.Embed(title=f'Message from {ctx.message.author}:', color=0x5643fd, description=message,
                              timestamp=ctx.message.created_at)
        await member.send(embed=embed)

    @commands.command()
    async def news(self, ctx, result: int = 0):
        """Show the top headlines in the U.S. for today. Enter a number (0-15) to show a certain result. """
        url = f'https://newsapi.org/v2/top-headlines?country=us&apiKey={news_key}'
        # I could get a lot more results than 15 articles but it updates everyday and the results are always different
        # I had to put a reasonable limit on the index so the index was always in range to avoid errors.
        sort = range(-1, 16)
        if result not in sort:
            return await ctx.send('<:redx:732660210132451369> This is not a valid search index. Please choose a number '
                                  'between 0 and 15.')
        if result in sort:
            async with aiohttp.ClientSession() as cs, ctx.typing():
                async with cs.get(url) as resp:
                    if resp.status == 500:
                        return await ctx.send("<:redx:732660210132451369> The API's server is currently down. "
                                              "Check back later. This is not a problem on my end.")
                    if resp.status == 429:
                        return await ctx.send('<:redx:732660210132451369> This command is on a timeout. '
                                              'Check back tomorrow when we have more API requests available.')
                    if resp.status == 400:
                        return await ctx.send('<:redx:732660210132451369> Something went wrong with the request. '
                                              'Try again with different parameters.')
                    if resp.status == 200:
                        js = await resp.json()
                        # result is the index
                        a = js['articles'][result]
                        embed = discord.Embed(color=0x5643fd, timestamp=ctx.message.created_at, title=a['title'],
                                              url=a['url'])
                        embed.add_field(name='Content', inline=False, value=a['content'])
                        embed.add_field(name='Publish Date', inline=False, value=a['publishedAt'])
                        embed.add_field(name='Source', inline=False, value=a['source']['name'])
                        embed.set_author(name=a['author'])
                        embed.set_image(url=a['urlToImage'])
                        return await ctx.send(embed=embed)

    @commands.command()
    async def chat(self, ctx, *, words):
        """Chat with an AI."""
        url = f'https://some-random-api.ml/chatbot?message={words}'
        async with aiohttp.ClientSession() as cs, ctx.typing():
            async with cs.get(url) as resp:
                if resp.status != 200:
                    return await ctx.send("<:redx:732660210132451369> Looks like there was an error and you won't be "
                                          "able to chat today.")
                js = await resp.json()
                await ctx.send(js['response'])

    @commands.command()
    async def lyrics(self, ctx, *, song):
        """Find song lyrics."""
        url = f'https://some-random-api.ml/lyrics?title={song}'
        async with aiohttp.ClientSession() as cs, ctx.typing():
            async with cs.get(url) as resp:
                if resp.status != 200:
                    return await ctx.send("<:redx:732660210132451369> Could not find any lyrics for that song.")
                js = await resp.json()
                thumbnail = js['thumbnail']
                links = js['links']
                embed = discord.Embed(title=js['title'], color=0x5643fd, timestamp=ctx.message.created_at,
                                      description=f"*[Find the full lyrics on genius.com"
                                                  f"]({links['genius']})*\n\n{js['lyrics'][:1000]}")
                embed.set_thumbnail(url=thumbnail['genius'])
                embed.set_author(name=f"By: {js['author']}")

                await ctx.send(embed=embed)

    @commands.command(aliases=['thispersondoesnotexist'])
    async def person(self, ctx):
        """This person does not exist."""
        async with aiohttp.ClientSession() as cs, ctx.typing():
            async with cs.get('https://fakeface.rest/face/json') as resp:
                if resp.status != 200:
                    return await ctx.send("<:redx:732660210132451369> Could not find you a person.")
                js = await resp.json()
                gender = js['gender'].capitalize()
                embed = discord.Embed(title='This person does not exist', timestamp=ctx.message.created_at,
                                      color=0x5643fd)
                embed.set_image(url=js['image_url'])
                embed.add_field(name='Age:', value=js['age'], inline=True)
                embed.add_field(name='Gender:', value=gender, inline=True)
                embed.set_footer(text=f"Source: {js['source']}")
                await ctx.send(embed=embed)

    @commands.command()
    async def weather(self, ctx, *, city):
        """Gather weather data for a given city."""
        url = f'http://api.weatherapi.com/v1/current.json?key=c1319477d52b4806a66154914200211&q={city}'
        direction_list = {
            "N": "North",
            "S": "South",
            "E": "East",
            "W": "West",
            "NW": "Northwest",
            "NE": "Northeast",
            "SE": "Southeast",
            "SW": "Southwest",
            "NNW": "North-Northwest",
            "NNE": "North-Northeast",
            "WNW": "West-Northwest",
            "ENE": "East-Northeast",
            "WSW": "West-Southwest",
            "ESE": "East-Southeast",
            "SSW": "South-Southwest",
            "SSE": "South-Southeast"}
        async with aiohttp.ClientSession() as cs, ctx.typing():
            async with cs.get(url) as resp:
                if resp.status != 200:
                    return await ctx.send(f"<:redx:732660210132451369> Could not find any weather data for ``{city}``.")
                js = await resp.json()
                embed = discord.Embed(color=0x5643fd, title=js['location']['name'], timestamp=ctx.message.created_at,
                                      description=f"**Region:** {js['location']['region']}\n"
                                                  f"**Country:** {js['location']['country']}\n"
                                                  f"**Coordinates:** {js['location']['lat']}, {js['location']['lon']}\n"
                                                  f"**Timezone:** {js['location']['tz_id']}\n"
                                                  f"**Local Time:** {js['location']['localtime']}")
                embed.set_thumbnail(url=f"https:{js['current']['condition']['icon']}")
                embed.add_field(name='**__Weather Data:__** <:temperature:742933558221340723>☀', inline=False,
                                value=
                                f"**Overview:** {js['current']['condition']['text']}\n"
                                f"**Temperature:** {js['current']['temp_c']} Celsius | "
                                f"{js['current']['temp_f']} Fahrenheit\n"
                                f"**Feels like:** {js['current']['feelslike_c']} Celsius | "
                                f"{js['current']['feelslike_f']} Fahrenheit\n"
                                f"**Wind Speed:** {js['current']['wind_kph']} kph | {js['current']['wind_mph']} mph\n"
                                f"**Wind Direction:** {direction_list[js['current']['wind_dir']]}\n"
                                f"**Humidity:** {js['current']['humidity']}\n"
                                f"**Cloud Coverage:** {js['current']['cloud']}%")
                await ctx.send(embed=embed)

    @commands.command()
    async def mastermind(self, ctx):
        """You have 10 tries to guess a 4 digit code. Can you do it?"""
        part = random.sample(list(map(str, list(range(9)))), 4)
        code = [int(x) for x in part]
        human_code = "".join(str(x) for x in code)
        print(human_code)
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
                                   f"<a:party:773063086109753365>\nYou cracked the code in **{i+1}** tries.")
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


def setup(client):
    client.add_cog(Fun(client))
