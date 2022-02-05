import os  
import asyncio
import  datetime, time
from os import name
import discord
import json
from discord import member
from discord.client import Client
from discord.colour import Color
from discord.embeds import Embed
from discord.enums import Status
from discord.ext import commands, tasks
from discord.ext.commands import bot
from discord.ext.commands import context
from discord.ext.commands.core import has_guild_permissions
from discord.ext.commands.help import HelpCommand
from discord.user import User
from discord.utils import get

class WelcomeLeave(commands.Cog):
    def __init__(self,client):
        self.client = client
      
    def get_w_message(self, message):
      with open('w_message.json', 'r') as c:
        w_message = json.load(c)
      return w_message[str(message.guild.id)]

    def get_w_channel(self, message):
      with open('w_channel.json', 'r') as c:
        w_channel = json.load(c)
      return w_channel[str(message.guild.id)]   

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def welcome_message(self,ctx,*,message):
      with open('w_message.json', 'r') as c:
        w_message= json.load(c)
      w_message[str(ctx.guild.id)] = message
      
      with open('w_message.json', 'w') as c:
        json.dump(w_message, c, indent=4)
      
      await ctx.send(f'<a:green_tick:938409780450557974>| **Successfully set the welcome message**')

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def welcome_channel(self,ctx,channel: discord.TextChannel):
      with open('w_channel.json', 'r') as c:
        w_channel= json.load(c)
      w_channel[str(ctx.guild.id)] = channel.id
      
      with open('w_channel.json', 'w') as c:
        json.dump(w_channel, c, indent=4)
      await ctx.send(f'<a:green_tick:938409780450557974>| {channel.mention} **is now the welcome channel**')

    def get_l_message(self, message):
      with open('l_message.json', 'r') as c:
        l_message = json.load(c)
      return l_message[str(message.guild.id)]

    def get_l_channel(self, message):
      with open('l_channel.json', 'r') as c:
        l_channel = json.load(c)
      return l_channel[str(message.guild.id)] 

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def leave_message(self,ctx,*,message):
      with open('l_message.json', 'r') as c:
        l_message= json.load(c)
      l_message[str(ctx.guild.id)] = message
      
      with open('l_message.json', 'w') as c:
        json.dump(l_message, c, indent=4)
      await ctx.send(f'<a:green_tick:938409780450557974>| **Successfully set the leave message**')

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def leave_channel(self,ctx,channel: discord.TextChannel):
      with open('l_channel.json', 'r') as c:
        l_channel= json.load(c)
      l_channel[str(ctx.guild.id)] = channel.id
      
      with open('l_channel.json', 'w') as c:
        json.dump(l_channel, c, indent=4)
      await ctx.send(f'<a:green_tick:938409780450557974>| {channel.mention} **is now the leave channel**')

    @commands.Cog.listener()
    async def on_member_join(self,member):
      server=member.guild.name
      with open("w_message.json") as f:
        w_message = json.load(f)
      w_message = w_message[str(member.guild.id)]
      
      with open("w_channel.json") as f:
        w_channel = json.load(f)
      welcome_channel = w_channel[str(member.guild.id)]
      channel = self.client.get_channel(welcome_channel)
      await channel.send(eval(f'f"{w_message}"'))

    @commands.Cog.listener()
    async def on_member_remove(self,member):
      server=member.guild.name
      with open("l_message.json") as f:
        l_message = json.load(f)
      l_message = l_message[str(member.guild.id)]
      
      with open("l_channel.json") as f:
        l_channel = json.load(f)
      leave_channel = l_channel[str(member.guild.id)]
      channel = self.client.get_channel(leave_channel)
      await channel.send(eval(f'f"{l_message}"'))

def setup(bot):
    bot.add_cog(WelcomeLeave(bot))