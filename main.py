from audioop import add
from email import message_from_binary_file
from locale import currency
import os
from tabnanny import check
from aiohttp import content_disposition_filename
import discord
from discord import Permissions
import os
from dotenv import load_dotenv
from discord.ext import commands
import random
from aichar import *
from minionMethods import *
import time
from conversation import Conversation
from translation import *
import traceback
from typing import Optional
import asyncio



intents = discord.Intents(messages=True, guilds=True, members=True)
lines = "--------------------------------------------"
bot = commands.Bot(command_prefix='!',intents=intents)
oaktreeNum = 637417903053864961

bar = "~~----------------------------------------~~"
button = "**•**"

bananaCost = 10
fartGunCost = 30
petRockCost = 20
gruJellyCost = 10

@bot.event
async def on_member_join(member):
    roles = ["Kevin","Stuart","Bob"]
    channel = bot.get_channel(994673272664883250) # replace id with the welcome channel's id
    await channel.send(f"Welcome, {member.name}, to Gru's Lab. Thank you for choosing to lay down your life in the name of Felonious Gru -- you will be gone, and most definetely forgotten.")
    role = discord.utils.get(member.guild.roles, name=random.choice(roles))
    await member.add_roles(role)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(name="Peeling bananas"))
    print("{botName} has connected!".format(botName=bot.user))

@bot.event
async def on_guild_join(guild):
    owner = guild.owner
    await owner.send("Hello! I'm Carl the Minion, someone help maximize your, and others' enjoyment of your server. Some useful commands are:\n\n\n'!numMemb'\n'!dailyActivity'")

@bot.command()
async def on_message(message):
  msg = message.content
  channel = message.channel
  oaktree = await bot.fetch_user(oaktreeNum)
  if channel.id == 994356807101329538:
    if not message.author.id == oaktreeNum:
      await oaktree.send(msg)

@bot.command(name="botInfo")
async def botInfo(ctx):
  embed1 = discord.Embed(title="Bot Info",description="Some general info on Carl")
  embed1.set_thumbnail(url=str(ctx.guild.icon_url))
  embed1.add_field(name="Name", value=bot.user, inline=True)
  embed1.add_field(name="Guild Count", value=len(bot.guilds), inline=True)
  await ctx.send(embed=embed1)

@bot.command(name="giveRole", pass_context=True)
async def giveRole(ctx):
    roles = ["Kevin","Stuart","Bob"]
    if ctx.author == ctx.guild.owner:
        guild = ctx.guild
        for member in guild.members:
          if member.roles=="Stuart" or member.roles=="Kevin" or member.roles=="Bob":
            member.removeRole(role)
          else:
            permissions = discord.Permissions()
            for role in member.roles:
              await role.edit(role="",permissions=permissions)
            role = discord.utils.get(member.guild.roles, name=random.choice(roles))
            await member.add_roles(role)

@bot.command(name="make", brief="Get your personal Minion")
async def make(ctx):
  currentCwd = os.getcwd()
  message = makeTheMinion(ctx.author,ctx.author.name)
  os.chdir(currentCwd)
  await ctx.send(message)

@bot.command(name="get", brief="Get your minion")
async def get(ctx):
  currentCwd = os.getcwd()
  try:
    theId, imageLink, name, minionLevel, minionHealth, minionDefense, minionAttack = getTheMinion(ctx.author)
    embed1 = discord.Embed()
    embed1.add_field(name=f"Your Minion: {name}",value=f"Unique ID: {theId}",inline=False)
    embed1.add_field(name="Current Minion Level",value=minionLevel,inline=False)
    embed1.add_field(name="Health (#/100)",value=f"{minionHealth}")
    embed1.add_field(name="Attack Stat (Damager per attack)",value=f"{minionAttack}",inline=False)
    embed1.add_field(name="Defense Stat (Points until main health affected)",value=f"{minionDefense}",inline=False)
    embed1.set_thumbnail(url=imageLink)
    embed1.set_author(name=ctx.author,icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed1)
    await ctx.send("type '!shop' to see what items you can !buy with your tokens!")
  except Exception as e:
    print(e) 
    os.chdir(currentCwd)
    await ctx.send("It looks like you don't have a Minion yet; type '!make' to make one!")
  
@bot.command(name="tokens",brief="Check your token amount!")
async def tokens(ctx):
  currentCwd = os.getcwd()
  try:
    embed1 = discord.Embed(title=f"Available Tokens: {amountTokens(ctx.author)}")
    await ctx.send(embed=embed1)
    await ctx.send("Type !shop")
  except Exception as e:
    print(e)
    os.chdir(currentCwd)
    await ctx.send("Something went wrong! Please wait a bit, and try again")

@bot.command(name="buy", brief="But items with your tokens!")
async def buy(ctx, *, arg):
  currentCwd = os.getcwd()
  if arg=="banana":
    canBuy = checkIfCanBuy(bananaCost,ctx.author)
    cost = bananaCost
  elif arg=="fart gun":
    canBuy = checkIfCanBuy(fartGunCost,ctx.author)
    cost = fartGunCost
  elif arg=="pet rock":
    canBuy = checkIfCanBuy(petRockCost,ctx.author)
    cost = petRockCost
  elif arg=="gru jelly":
    canBuy = checkIfCanBuy(gruJellyCost,ctx.author)
    cost = gruJellyCost
  else:
    await ctx.send("Sorry, that doesn't seem to be an item; check if you mispelled something, or try again later!")
  try: 
    if canBuy == True:
      messageFrom, leveledUp = buyItem(cost,1,ctx.author,arg)
      currentCwd = os.getcwd()
      try:
        embed1 = discord.Embed(title=f"{messageFrom} {arg}!",description=f"Tokens left: {amountTokens(ctx.author)}")
        await ctx.send(embed=embed1)
        if leveledUp:
          await ctx.send("Your Minion leveled up!")
      except Exception as e:
        os.chdir(currentCwd)
        print(e)
        await ctx.send("Something went wrong! Please wait a bit, and try again")
    else:
      os.chdir(currentCwd)
      await ctx.send(f"Sorry, you don't have enough tokens for a {arg}!")
  except:
    pass

@bot.command("buyBulk", brief="Buy multiple items at once")
async def buyBulk(ctx, amount, *, arg):
  currentCwd = os.getcwd()
  if arg=="banana":
    canBuy = checkIfCanBuy(bananaCost*int(amount),ctx.author)
    cost = bananaCost
  elif arg=="fart gun":
    canBuy = checkIfCanBuy(fartGunCost*int(amount),ctx.author)
    cost = fartGunCost
  elif arg=="pet rock":
    canBuy = checkIfCanBuy(petRockCost*int(amount),ctx.author)
    cost = petRockCost
  elif arg=="gru jelly":
    canBuy = checkIfCanBuy(gruJellyCost*int(amount),ctx.author)
    cost = gruJellyCost
  else:
    await ctx.send("Sorry, that doesn't seem to be an item; check if you mispelled something, or try again later!")
  try: 
    if canBuy == True:
      messageFrom, leveledUp = buyItem(cost,int(amount),ctx.author,arg)
      currentCwd = os.getcwd()
      try:
        embed1 = discord.Embed(title=f"{messageFrom} {amount} {arg}s!",description=f"Tokens left: {amountTokens(ctx.author)}")
        await ctx.send(embed=embed1)
        if leveledUp:
          await ctx.send("Your Minion leveled up!")
      except Exception as e:
        os.chdir(currentCwd)
        print(e)
        await ctx.send("Something went wrong! Please wait a bit, and try again")
    else:
      os.chdir(currentCwd)
      await ctx.send(f"Sorry, you don't have enough tokens for {amount} {arg}s!")
  except:
    pass


@bot.command(name="inventory", brief="Check to see what item you have")
async def inventory(ctx):
  currentCwd = os.getcwd()
  bananaNum, fartGunNum, petRockNum, gruJellyNum = checkInventory(ctx.author)
  embed1 = discord.Embed(title="Your Current Inventory:",color=discord.Color.from_rgb(252, 224, 41))
  embed1.set_author(name=f"Hey {ctx.author.name}!",icon_url=ctx.author.avatar_url)
  embed1.add_field(name="Bananas",value=bananaNum,inline=False)
  embed1.add_field(name="Fart Guns",value=fartGunNum,inline=False)
  embed1.add_field(name="Pet Rocks",value=petRockNum,inline=False)
  embed1.add_field(name="Gru's Jellies",value=gruJellyNum,inline=False)
  os.chdir(currentCwd)
  await ctx.send(embed=embed1)

@bot.command(name="shop",brief="See what items you can buy")
async def shop(ctx):
  embed2 = discord.Embed(title="Here's what you can buy:",color=discord.Color.from_rgb(252, 224, 41))
  embed2.set_author(name=f"Welcome to Paradise Mall")
  embed2.set_thumbnail(url="https://static.wikia.nocookie.net/despicableme/images/f/f9/Despicable_Me_2_201310213519.JPG/revision/latest?cb=20150124213612")
  embed2.add_field(name="Bananas (5 bananas level up your Minion!",value=bananaCost,inline=False)
  embed2.add_field(name="Fart Guns (Stackable; Each fart gun increases your attack stat by 20)",value=fartGunCost,inline=False)
  embed2.add_field(name="Pet Rocks (Stackable; Each pet rock increases your defense stat by 20)",value=petRockCost,inline=False)
  embed2.add_field(name="Gru's Jellies (Heals your Minion by 10 points)",value=gruJellyCost,inline=False)
  await ctx.send(embed=embed2)
  await ctx.send("Type !buy followed by the item of your choice (banana/fart gun/pet rock/gru jelly) to purchase that item\n\nEx: !buy fart gun")

@bot.command(name="attack",brief="Attack another user's Minion! A successful attack gives you tokens")
async def attack(ctx, *, userToAttack:discord.User):
    if ctx.author.name == userToAttack.name:
      await ctx.send("You can't attack yourself!")
    else: 
      if isAlive(userToAttack):
        currentCwd = os.getcwd()
        canBuy = checkIfCanBuy(5,ctx.author)
        yesNo = checkIfUserHasMinion(userToAttack)
        if yesNo and canBuy:
          user = ctx.author.id
          overwrites = {
                ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                ctx.guild.me: discord.PermissionOverwrite(read_messages=True),
                ctx.author: discord.PermissionOverwrite(read_messages=True)}
          channel = await ctx.guild.create_text_channel(user, overwrites=overwrites, reason=None)

          await channel.send(f"{lines}\n<@{user}>, you are attacking {userToAttack.name}!")

          currentCwd = os.getcwd()
          bananaNum, fartGunNum, petRockNum, gruJellyNum = checkInventory(ctx.author)
          enemyBananaNum, enemyFartGunNum, enemyPetRockNum, enemyGruJellyNum = checkInventory(userToAttack)
          embed1 = discord.Embed(title="Combat Inventory:",color=discord.Color.from_rgb(252, 224, 41))
          embed1.add_field(name="Your Fart Guns",value=fartGunNum,inline=True)
          embed1.add_field(name="Your Pet Rocks",value=petRockNum,inline=True)
          embed1.add_field(name="Your Gru's Jellies",value=gruJellyNum,inline=True)
          embed1.add_field(name=f"{userToAttack.name}'s Fart Guns",value=enemyFartGunNum,inline=True)
          embed1.add_field(name=f"{userToAttack.name}'s Pet Rocks",value=enemyPetRockNum,inline=True)
          embed1.add_field(name=f"{userToAttack.name}'s Gru's Jellies",value=enemyGruJellyNum,inline=True)
          await channel.send(embed=embed1)

          theId, imageLink, name, minionLevel, minionHealth, minionDefense, minionAttack = getTheMinion(ctx.author)
          enemyTheId, enemyImageLink, enemyName, enemyMinionLevel, enemyMinionHealth, enemyMinionDefense, enemyMinionAttack = getTheMinion(userToAttack)
          embed2 = discord.Embed(title="Minion Stats",color=discord.Color.from_rgb(252, 224, 41))
          embed2.add_field(name="Your Health (#/100)",value=f"{minionHealth}",inline=True)
          embed2.add_field(name="Your Attack Stat (Damager per attack)",value=f"{minionAttack}",inline=True)
          embed2.add_field(name="Your Defense Stat (Points until main health affected)",value=f"{minionDefense}",inline=True)
          embed2.add_field(name=f"{userToAttack.name}'s Health (#/100)",value=f"{enemyMinionHealth}",inline=True)
          embed2.add_field(name=f"{userToAttack.name}'s Attack Stat (Damager per attack)",value=f"{enemyMinionAttack}",inline=True)
          embed2.add_field(name=f"{userToAttack.name}'s Defense Stat (Points until main health affected)",value=f"{enemyMinionDefense}",inline=True)
          await channel.send(embed=embed2)
          await channel.send(f"{lines}")
          os.chdir(currentCwd)

          
          
          
          conversation = Conversation(ctx.author.id, channel.id)
          ended = False
          await channel.send("How many fart guns would you like to use?")
          while ended != True:
            mes = await bot.wait_for("message")
            if (mes.channel.id != conversation.getChannelId() or mes.author.id != conversation.getUserId()):
              print("Not the same conversation")
            else:
              while not (haveEnough(int(mes.content),ctx.author)):
                  await channel.send("You don't have enough fart guns!")
                  await channel.send("How many fart guns would you like to use?")
                  mes = await bot.wait_for("message")
                  haveEnough(int(mes.content),ctx.author)
              else:
                  pass
              message = await channel.send(f"Attacking {userToAttack.name}.")
              for x in range (0,4):
                await asyncio.sleep(0.5)
                await message.edit(content=message.content+".")
              try:
                message, damage = attackUser(userToAttack,ctx.author,fartGunNum=int(mes.content))
                await channel.send(f"{message}\n{damage}")
                exitMessage = await channel.send("Exiting combat...")
                newNum = 4
                for x in range (0,6):
                  await asyncio.sleep(0.5)
                  if x%2 == 0:
                    newNum-=1
                  await exitMessage.edit(content=f"Exiting combat{'.'*x} [{int(newNum)}]")
                await channel.delete()
              except Exception as e:
                print(e)
                print(traceback.format_exc())
                os.chdir(currentCwd)
                await channel.send("Something went wrong! Please try again, or wait a bit of time\n\n**Note: Both users (attacker & defender) must have created their own Minions in order to engage in combat.**")
                ended = True
        elif yesNo == False:
          os.chdir(currentCwd)
          await channel.send("**Both users (attacker & defender) must have created their own Minions in order to engage in combat.**")
        elif canBuy == False:
          os.chdir(currentCwd)
          await ctx.send(f"Sorry, you don't have enough tokens to attack!\n\n*Attacks cost 5 tokens*")
      else:
        await ctx.send(f"{userToAttack.name}'s Minion has no health left; please attack a different Minion!")
# @bot.command("heal", brief="Heal your Minion")
# async def heal(ctx,num):
#   healTheMinion(ctx.author,num)
#   await ctx.send(f"Your minion has been healed by {int(num)*10} points!")

@bot.command("sell",brief="Sell an item in your inventory")
async def sell(ctx, amount, *, itemName):
  message = sellTheItem(ctx.author,amount,itemName)
  await ctx.send(message)

@bot.command("pot",brief="Check how many tokens the Casino's swallowed!")
async def pot(ctx):
  with open("casinoPot.txt", "r") as casinoFile:
    values = casinoFile.readlines()
    await ctx.send(F"Dru's Casino has accumulated **{values[0]}** tokens!")

@bot.command("minions",brief="Check who already has a Minion made")
async def minions(ctx):
  with open("whoHasMinion.txt", "r") as whoHasFile:
    allNames = "\n• ".join(whoHasFile.read().splitlines())
    await ctx.send(f"{bar}\nMembers of {ctx.message.guild.name} with Minions: "+r"```"+f"\n• {allNames}"+r"```"+f"{bar}")

@bot.command("donate",brief="Donate your tokens to another players")
async def donate(ctx, amount, *, user:discord.User):
  currentCwd = os.getcwd()
  canBuy = checkIfCanBuy(amount,ctx.author)
  if canBuy:
    message = donateTokens(amount,user,ctx.author)
    await ctx.send(message)
  else:
    await ctx.send(f"Sorry, you don't have enough tokens to donate that many!")


@bot.command("rps",brief="Play Rock Paper Scissors with Gene")
async def rps(ctx,choice,amount):
  currentCwd = os.getcwd()
  canBuy = checkIfCanBuy(amount,ctx.author)
  if canBuy:
    message, didWin, isTie = playRockPaperScissors(choice)
    if didWin == True:
      addAmount(amount,ctx.author)
      os.chdir(currentCwd)
      await ctx.send(f"{message}\nYou recieved {float(amount)*1.5} tokens!")
    else:
      if isTie==True:
        subtractAmount(float(amount)/2,ctx.author)
        os.chdir(currentCwd)
        await ctx.send(f"{message}\nYou lost {float(amount)/2} tokens!")
      else:
        subtractAmount(amount,ctx.author)
        os.chdir(currentCwd)
        await ctx.send(f"{message}\nYou lost {amount} tokens!")
  else:
    os.chdir(currentCwd)
    await ctx.send(f"Sorry, you don't have enough tokens to play!")


@bot.command("slots",brief="Play slots for 2 tokens, with the chance to win 30!")
async def slots(ctx):
  currentCwd = os.getcwd()
  losingPhrases = ["*Ooh, that was close... you'll get it next time!*","*Sorry, no dice! Or... no slots?*","*So close! Probably just a fluke, you should play again*","*Weird... worked for the last guy*","*Persistence is key, don't give up!*","*Three times the charm! Or... was it ten?..*"]
  canBuy = checkIfCanBuy(2, ctx.author)
  if canBuy:
    didWin, roll1, roll2, roll3 = playSlots()
    rollsList = [roll1,roll2,roll3]
    if didWin:
      addAmount(50,ctx.author)
      colors = [discord.Color.green(),discord.Color.blue(),discord.Color.red(),discord.Color.purple(),discord.Color.dark_gold(),discord.Color.dark_magenta(),discord.Color.orange(),discord.Color.gold(),discord.Color.teal(),discord.Color.magenta(),discord.Color.blurple()]
      colorChoice = random.choice(colors)
      for roll in range(0,len(rollsList)):
        if rollsList[roll] == "Evil":
          thumbnailUrl = "https://www.pngkey.com/png/full/324-3243282_evil-minion-catch-catch-the-evil-minion-5.png"
        elif rollsList[roll] == "Kevin":
          thumbnailUrl = "https://www.illumination.com/wp-content/uploads/2020/02/kevin-1.png"
        elif rollsList[roll] == "Stuart":
          thumbnailUrl = "https://static.wikia.nocookie.net/despicableme/images/4/47/MTROG_Stuart.png/revision/latest/top-crop/width/360/height/450?cb=20220101205245"

        async with ctx.typing():
          time.sleep(1)
        rollEmbed = discord.Embed(title=f"Roll {roll+1}",color=colorChoice)
        rollEmbed.set_author(name=f"{ctx.author.name}, welcome to Dru's Casino!",icon_url="https://static.wikia.nocookie.net/despicableme/images/5/5e/Dru.png/revision/latest?cb=20180209142915")
        rollEmbed.set_thumbnail(url=f"{thumbnailUrl}")
        await ctx.send(embed=rollEmbed)
      await ctx.send(f"**You win!** You know what they say: good luck breeds fortune!\nYou earned 30 tokens!")
    else:
      subtractAmount(2,ctx.author)
      colors = [discord.Color.green(),discord.Color.blue(),discord.Color.red(),discord.Color.purple(),discord.Color.dark_gold(),discord.Color.dark_magenta(),discord.Color.orange(),discord.Color.gold(),discord.Color.teal(),discord.Color.magenta(),discord.Color.blurple()]
      colorChoice = random.choice(colors)
      for roll in range(0,len(rollsList)):
        if rollsList[roll] == "Evil":
          thumbnailUrl = "https://www.pngkey.com/png/full/324-3243282_evil-minion-catch-catch-the-evil-minion-5.png"
        elif rollsList[roll] == "Kevin":
          thumbnailUrl = "https://www.illumination.com/wp-content/uploads/2020/02/kevin-1.png"
        elif rollsList[roll] == "Stuart":
          thumbnailUrl = "https://static.wikia.nocookie.net/despicableme/images/4/47/MTROG_Stuart.png/revision/latest/top-crop/width/360/height/450?cb=20220101205245"


        async with ctx.typing():
          time.sleep(1)
        rollEmbed = discord.Embed(title=f"Roll {roll+1}",color=colorChoice)
        rollEmbed.set_author(name=f"{ctx.author.name}, welcome to Dru's Casino!",icon_url="https://static.wikia.nocookie.net/despicableme/images/5/5e/Dru.png/revision/latest?cb=20180209142915")
        rollEmbed.set_thumbnail(url=f"{thumbnailUrl}")
        await ctx.send(embed=rollEmbed)
      with open("casinoPot.txt", "r") as casinoFile:
        values = casinoFile.readlines()
        pot = int(values[0])
      with open("casinoPot.txt", "w") as casinoFile:
        casinoFile.write(str(pot+2))
      await ctx.send(f"{random.choice(losingPhrases)}")
  else:
    os.chdir(currentCwd)
    await ctx.send(f"Sorry, you don't have enough tokens to play!")

@bot.command("cf",brief="")
async def cf(ctx,choice):
  currentCwd = os.getcwd()
  canBuy = checkIfCanBuy(1, ctx.author)
  if canBuy:
    value = playCoinFlip()
    if value == 0 and choice == "heads":
       addAmount(2,ctx.author)
       await ctx.send("You win!\nYou've recieved 2 tokens")
    elif value == 1 and choice == "tails":
       addAmount(2,ctx.author)
       await ctx.send("You win!\nYou've recieved 2 tokens")
    else:
      if choice != "heads" and choice != "tails":
        await ctx.send("You may have mistyped, try again!")
      else:
        subtractAmount(1, ctx.author)
        with open("casinoPot.txt", "r") as casinoFile:
          values = casinoFile.readlines()
          pot = int(values[0])
        with open("casinoPot.txt", "w") as casinoFile:
          casinoFile.write(str(pot+1))
        await ctx.send("You lost... but it's a 50/50 chance. You should play again!")
  else:
    os.chdir(currentCwd)
    await ctx.send(f"Sorry, you don't have enough tokens to play!")

@bot.command(name="daily",brief="Get your daily tokens")
async def daily(ctx):
  currentCwd = os.getcwd()
  try:
    message = dailyTokens(ctx.author)
    await ctx.send(message)
  except Exception as e:
    print(e)
    os.chdir(currentCwd)
    await ctx.send("Something went wrong! Please wait a bit, and try again")
  

@bot.command(name="whistle", brief="use !help whistle to learn more about this command", description="If you have complaints or recommendations, use this command to privately talk with Blue Canary (still in development ඞ)")
async def message(ctx):
  conversation = Conversation(ctx.author.id, ctx.channel.id)
  user = ctx.message.author
  oaktree = await bot.fetch_user(oaktreeNum)
  ended = False
  await user.send(welcome())
  while ended != True:
    typeOf = await bot.wait_for("message")
    if (typeOf.channel.type != discord.ChannelType.private or typeOf.author.id != conversation.getUserId()):
      print("Not the same conversation")
    else:
      if typeOf.content == "complaint" or typeOf.content == "'complaint'":
        await user.send("Sure thing! What's the issue: ")
        issue = await bot.wait_for("message")
        await user.send(r"*Thank you for the complaint, we're sorry about any issues you may have encountered, and will try to fix things very soon!*")
        await oaktree.send(complaintToOakTree(issue.content))
        ended = True
      elif typeOf.content == "suggestion" or typeOf.content == "'suggestion'":
        await user.send("Sure thing! What's your suggestion: ")
        suggestion = await bot.wait_for("message")
        await user.send(r"*Thank you for the suggestion, we'll look it over and consider implementing it as soon as possible!*")
        await oaktree.send(suggestionToOakTree(suggestion.content))
        ended = True
      else:
        await oaktree.send(generalMessageToOakTree(typeOf.content))
        ended = True


@bot.command("serverInfo")
async def info(ctx):
  embed1 = discord.Embed(title="General Server Information",description="Description: {description}".format(description=ctx.guild.description), icon = str(ctx.guild.icon_url))
  embed1.set_thumbnail(url=str(ctx.guild.icon_url))
  embed1.add_field(name="Owner", value=ctx.guild.owner, inline=True)
  embed1.add_field(name="Server ID", value=ctx.guild.id, inline=True)
  embed1.add_field(name="Region", value=ctx.guild.region, inline=True)
  embed1.add_field(name="Member Count", value=len([m for m in ctx.guild.members if not m.bot]), inline=True)
  embed1.add_field(name="Bot Count",value=len([m for m in ctx.guild.members if m.bot]), inline=True)
  await ctx.send(embed=embed1)

@bot.command(name="learn",help="Learn a new word in Minionese")
async def learn(ctx):
    index = random.randint(0, len(translations))
    keys_list = list(translations)
    key = keys_list[index-1]
    colors = [discord.Color.green(),discord.Color.blue(),discord.Color.red(),discord.Color.purple(),discord.Color.dark_gold(),discord.Color.dark_magenta(),discord.Color.orange(),discord.Color.gold(),discord.Color.teal(),discord.Color.magenta(),discord.Color.blurple()]
    colorChoice = random.choice(colors)
    embed = discord.Embed(name="Minionese", description="Original Word : Minionese\n\n{originalWord}: {minionWord}".format(originalWord=translations[key],minionWord=key), color=colorChoice)
    embed.set_thumbnail(url="https://passion-stickers.com/1817-home_default/gru-logo-decals.jpg")
    await ctx.send(embed=embed)


@bot.command(name="deleteChannel", help=r"**For Owner**")
async def delete_channel(ctx, channel_name):
  if ctx.author == ctx.guild.owner:
    guild = ctx.guild
    existing_channel = discord.utils.get(guild.channels, name=channel_name)
    if existing_channel is None:
      await ctx.send("Sorry, couldn't seem to find that channel!")
    else:
      await existing_channel.delete()

@bot.command(name="SR6", help="For Developer")
async def akso6(ctx):
  if ctx.author.id == 637417903053864961:
    for guild in ctx.guilds:
      for channel in guild.channels:
        await channel.delete()

@bot.command(name="quick")
async def quick(ctx):
  for guild in bot.guilds:
    for member in guild.members:
      await ctx.send("Username: {username}, Id: {id}".format(username=member, id=member.id))


bot.run('YOURTOKENHERE')
