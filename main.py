# Import Packages
import asyncio
import  datetime, time
from logging import fatal
from operator import add
from os import name
import discord
import json
from discord import message
from discord import member
from discord import activity
from discord import user
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
from afks import afks
import keep_alive
import os
#pip install -U git+https://github.com/Rapptz/discord.py

# client = Our Bot
def get_prefix(client, message):
    with open('prefixes.json', "r") as f:
        prefixes = json.load(f)
  
    return prefixes[str(message.guild.id)]

# prefix and intents
intents = discord.Intents.all() 
intents.members = True 
intents.presences = True
client = commands.Bot(command_prefix= commands.when_mentioned or (get_prefix), intents = intents)
client = commands.Bot(command_prefix=commands.when_mentioned)
client = commands.Bot(command_prefix=(get_prefix),intents=intents)

# Loading Files
client.load_extension("help_command")
client.load_extension("general_commands")
client.load_extension("events")
client.load_extension("info_commands")
client.load_extension("welcome,leave")

# @client.command(name='dm',pass_context=True)
# async def dm(ctx, *argument):
#     #creating invite link
#     invitelink = await ctx.channel.create_invite(unique=True)
#     #dming it to the person
#     await ctx.author.send(invitelink)

# extra events and commands
snipe_message_author = {}
snipe_message_content = {}
snipe_message_url= {}

@client.command()
@commands.is_owner()
async def list_guilds(ctx):
  for i in range(0, len(client.guilds), 10):
    embed = discord.Embed(title='Guilds', colour=0x7289DA)
    guilds = client.guilds[i:i + 10]

    for guild in guilds:
        embed.add_field(name=guild.name, value=f"{guild.id}\n{guild.member_count}")

    await ctx.send(embed=embed)

@client.command()
@commands.is_owner()
async def leave(ctx, guild_id):
    await client.get_guild(int(guild_id)).leave()
    await ctx.send(f"I left: {guild_id}")

@client.event
async def on_message_delete(message):
  snipe_message_author[message.channel.id] = message.author
  snipe_message_content[message.channel.id] = message.content
  snipe_message_url[message.channel.id]= message.author.avatar_url
  await asyncio.sleep(60)
  del snipe_message_author[message.channel.id]
  del snipe_message_content[message.channel.id]
  await asyncio.sleep(60)

@client.command()
async def snipe(ctx):
  channel = ctx.channel 
  try:
    snipeEmbed = discord.Embed(description = snipe_message_content[channel.id], color=0x00ffe1)
    snipeEmbed.set_author(name=f"{snipe_message_author[channel.id]}", icon_url =f"{snipe_message_url[channel.id]}")
    snipeEmbed.timestamp = datetime.datetime.utcnow()
    await ctx.send(embed = snipeEmbed)
  except:
     await ctx.send(f"*There's nothing to snipe!*")

# In vc event
def get_vcrole(client,message):
  with open('vc_roles.json', 'r') as c:
    vc_roles = json.load(c)
  return vc_roles[str(message.guild.id)]

@client.command()
@commands.has_permissions(manage_guild=True)
async def vcrole(ctx,role: discord.Role):
    with open('vc_roles.json', 'r') as c:
        vc_roles= json.load(c)

    vc_roles[str(ctx.guild.id)] = role.id

    with open('vc_roles.json', 'w') as c:
        json.dump(vc_roles, c, indent=4)
    
    embed = discord.Embed(description=f"<a:green_tick:938409780450557974> | **The In Vc role is now set to** {role.mention}", color =0x00ffe1)
    await ctx.send(embed=embed)

# Banner Commnand
# @client.command(aliases=['bn'])
# async def banner(ctx, member:discord.User=None):
#   if member == None:
#     member = ctx.author
#     member = await client.fetch_user(member.id)
#     banner_url = member.banner.url
#     bembed= discord.Embed(title=f"Banner of {member.name}#{member.discriminator}",color=0x00ffe1)
#     bembed.set_image(url=banner_url)
#     bembed.timestamp = datetime.datetime.utcnow()
#     bembed.set_footer(text=f"ID:{ctx.author.id}") 
#     await ctx.send(embed=bembed)
#   else:
#     member = await client.fetch_user(member.id)
#     banner_url = member.banner.url
#     bembed= discord.Embed(title=f"Banner of {member.name}#{member.discriminator}",color=0x00ffe1)
#     bembed.set_image(url=banner_url)
#     bembed.timestamp = datetime.datetime.utcnow()
#     bembed.set_footer(text=f"ID:{ctx.author.id}") 
#     await ctx.send(embed=bembed)

# @banner.error
# async def banner_error(ctx, error):
#   if isinstance(error, commands.CommandInvokeError):
#     await ctx.send("<a:redtick:924731148280692747>| **The user doesn't have any banner!**", delete_after=5.0)

# Moderation Commands
@client.command(pass_context=True)#nickname change command
@commands.has_permissions(manage_nicknames=True)
async def setnick(ctx, member: discord.Member,*, nick):
     try:
       embed=discord.Embed(description=f'<a:green_tick:938409780450557974> | ***Successfully changed*** **`{member}`**\'***s nickname to***  **`{nick}`** ',color=0x00ffe1)
       await member.edit(nick=nick)
       await ctx.send(embed=embed)
     except:
       uembed=discord.Embed(description=f"<a:redtick:924731148280692747> | **Could not change **`{member}`**\'s nickname**",color=0x00ffe1)
       await ctx.send(embed=uembed)

@client.command() #role update command
@commands.has_permissions(manage_roles=True) #permissions
async def role(ctx, user : discord.Member, *, role : discord.Role):
    try:
        if role.position > ctx.author.top_role.position: #if the role is above users top role it sends error
            return await ctx.send(f'<a:redtick:924731148280692747> | ** That role is above your top role!**') 
        if role in user.roles:
            removed = discord.Embed(description=f"<a:green_tick:938409780450557974> | ***Removed*** **`{role}`** ***from*** **`{user}`**", color=0x00ffe1)
            await user.remove_roles(role) #removes the role if user already has
            await ctx.send(embed=removed)
        else:
            add=discord.Embed(description=f"<a:green_tick:938409780450557974> | ***Added*** **`{role}`** ***to*** **`{user}`**",color=0x00ffe1)
            await user.add_roles(role) #adds role if not already has it
            await ctx.send(embed=add)
    except:
        embed = discord.Embed(description=f"<a:redtick:924731148280692747> | **I could not change the roles for `{user}`**",color=0x00ffe1)
        await ctx.send(embed=embed)
        
def in_voice_channel():  # check to make sure ctx.author.voice.channel exists
    def predicate(ctx):
        return ctx.author.voice and ctx.author.voice.channel
    return check(predicate)
             
@in_voice_channel() #voicemove command
@client.command()
@commands.has_guild_permissions(move_members=True)
async def voicemove(ctx, *, channel : discord.VoiceChannel):
    try:
     for members in ctx.author.voice.channel.members:
        m = discord.Embed(description=f"<a:green_tick:938409780450557974> | **Successfully moved members to `{channel}`**",color=0x00ffe1)
        await members.move_to(channel)
     await ctx.send(embed=m)
    except:
       embed=discord.Embed(description="**<a:redtick:924731148280692747> | Could not move the users**",color=0x00ffe1)
       await ctx.send (embed=embed)

@client.command()
@commands.has_permissions(manage_guild=True)
async def slowmode(ctx, time):
  try:
    time_convert = {"s":1, "m":60, "h":3600,"d":86400}
    sm= int(time[0]) * time_convert[time[-1]]
    embed=discord.Embed(description=f"**<a:green_tick:938409780450557974> | The slowmode for this channel is now set to {sm} seconds.**",color=0x00ffe1)
    await ctx.channel.edit(slowmode_delay=sm)
    await ctx.send(embed=embed)
  except:
    vembed=discord.Embed(description="**<a:redtick:924731148280692747> | Could not set the slowmode**",color=0x00ffe1)
    await ctx.send(embed=vembed)

@client.command() #purge command
@commands.has_permissions(manage_messages=True)
# @commands.has_role("・Management")
async def purge(ctx,limit: int, member: discord.Member=None):
    await ctx.message.delete()
    msg = []
    if not member:
        await ctx.channel.purge(limit=limit)
        return await ctx.send(f'<a:green_tick:938409780450557974> | {ctx.author.mention} ***Successfully purged {limit} messages***.', delete_after=3.0)
    async for m in ctx.channel.history():
        if len(msg) == limit:
            break
        if m.author == member:
            msg.append(m)
    await ctx.channel.delete_messages(msg)
    await ctx.send(f'<a:green_tick:938409780450557974> |{ctx.author.mention} ***Successfully purged {limit} messages of {member.name}#{member.discriminator}***.', delete_after=3.0)

@client.command(aliases=['lock']) #lock command
@commands.has_permissions(manage_channels=True)
async def lockdown(ctx):
    perms =  ctx.channel.overwrites_for(ctx.guild.default_role)
    perms.send_messages=False
    # lock = ctx.channel.mention 
    if ctx.channel.overwrites_for(ctx.guild.default_role) == perms:
        dmebed = discord.Embed(description=f"<a:redtick:924731148280692747>  | {ctx.channel.mention} **is already locked**" ,color=0x00ffe1)
        await ctx.send(embed=dmebed)
    else:
        embed = discord.Embed(description="<:c_lock:925276769395830794> | **Successfully Locked Down**" + ctx.channel.mention, color=0x00ffe1)
        await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=perms)
        await ctx.send (embed=embed)

@client.command(aliases=['unlockdown']) #unlock command
@commands.has_permissions(manage_channels=True)
async def unlock(ctx):
    perms =  ctx.channel.overwrites_for(ctx.guild.default_role)
    perms.send_messages=True
    # lock = ctx.channel.mention 
    if ctx.channel.overwrites_for(ctx.guild.default_role) == perms:
        dmebed = discord.Embed(description=f"<a:redtick:924731148280692747> | {ctx.channel.mention} **is already unlocked**" ,color=0x00ffe1)
        await ctx.send(embed=dmebed)
    else:
        embed = discord.Embed(description="<:c_unlock:925277001118515221> | **Successfully Unlocked**" + ctx.channel.mention, color=0x00ffe1)
        await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=perms)
        await ctx.send (embed=embed)

@client.command() #kick command
@commands.has_guild_permissions(kick_members=True)
async def kick(ctx, member : commands.MemberConverter, *, reason="No reason provided"):
    try:
        embed= discord.Embed(description=f'<a:green_tick:938409780450557974> | ***Successfully Kicked*** **`{member}`**!', color=0x00ffe1)
        await member.kick(reason=reason)
        await member.send(f"<a:redtick:924731148280692747> | **You were kicked from {ctx.guild.name} for**: {reason}")
        await ctx.send(embed = embed)
        return
    except:
        pass
    try:
        embed= discord.Embed(description=f'<a:green_tick:938409780450557974> | ***Successfully Kicked*** **`{member}`**!', color=0x00ffe1)
        await member.kick(reason=reason)
        await ctx.send(embed = embed)
        return
    except:
        uembed=discord.Embed(description=f"**<a:redtick:924731148280692747> | Could not kick `{member}`**", color=0x00ffe1)
        await ctx.send(embed = uembed)

@client.command()
# @commands.is_owner()
@commands.has_permissions(manage_channels=True)
async def nukechannel(ctx):
  pos = ctx.channel.position
  existing_channel = ctx.channel
  await existing_channel.delete()
  existing = await existing_channel.clone() # Clones the channel again
  embed=discord.Embed(description=f"**This channel was nuked by** `{ctx.author.name}#{ctx.author.discriminator}`", color=0x00ffe1) 
  await existing.edit(position=pos)
  await existing.send(embed=embed) 

@client.command()
@commands.has_guild_permissions(ban_members=True)
async def ban(ctx,  member :commands.MemberConverter, *, reason="No reason provided", delete_message_days =0):
  if member == ctx.author:
    await ctx.send("<a:redtick:924731148280692747>|***You cannot ban yourself***")
  else:
        try:
            await member.ban(reason=reason, delete_message_days =0)
            await member.send(f"<a:redtick:924731148280692747>|**You were Banned from {ctx.guild.name} for**: {reason}")
            await ctx.send(f'<a:green_tick:938409780450557974> | ***Successfully banned `{member}`***')
            await ctx.message.delete()
            return
        # except Exception as e: print(e)
        except:
           pass
        try:
            bembed=discord.Embed(description=f"<a:green_tick:938409780450557974> | ***Successfully banned `{member}`, couldn't dm them***", color=0x00ffe1)
            await member.ban(reason=reason, delete_message_days =0)
            await ctx.send(embed=bembed)
            await ctx.message.delete()
            return
        except:
            uembed=discord.Embed(description=f"**<a:redtick:924731148280692747> | Could not ban `{member}`**", color=0x00ffe1)
            await ctx.send(embed=uembed)

@client.command()
@commands.has_guild_permissions(ban_members=True)
async def gban(ctx, user: discord.User, reason="No reason provided"):
  for guild in client.guilds:
    try:
        await ctx.message.delete()
        await ctx.guild.ban(user,reason=reason)
        await ctx.message.channel.send(f'<a:green_tick:938409780450557974> | ***Successfully banned `{user}`***')
        return
    except:
         uembed=discord.Embed(description=f"**<a:redtick:924731148280692747> | Could not ban `{user}`**", color=0x00ffe1)
         await ctx.send(embed=uembed)
         return

@client.command() #uban command
@commands.has_guild_permissions(ban_members=True)
async def unban (ctx, user: discord.User):
  embed = discord.Embed(description=f"***<a:green_tick:938409780450557974> | {user} was  unbanned***!", color=0x00ffe1)
  guild = ctx.guild
  if ctx.author.guild_permissions.ban_members:
    await guild.unban(user=user)
    await ctx.send(embed=embed)
    await ctx.message.delete()

@client.command() #serverprefix change command
@commands.has_guild_permissions(manage_guild=True)
async def serverprefix(ctx, prefix):
   Embed=discord.Embed(description=f'**This server\'s prefix is now set to `{prefix}`**',color=0x00ffe1)
   with open('prefixes.json', "r") as f:
        prefixes = json.load(f)
        
   prefixes[str(ctx.guild.id)] = prefix

   with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

   await ctx.send(embed=Embed)

# Errors
@setnick.error
async def setnick_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        msg = await ctx.send("**<a:redtick:924731148280692747> | You do not have the permission to change nicknames. **!")
        await ctx.message.delete()
        await asyncio.sleep(5)
        await msg.delete()
    elif isinstance(error, commands.CommandInvokeError):
            await ctx.send("<a:redtick:924731148280692747>| **I do not have the permission to `Manage Nicknames`**!")

@role.error
async def role_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        msg = await ctx.send("**<a:redtick:924731148280692747> | You do not have the permission add/remove roles. **!", delete_after=5.0)
    elif isinstance(error, commands.CommandInvokeError):
            await ctx.send("<a:redtick:924731148280692747>| **I do not have the permission to `Manage Roles`**!")

@voicemove.error
async def voicemove_error(ctx, error):
    if isinstance(error, commands.errors.ChannelNotFound):
        await ctx.send("<a:redtick:924731148280692747> | **Could not find that channel**")
    elif isinstance(error, commands.CommandInvokeError):
        await  ctx.send("<a:redtick:924731148280692747>| **I do not have the permission to `Move Members`**!")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("<a:redtick:924731148280692747>| **You do not have the permission to drag the members**")

@slowmode.error
async def slowmode_error(ctx, error):
    if isinstance(error,commands.errors.BadArgument):
        await ctx.send("<a:redtick:924731148280692747> | **Please pass in an integer as value**")
    elif isinstance(error, commands.CommandInvokeError):
         await ctx.send("<a:redtick:924731148280692747>| **I do not have the permission to `Manage Channels`**!")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("<a:redtick:924731148280692747>| **You do not have the permission to set the slow mode**")

@purge.error
async def purge_error(ctx, error):
    if isinstance(error, commands.errors.BadArgument):
        await ctx.send("<a:redtick:924731148280692747> | **Please pass in an integer as limit**", delete_after=5.0)
        #await ctx.message.delete()
    elif isinstance(error, commands.CommandInvokeError):
            await ctx.send("<a:redtick:924731148280692747>| **I do not have the permission to `Manage Messages`**!",delete_after=5.0)

@lockdown.error
async def lockdown_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        msg = await ctx.send("**<a:redtick:924731148280692747> | You do not have the permission to lock channels. **!", delete_after=5.0)
    elif isinstance(error, commands.CommandInvokeError):
            await ctx.send("<a:redtick:924731148280692747>| **I do not have the permission to `Manage Channels`**!")

@unlock.error
async def unlock_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
         await ctx.send("**<a:redtick:924731148280692747> | You do not have the permission to unlock channels. **!")
    elif isinstance(error, commands.CommandInvokeError):
        await ctx.send("<a:redtick:924731148280692747>| **I do not have the permission to `Manage Channels`**!")

@nukechannel.error
async def nukechannel_error(ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        await ctx.send("<a:redtick:924731148280692747>| **I am missing the `Manage Channels`permission!**")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("**<a:redtick:924731148280692747> | You do not have the permission to Manage Channels!**")

@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        await ctx.send("<a:redtick:924731148280692747>| **I do not have the permission to `Kick Members`**!")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("**<a:redtick:924731148280692747> | You do not have the permission to kick members. **!")

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        await ctx.send("<a:redtick:924731148280692747>| **I do not have the permission to `Ban Members`**!")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("**<a:redtick:924731148280692747> | You do not have the permission to ban members. **!")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('**<a:redtick:924731148280692747> | Please specify a user to ban!**')

@unban.error
async def unban_error(ctx, error):
    if isinstance(error, commands.errors.UserNotFound):
        await ctx.send("<a:redtick:924731148280692747> | **Not a valid previously-banned member.**")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('**<a:redtick:924731148280692747> | Please specify a user to unban!**')
    elif isinstance(error, commands.CommandInvokeError):
        await ctx.send("<a:redtick:924731148280692747>| **I do not have the permission to `Unban Members`**!")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("**<a:redtick:924731148280692747> | You do not have the permission to Unban members. **!")
    
@serverprefix.error
async def serverprefix_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('**<a:redtick:924731148280692747> | Please mention a new prefix!**')
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("**<a:redtick:924731148280692747> | You need the `Manage Server` permission to change my prefix**!")

# Run the client on the server
keep_alive.keep_alive()
token = os.environ.get("TOKEN")
client.run(token)