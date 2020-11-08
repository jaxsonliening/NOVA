import discord
import cmath
import random
from discord.ext import commands


class Math(commands.Cog):
    """Various commands using math"""

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['calc'])
    async def calculate(self, ctx, *, operation):
        """Calculate an expression using a fancy discord calculator"""
        expression = operation
        words = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                 'u', 'v', 'w', 'x', 'y', 'z', '\\', '{', '}', '"', '&', '^', '$', '#', '@', '[', ']', '|', '?', '**']
        if any(words in operation for words in words):
            embed = discord.Embed(title='Warning', description='You are not allowed to do that.', color=0xFF0000,
                                  timestamp=ctx.message.created_at)
            embed.set_footer(text=f'Error occurred',
                             icon_url=ctx.message.author.avatar_url)
            embed.set_thumbnail(url='https://i.imgur.com/uafPEpb.png')
            await ctx.send(embed=embed)
            return
        meme = ['9+10']
        if any(words in operation for words in meme):
            embed = discord.Embed(title='Discord Calculator', color=0x5643fd, timestamp=ctx.message.created_at)
            embed.set_footer(text=f'Requested by {ctx.message.author}', icon_url=ctx.message.author.avatar_url)
            embed.set_thumbnail(url='https://pngimg.com/uploads/calculator/calculator_PNG7939.png')

            embed.add_field(name='Input Expression', value=f"```py\n{expression}```", inline=False)

            embed.add_field(name='Output Solution', value="```py\n21```", inline=False)

            return await ctx.send(embed=embed)
        if len(str(operation)) < 21:
            try:
                solution = eval(operation)
                embed = discord.Embed(title='Discord Calculator', color=0x5643fd, timestamp=ctx.message.created_at)
                embed.set_footer(text=f'Requested by {ctx.message.author}', icon_url=ctx.message.author.avatar_url)
                embed.set_thumbnail(url='https://pngimg.com/uploads/calculator/calculator_PNG7939.png')

                embed.add_field(name='Input Expression', value=f"```py\n{expression}```", inline=False)

                embed.add_field(name='Output Solution', value=f"```py\n{solution}```", inline=False)

                await ctx.send(embed=embed)
            except ZeroDivisionError:
                embed = discord.Embed(title='Error...', color=0xFF0000, description="You cannot divide by zero.",
                                      timestamp=ctx.message.created_at)
                embed.set_footer(text=f'Error occurred',
                                 icon_url=ctx.message.author.avatar_url)
                embed.set_thumbnail(url='https://i.imgur.com/uafPEpb.png')
                await ctx.send(embed=embed)
            except ValueError:
                embed = discord.Embed(title='Error...', color=0xFF0000, description="That expression is invalid.",
                                      timestamp=ctx.message.created_at)
                embed.set_footer(text=f'Error occurred',
                                 icon_url=ctx.message.author.avatar_url)
                embed.set_thumbnail(url='https://i.imgur.com/uafPEpb.png')
                await ctx.send(embed=embed)
            return
        else:
            embed = discord.Embed(title='Warning!', color=0xFF0000,
                                  description='Your operation must be under 21 characters long.',
                                  timestamp=ctx.message.created_at)
            embed.set_footer(text=f'Error occurred',
                             icon_url=ctx.message.author.avatar_url)
            embed.set_thumbnail(url='https://i.imgur.com/uafPEpb.png')
            await ctx.send(embed=embed)

    @commands.command(aliases=['quad'])
    async def quadratic(self, ctx, a: float = 1, b: float = 1, c: float = 0):
        """Calculate the solutions for a quadratic equation."""
        d = (b ** 2) - (4 * a * c)
        sol1 = (-b - cmath.sqrt(d)) / (2 * a)
        sol2 = (-b + cmath.sqrt(d)) / (2 * a)
        embed = discord.Embed(title='Solved!', timestamp=ctx.message.created_at, color=0x5643fd,
                              description=f'A value = ``{a}``\n'
                                          f'B value = ``{b}``\n'
                                          f'C value = ``{c}``')
        embed.set_image(url='https://imgur.com/X134y4a.png')
        embed.add_field(name='Solution One', value=f'```py\n{sol1}```', inline=False)
        embed.add_field(name='Solution Two', value=f'```py\n{sol2}```', inline=False)
        await ctx.send(embed=embed)

    @commands.command(aliases=['randomnumbergenerator', 'randomnum'])
    async def rng(self, ctx, num1: int = 1, num2: int = 100):
        """Have NOVA randomly choose from a range of numbers"""
        selection = (random.randint(num1, num2))
        embed = discord.Embed(title='Random Number Generator', color=0x5643fd, timestamp=ctx.message.created_at,
                              description=f'Choosing between ``{num1}`` and ``{num2}``\nI have chosen ``{selection}``')
        await ctx.send(embed=embed)

    @commands.group(invoke_without_command=True)
    async def convert(self, ctx):
        """Convert numbers across the imperial and metric system"""
        embed = discord.Embed(color=0x5643fd, title='Conversion Commands', timestamp=ctx.message.created_at,
                              description='**Do ``n.convert (command name) (unit)`` to use this command**\n\n'
                                          '``centimeters`` ----> Convert inches to centimeters\n'
                                          '``inches`` ----> Convert centimeters to inches\n'
                                          '``celsius`` ----> Convert Farenheit to Celsius\n'
                                          '``fahrenheit`` ----> Convert Celsius to Farenheit\n'
                                          '``meters`` ----> Convert feet to meters\n'
                                          '``feet`` ----> Convert meters to feet\n'
                                          '``kilograms`` ----> Convert pounds to kilograms\n'
                                          '``pounds`` ----> Convert kilograms to pounds\n'
                                          '``kilometers`` ----> Convert miles to kilometers\n'
                                          '``miles`` ----> Convert kilometers to miles')
        embed.set_footer(text=f'Requested by {ctx.message.author}', icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=embed)

    @convert.command(aliases=['cm'])
    async def centimeters(self, ctx, inches):
        """Convert inches to centimeters"""
        words = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                 'u', 'v', 'w', 'x', 'y', 'z', '\\', '{', '}', '"', '&', '^', '$', '#', '@', '[', ']', '|', '?', '**',
                 '*', '+', '=']
        if any(words in inches for words in words):
            embed = discord.Embed(title='Warning', description='This is not a valid number of inches', color=0xFF0000,
                                  timestamp=ctx.message.created_at)
            embed.set_footer(text=f'Error occurred',
                             icon_url=ctx.message.author.avatar_url)
            embed.set_thumbnail(url='https://i.imgur.com/uafPEpb.png')
            await ctx.send(embed=embed)
            return
        thing = eval(inches)
        solution = thing * 2.54
        cm = round(solution, 2)
        embed = discord.Embed(title=f'Converting {inches} inches to centimeters', color=0x5643fd,
                              timestamp=ctx.message.created_at)
        embed.add_field(name='Inches', value=f'```py\n{inches}```', inline=True)
        embed.add_field(name='Centimeters', value=f'```py\n{cm}```', inline=True)
        embed.add_field(name='Conclusion', value=f'``{inches}`` inches is equal to ``{cm}`` centimeters.', inline=False)
        await ctx.send(embed=embed)

    @convert.command(aliases=['in'])
    async def inches(self, ctx, centimeters):
        """Convert centimeters to inches"""
        words = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                 'u', 'v', 'w', 'x', 'y', 'z', '\\', '{', '}', '"', '&', '^', '$', '#', '@', '[', ']', '|', '?', '**',
                 '*', '+', '=']
        if any(words in centimeters for words in words):
            embed = discord.Embed(title='Warning', description='This is not a valid number of centimeters',
                                  color=0xFF0000,
                                  timestamp=ctx.message.created_at)
            embed.set_footer(text=f'Error occurred',
                             icon_url=ctx.message.author.avatar_url)
            embed.set_thumbnail(url='https://i.imgur.com/uafPEpb.png')
            await ctx.send(embed=embed)
            return
        thing = eval(centimeters)
        solution = thing * .3937
        inch = round(solution, 2)
        embed = discord.Embed(color=0x5643fd, timestamp=ctx.message.created_at,
                              title=f'Converting {centimeters} centimeters to inches')
        embed.add_field(name='Centimeters', value=f'```py\n{centimeters}```', inline=True)
        embed.add_field(name='Inches', value=f'```py\n{inch}```', inline=True)
        embed.add_field(name='Conclusion', value=f'``{centimeters}`` centimeters is equal to ``{inch}`` inches.',
                        inline=False)
        await ctx.send(embed=embed)

    @convert.command(aliases=['c'])
    async def celsius(self, ctx, fahrenheit):
        """Convert Fahrenheit to Celsius"""
        words = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                 'u', 'v', 'w', 'x', 'y', 'z', '\\', '{', '}', '"', '&', '^', '$', '#', '@', '[', ']', '|', '?', '**',
                 '*', '+', '=']
        if any(words in fahrenheit for words in words):
            embed = discord.Embed(title='Warning', description='This is not a valid amount of degrees Fahrenheit.',
                                  color=0xFF0000,
                                  timestamp=ctx.message.created_at)
            embed.set_footer(text=f'Error occurred',
                             icon_url=ctx.message.author.avatar_url)
            embed.set_thumbnail(url='https://i.imgur.com/uafPEpb.png')
            await ctx.send(embed=embed)
            return
        thing = eval(fahrenheit)
        solution1 = thing - 32
        solution2 = solution1 * 5 / 9
        celsius = round(solution2, 2)
        embed = discord.Embed(title=f'Converting {fahrenheit} degrees Fahrenheit to degrees Celsius', color=0x5643fd,
                              timestamp=ctx.message.created_at)
        embed.add_field(name='Fahrenheit', value=f'```py\n{fahrenheit}```', inline=True)
        embed.add_field(name='Celsius', value=f'```py\n{celsius}```', inline=True)
        embed.add_field(name='Conclusion', value=f'``{fahrenheit}`` degrees Fahrenheit is equal to ``{celsius}`` '
                                                 f'degrees Celsius.', inline=False)
        await ctx.send(embed=embed)

    @convert.command(aliases=['f'])
    async def fahrenheit(self, ctx, celsius):
        """Convert Celsius to Fahrenheit"""
        words = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                 'u', 'v', 'w', 'x', 'y', 'z', '\\', '{', '}', '"', '&', '^', '$', '#', '@', '[', ']', '|', '?', '**',
                 '*', '+', '=']
        if any(words in celsius for words in words):
            embed = discord.Embed(title='Warning', description='This is not a valid amount of degrees Celsius.',
                                  color=0xFF0000,
                                  timestamp=ctx.message.created_at)
            embed.set_footer(text=f'Error occurred',
                             icon_url=ctx.message.author.avatar_url)
            embed.set_thumbnail(url='https://i.imgur.com/uafPEpb.png')
            await ctx.send(embed=embed)
            return
        thing = eval(celsius)
        solution1 = thing * 9 / 5
        solution2 = solution1 + 32
        fahrenheit = round(solution2, 2)
        embed = discord.Embed(title=f'Converting {celsius} degrees Celsius to degrees Fahrenheit', color=0x5643fd,
                              timestamp=ctx.message.created_at)
        embed.add_field(name='Celsius', value=f'```py\n{celsius}```', inline=True)
        embed.add_field(name='Farenheit', value=f'```py\n{fahrenheit}```', inline=True)
        embed.add_field(name='Conclusion', value=f'``{celsius}`` degrees Celsius is equal to ``{fahrenheit}`` '
                                                 f'degrees Fahrenheit.', inline=False)
        await ctx.send(embed=embed)

    @convert.command(aliases=['metres'])
    async def meters(self, ctx, feet):
        """Convert feet to meters"""
        words = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                 'u', 'v', 'w', 'x', 'y', 'z', '\\', '{', '}', '"', '&', '^', '$', '#', '@', '[', ']', '|', '?', '**',
                 '*', '+', '=']
        if any(words in feet for words in words):
            embed = discord.Embed(title='Warning', description='This is not a valid number of feet', color=0xFF0000,
                                  timestamp=ctx.message.created_at)
            embed.set_footer(text=f'Error occurred',
                             icon_url=ctx.message.author.avatar_url)
            embed.set_thumbnail(url='https://i.imgur.com/uafPEpb.png')
            await ctx.send(embed=embed)
            return
        thing = eval(feet)
        solution = thing * .3048
        meters = round(solution, 2)
        embed = discord.Embed(title=f'Converting {feet} feet to meters', color=0x5643fd,
                              timestamp=ctx.message.created_at)
        embed.add_field(name='Feet', value=f'```py\n{feet}```', inline=True)
        embed.add_field(name='Meters', value=f'```py\n{meters}```', inline=True)
        embed.add_field(name='Conclusion', value=f'``{feet}`` feet is equal to ``{meters}`` meters.', inline=False)
        await ctx.send(embed=embed)

    @convert.command()
    async def feet(self, ctx, meters):
        """Convert meters to feet"""
        words = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                 'u', 'v', 'w', 'x', 'y', 'z', '\\', '{', '}', '"', '&', '^', '$', '#', '@', '[', ']', '|', '?', '**',
                 '*', '+', '=']
        if any(words in meters for words in words):
            embed = discord.Embed(title='Warning', description='This is not a valid number of meters', color=0xFF0000,
                                  timestamp=ctx.message.created_at)
            embed.set_footer(text=f'Error occurred',
                             icon_url=ctx.message.author.avatar_url)
            embed.set_thumbnail(url='https://i.imgur.com/uafPEpb.png')
            await ctx.send(embed=embed)
            return
        thing = eval(meters)
        solution = thing * 3.28084
        feet = round(solution, 2)
        embed = discord.Embed(title=f'Converting {meters} meters to feet', color=0x5643fd,
                              timestamp=ctx.message.created_at)
        embed.add_field(name='Meters', value=f'```py\n{meters}```', inline=True)
        embed.add_field(name='Feet', value=f'```py\n{feet}```', inline=True)
        embed.add_field(name='Conclusion', value=f'``{meters}`` meters is equal to ``{feet}`` feet.', inline=False)
        await ctx.send(embed=embed)

    @convert.command(aliases=['kg'])
    async def kilograms(self, ctx, pounds):
        """Convert pounds to kilograms"""
        words = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                 'u', 'v', 'w', 'x', 'y', 'z', '\\', '{', '}', '"', '&', '^', '$', '#', '@', '[', ']', '|', '?', '**',
                 '*', '+', '=']
        if any(words in pounds for words in words):
            embed = discord.Embed(title='Warning', description='This is not a valid number of pounds', color=0xFF0000,
                                  timestamp=ctx.message.created_at)
            embed.set_footer(text=f'Error occurred',
                             icon_url=ctx.message.author.avatar_url)
            embed.set_thumbnail(url='https://i.imgur.com/uafPEpb.png')
            await ctx.send(embed=embed)
            return
        thing = eval(pounds)
        solution = thing * .453592
        kg = round(solution, 2)
        embed = discord.Embed(title=f'Converting {pounds} pounds to kilograms', color=0x5643fd,
                              timestamp=ctx.message.created_at)
        embed.add_field(name='Pounds', value=f'```py\n{pounds}```', inline=True)
        embed.add_field(name='Kilograms', value=f'```py\n{kg}```', inline=True)
        embed.add_field(name='Conclusion', value=f'``{pounds}`` pounds is equal to ``{kg}`` kilograms.', inline=False)
        await ctx.send(embed=embed)

    @convert.command(aliases=['lbs'])
    async def pounds(self, ctx, kilograms):
        """Convert kilograms to pounds"""
        words = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                 'u', 'v', 'w', 'x', 'y', 'z', '\\', '{', '}', '"', '&', '^', '$', '#', '@', '[', ']', '|', '?', '**',
                 '*', '+', '=']
        if any(words in kilograms for words in words):
            embed = discord.Embed(title='Warning', description='This is not a valid number of kilograms',
                                  color=0xFF0000, timestamp=ctx.message.created_at)
            embed.set_footer(text=f'Error occurred',
                             icon_url=ctx.message.author.avatar_url)
            embed.set_thumbnail(url='https://i.imgur.com/uafPEpb.png')
            await ctx.send(embed=embed)
            return
        thing = eval(kilograms)
        solution = thing * 2.20462
        lbs = round(solution, 2)
        embed = discord.Embed(title=f'Converting {kilograms} kilograms to pounds', color=0x5643fd,
                              timestamp=ctx.message.created_at)
        embed.add_field(name='Kilograms', value=f'```py\n{kilograms}```', inline=True)
        embed.add_field(name='Pounds', value=f'```py\n{lbs}```', inline=True)
        embed.add_field(name='Conclusion', value=f'``{kilograms}`` kilograms is equal to ``{lbs}`` pounds.',
                        inline=False)
        await ctx.send(embed=embed)

    @convert.command(aliases=['km'])
    async def kilometers(self, ctx, miles):
        """Convert miles to kilometers"""
        words = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                 'u', 'v', 'w', 'x', 'y', 'z', '\\', '{', '}', '"', '&', '^', '$', '#', '@', '[', ']', '|', '?', '**',
                 '*', '+', '=']
        if any(words in miles for words in words):
            embed = discord.Embed(title='Warning', description='This is not a valid number of miles',
                                  color=0xFF0000, timestamp=ctx.message.created_at)
            embed.set_footer(text=f'Error occurred',
                             icon_url=ctx.message.author.avatar_url)
            embed.set_thumbnail(url='https://i.imgur.com/uafPEpb.png')
            await ctx.send(embed=embed)
            return
        thing = eval(miles)
        solution = thing * 1.60934
        km = round(solution, 2)
        embed = discord.Embed(title=f'Converting {miles} miles to kilometers', color=0x5643fd,
                              timestamp=ctx.message.created_at)
        embed.add_field(name='Miles', value=f'```py\n{miles}```', inline=True)
        embed.add_field(name='Kilometers', value=f'```py\n{km}```', inline=True)
        embed.add_field(name='Conclusion', value=f'``{miles}`` miles is equal to ``{km}`` kilometers.',
                        inline=False)
        await ctx.send(embed=embed)

    @convert.command()
    async def miles(self, ctx, kilometers):
        """Convert kilometers to miles"""
        words = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                 'u', 'v', 'w', 'x', 'y', 'z', '\\', '{', '}', '"', '&', '^', '$', '#', '@', '[', ']', '|', '?', '**',
                 '*', '+', '=']
        if any(words in kilometers for words in words):
            embed = discord.Embed(title='Warning', description='This is not a valid number of kilometers',
                                  color=0xFF0000, timestamp=ctx.message.created_at)
            embed.set_footer(text=f'Error occurred',
                             icon_url=ctx.message.author.avatar_url)
            embed.set_thumbnail(url='https://i.imgur.com/uafPEpb.png')
            await ctx.send(embed=embed)
            return
        thing = eval(kilometers)
        solution = thing * .621371
        miles = round(solution, 2)
        embed = discord.Embed(title=f'Converting {kilometers} kilometers to miles', color=0x5643fd,
                              timestamp=ctx.message.created_at)
        embed.add_field(name='Kilometers', value=f'```py\n{kilometers}```', inline=True)
        embed.add_field(name='Miles', value=f'```py\n{miles}```', inline=True)
        embed.add_field(name='Conclusion', value=f'``{kilometers}`` kilometers is equal to ``{miles}`` miles.',
                        inline=False)
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Math(client))