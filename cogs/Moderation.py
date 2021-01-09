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
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_guild_permissions(manage_channels=True, manage_roles=True)
    async def unmute(self, ctx, member: discord.Member = None):
        """Unmute a member."""
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        await member.remove_roles(role)
        await member.send(f"You have been unmuted in **{ctx.guild}**. Welcome back!")
        await ctx.send(f"<a:a_check:742966013930373151> {member} was successfully unmuted.")

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

    @commands.group(invoke_without_command=True, aliases=['config'])
    async def configure(self, ctx):
        """Configure your server to use some of NOVA's more complex moderation features."""
        embed = discord.Embed(color=0x5643fd, title='🛠️ Configuration Options 🛠️', timestamp=ctx.message.created_at)
        embed.add_field(name='``n.configure server-mute``', value='Adds a #muted channel and a muted role to your '
                                                                  'server. Do n.mute [member] [reason] in order to '
                                                                  'mute '
                                                                  'someone and remove '
                                                                  'their permissions to send messages.', inline=False)
        embed.add_field(name='``n.configure mail``', value='Adds a #modmail channel and allows users to '
                                                           'have interactions with the server staff in a private '
                                                           'area.',
                        inline=False)
        embed.set_thumbnail(url='https://imgur.com/uMhz173.png')
        await ctx.send(embed=embed)

    @configure.command()
    @commands.has_permissions(administrator=True)
    @commands.bot_has_guild_permissions(manage_channels=True)
    async def mail(self, ctx):
        """Use this command to set up modmail for your server."""
        guild = ctx.guild
        channel = discord.utils.get(guild.channels, name="modmail")
        if channel:
            return await ctx.send(embed=discord.Embed(color=0x5643fd,
                                                      description='Modmail has already been configured for this server!'
                                                                  ' If you have not configured modmail yet but you are '
                                                                  'still seeing this message, delete any channels named'
                                                                  ' ``modmail`` and run the command again.'))
        else:
            try:
                overwrites = {ctx.guild.default_role: discord.PermissionOverwrite(read_message_history=False),
                              ctx.guild.me: discord.PermissionOverwrite(send_messages=True)}
                await ctx.guild.create_text_channel(name='modmail', overwrites=overwrites)
                x = discord.utils.get(guild.channels, name="modmail")
                await x.set_permissions(target=ctx.guild.default_role, send_messages=False,
                                        read_message_history=False,
                                        read_messages=False)
                m = await x.send(f"Welcome to Modmail! Users will send messages here and it is your duty "
                                 f"to respond.")
                await m.pin()
                await ctx.send(f"<a:a_check:742966013930373151> You're all set! Modmail has succeessfully"
                               f" been configured for **{guild}**.")
            except discord.Forbidden:
                return await ctx.send("<:redx:732660210132451369> I have no permissions to perform these actions.")

    @configure.command(name='server-mute')
    @commands.has_permissions(administrator=True)
    @commands.bot_has_guild_permissions(manage_channels=True, manage_roles=True)
    async def server_mute(self, ctx):
        """Use this command to set up the mute command for your server."""
        guild = ctx.guild
        roles = discord.utils.get(guild.roles, name="Muted")
        channels = discord.utils.get(guild.channels, name="muted")
        if roles or channels:
            return await ctx.send(embed=discord.Embed(color=0x5643fd, description=f"Muting has already been configured "
                                                                                  f"for this server! If you have not "
                                                                                  f"configured "
                                                                                  f"muting yet but you are still seeing"
                                                                                  f" this message, delete any channels"
                                                                                  f" named ``muted"
                                                                                  f"`` and any roles named ``Muted``."))
        else:
            await ctx.guild.create_role(name="Muted", reason="To use for muting.")
            thingy = discord.utils.get(guild.roles, name="Muted")
            overwrites = {ctx.guild.default_role: discord.PermissionOverwrite(read_message_history=False),
                          ctx.guild.me: discord.PermissionOverwrite(send_messages=True),
                          thingy: discord.PermissionOverwrite(read_message_history=True)}
            await ctx.guild.create_text_channel(name='muted', overwrites=overwrites)
            try:
                x = discord.utils.get(guild.channels, name="muted")
                y = discord.utils.get(guild.roles, name="Muted")
                await x.set_permissions(target=y, send_messages=True,
                                        read_message_history=True,
                                        read_messages=True)
                await x.set_permissions(target=ctx.guild.default_role, send_messages=False,
                                        read_message_history=False,
                                        read_messages=False)
                m = await x.send(f'Welcome to your new home {thingy.mention}. Enjoy the silence.')
                await m.pin()
                await ctx.send(f"<a:a_check:742966013930373151> "
                               f"You're all set! Muting has been enabled for **{guild}**. Do ``n.help mute``"
                               f" to get started.")
            except discord.Forbidden:
                return await ctx.send("<:redx:732660210132451369> I have no permissions to perform these actions.")

    @commands.command()
    @commands.bot_has_guild_permissions(manage_channels=True)
    @commands.has_permissions(manage_channels=True)
    async def pin(self, ctx, message: discord.Message):
        """Pin a message using an ID link."""
        msg = message
        await msg.pin()
        await ctx.send(f"<a:a_check:742966013930373151> A message has been pinned in <#{msg.channel.id}>.")

    @commands.command()
    @commands.bot_has_guild_permissions(manage_channels=True)
    @commands.has_permissions(manage_channels=True)
    async def unpin(self, ctx, message: discord.Message):
        """Unpin a message using an ID link."""
        msg = message
        await msg.unpin()
        await ctx.send(f"<a:a_check:742966013930373151> A message has been unpinned in <#{msg.channel.id}>.")

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

    @commands.command()
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_guild_permissions(manage_channels=True, manage_roles=True)
    async def mute(self, ctx, member: discord.Member, *, reason=None):
        """Mute a member. Do ``n.configure server-mute`` first!"""
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        channel = discord.utils.get(ctx.guild.channels, name="muted")
        roles = []
        if role and channel:
            await member.edit(roles=roles)
            await member.add_roles(role)
            await member.send(f"You were muted in **{ctx.guild}** for: ```py\n{reason}```")
            await ctx.send(f"<a:a_check:742966013930373151> {member} was successfully muted for ``{reason}``.")
            return
        else:
            await ctx.send("<:redx:732660210132451369>"
                           "Muting has not been enabled for this server yet! Have an administrator do "
                           "``n.configure server-mute`` in order to successfully run this command.")

    @commands.command()
    async def modmail(self, ctx, *, message):
        """Message the moderators of a server."""
        channel = discord.utils.get(ctx.guild.channels, name="modmail")
        member = ctx.message.author
        if channel:
            try:
                mailbox = discord.utils.get(ctx.guild.channels, name="modmail")
                z = await ctx.send("<:wumpus:742965982640865311> Check your DMs")
                await asyncio.sleep(2)
                await z.delete()
                await ctx.message.delete()
                await member.send("Your message has been recorded. "
                                  " \nWould you like your message to be anonymous? \n**yes**|**no**")
                hehe = await self.client.wait_for('message', check=lambda m: m.channel == member.dm_channel, timeout=30)
                if hehe.content in ['yes', 'YES', 'Yes', 'y', 'ye', 'Y', 'yE', 'Ye', 'yES', 'YEs', 'yEs', 'yeS']:
                    await member.send('Message will be sent anonymously')
                    await mailbox.send(embed=discord.Embed(title='Anonymous Message:', description=f"{message}",
                                                           color=0x5643fd, timestamp=ctx.message.created_at).
                                       set_thumbnail(url='https://www.freepnglogos.com/uploads/gmail-'
                                                         'email-logo-png-16.png'))
                    await asyncio.sleep(3)
                    await member.send('<a:a_check:742966013930373151> Your message has successfully been sent!')
                    return
                elif hehe.content in ['no', 'No', 'NO', 'nO']:
                    await member.send('Message will **not** be sent anonymously')
                    await mailbox.send(embed=discord.Embed(title=f'New message from **{ctx.message.author}**:',
                                                           description=message,
                                                           color=0x5643fd, timestamp=ctx.message.created_at).
                                       set_thumbnail(url=ctx.message.author.avatar_url))
                    await asyncio.sleep(3)
                    await member.send('<a:a_check:742966013930373151> Your message has successfully been sent!')
                    return
                else:
                    await member.send('You did not clarify yes or no, message will be sent normally.')
                    await mailbox.send(embed=discord.Embed(title=f'New message from **{ctx.message.author}**:',
                                                           description=message,
                                                           color=0x5643fd, timestamp=ctx.message.created_at).
                                       set_thumbnail(url=ctx.message.author.avatar_url))
                    await asyncio.sleep(3)
                    await member.send('<a:a_check:742966013930373151> Your message has successfully been sent!')
            except asyncio.TimeoutError:
                await member.send("<:redx:732660210132451369> You took too long to respond, try again by running "
                                  "``n.modmail <message>``.")
        else:
            await ctx.send("<:redx:732660210132451369>"
                           "Modmail has not been enabled for this server yet! Have an administrator do "
                           "``n.configure mail`` in order to successfully run this command.")


def setup(client):
    client.add_cog(Moderation(client))
