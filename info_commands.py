import discord
import asyncio
from datetime import datetime
import time
from discord.ext import commands
from discord.client import Client
from discord.embeds import Embed

class InfoCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

        client.launch_time = datetime.utcnow()

    @commands.command()
    async def uptime(self,ctx):
      delta_uptime = datetime.utcnow() - self.client.launch_time
      hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
      minutes, seconds = divmod(remainder, 60)
      days, hours = divmod(hours, 24)
      embed = discord.Embed(title="Current Uptime", description=f"I'm online from `{days}d`, `{hours}h`, `{minutes}m`, `{seconds}s`", color = 0x00ffe1)
      embed.timestamp = datetime.utcnow()
      embed.set_footer(text="\n\u200b",icon_url="https://cdn.discordapp.com/attachments/881531276400681020/924280371821035530/Untitled.png")
      await ctx.send(embed=embed)

    @commands.command() #membercount command
    async def membercount(self,ctx):
        members = ctx.guild.member_count
        humans = len([m for m in ctx.guild.members if not m.bot])
        embed = discord.Embed(description=f"{ctx.guild.name}'s members !", color=0x00ffe1)
        embed.set_author(name="Members !",icon_url=ctx.guild.icon_url)
        embed.add_field(name="All Members", value=members, inline=True)
        embed.add_field(name="Human Count", value=humans,inline=True)
        embed.timestamp = datetime.utcnow()
        await ctx.send(embed=embed)

    @commands.command(aliases=['whois']) #userinfo command
    async def userinfo(self,ctx,*,member:commands.MemberConverter=None):
      if not member:
        member = ctx.message.author
        memberroles = len(member.roles) - 1
                
        embed = discord.Embed( description =f"{member.mention}", color=member.color)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name ="Name", value =f"{member.name}#{member.discriminator}", inline=True)
        embed.add_field(name="Joined at", value =member.joined_at.strftime('%d-%b-%Y, %H:%M '))
        embed.add_field(name="Account created", value=member.created_at.strftime('%d-%b-%Y, %H:%M '))
        embed.add_field(name=f"roles ", value=memberroles, inline=True)
        embed.add_field(name='Status', value= member.status, inline=True)
        embed.timestamp =  datetime.utcnow()
        embed.set_footer(text=f"ID:{member.id}")
        await ctx.send(embed=embed)
      else:
        # mention = [] 
        # for role in member.roles:
        #     if role.name != "@everyone":
        #         mention.append(role.mention)
        #         b = ", ".join(mention)
                memberroles = len(member.roles) - 1
                
                embed = discord.Embed( description =f"{member.mention}", color=member.color)
                embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
                embed.set_thumbnail(url=member.avatar_url)
                embed.add_field(name ="Name", value =f"{member.name}#{member.discriminator}", inline=True)
                embed.add_field(name="Joined at", value =member.joined_at.strftime('%d-%b-%Y, %H:%M '))
                embed.add_field(name="Account created", value=member.created_at.strftime('%d-%b-%Y, %H:%M '))
                # embed.add_field(name=f"<a:roles:924913249558880267>Roles [{memberroles}] ", value=b, inline=True)
                embed.add_field(name=f"roles ", value=memberroles, inline=True)
                embed.add_field(name='Status', value= member.status, inline=True)
                embed.timestamp =  datetime.utcnow()
                embed.set_footer(text=f"ID:{member.id}")
                await ctx.send(embed=embed)
              
    @commands.command() #serverinfo command
    async def serverinfo(self,ctx):
        name = str(ctx.guild.name)
        owner = str(ctx.guild.owner)
        id = str(ctx.guild.id)
        region = str(ctx.guild.region)
        UserCount = str(ctx.guild.member_count)
        icon = str(ctx.guild.icon_url)
        text_channels = len(ctx.guild.text_channels)
        voice_channels = len(ctx.guild.voice_channels)
        categories = len(ctx.guild.categories)
        roles = len(ctx.guild.roles) -1
        boosts = (ctx.guild.premium_subscription_count)

        embed = discord.Embed(
            title = name + " Server Information",
            color=0x00ffe1
            )
        embed.set_thumbnail(url=icon)
        embed.add_field(name="Owner", value=owner, inline=True)
        embed.add_field(name="Channel Categories", value=categories, inline=True)
        embed.add_field(name="Text Channels", value= text_channels, inline=True)
        embed.add_field(name="Voice Channels", value=voice_channels, inline=True)
        embed.add_field(name="Members", value=UserCount, inline=True)
        embed.add_field(name="Roles", value = roles, inline=True)
        # embed.add_field(name="<:region:924915424213221426>Region", value=region, inline=True)
        embed.add_field(name="Boosts", value=boosts, inline=True)
        # embed.add_field(name='Server Created', value=ctx.guild.created_at.__format__('%A, %d %B %Y at %H:%M %p'), inline=True)
        embed.timestamp = datetime.utcnow()
        embed.set_footer(text=f"ID:{ctx.guild.id} | Server created on {ctx.guild.created_at.__format__('%A, %d %B %Y at %H:%M %p')}")
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(InfoCommands(client))