import os
import nextcord
from replit import db
from keep_alive import keep_alive
from nextcord.utils import get
from nextcord.ext import commands
import logging
#import pandas as pd
#from modules.classes.Structure import Structure
from functions import staticValues as sv
from functions import setupFunc as sf

logging.basicConfig(level=logging.INFO)

intents = nextcord.Intents.default()
intents.members = True
intents.reactions = True
client = commands.Bot(intents=intents, command_prefix="??")


@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))
  sf.loadCogs(client)
  #sf.importStructureCSV()

@client.event
async def on_message(message):
  msg = message.content.lower()
  if message.author == client.user or message.author.bot:
    return
    
  #Target Planner
  if message.channel.name == 'target-planning':
    #Help
    if msg.startswith('help'):
      annChannel = get(message.author.guild.channels, name='announcements')
      sentMsg = await message.channel.send("Here is your help:\n**add** - add target *Name*, *Coordinates*, *time*, *flag*, *team*, *note* (optional)\nPlease mind the comma otherwise your request can't be processed\n**flag** lists all flag castles\n**remove** *X* - remove a target from the list by ID\n**switch** *X* *Y*- Switch the order of 2 targets by ID\n**publish** - Publish the current target list to {0.mention}".format(annChannel))
      if len(db.prefix("msgHelpMessage")) > 0:
        omID = db["msgHelpMessage"]
        oldMsg = await message.channel.fetch_message(omID)
        await oldMsg.delete()
      db["msgHelpMessage"] = sentMsg.id
      await message.delete()
      return

  #Availability
  elif message.channel.name == "availability":
    msg = message.content.lower()
    allowed = False
    for r in message.author.roles:
      if r.name == 'Leadership':
        allowed = True
      elif r.name == 'Developers':
        allowed = True
    if not(allowed):
      await message.delete()
      return
    #help function
    if msg.startswith('help'):
      annChannel = get(message.author.guild.channels, name='announcements')
      sentMsg = await message.channel.send("Here is your help (only Leadership can use these):\n**eval** - evaluate the current availability\n**help** - overview of all commands")
      if len(db.prefix("avlMsgHelp")) > 0:
        omID = db["avlMsgHelp"]
        oldMsg = await message.channel.fetch_message(omID)
        await oldMsg.delete()
      db["avlMsgHelp"] = sentMsg.id
      await message.delete()
      return

    #evaluate the availability survey
    elif msg.startswith('eval'):
      sentProgMsg = await message.channel.send('Thinking, please wait...')
      chan = message.channel
      await message.delete()
      [options, optionsTxt] = db["avlOptionsSurvey"]
      results = []
      result = '**Names in brackets still need to be assigned to a team**\n'
      survey = await chan.fetch_message(db["avlMsgSurvey"])
      votes = {}
      for reaction in survey.reactions:
        allUsers = await reaction.users().flatten()
        users = []
        for u in allUsers:
          if u.bot:
            continue
          users.append(u)
        votes[reaction.emoji] = users
      votersAlways = votes[options[-1]]
      for i in range(len(options)-1):
        #voters = db["avlPoll" + options[i]]
        voters = votes[options[i]]
        for v in votersAlways:
          if v in voters:
            voters.remove(v)
          voters.append(v)
        unassignedVoters = []
        for v in voters:
          assigned = False
          for r in v.roles:
            if r.name.lower().startswith('team'):
              assigned = True
          if not(assigned):
            unassignedVoters.append(v)
        uV = ''
        for v in unassignedVoters:
          uV += v.display_name + ', '
        uV = uV[0:-2]
        optionRes = '**' +options[i] + ' - ' + str(len(voters)) + ' available** (' + uV +')\n'
        if len(result) + len(optionRes) >= 2000:
          results.append(result)
          result = optionRes
          continue
        result += optionRes
      results.append(result)

      mesIDs = []
      for r in results:
        sentMsg = await chan.send(r)
        mesIDs.append(sentMsg.id)

       
      dataset = open("results.csv","w")
      for r in results:
        dataset.write(r)
      dataset.close()
      dataset = open("results.csv", "r")
      sentMsg = await chan.send(file=nextcord.File(dataset))
      
      mesIDs.append(sentMsg.id)


      #sentMsg = await chan.send(result)
      #del db["avlMsgEvals"]
      if len(db.prefix("avlMsgEvals")) > 0:
        omIDs = db["avlMsgEvals"]
        for omID in omIDs:
          oldMsg = await chan.fetch_message(omID)
          await oldMsg.delete()
      db["avlMsgEvals"] = mesIDs
      await sentProgMsg.delete()
      return

    #survey 
    elif msg.startswith('survey'):
      rEmbed = nextcord.Embed(
          color = nextcord.Colour.blue(),
          description = 'Please react to all the times you (or your account) can be online.'
        )
      text = '```'
      options = []
      optionsTxt = []
      for i in range(12):
        options.append(sv.emojiAlph[i])
        optionsTxt.append(time2str(i*2) + ' - ' + time2str(i*2+2))
        text += options[-1]+' ' + optionsTxt[-1] + "\n"
        db["avlPoll"+options[-1]] = []
      options.append(sv.emojiAlph[12])
      db["avlPoll"+options[-1]] = []
      optionsTxt.append('Always')
      text += options[-1] + ' ' + optionsTxt[-1] + '```'
      rEmbed.add_field(name='**Availability (server time)**',value=text,inline=False)
      sentMsg = await message.channel.send(embed=rEmbed)
      for em in options:
        await sentMsg.add_reaction(em)
      db["avlOptionsSurvey"] = [options, optionsTxt]
      if len(db.prefix("avlMsgSurvey")) > 0:
        omID = db["avlMsgSurvey"]
        oldMsg = await message.channel.fetch_message(omID)
        await oldMsg.delete()
      db["avlMsgSurvey"] = sentMsg.id
      await message.delete()
      return

    #Clean DB
    elif "clean" in msg.lower():
      roles = message.author.roles
      allowed = False
      for r in roles:
        if 'Host' == r.name:
          allowed = True
      if allowed == False:
        await message.delete()
        return
      
      msgDB = db.prefix("avlMsg")
      for dbEntry in msgDB:
        del db[dbEntry]
      await message.delete()
    else:
      sentMsg = await message.channel.send("Sorry couldn't process your request: " + msg)
      if len(db.prefix("msgErrorAvl")) > 0:
        omID = db["msgErrorAvl"]
        oldMsg = await message.channel.fetch_message(omID)
        await oldMsg.delete()
      db["msgErrorAvl"] = sentMsg.id
      await message.delete()
      return

@client.event
async def on_raw_reaction_add(payload):
  if payload.member.id == client.user.id:
    return
  avSurvID = 0
  if len(db.prefix("avlMsgSurvey")) > 0:
      avSurvID = db["avlMsgSurvey"]
  if payload.message_id == avSurvID:
    for e in sv.emojiAlph:
      if e == payload.emoji.name:
        curL = []
        if len(db.prefix("avlPoll"+e)) > 0:
          curL = db["avlPoll"+e]
          if any(m == payload.member.id for m in curL):
            print(payload.member.display_name + ' already in the db for ' + e)
            return
        curL.append(payload.member.id)
        db["avlPoll"+e] = curL
        print(payload.member.display_name + ' added to the db for ' + e)
  else:
    print(payload)

@client.event
async def on_raw_reaction_remove(payload):
  if payload.user_id == client.user.id:
    return
  avSurvID = 0
  if len(db.prefix("avlMsgSurvey")) > 0:
      avSurvID = db["avlMsgSurvey"]
  if payload.message_id == avSurvID:
    for e in sv.emojiAlph:
      if e == payload.emoji.name:
        curL = []
        if len(db.prefix("avlPoll"+e)) > 0:
          curL = db["avlPoll"+e]
          if any(m == payload.user_id for m in curL):
            print(str(payload.user_id) + ' removed from the db for ' + e)
            curL.remove(payload.user_id)
            db["avlPoll"+e] = curL
            return
  else:
    print(payload)


keep_alive()
client.run(os.environ['TOKEN'])