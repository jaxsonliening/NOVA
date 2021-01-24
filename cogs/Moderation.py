import discord
import asyncio
import random
from discord.ext import commands


class Moderation(commands.Cog):
    """Commands to help you better manage your server"""

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_guild_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        """Kick a member from the server"""
        await member.kick(reason=reason)
        await ctx.send(f"<a:a_check:742966013930373151> Successfully kicked ``{member}``")
        await member.send(f"You have been kicked from **{ctx.guild.name}** for the following reason:"
                          f"\n```py\n{reason}```")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_guild_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        """Ban a member from the server"""
        await member.ban(reason=reason)
        await ctx.send(f"<a:a_check:742966013930373151> Successfully banned ``{member}``")
        await member.send(f"You have been banned from **{ctx.guild.name}** for the following reason:"
                          f"\n```py\n{reason}```")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_guild_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        """Unban a member"""
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f"<a:a_check:742966013930373151> Successfully unbanned ``{user}``")
                await user.send(f'<a:a_check:742966013930373151> You have been unbanned from **{ctx.guild.name}**')
                return

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_guild_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int = 5):
        """Purge any amount of messages with a default of 5"""
        await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f'<a:a_check:742966013930373151>  ``{amount}`` messages have been cleared',
                       delete_after=3.0)

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_guild_permissions(manage_channels=True)
    async def slowmode(self, ctx, seconds: int = 10):
        """Set the slowmode for a channel"""
        if 0 < seconds < 21601:
            await ctx.channel.edit(slowmode_delay=seconds)
            return await ctx.send(f"<a:a_check:742966013930373151> "
                                  f"Slowmode for <#{ctx.channel.id}> has been set to ``{seconds}`` seconds."
                                  f"\nDo ``n.slowmode 0`` to remove slowmode!")
        if seconds == 0:
            await ctx.channel.edit(slowmode_delay=0)
            return await ctx.send(f"<a:a_check:742966013930373151> "
                                  f"Slowmode for <#{ctx.channel.id}> has been removed.")
        if seconds > 21600:
            return await ctx.send(f"<:redx:732660210132451369> That is not a valid option for slowmode. Please choose a"
                                  f"number between ``0`` and ``21,600`` to enable slowmode.")

    @commands.command(aliases=['suggest', 'vote'])
    async def poll(self, ctx, *, msg):
        """Use NOVA to hold an organized vote"""
        embed = discord.Embed(title=f'New Poll', color=0x5643fd, description=msg, timestamp=ctx.message.created_at)
        embed.set_thumbnail(url='https://imgur.com/ES5SD0L.png')
        embed.set_author(name=ctx.message.author)
        message = await ctx.send(embed=embed)
        for i in ["⬆️", "⬇️"]:
            await message.add_reaction(i)

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_guild_permissions(manage_channels=True)
    async def makechannel(self, ctx, *, name):
        """Make a channel."""
        if len(name) > 100:
            return await ctx.send("<:redx:732660210132451369> "
                                  "That is too many characters! Your channel name must be under 100 characters.")
        else:
            channel = await ctx.guild.create_text_channel(name.replace(" ", "-"))
            await ctx.send(f"<a:a_check:742966013930373151> Successfully created {channel.mention}")

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_guild_permissions(manage_channels=True)
    async def makerole(self, ctx, *, name):
        """Make a role."""
        if len(name) > 100:
            return await ctx.send("<:redx:732660210132451369> "
                                  "That is too many characters! Your role name must be under 100 characters.")
        else:
            role = await ctx.guild.create_role(name=name)
            await ctx.send(f"<a:a_check:742966013930373151> Successfully created {role.mention}")
            return

    @commands.command(aliases=['nick'])
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_guild_permissions(manage_messages=True)
    async def nickname(self, ctx, member: discord.Member, *, nickname=None):
        """Change the nickname of a member."""
        await member.edit(nick=nickname)
        if nickname is None:
            await ctx.send(f"<a:a_check:742966013930373151> The nickname for ``{member}``"
                           f" has successfully been reset.")
        else:
            await ctx.send(f"<a:a_check:742966013930373151> The nickname for ``{member}``"
                           f" has successfully been changed to ``{nickname}``")


def setup(client):
    client.add_cog(Moderation(client))
