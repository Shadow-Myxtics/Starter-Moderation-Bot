import discord
import asyncio
import datetime
import os
import json
import requests
from discord.ext.commands import has_permissions, MissingPermissions
from discord.ext import commands
from blurple import ui
bot = commands.Bot(command_prefix=commands.when_mentioned_or('prefix'))
bot.remove_command('help')
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"stats"))



@bot.event
async def on_command_error(ctx, error):
    await ctx.send(f":x: An error occured: `{str(error)}`")       

@bot.command()
async def help(ctx):
  embed = discord.Embed(title="Help", description="\nModerator Commands\n`vm warn <@member> [reason]` - Warns member\n`vm kick <@member> [reason]` - Kicks member\n`vm ban <@member> [reason]` - Bans member\n`vm mute <@member>`- Mutes a member \n`vm unmute <@member>` - Unmutes a member\n`vm tempban <@member> [Reason]`- Temp Ban A user\n")
  await ctx.send(embed=embed)
#end
#--------------------------------
#Warn command
@bot.command()
async def warn(ctx, member: discord.Member, *, arg = None):
  if member:
    if arg != None:
      try:
        await member.send(f"You recieved a warning in {ctx.message.guild.name} for reason {arg}")
      except:
        await ctx.send("Cannot warn: Target has disabled DMs")
      await ctx.send(embed=ui.Alert(ui.Style.SUCCESS, title="Member warned via DMs"))
    else:
      try:
        await member.send(f"You recieved a warning in {ctx.message.guild.name}")
      except:
        await ctx.send("Cannot warn: Target has disabled DMs")
      await ctx.send(embed=ui.Alert(ui.Style.SUCCESS, title="Member warned via DMs"))
  else:
    await ctx.send("Cannot warn: Provide a member")


#Kick command
@bot.command()
@commands.bot_has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, arg = None, reason=None):
  if member:
    if arg != None:
      if ctx.message.author.guild_permissions.kick_members:
        try:
          await member.send(f"You've been kicked from {ctx.message.guild.name} for reason {arg}")
        except:
          await member.kick(reason=reason)
          await ctx.send(embed=ui.Alert(ui.Style.SUCCESS, title="Member kicked. Didn't DM."))
        await member.kick(reason=reason)
        await ctx.send(embed=ui.Alert(ui.Style.SUCCESS, title="Member kicked & DMed."))
      else:
        await ctx.send("Cannot kick: You need kick_members permission")
    else:
      if ctx.message.author.guild_permissions.kick_members:
        try:
          await member.send(f"You've been kicked from {ctx.message.guild.name}")
        except:
          await member.kick(reason=reason)
          await ctx.send(embed=ui.Alert(ui.Style.SUCCESS, title="Member kicked. Didn't DM."))
        await member.kick(reason=reason)
        await ctx.send(embed=ui.Alert(ui.Style.SUCCESS, title="Member kicked & DMed."))
      else:
        await ctx.send("Cannot kick: You need kick_members permission")
  else:
    await ctx.send("Cannot kick: No member provided")




#Ban command
@bot.command()
@commands.bot_has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, arg = None, reason=None):
  if member:
    if arg != None:
      if ctx.message.author.guild_permissions.ban_members:
        try:
          await member.send(f"You've been banned from {ctx.message.guild.name} for reason {arg}")
        except:
          await member.ban(reason=reason)
          await ctx.send(embed=ui.Alert(ui.Style.SUCCESS, title="Member banned. Didn't DM."))
        await member.ban(reason=reason)
        await ctx.send(embed=ui.Alert(ui.Style.SUCCESS, title="Member banned & DMed."))
      else:
        await ctx.send("Cannot ban: You need ban_members permission")
    else:
      if ctx.message.author.guild_permissions.ban_members:
        try:
          await member.send(f"You've been banned from {ctx.message.guild.name}")
        except:
          await member.ban(reason=reason)
          await ctx.send(embed=ui.Alert(ui.Style.SUCCESS, title="Member banned. Didn't DM."))
        await member.ban(reason=reason)
        await ctx.send(embed=ui.Alert(ui.Style.SUCCESS, title="Member banned & DMed."))
      else:
        await ctx.send("Cannot ban: You need ban_members permission")
  else:
    await ctx.send("Cannot ban: No member provided")

#mute
@bot.command()
async def mute(ctx, member: discord.Member, *, reason=None):
	    guild = ctx.guild
	    mutedRole = discord.utils.get(guild.roles, name="Muted")

	    if not mutedRole:
	        mutedRole = await guild.create_role(name="Muted")

	        for channel in guild.channels:
	            await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=False)
	    embed = discord.Embed(title="Muted", description=f"{member.mention} was muted ", colour=discord.Colour.blue(), timestamp=datetime.datetime.utcnow())
	    embed.add_field(name="Reason:", value=reason, inline=False)
	    await ctx.reply(embed=embed)
	    await member.add_roles(mutedRole, reason=reason)
	    await member.send(f"You have been muted from: {guild.name} Reason: {reason}")
#end

#unmute
@bot.command()
async def unmute(ctx, member: discord.Member):
	    mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")

	    await member.remove_roles(mutedRole)
	    await member.send(f"You have unmuted from: {ctx.guild.name}")
	    embed = discord.Embed(title="Unmute", description=f"Unmuted {member.mention}", colour=discord.Colour.blue(), timestamp=datetime.datetime.utcnow())
	    await ctx.reply(embed=embed)
#end
#---------------------
#tempban
@bot.command()
async def tempban(ctx, member: discord.Member, time, d, *, reason="No Reason"):
		if member == None:
			embed = discord.Embed(f"{ctx.message.author}, Please enter a valid user!")
			await ctx.reply(embed=embed)
			

		else:
			guild = ctx.guild
			embed = discord.Embed(title="Banned!", description=f"{member.mention} has been banned!", colour=discord.Colour.blue(), timestamp=datetime.datetime.utcnow())
			embed.add_field(name="Reason: ", value=reason, inline=False)
			embed.add_field(name="Time left for the ban:", value=f"{time}{d}", inline=False)
			await ctx.reply(embed=embed)
			await guild.ban(user=member)

			if d == "s":
				await asyncio.sleep(int(time))
				await guild.unban(user=member)
			if d == "m":
				await asyncio.sleep(int(time*60))
				await guild.unban(user=member)
			if d == "h":
				await asyncio.sleep(int(time*60*60))
				await guild.unban(user=member)
			if d == "d":
				await asyncio.sleep(time*60*60*24)
				await guild.unban(int(user=member))
#end
#---------------
#unban
@bot.command()
async def unban(ctx, user: discord.User):
		if user == None:
			embed = discord.Embed(f"{ctx.message.author}, Please enter a valid user!")
			await ctx.reply(embed=embed)

		else:
			guild = ctx.guild
			embed = discord.Embed(title="Unbanned!", description=f"{user.display_name} has been unbanned!", colour=discord.Colour.blue(), timestamp=datetime.datetime.utcnow())
			await ctx.reply(embed=embed)
			await guild.unban(user=user)
#end

bot.run("Token")
