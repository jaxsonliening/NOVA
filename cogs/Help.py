import discord
from discord.ext import commands

colour = 0x5643fd


class Help(commands.Cog):
    """Your personal guide to using NOVA"""

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def cogs(self, ctx):
        """Shows all of NOVA's cogs"""
        cogs = []
        for cog in self.client.cogs:
            cogs.append(
                f"`{cog}` • {self.client.cogs[cog].__doc__}")
            # adds cogs and their description to list. if the cog doesnt have a description it will return as "None"
        await ctx.send(embed=discord.Embed(colour=colour, title=f"All Cogs ({len(self.client.cogs)})",
                                           description=f"Do `{ctx.prefix}help <cog>` to show info for any cog!"
                                                       + "\n\n" + "\n".join(
                                               cogs)))

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
                    k.append(f'➤ **{cog_name}**\n{"**•**".join(sorted(cmds))}\n')
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
                                      description=f"<:news:730866149109137520> You can do `{pre}help [category]` for "
                                                  f"more "
                                                  f"info on a category.\n<:news:730866149109137520> You can also do "
                                                  f"`{pre} "
                                                  f"help [command]` for more info on a command.\n\nThanks to "
                                                  f"♿nizcomix#7532 for help with this command. Find it on "
                                                  f"GitHub [here.]("
                                                  f"https://github.com/niztg/CyberTron5000/blob/master/cogs/info.py"
                                                  f"#L9-L109)"
                                                  f"\n\n" + "\n".join(k))
                embed.add_field(name='Like what you see?',  inline=False,
                                value='<:share:730823872265584680>[Invite NOVA]'
                                      '(https://discord.com/api/oauth2/authorize?client_id=709922850953494598&permis'
                                      'sions=1573252215&scope=bot)\n'
                                      '<:share:730823872265584680>[Join the support server]'
                                      '(https://discord.gg/Uqh9NXY)\n<:share:730823872265584680>[View the source code]'
                                      '(https://github.com/YeetVegetabales/NOVA/tree/master/cogs)')
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