import discord
import aiohttp
import random
import asyncio
import io
import re
import wikipedia
import json
import requests
from aiotrivia import TriviaClient, AiotriviaException
from discord.ext import commands
from secrets import *
from random import randint, choice, sample
from big_lists import *


async def send_wiki():
    thing = discord.Embed(title='Loading...', color=0x5643fd,
                          description='Please stand by this process should be over shortly',
                          timestamp=ctx.message.created_at)
    thing.set_image(url='https://i.imgur.com/gVX3yPJ.gif?noredirect')
    thing.set_footer(text=f'Requested by {ctx.message.author}', icon_url=ctx.message.author.avatar_url)
    message = await ctx.send(embed=thing)
    waki = wikipedia.page(topic)
    image = wikipedia.page(topic).images[0]
    embed = discord.Embed(title=waki.title, color=0x5643fd, url=waki.url, timestamp=ctx.message.created_at,
                          description=f"{wikipedia.summary(topic, sentences=2)}\n\n*For more "
                                      f"information, click the title.*")
    embed.set_image(url=image)
    embed.set_thumbnail(url="https://imgur.com/UFc1ntQ.png")
    await message.edit(embed=embed)


class api(commands.Cog):
    """Interact with other parts of the internet using APIs."""

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['wiki'])
    async def wikipedia(self, ctx, *, topic):
        """Find information on any topic using wikipedia."""
        results = wikipedia.search(topic)
        if len(results) == 1:
            await send_wiki()
        elif len(results) == 0:
            await ctx.send("<:redx:732660210132451369> No pages could be found relating to this topic.")
        else:
            top = ""
            result_keys = []
            values = []
            for index, value in enumerate(results, 1):
                top += "{}. {}\n".format(index, value)
                result_keys.append(str(index))
                values.append(value)
            embed = discord.Embed(title=f"I found {len(results)} results for your topic.", color=0x5643fd,
                                  timestamp=ctx.message.created_at,
                                  description=f'Are any of these your topic? Reply with the number of the desired '
                                              f'result if it shows '
                                              f'up otherwise just reply with **no**.\n\n'
                                              f'{top}')
            delete_this_one = await ctx.send(embed=embed)
            try:
                while True:
                    ms = await self.client.wait_for("message", check=lambda m: m.author == ctx.author, timeout=60)
                    if ms.content.lower() in (yee.lower() for yee in results):
                        topi = ms.content
                        thing = discord.Embed(title='Loading...', color=0x5643fd,
                                              description='Please stand by this process should be over shortly',
                                              timestamp=ctx.message.created_at)
                        thing.set_image(url='https://i.imgur.com/gVX3yPJ.gif?noredirect')
                        thing.set_footer(text=f'Requested by {ctx.message.author}',
                                         icon_url=ctx.message.author.avatar_url)
                        message = await ctx.send(embed=thing)
                        waki = wikipedia.page(topi)
                        image = wikipedia.page(topi).images[0]
                        embed = discord.Embed(title=waki.title, color=0x5643fd, url=waki.url,
                                              timestamp=ctx.message.created_at,
                                              description=f"{wikipedia.summary(topi, sentences=2)}\n\n*For more "
                                                          f"information, click the title.*")
                        embed.set_image(url=image)
                        embed.set_thumbnail(url="https://imgur.com/UFc1ntQ.png")
                        await delete_this_one.delete()
                        await ms.delete()
                        await message.edit(embed=embed)
                        return False
                    elif ms.content in result_keys:
                        value_index = int(ms.content) - 1
                        topico = values[value_index]
                        thing = discord.Embed(title='Loading...', color=0x5643fd,
                                              description='Please stand by this process should be over shortly',
                                              timestamp=ctx.message.created_at)
                        thing.set_image(url='https://i.imgur.com/gVX3yPJ.gif?noredirect')
                        thing.set_footer(text=f'Requested by {ctx.message.author}',
                                         icon_url=ctx.message.author.avatar_url)
                        message = await ctx.send(embed=thing)
                        waki = wikipedia.page(topico)
                        image = wikipedia.page(topico).images[0]
                        embed = discord.Embed(title=waki.title, color=0x5643fd, url=waki.url,
                                              timestamp=ctx.message.created_at,
                                              description=f"{wikipedia.summary(topico, sentences=2)}\n\n*For more "
                                                          f"information, click the title.*")
                        embed.set_image(url=image)
                        embed.set_thumbnail(url="https://imgur.com/UFc1ntQ.png")
                        await delete_this_one.delete()
                        await ms.delete()
                        await message.edit(embed=embed)
                        return False
                    elif ms.content.lower() == "no":
                        await delete_this_one.delete()
                        await ctx.send("Welp sorry about that :/\nMaybe try again with more specific search terms.")
                        return False
                    else:
                        await delete_this_one.delete()
                        await ctx.send("You didn't reply with one of the options or no.")
                        return True
            except wikipedia.PageError:
                return await ctx.send("<:redx:732660210132451369> Sorry, but we could not access a page "
                                      "under this name.")
            except wikipedia.DisambiguationError:
                return await ctx.send("<:redx:732660210132451369> Sorry, but we could not access a page "
                                      "under this name.")
            except asyncio.TimeoutError:
                return await ctx.send("You never responded so the process was abandoned.")
            except discord.Forbidden:
                pass

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
                    await ctx.send(embed=embed)



def setup(client):
    client.add_cog(api(client))
