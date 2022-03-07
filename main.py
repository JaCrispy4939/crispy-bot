#By Ja'Crispy and IntelScripter
import discord
import os
from discord.colour import Colour
from discord.embeds import Embed
import requests
import json
from discord.ext import commands
import math
import random
import time


start_time = time.time()

client = commands.Bot(command_prefix=".")
client.remove_command('help') # Removes the default help command

colors = [0, 10000]

# Embed for help command
ehelp = discord.Embed(
    title="Commands",
    
    #description="MODERATION\n .kick (@user)\n.ban (@user)\n.clear (amount)\n\nFUN STUFF\n.inspire\n.rps (rock, paper or scissors)\n.echo (message)\n.embed (message)\n\n\n\nUSEFUL\n.serverinfo\n.userinfo (@user)\n.botinfo\n\n\nMISC\n.uptime\n .invite",
    colour= discord.Colour.from_rgb(102, 255, 255)
)   
ehelp.add_field(name="Moderation", value=".kick (@user)\n.ban (@user)\n.clear")
ehelp.add_field(name="Fun", value=".inspire\n.rps \n.echo (message)\n.embed (message)\n.coinflip")
ehelp.add_field(name="Misc", value=".serverinfo\n.userinfo (@user)\n.botinfo\n.uptime\n.invite")

@client.event
async def on_member_join(ctx, member):
  for channel in member.guild.channels:
      if str(channel) == "general-chat":
          await ctx.channel.send_message(f"""Welcome {member.mention} Please check out #roles""")

@client.event
async def on_ready():
  servercount = len(client.guilds)
  membercount = sum(g.member_count for g in client.guilds)
  membersrounded = math.floor(membercount)
  await client.change_presence(status=discord.Status.idle,  activity=discord.Activity(type= discord.ActivityType.playing, name=f".help | servers: {servercount}"))
  client.intents.all()
  client.intents.members

#help command
@client.command()
async def help(ctx):
  await ctx.send(embed = ehelp)

#invite bot command
@client.command()
async def invite(ctx):
  await ctx.send("invite link: https://discord.com/oauth2/authorize?client_id=650122164669906947&scope=bot")

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)


@client.command()
async def coinflip(ctx):
  coin = ["Heads", "Tails"]
  flip = random.choice(coin)
  await ctx.send("Flipping a coin...")
  time.sleep(3)
  await ctx.send("The coin landed on " + flip)

@client.command()
async def inspire(ctx):
    quote = get_quote()
    await ctx.send(quote)
#kick command
@client.command()
@commands.has_permissions(administrator= True)
async def kick(ctx, member : discord.Member, *, reason=None):
    await member.kick(reason= reason)
#ban command
@client.command()
@commands.has_permissions(administrator= True)
async def ban(ctx, member : discord.Member, *, reason=None):
    await member.ban(reason= reason)

#unban command
@client.command()
@commands.has_permissions(administrator= True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_number = member.split('#')
    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name and user.discriminator) == (member_name and member_number):
            await ctx.guild.unban(user)
            await ctx.send("Unbanned {user.mention}")
            return

#clear command
@client.command()
@commands.has_permissions(administrator= True)
async def clear(ctx, amount=5):
    await ctx.send("Clearing Messages...")
    time.sleep(3)
    await ctx.channel.purge(limit=amount + 2)


  

#rock paper scissors game
@client.command()
async def rps(ctx, *, choice):
    choices = ['rock', 'paper', 'scissors']
    RPS = choices[random.randint(0, 2)]

        # Embeds for rps
    tie_embed = discord.Embed(
        title= "We Tied",
        description= f"We both had {choice}",
        colour= discord.Colour.from_rgb(0, 0, 0)
    )
    player_win_embed = discord.Embed(
    title= "You Win",
    description= f"I had {RPS}",
    colour= discord.Colour.from_rgb(0, 0, 0)
    )
    player_lose_embed = discord.Embed(
    title= "You Lose",
    description= f"I had {RPS}",
    colour= discord.Colour.from_rgb(0, 0, 0)
    )



    #rock paper scissors command
    if choice == RPS:
        await ctx.send(embed= tie_embed)
    elif choice == 'rock':
        if RPS == 'paper':
            await ctx.send(embed= player_lose_embed)
        elif RPS == 'scissors':
            await ctx.send(embed= player_win_embed)
    elif choice == 'scissors':
        if RPS == 'paper':
            await ctx.send(embed= player_win_embed)
        elif RPS == 'rock':
            await ctx.send(embed= player_lose_embed)
    elif choice == 'paper':
        if RPS == 'scissors':
            await ctx.send(embed= player_lose_embed)
        elif RPS == 'rock':
            await ctx.send(embed= player_win_embed)
    else:
        await ctx.send("Please pick rock, paper, or scissors")


#echo embed message #hey scripter, i almost have this command but i need some help
@client.command()
async def embed(ctx, *, echoCommand):
  sender = str(ctx.author)

  #echo embed
  echo_embed = discord.Embed(
  title= "Embedded Message",
  colour= discord.Colour.from_rgb(100, 0, 0),
  description= echoCommand
)

  echo_embed.set_footer(text=f'Sent by {sender}')

  await ctx.channel.purge(limit= 1)
  time.sleep(.5)
  await ctx.send(embed= echo_embed)


#echo command
@client.command()
async def echo(ctx, *, echoCommand):
  await ctx.channel.purge(limit= 1)
  time.sleep(.5)
  await ctx.send(echoCommand)

@client.command()
async def serverinfo(ctx):
  guild = ctx.guild
  name = str(ctx.guild.name)
  description = str(ctx.guild.description)
  owner = (guild.owner)
  icon = str(ctx.guild.icon_url)
  memberCount = str(ctx.guild.member_count)
  onlineMembers = (member.status==discord.Status.online for member in ctx.guild.members)
  offlineMembers = sum(member.status==discord.Status.offline for member in ctx.guild.members)
  bots = sum(member.bot for member in ctx.guild.members)
  channels = len(guild.channels)
  categories = len(guild.categories)
  region = str(ctx.guild.region)
  text_channels = len(guild.text_channels)
  voice_channels = len(guild.voice_channels)
  id = str(ctx.guild.id)
  serverinfoEmbed = discord.Embed(

    title =f"Server Info for {name}",
    colour= discord.Colour.from_rgb(0, 0, 0)

  )

  date_format = "%a, %d %b %Y %I:%M %p"

  serverinfoEmbed.set_thumbnail(url=icon)
  serverinfoEmbed.add_field(name="Owner", value=f"owner" , inline=True)
  serverinfoEmbed.add_field(name="Members", value=f'Members: {memberCount}\nOnline: {onlineMembers}, \nBots: {bots}', inline=True)
  serverinfoEmbed.add_field(name="Channels", value=f'{channels} total channels\n{categories} total categories\n{text_channels} text channels\n{voice_channels} voice channels', inline=True)
  serverinfoEmbed.add_field(name="Region", value=region, inline=True)
  serverinfoEmbed.add_field(name="Created On", value=guild.created_at.strftime(date_format))
  serverinfoEmbed.add_field(name="Total Roles", value=len(guild.roles))
  serverinfoEmbed.set_footer(text=f"ID: {id}")
  


  await ctx.send(embed=serverinfoEmbed)



@client.command()
async def botinfo(ctx):
  import datetime, time

  sender = str(ctx.author)

  botinfoembed = discord.Embed(

    title ="Bot Info",
    colour= discord.Colour.from_rgb(0, 0, 0)

  )
  current_time = time.time()
  difference = int(round(current_time - start_time))
  text = str(datetime.timedelta(seconds=difference))


  botinfoembed.set_footer(text=f"Requested by: {sender}")
  members = sum(g.member_count for g in client.guilds)
  membersrounded = math.floor(members)
  botinfoembed.add_field(name="Servers", value=f"{len(client.guilds)}")
  botinfoembed.add_field(name="Members", value=f"{membersrounded}")
  botinfoembed.add_field(name="Uptime", value=f"{text}")
  botinfoembed.add_field(name="Developer", value=f"Ja'Crispy#6927")

  await ctx.send(embed=botinfoembed)

#userinfo command
@client.command()
async def userinfo(ctx, *, Member: discord.Member = None):
  
  if Member is None:
      Member = ctx.author

  userinfo_embed = discord.Embed(
    colour= discord.Colour.from_rgb(0, 0, 0)
    
  )

  date_format = "%a, %d %b %Y %I:%M %p"

  userinfo_embed.set_author(name=str(Member), icon_url=Member.avatar_url)
  userinfo_embed.set_thumbnail(url=Member.avatar_url)
  userinfo_embed.add_field(name="Joined Server", value=Member.joined_at.strftime(date_format))
  userinfo_embed.add_field(name="Joined Discord", value=Member.created_at.strftime(date_format))
  if len(Member.roles) > 1:
        role_string = ' '.join([r.mention for r in Member.roles][1:])
        userinfo_embed.add_field(name="Roles [{}]".format(len(Member.roles)-1), value=role_string, inline=False)
  perm_string = ', '.join([str(p[0]).replace("_", " ").title() for p in Member.guild_permissions if p[1]])
  userinfo_embed.add_field(name="Server Permissions", value=perm_string, inline=False)
  userinfo_embed.set_footer(text='ID: ' + str(Member.id))

  await ctx.send(embed=userinfo_embed)

#auto message for new users on Programming Central
@client.event
async def on_member_join(member):
  print("member joined")
  await member.send(f"Welcome to the server {member.name}! Feel free to pick up some roles in #roles")


@client.command()
async def uptime(ctx):
  import datetime, time
  current_time = time.time()
  difference = int(round(current_time - start_time))
  text = str(datetime.timedelta(seconds=difference))
  embed = discord.Embed(colour=0xc8dc6c)
  embed.add_field(name="Uptime", value=text)
  embed.set_footer(text=".help")
  await ctx.send(embed=embed)


@client.command()
async def github(ctx):
  await ctx.send("View the bots code: https://github.com/JaCrispy4939/crispy-bot")




print("Bot Online")

client.run("Nope")
