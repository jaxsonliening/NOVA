import discord
import random
import asyncio
import json
from discord.ext import commands
from secrets import *


class economy(commands.Cog):
    """NOVA's special economy system."""

    def __init__(self, client):
        self.client = client
        self.coin = "<:coin:781367758612725780>"

    @commands.command()
    async def create(self, ctx):
        """Create your bank account."""
        econ_data = open("economy.json", "r")
        money = json.load(econ_data)
        econ_data.close()
        if str(ctx.message.author.id) in money.keys():
            return await ctx.send("You can't create a bank account if you already have one dumbo. "
                                  "Use `n.balance` to see how much money you have.")
        else:
            money[str(ctx.message.author.id)] = {"wallet": 100, "bank": 0}
            econ_data = open("economy.json", "w")
            json.dump(money, econ_data)
            econ_data.close()
            return await ctx.send(f"Your account has been created! \nYou have been granted {self.coin}100 "
                                  f"coins in your wallet to start. \nUse `n.balance` to check how much money you have!")

    @commands.command(aliases=['bal'])
    async def balance(self, ctx, member: discord.Member = None):
        user = member or ctx.message.author
        """"Check how much money you have."""
        econ_data = open("economy.json", "r")
        money = json.load(econ_data)
        econ_data.close()
        if str(ctx.message.author.id) not in money.keys():
            return await ctx.send("You haven't created an account yet! Run `n.create` to do so.")
        elif member and str(member.id) not in money.keys():
            return await ctx.send("This user does not have an account!")
        else:
            wallet_amount = money[str(user.id)]['wallet']
            bank_amount = money[str(user.id)]['bank']
            embed = discord.Embed(title=f"{user.display_name}'s Balance", color=0x5643fd,
                                  timestamp=ctx.message.created_at)
            embed.add_field(name="Wallet Amount", value=f"{self.coin}`{wallet_amount}`", inline=False)
            embed.add_field(name="Bank Amount", value=f"{self.coin}`{bank_amount}`", inline=False)
            embed.set_thumbnail(url=user.avatar_url)
            return await ctx.send(embed=embed)

    @commands.command(aliases=['dep'])
    async def deposit(self, ctx, deposit_amount):
        """Move money from your wallet to your bank."""
        econ_data = open("economy.json", "r")
        money = json.load(econ_data)
        econ_data.close()
        if str(ctx.message.author.id) not in money.keys():
            return await ctx.send("You haven't created an account yet! Run `n.create` to do so.")
        else:
            if deposit_amount == 'all':
                new_amount = money[str(ctx.message.author.id)]['wallet']
                wallet_amount = 0
                bank_amount = int(money[str(ctx.message.author.id)]['bank']) + int(new_amount)
                money[str(ctx.message.author.id)]['wallet'] = wallet_amount
                money[str(ctx.message.author.id)]['bank'] = bank_amount
                econ_data = open("economy.json", "w")
                json.dump(money, econ_data)
                econ_data.close()
                return await ctx.send(f"{self.coin}`{new_amount}` has been deposited into your bank.\n"
                                      f"Your new bank balance is {self.coin}`{bank_amount}`.")
            try:
                amount = int(deposit_amount)
                if amount > money[str(ctx.message.author.id)]['wallet']:
                    return await ctx.send("You can't deposit more money than you own. \n"
                                          "Try again with a smaller amount "
                                          "or use `n.withdraw <amount>`.")
                elif amount < 1:
                    return await ctx.send("You can't deposit nothing. Try again with a bigger amount.")
                else:
                    wallet_amount = int(money[str(ctx.message.author.id)]['wallet']) - int(amount)
                    bank_amount = int(money[str(ctx.message.author.id)]['bank']) + int(amount)
                    money[str(ctx.message.author.id)]['wallet'] = wallet_amount
                    money[str(ctx.message.author.id)]['bank'] = bank_amount
                    econ_data = open("economy.json", "w")
                    json.dump(money, econ_data)
                    econ_data.close()
                    return await ctx.send(f"{self.coin}`{amount}` has been deposited into your bank.\n"
                                          f"Your new bank balance is {self.coin}`{bank_amount}`.")
            except ValueError:
                return await ctx.send("Only numbers can be used to deposit.")

    @commands.command(aliases=['with'])
    async def withdraw(self, ctx, withdraw_amount):
        """Move money from your bank to your wallet."""
        econ_data = open("economy.json", "r")
        money = json.load(econ_data)
        econ_data.close()
        if str(ctx.message.author.id) not in money.keys():
            return await ctx.send("You haven't created an account yet! Run `n.create` to do so.")
        else:
            if withdraw_amount == 'all':
                new_amount = money[str(ctx.message.author.id)]['bank']
                bank_amount = 0
                wallet_amount = int(money[str(ctx.message.author.id)]['wallet']) + int(new_amount)
                money[str(ctx.message.author.id)]['wallet'] = wallet_amount
                money[str(ctx.message.author.id)]['bank'] = bank_amount
                econ_data = open("economy.json", "w")
                json.dump(money, econ_data)
                econ_data.close()
                return await ctx.send(f"{self.coin}`{new_amount}` has been added to your wallet.\n"
                                      f"Your new wallet balance is {self.coin}`{wallet_amount}`.")
            try:
                amount = int(withdraw_amount)
                if amount > money[str(ctx.message.author.id)]['bank']:
                    return await ctx.send("You can't withdraw more money than you own. \n"
                                          "Try again with a smaller amount "
                                          "or use `n.deposit <amount>`.")
                elif amount < 1:
                    return await ctx.send("You can't withdraw nothing. Try again with a bigger amount.")
                else:
                    bank_amount = int(money[str(ctx.message.author.id)]['bank']) - int(amount)
                    wallet_amount = int(money[str(ctx.message.author.id)]['wallet']) + int(amount)
                    money[str(ctx.message.author.id)]['bank'] = bank_amount
                    money[str(ctx.message.author.id)]['wallet'] = wallet_amount
                    econ_data = open("economy.json", "w")
                    json.dump(money, econ_data)
                    econ_data.close()
                    return await ctx.send(f"{self.coin}`{amount}` has been moved to your wallet.\n"
                                          f"Your new wallet balance is {self.coin}`{wallet_amount}`.")
            except ValueError:
                return await ctx.send("Only numbers can be used to withdraw.")

    @commands.command()
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def beg(self, ctx):
        """Beg for money like that weird homeless dude on the street corner."""
        econ_data = open("economy.json", "r")
        money = json.load(econ_data)
        econ_data.close()
        if str(ctx.message.author.id) not in money.keys():
            return await ctx.send("You haven't created an account yet! Run `n.create` to do so.")
        else:
            person = ['stranger', 'random dude', 'stalker', 'simp', 'weirdo', 'loser', 'police officer', 'young child']
            gift = random.randint(1, 75)
            money[str(ctx.message.author.id)]['wallet'] += gift
            econ_data = open("economy.json", "w")
            json.dump(money, econ_data)
            econ_data.close()
            return await ctx.send(f"A {random.choice(person)} gave you {self.coin}`{gift}` for your wallet.")


def setup(client):
    client.add_cog(economy(client))
