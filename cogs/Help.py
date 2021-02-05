import discord
from discord.ext import commands

colour = 0x5643fd


class Help(commands.Cog):
    """Your personal guide to using NOVA"""

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def help(self, ctx, *, command=None):
        """Your go to guide for using NOVA!"""
        pre = ctx.prefix
        footer = f"Do '{pre}help [command/cog]' for more information!"
        list_of_cogs = []
        walk_commands = []
        final_walk_command_list = []
        sc = []
        format = []
        try:
            for cog in self.client.cogs:
                list_of_cogs.append(cog)
            if command:
                cmd = self.client.get_command(command)
            else:
                cmd = None
            if not command:
                k = []
                for cog_name, cog_object in self.client.cogs.items():
                    cmds = []
                    for cmd in cog_object.get_commands():
                        if not cmd.hidden:
                            cmds.append(f"`{cmd.name}`")
                    k.append(f'➤ **{cog_name}**\n`n.help {cog_name}`')
                for wc in self.client.walk_commands():
                    if not wc.cog_name and not wc.hidden:
                        if isinstance(wc, commands.Group):
                            walk_commands.append(wc.name)
                            for scw in wc.commands:
                                sc.append(scw.name)
                        else:
                            walk_commands.append(wc.name)
                for item in walk_commands:
                    if item not in final_walk_command_list and item not in sc:
                        final_walk_command_list.append(item)
                for thing in final_walk_command_list:
                    format.append(f"`{thing}`")
                embed = discord.Embed(title=f"{self.client.user.name} Help", color=0x5643fd,
                                      description=f"<:news:730866149109137520>`{pre}help [category]` for "
                                                  f"more "
                                                  f"info on a category\n<:news:730866149109137520>"
                                                  f"`{pre}"
                                                  f"help [command]` for more info on a command"
                                                  f"\n\n<:share:730823872265584680>[Invite NOVA]"
                                      f"(https://discord.com/api/oauth2/authorize?client_id=709922850953494598&permis"
                                      f"sions=1573252215&scope=bot)\n"
                                      f"<:share:730823872265584680>[Join the support server]"
                                      f"(https://discord.gg/Uqh9NXY)\n<:share:730823872265584680>[View the source code]"
                                      f"(https://github.com/YeetVegetabales/NOVA/tree/master/cogs)")
                embed.add_field(name='➤ **Fun**', value='`n.help fun`', inline=False)
                embed.add_field(name='➤ **Moderation**', value='`n.help moderation`', inline=False)
                embed.add_field(name='➤ **Math**', value='`n.help math`', inline=False)
                embed.add_field(name='➤ **Games**', value='`n.help games`', inline=False)
                embed.add_field(name='➤ **Reddit**', value='`n.help reddit`', inline=False)
                embed.add_field(name='➤ **Miscellaneous**', value='`n.help miscellaneous`', inline=False)
                embed.add_field(name='➤ **Info**', value='`n.help info`', inline=False)
                embed.add_field(name='➤ **Image**', value='`n.help image`', inline=False)
                embed.add_field(name='➤ **Api**', value="`n.help api`", inline=False)
                embed.add_field(name='➤ **Economy**', value="`n.help economy`", inline=False)
                embed.set_thumbnail(url='https://images-ext-2.discordapp.net/external/AQCEqCF4Yl_PWAfuA-GReZoDify6--y'
                                        '4hXOJVkqaDHo/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/7099228509534945'
                                        '98/f78ed19924e8c95abc30f406d47670d7.png')
                embed.set_author(name='Developed by YeetVegetabales#5313', icon_url='https://cdn.discordapp.com/attach'
                                                                                    'ments/710565131167203408/7820137'
                                                                                    '06296360970/image0.png')
                await ctx.send(embed=embed)
            elif command in list_of_cogs:
                i = []
                cog_doc = self.client.cogs[command].__doc__ or " "
                for cmd in self.client.cogs[command].get_commands():
                    if not cmd.aliases:
                        char = "\u200b"
                    else:
                        char = "•"
                    help_msg = cmd.help or "No help provided for this command"
                    i.append(f"→ `{cmd.name}{char}{'•'.join(cmd.aliases)} {cmd.signature}` • {help_msg}")
                await ctx.send(embed=discord.Embed(title=f"{command} Cog", colour=colour,
                                                   description=cog_doc + "\n\n" + "\n".join(i)).set_footer(text=footer))
            elif command and cmd:
                help_msg = cmd.help or "No help provided for this command"
                parent = cmd.full_parent_name
                if len(cmd.aliases) > 0:
                    aliases = '•'.join(cmd.aliases)
                    cmd_alias_format = f'{cmd.name}•{aliases}'
                    if parent:
                        cmd_alias_format = f'{parent} {cmd_alias_format}'
                    alias = cmd_alias_format
                else:
                    alias = cmd.name if not parent else f'{parent} {cmd.name}'
                embed = discord.Embed(title=f"{alias} {cmd.signature}", description=help_msg, colour=colour)
                embed.set_footer(text=footer)
                if isinstance(cmd, commands.Group):
                    sub_cmds = []
                    for sub_cmd in cmd.commands:
                        schm = sub_cmd.help or "No help provided for this command"
                        if not sub_cmd.aliases:
                            char = "\u200b"
                        else:
                            char = "•"
                        sub_cmds.append(
                            f"→ `{cmd.name} {sub_cmd.name}{char}{'•'.join(sub_cmd.aliases)} {sub_cmd.signature}` • "
                            f"{schm}")
                    scs = "\n".join(sub_cmds)
                    await ctx.send(
                        embed=discord.Embed(title=f"{alias} {cmd.signature}", description=help_msg + "\n\n" + scs,
                                            colour=colour).set_footer(text=f"{footer} • → are subcommands"))
                else:
                    await ctx.send(embed=embed)
            else:
                embed = discord.Embed(description=f"No command named `{command}` found.", title='Error', color=0xFF0000)
                await ctx.send(embed=embed)
        except Exception as er:
            await ctx.send(er)


def setup(client):
    client.add_cog(Help(client))