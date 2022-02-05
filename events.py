import os  
import asyncio
import datetime,time
from logging import fatal
from operator import add
from os import name
import discord
import json
from discord import message
from discord import member
from discord import activity
from discord.activity import BaseActivity, CustomActivity
from discord.client import Client
from discord.colour import Color
from discord.embeds import Embed
from discord.enums import Status
from discord.ext import commands, tasks
from discord.ext.commands import bot, check
from itertools import cycle
from discord.ext.commands import context
from discord.ext.commands.converter import GuildConverter, MemberConverter, clean_content
from discord.ext.commands.core import has_guild_permissions
from discord.ext.commands.help import HelpCommand
from discord.user import User
from discord.utils import get
from itertools import cycle
from afks import afks
import general_commands


def remove(afk):
    if "(AFK)" in afk.split():
        return " ".join(afk.split()[1:])
    else:
        return afk

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        global startTime 
        startTime = time.time()
        await self.bot.change_presence(activity=discord.Game("My prefix is +help"))
        print("Fusion's Ready!")
        # servers = len(self.bot.guilds)
        # members = 0
        # for guild in self.bot.guilds:
        #     members += guild.member_count - 1
        # await self.bot.change_presence(status=discord.Status.idle,activity = discord.Activity(type=discord.ActivityType.watching,name=f'{servers} servers and {members} members'))

    @commands.Cog.listener()
    async def on_voice_state_update(self,member, before, after):
      if not before.channel and after.channel:
        with open("vc_roles.json") as f:
          vc_roles = json.load(f)
        vc_role = vc_roles[str(member.guild.id)]
        role = member.guild.get_role(vc_role)
        await member.add_roles(role)
      elif before.channel and not after.channel:
        with open("vc_roles.json") as f:
          vc_roles = json.load(f)
        vc_role = vc_roles[str(member.guild.id)]
        role = member.guild.get_role(vc_role)
        await member.remove_roles(role)

    @commands.Cog.listener()
    async def on_guild_join(self,guild):
      # invitelink = await ld.text_channels[0].create_invite( max_age=0,max_use, temporary=False, unique=True)
      # channel=self.bot.get_channel(935602949076430869)
      # await channel.send(invitelink)

      with open('prefixes.json', "r") as f:
        prefixes = json.load(f)
        
      prefixes[str(guild.id)] = '+'

      with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

      owner = guild.owner
      await owner.send(f"**Hello ! Thank You for adding me in {guild.name}, You can join our support server if you have any queries related to our bot**") #**\nhttps://discord.gg/cFughHCrN6"

    @commands.Cog.listener()
    async def on_guild_remove(self,guild):
      with open('prefixes.json', "r") as f:
         prefixes = json.load(f)
        
      prefixes.pop(str(guild.id))

      with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

      with open("vc_roles.json","r") as f:
        vc_roles=json.load(f)

      vc_roles.pop(str(guild.id))

      with open("vc_roles.json", "w") as f:
        json.dump(vc_roles, f,indent=4 )

      with open("w_channel.json","r") as f:
        w_channel=json.load(f)

      w_channel.pop(str(guild.id))
    
      with open("w_channel.json", "w") as f:
        json.dump(w_channel, f,indent=4 )

      with open("l_channel.json","r") as f:
        l_channel=json.load(f)

      l_channel.pop(str(guild.id))
    
      with open("l_channel.json", "w") as f:
        json.dump(l_channel, f,indent=4 )

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.errors.CommandNotFound):
            await ctx.send("<a:redtick:924731148280692747>|**No such command was found**!", delete_after=5.0)
        # elif isinstance(error, commands.CommandInvokeError):
        #     await ctx.send("<a:redtick:924731148280692747>|**I do not have the permission to do that**!", delete_after=5.0)
        elif isinstance(error, commands.errors.MemberNotFound):
            await ctx.send("<a:redtick:924731148280692747>|**I couldn't find that member**!", delete_after=5.0)
        elif isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send("<a:redtick:924731148280692747>| **You're missing a required argument**!", delete_after=3.0)
        elif isinstance(error, commands.errors.UserNotFound):
            await ctx.send("<a:redtick:924731148280692747>|**I couldn't find that user**!", delete_after=5.0)
        else:
            raise error

    @commands.Cog.listener()
    async def on_message (self,message):
        # mention = f'<@!{client.user.id}>'
        mention = f'<@!924240436976029697>'
        hmention = f'<@!924240436976029697> help'
        if message.author.id in afks.keys():
            afks.pop(message.author.id)
            try:
                await message.author.edit(nick = remove(message.author.display_name))
            except:
                pass
            await message.channel.send(f"**Welcome back {message.author.mention}, I removed your AFK** !")
        for id, reason in afks.items():
            member = get(message.guild.members, id = id)
            if (message.reference and member == (await message.channel.fetch_message(message.reference.message_id)).author) or member.id in message.raw_mentions:
                await message.reply(f"`{member.display_name}` **is AFK**-  {reason}")
                                       #member.name

        if message.content == mention:
            with open('prefixes.json', 'r') as f:
              prefixes = json.load(f) 
            prefix = prefixes[str(message.guild.id)]
            await message.channel.send(f"**My prefix for this server is `{prefix}`**")
        
        if message.content == hmention:
           with open('prefixes.json', 'r') as f:
             prefixes = json.load(f) 
           prefix = prefixes[str(message.guild.id)]
           embed = discord.Embed(title="**Fusion's • Help Menu**",description=f"*Type {prefix}help [command] for more | Have a nice day!*", color =0x00ffe1)
           embed.add_field(name ="General[4]",value="`ping`, `avatar`, `enlarge`,`afk`", inline=False)
           embed.add_field(name="Info[5]", value="`uptime`,`serverinfo`,`whois`,`snipe`,`membercount`", inline=False)
           embed.add_field(name="Utility[6]", value="`serverprefix`,`vcrole`,`welcome_channel`,`welcome_message`,`leave_channel`,`leave_message`")
           embed.add_field(name = "Moderation[12]", value= '`gban`,`ban`,`kick`,`purge`,`role`,`unban`,`setnick`,`lockdown`,`unlock`, `nukechannel`, `voicemove`,`slowmode`', inline=False)
           embed.add_field(name="\u200B",value="<a:sparklesblue:929627956970680330> [invite me](https://discord.com/oauth2/authorize?client_id=924240436976029697&scope=bot&permissions=1099511627775) | [vote for me](https://top.gg/bot/924240436976029697/vote) | [support server](https://discord.gg/btVvCpbkj4)")
           embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/881531276400681020/924280371821035530/Untitled.png")
           embed.timestamp = datetime.datetime.utcnow()
           embed.set_footer(text="Thanks for Choosing Fusion!",
           icon_url="https://cdn.discordapp.com/attachments/881531276400681020/924280371821035530/Untitled.png")
           await message.channel.send(embed=embed)
        else:
           pass
    # # #     # await self.bot.process_commands(message,self)

def setup(bot):
    bot.add_cog(Events(bot))