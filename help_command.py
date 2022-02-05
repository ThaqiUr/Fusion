import discord
import asyncio
import datetime
from discord.ext import commands
from discord.client import Client
import json
from discord.embeds import Embed

class HelpCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        bot.remove_command("help")

    @commands.group(name = "help", invoke_without_command=True)
    async def help(self,ctx):
      with open('prefixes.json', 'r') as f:
        prefixes = json.load(f) 
      prefix = prefixes[str(ctx.guild.id)]
      embed = discord.Embed(title="**Fusion's • Help Menu**",description=f"Number of commands : **27**\n🌟 : Premium Commands", color =0x0dc2ca)
      embed.add_field(name ="<:System_square:938302465902776321> General  [4]",value="`ping`,  `avatar`, `enlarge`, `afk`", inline=False)
      embed.add_field(name="🟦 Info[5]", value="`uptime`, `serverinfo`, `whois`, `snipe`, `membercount`", inline=False)
      embed.add_field(name="🟩 Utility[6]", value="`serverprefix`, `vcrole`, `welcome_channel`, `welcome_message`, `leave_channel`, `leave_message`")
      embed.add_field(name = "🟪 Moderation[12]", value= '`gban`,`ban`,`kick`,`purge`,`role`,`unban`,`setnick`,`lockdown`,`unlock`, `nukechannel`, `voicemove`,`slowmode`', inline=False)
      embed.add_field(name=":link: Links",value="[**Add Fusion**](https://discord.com/oauth2/authorize?client_id=924240436976029697&scope=bot&permissions=1099511627775) **•** [**Support**](https://discord.gg/btVvCpbkj4) **•** [**Vote for Fusion**](https://top.gg/bot/924240436976029697/vote)")
      embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/881531276400681020/924280371821035530/Untitled.png")
      embed.set_footer(text="Thanks for Choosing Fusion!", icon_url="https://cdn.discordapp.com/attachments/881531276400681020/924280371821035530/Untitled.png")
      await ctx.message.channel.send(embed=embed)

    @help.group()
    async def gban(self,ctx):
      embed = discord.Embed(title="**Help:Gban**",description="`gban [user ID] [reason]` **(use this command to ban someone who isn't there in the server)**", color=0x00ffe1)
      await ctx.send(embed=embed)

    @help.group()
    async def ban(self,ctx):
      embed = discord.Embed(title="**Help:Ban**",description="`ban [member ID] [reason]`", color=0x00ffe1)
      await ctx.send(embed=embed)

    @help.group()
    async def kick(self,ctx):
      embed = discord.Embed(title="**Help:Kick**",description="`kick [user ID] [reason]`", color=0x00ffe1)
      await ctx.send(embed=embed)

    @help.group()
    async def purge(self,ctx):
      embed = discord.Embed(title="**Help:Purge**",description="`purge [amount]\npurge [amount] [member]`**(this command deletes the messages of a specific user)**", color=0x00ffe1)
      await ctx.send(embed=embed)
    
    @help.group()
    async def role(self,ctx):
      embed = discord.Embed(title="**Help:Role**",description="`role [member ID] [role id or role name]`", color=0x00ffe1)
      await ctx.send(embed=embed)

    @help.group()
    async def unban(self,ctx):
      embed = discord.Embed(title="**Help:Unban**",description="`unban [member ID]`", color=0x00ffe1)
      await ctx.send(embed=embed)

    @help.group()
    async def serverprefix(self,ctx):
      embed = discord.Embed(title="**Help:Serverprefix**",description="`serverprefix [custom prefix]`", color=0x00ffe1)
      await ctx.send(embed=embed)

    @help.group()
    async def setnick(self,ctx):
      embed = discord.Embed(title="**Help:Setnick**",description="`setnick [member ID] [nick]`", color=0x00ffe1)
      await ctx.send(embed=embed)

    @help.group()
    async def voicemove(self,ctx):
      embed = discord.Embed(title="**Help:Voicemove**",description="`voicemove [voice channel's id]`", color=0x00ffe1)
      await ctx.send(embed=embed)

    @help.group()
    async def slowmode(self,ctx):
      embed = discord.Embed(title="**Help:Slowmode**",description="`slowmode [time]` **(s:1, m:60,h:3600)**", color=0x00ffe1)
      await ctx.send(embed=embed)

    @help.group()
    async def vcrole(self,ctx):
      embed = discord.Embed(title="**Help:VcRole**",description="`vcrole [role]` **(make sure that the role is below my role)**", color=0x00ffe1)
      await ctx.send(embed=embed)

    @help.group()
    async def welcome_channel(self,ctx):
      embed=discord.Embed(title="**Help:WelcomeChannel**",
      description="`welcome_channel [channel]` **(make sure you mention the channel or use the channel id)**",
      color=0x00ffe1)
      await ctx.send(embed=embed)

    @help.group()
    async def welcome_message(self,ctx):
      embed=discord.Embed(title="**Help:WelcomeMessage**",
      description="`welcome_message [message]` **(make sure you've set the welcome channel)**",
      color=0x00ffe1)
      embed.set_footer(text="Put {member.mention} in your message to mention the member || {member} to display member's name")
      await ctx.send(embed=embed)

    @help.group()
    async def leave_channel(self,ctx):
      embed=discord.Embed(title="**Help:LeaveChannel**",
      description="`leave_channel [channel]` **(make sure you mention the channel or use the channel id)**",
      color=0x00ffe1)
      await ctx.send(embed=embed)

    @help.group()
    async def leave_message(self,ctx):
      embed=discord.Embed(title="**Help:LeaveMessage**",
      description="`leave_message [message]` **(make sure you've set the leave channel)**",
      color=0x00ffe1)
      embed.set_footer(text="Put {member.mention} in your message to mention the member || {member} to display member's name || we recommnend using {member}")
      await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(HelpCommand(bot))

