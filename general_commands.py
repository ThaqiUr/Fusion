import discord
import asyncio
import datetime
from discord import user
from discord import message
from discord.ext import commands
from discord.client import Client
from discord.embeds import Embed
from discord.ext.commands import bot
from io import BytesIO
from afks import afks
from events import Events

class GeneralCommands(commands.Cog):
    def __init__(self,client):
        self.client = client
    
    @commands.command() #ping command
    async def ping(self,ctx):
        #<a:loading:924934443041443861>
        message=await ctx.send(f'Pong!``{round(self.client.latency * 1000)}ms``')
        await asyncio.sleep(0.1)
        await message.edit(content=f'Pong!`{round(self.client.latency * 1000)}ms`')
       

    @commands.command(pass_context=True) #servers check command
    async def guilds(self,ctx):
        embed =discord.Embed(description=f"<a:pepe_shazam:854915704255807508> **I'm in " + str(len(self.client.guilds)) + " servers!**", color = 0x00ffe1)
        await ctx.send(embed=embed)
        await ctx.message.delete()

    @commands.command(aliases=['av']) #avatar command
    # async def avatar(self,ctx, *,  member : commands.MemberConverter=None):
    async def avatar(self,ctx,  *,  member : discord.User=None): 
        if not member:
            avurl=ctx.author.avatar_url
            avembed = discord.Embed(title=f"Avatar of {ctx.author.name}#{ctx.author.discriminator}",color=0x00ffe1)
            avembed.set_image(url=avurl)
            avembed.timestamp = datetime.datetime.utcnow()
            avembed.set_footer(text=f"ID:{ctx.author.id}")
            await ctx.send(embed=avembed)
        else:
            userAvatarUrl = member.avatar_url
            avembed = discord.Embed(title=f"Avatar of {member.name}#{member.discriminator}",color=0x00ffe1)
            avembed.set_image(url=userAvatarUrl)
            avembed.timestamp = datetime.datetime.utcnow()
            avembed.set_footer(text=f"ID:{member.id}")
            await ctx.send(embed=avembed)

    @commands.command() #enlarge emoji command
    async def enlarge(self,ctx, emoji: discord.PartialEmoji = None):
        emoji=emoji.url
        embed=discord.Embed(color=0x00ffe1)
        embed.set_author(name="Enlarged Emoji!",icon_url=ctx.author.avatar_url)
        embed.set_image(url=emoji)
        await ctx.send(embed=embed)

    @commands.command()
    async def afk(self, ctx, *, reason="No reason provided"):
        member = ctx.author
        if member.id in afks.keys():
            afks.pop(member.id)
        else:
            try:
                await member.edit(nick=f"(AFK) {member.display_name}")
            except:
                pass
        # mem = ctx.author.display_name
        afks[member.id] = reason
        embed = discord.Embed(description =f"<:afk:925274319288926228>**AFK note**: *{reason}*", color = member.color)
        embed.set_author(name=f"{member.name} I set your afk", icon_url=ctx.author.avatar_url)
        # embed.add_field(name="AFK note:", value=reason)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(GeneralCommands(bot))