import discord
import cmath
import random
import asyncio
import numpy as np
import matplotlib.pyplot as plt
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

    @commands.command(aliases=['poly'])
    async def polynomial(self, ctx, *, coefficients):
        """Solve polynomials using NOVA"""
        await ctx.send('**Warning!** This command only works if you state the coefficients of each variable and '
                       'space them out. (Ex. 1 2 3 for the equation x^2 + 2x + 3 = 0)\n'
                       '**Also,** make sure your polynomial is equal to zero '
                       'or else you will not get the right answers.')
        try:
            numbers = coefficients.split(' ')
            newnumbers = []
            for number in numbers:
                try:
                    newnumbers.append(int(number))
                except ValueError:
                    await ctx.send("You did not enter a number!")
            p = np.poly1d(newnumbers)
            roots = p.roots
            solutions = '\n'.join([str(root) for root in roots])
            embed = discord.Embed(title='Polynomial Solved!', color=0x5643fd, timestamp=ctx.message.created_at,
                                  description='**NOTE:** The numbers above the coefficients are the degrees '
                                              'of the term.')
            embed.add_field(name='Polynomial Equation', value=f"```{p} = 0```", inline=False)
            embed.add_field(name='Roots', value=f"```py\n{solutions}```", inline=False)
            await ctx.send(embed=embed)
        except asyncio.TimeoutError:
            await ctx.send('You never responded, process abandoned.')
        except ValueError:
            await ctx.send("You did not enter a number!")

    @commands.group(invoke_without_command=True)
    async def graph(self, ctx):
        """
        Graph equations using matplotlib.
        """
        await ctx.send('Send your equation in chat below. **Remember to not include `y =`**.\n'
                       'For further help use `n.graph guide` to see a complete guide.')
        msg = await self.client.wait_for('message', timeout=60, check=lambda g: g.author == ctx.author)
        f = await ctx.send('Your equation has been recorded, now send your x range below.')
        part = msg.content
        cheese = await self.client.wait_for('message', timeout=60, check=lambda u: u.author == ctx.author)
        x_range = int(cheese.content)
        k = await ctx.send('Your x range has been recorded, the graph will now be made.')
        m = await ctx.send('<a:loading:743537226503421973> Loading... <a:loading:743537226503421973>')
        await asyncio.sleep(2)
        x = np.array(range(1, x_range))
        y = eval(part)
        title = f"{ctx.message.author}'s Graph"
        label = f"y = {part}"
        plt.plot(x, y, label=label)
        plt.grid(alpha=1, linestyle='-')
        plt.title(title)
        plt.legend()
        plt.xlabel('Independent Variable')
        plt.ylabel('Dependent Variable')
        plt.savefig("graph.png")
        plt.close()
        image = discord.File("graph.png")
        await ctx.send(file=image)
        await f.delete()
        await k.delete()
        await m.delete()

    @graph.command(aliases=['help'])
    async def guide(self, ctx):
        await ctx.send("Graph equations and get a picture in return. "
                       "\n**-**For exponents, represent the degree as `x*x`. "
                       "`x*x*x*x` would be for `x^4`. To add a coefficient,"
                       " multiply the number by the x expressions. For example"
                       " `4x^2` would be represented as `(4*x*x)` "
                       "\n**-**For division, try to put the division inside of "
                       "parentheses. For `1/2x^2` you would write `((1/2)*x*x)` "
                       "\n**-**Try putting each term in parentheses to make solving easier. "
                       "Example: `(4*x*x)*(-2*x)` for `4x^2-2x1.` "
                       "\n**-**When asked to send your equation in chat, do not write **Y =** or "
                       "else it will not work as intended. "
                       "\n**-**When asked to send your x-range in chat, pick the number that you "
                       "would like your graph to be scaled to on the x-axis.")

    @commands.group(invoke_without_command=True, aliases=['pythagoras', 'pyth'])
    async def pythagorean(self, ctx, a: int = 1, b: int = 1):
        """Find the hypotenuse of a right triangle."""
        try:
            a_squared = a * a
            b_squared = b * b
            c_squared = a_squared + b_squared
            c = cmath.sqrt(c_squared)
            x = str(c)
            final = x.strip("(+0j)")
            embed = discord.Embed(title='Pythagorean Theorem', color=0x5643fd, timestamp=ctx.message.created_at,
                                  description=f"**Solution:**\na value - `{a}`\nb value - `{b}`\nc value - `{final}`")
            embed.add_field(name='Steps:', value=f"```{a_squared} + {b_squared} = {c_squared}\n"
                                                f"(a squared + b squared = c squared)```")
            embed.set_image(url='https://imgur.com/t8XVeli.jpg')
            embed.add_field(value='Do `n.pythagorean c` to solve for side b given a hypotenuse and side length.',
                            name='Other Operations:', inline=False)
            await ctx.send(embed=embed)
        except ValueError:
            await ctx.send("You didn't enter a number!")

    @pythagorean.command()
    async def c(self, ctx, c: int = 1, a: int = 1):
        """Find the side length of a right triangle given a side length and hypotenuse."""
        try:
            if a > c:
                return await ctx.send('The side length cannot be larger than the hypotenuse.')
            else:
                a_squared = a * a
                c_squared = c * c
                b_squared = c_squared - a_squared
                b = cmath.sqrt(b_squared)
                x = str(b)
                final = x.strip("(+0j)")
                embed = discord.Embed(title='Pythagorean Theorem', color=0x5643fd, timestamp=ctx.message.created_at,
                                      description=f"**Solution:**\nc value - `{c}`\na value - `{a}`\nb value - "
                                                  f"`{final}`")
                embed.add_field(name='Steps:', value=f"```{c_squared} - {a_squared} = {b_squared}\n"
                                                     f"(c squared - a squared = b squared)```")
                embed.set_image(url='https://imgur.com/t8XVeli.jpg')
                await ctx.send(embed=embed)
        except ValueError:
            await ctx.send("You didn't enter a number!")


def setup(client):
    client.add_cog(Math(client))
