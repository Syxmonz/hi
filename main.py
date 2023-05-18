import nextcord
from nextcord.ext import commands
from nextcord.ext.commands import has_permissions, MissingPermissions
import asyncio
import datetime
from nextcord import Interaction
import re
from copy import deepcopy
from time import sleep
import time
import nextcord.ui
import os
import math
import aiosqlite
import parse

intents = nextcord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix="!", intents=nextcord.Intents.all())


@client.event
async def on_ready():
    await client.change_presence(status=nextcord.Status.online, activity=nextcord.Streaming(name='S World', url='https://nextcord.gg/QQChCusp'))
    print("The bot is now ready for use!")
    print("--------------------------")

testServerId = 1066392598815715458

@client.slash_command(name = "test", description = "Does this work...?", guild_ids=[testServerId])
async def test(interaction: Interaction):
     await interaction.response.send_message("Hello.")

@client.command()
async def hello(ctx):
    await ctx.send("Hello, I am S World.")

@client.command()
async def goodbye(ctx):
    await ctx.send("Goodbye!")

@client.command()
async def hola(ctx):
     await ctx.send("¿Hola cómo estás?")
     
@client.command(pass_context = True)
@commands.has_role('All perms')
async def join(ctx):
      if (ctx.author.voice):
            channel = ctx.message.author.voice.channel
            await channel.connect()
      else:
            await ctx.send("You are not in a voice channel, in order to run this command; please join a channel to run this command.")

@client.command(pass_context = True)
@commands.has_role('All perms')
async def leave(ctx):
      if (ctx.voice_client):
            await ctx.guild.voice_client.disconnect()
            await ctx.send("I have left the voice channel.")
      else:
            await ctx.send("I am not in a voice channel.")


@client.command()
@commands.has_role('Head Moderator')
@commands.has_role('Administration Team')
@commands.has_role('Executive Administrator')
@commands.has_role('All perms')
async def kick(ctx, member: nextcord.Member):
    try:
        await member.send("You have been kicked from **S World**, due to a violation of our server rules/guidelines.")
        await member.kick(reason="By a moderator.")
        await ctx.send(f"{member.mention} has been kicked.")
    except nextcord.Forbidden:
        await ctx.send("I couldn't send a direct message to the user.")
      
@kick.error
async def kick_error(ctx, error):
      if isinstance(error, commands.MissingPermissions):
            await ctx.send("Houston we have a problem here, you dont have the permissions to run this command! ⚠️")

@client.command()
@commands.has_role('Executive Administrator')
@commands.has_role('All perms')
async def ban(ctx, member: nextcord.Member):
    try:
        await member.send("You have been banned from **S World**, due to a violation of our server rules/guidelines.")
        await member.kick(reason="By a moderator.")
        await ctx.send(f"{member.mention} has been kicked.")
    except nextcord.Forbidden:
        await ctx.send("I couldn't send a direct message to the user.")
      
@ban.error
async def ban_error(ctx, error):
      if isinstance(error, commands.MissingPermissions):
            await ctx.send("Houston we have a problem here, you dont have the permissions to run this command! ⚠️")


@client.command()
@commands.has_role('Staff')
@commands.has_role('All perms')
async def message(ctx, user:nextcord.Member, *, message=None):
     message = "⚠️ Hello. This is a strict notice from the **S World Moderation Team**, we have recently noticed you breaking our Server Rules/Guidelines or nextcord's TOS. Please re-read our rules in: <#1066392599172231194>. Thank you!"
     embed = nextcord.Embed(title=message)
     await user.send(embed=embed)
     await ctx.send(f"{user.mention} has been given notice.")

@message.error
async def message_error(ctx, error):
      if isinstance(error, commands.MissingRole):
            await ctx.send("Houston we have a problem here, you dont have the permissions to run this command! ⚠️ | **Staff Role required ** |")

@client.command()
@commands.has_role('Staff')
@commands.has_role('All perms')
async def slowmode(ctx, *, seconds:int = None):
     if seconds is None:
          seconds = 5
          await ctx.channel.edit(slowmode_delay=seconds)
     else:
          await ctx.channel.edit(slowmode_delay=seconds)
          await ctx.send("**Slowmode has been changed to {seconds}, by {ctx.author}**")

@slowmode.error
async def slowmode_error(ctx, error):
     if isinstance(error, commands.MissingRole):
          await ctx.send("Houston we have a problem here, you dont have the permissions to run this command! ⚠️ | **Staff Role required ** |")

@commands.has_role('Moderation Team')
@commands.has_role('All perms')
@client.command(aliases = ["delete", "clear"])
async def purge(ctx, amount : int):
               await ctx.channel.purge(limit=amount+1)
               if amount > 101:
                     await ctx.send('Can not delete more than 100 messages!')
               else:
                     embed=nextcord.Embed(description=f"**Sucesfully purged {amount} message(s) in {ctx.channel}!**", color=nextcord.Colour.green())
               await ctx.send(embed=embed)

@purge.error
async def purge_error(ctx, error):
     if isinstance(error, commands.MissingRole):
          await ctx.send("Houston we have a problem here, you dont have the permissions to run this command! ⚠️ | **Moderation Team Only Command ** |")


@client.command()
async def mute(ctx, member : nextcord.Member, *, reason=None):
      if (not ctx.author.guild_permissions.manage_messages):
            await ctx.send('Houston we have a problem here, you dont have the permissions to run this command! ⚠️ | **Staff Role required ** |')
            return
      guild = ctx.guild
      mutedRole = nextcord.utils.get(guild.roles, name="Muted")

      await member.add_roles(mutedRole,  reason=reason)
      await ctx.send('User is now successfully muted!')
      await member.send(f"You have been muted from: **{guild.name}** | Reason: **{reason}**")

@client.command()
async def unmute(ctx, member : nextcord.Member, *, reason=None):
      if (not ctx.author.guild_permissions.manage_messages):
            await ctx.send('Houston we have a problem here, you dont have the permissions to run this command! ⚠️ | **Staff Role required ** |')
            return
      guild = ctx.guild
      mutedRole = nextcord.utils.get(guild.roles, name="Muted")

      await member.remove_roles(mutedRole,  reason=reason)
      await ctx.send('User is now successfully un-muted!')
      await member.send(f"You have been un-muted from: **{guild.name}** | Reason: **{reason}**")

@client.command()
@commands.has_role('Administration Team')
@commands.has_role('All perms')
async def lock(ctx):
      await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
      await ctx.send( ctx.channel.mention + " is now in lockdown mode.")

@client.command()
@commands.has_role('Administration Team')
@commands.has_role('All perms')
async def unlock(ctx):
      await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
      await ctx.send( ctx.channel.mention + " is now out of lockdown mode.")

@lock.error
async def lock_error(ctx, error):
     if isinstance(error, commands.MissingRole):
          await ctx.send("Houston we have a problem here, you dont have the permissions to run this command! ⚠️ | **Administrator Only Command ** |")

@unlock.error
async def unlock_error(ctx, error):
     if isinstance(error, commands.MissingRole):
          await ctx.send("Houston we have a problem here, you dont have the permissions to run this command! ⚠️ | **Administrator Only Command ** |")

@client.command(description="This command mutes a member for a specified duration!")
@commands.has_role('Staff')
@commands.has_role('All perms')
async def tempmute(ctx, member: nextcord.Member, duration: str):
    mute_role = nextcord.utils.get(ctx.guild.roles, name='Muted')

    if mute_role is None:
        # If 'Muted' role doesn't exist, create it
        mute_role = await ctx.guild.create_role(name='Muted')

        # Configure permissions for the 'Muted' role as needed
        # ...

    await member.add_roles(mute_role)
    await ctx.send(f'{member.mention} has been muted for **{duration}**.')

    await asyncio.sleep(parse_duration(duration))
    await member.remove_roles(mute_role)
    await ctx.send(f'{member.mention} has been unmuted.')

@tempmute.error
async def tempmute_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have permission to use that command.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please specify a member and duration for the mute.")

def parse_duration(duration):
    unit_map = {
        's': 1,  # seconds
        'm': 60,  # minutes
        'h': 3600,  # hours
        'd': 86400,  # days
    }
    unit = duration[-1]
    if unit not in unit_map:
        raise ValueError("Invalid duration format.")

    try:
        amount = int(duration[:-1])
    except ValueError:
        raise ValueError("Invalid duration format.")

    return amount * unit_map[unit]

@tempmute.error
async def tempmute_error(ctx, error):
     if isinstance(error, commands.MissingRole):
          await ctx.send("Houston we have a problem here, you dont have the permissions to run this command! ⚠️ | **Staff Only Command ** |")

@join.error
async def join_error(ctx, error):
     if isinstance(error, commands.MissingRole):
          await ctx.send("Houston we have a problem here, you dont have the permissions to run this command! ⚠️ | **All Perms Only Command ** |")

@leave.error
async def leave_error(ctx, error):
     if isinstance(error, commands.MissingRole):
          await ctx.send("Houston we have a problem here, you dont have the permissions to run this command! ⚠️ | **All Perms Only Command ** |")
async def initialize():
    await client.wait_until_ready()
    client.db = await aiosqlite.connect("expData.db")
    await client.db.execute("CREATE TABLE IF NOT EXISTS guildData (guild_id int, user_id int, exp int, PRIMARY KEY (guild_id, user_id))")


client.run('MTEwODA5MzMzMTI2NDc2NjE2Mg.GepBMX.Jbzx7IhYCkpasJI8nh_dsB9WgOltUDF-prYJQI')