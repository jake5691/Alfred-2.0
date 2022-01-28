import os
import nextcord
import re
from replit import db
from keep_alive import keep_alive
from nextcord.utils import get
from nextcord.ext import commands
import logging
import pandas as pd
from modules.classes.Structure import Structure

logging.basicConfig(level=logging.INFO)

intents = nextcord.Intents.default()
intents.members = True
intents.reactions = True
client = commands.Bot(intents=intents, command_prefix="??")
gIDS = [895003315883085865]
roles = {
    "RBC": 899673831633981503,
    "Leadership": 902605996713721888,
    "Developers": 898655389397168140,
    "Guild Leader": 910980797211746336
}

emojiAlph = ['🇦','🇧','🇨','🇩','🇪','🇫','🇬','🇭','🇮','🇯','🇰','🇱','🇲','🇳']

def loadCogs():
  #Initialize bot
  if os.path.exists(os.path.join("modules","setup","setup-cog.py")):
    client.load_extension(f"modules.setup.setup-cog")
  #Loading all cogs
  for  folder in os.listdir("modules"):
    if os.path.exists(os.path.join("modules",folder,"cog.py")):
      client.load_extension(f"modules.{folder}.cog")

def loadTargets():
  tList = []
  #Load current target list
  if len(db.prefix("targetList")) > 0:
    tList = db["targetList"]
  else:
    db["targetList"] = tList
  return tList

def addTarget(msg):
  msgL = msg.split(',')
  if len(msgL) >= 5:
    tList = loadTargets()
    
    #Format target to match DB
    tNum = 0
    if len(tList) > 0:
      tNum = tList[-1][0]
    tNum += 1
    thisTarget = [tNum]
    for f in msgL:
      thisTarget.append(f.strip())
    while len(thisTarget) < 7:
      thisTarget.append('')

    #Add target to DB
    tList.append(thisTarget)
    db["targetList"] = tList

    return True, tList
  return False, ''

def getAllTargets():
  tList = loadTargets()
  if len(tList) == 0:
    return '```List empty```'
  targets = '```'
  for t in tList:
    #Number
    tStr = str(t[0])
    while len(tStr) < 2:
      tStr = ' ' + tStr
    tStr += ': '
    #Name & Cords
    tStr += t[1] + ' (' + t[2] + ') '
    #Time
    tStr += '@' + t[3]
    #Flag
    tStr += ' - Flag: ' + t[4]
    #Team
    tStr += ' - ' + t[5]
    #Notes
    if t[6] != '':
      tStr += ' - ' + t[6]
    targets += tStr + '\n'
  targets += '```'
  return targets

def getAllTargetsWithMention():
  tList = loadTargets()
  if len(tList) == 0:
    return 'No targets for today.'
  targets = ''
  flags = []
  teams = []
  for t in tList:
    #Name & Cords
    tStr = ' (' + t[2] + ') ' + t[1]
    #Time
    tStr += ' @' + t[3]
    #Flag
    tStr += ' - Flag: ' + t[4]
    flags.append(t[4])
    #Team
    tStr += ' - ' + t[5]
    #Notes
    if t[6] != '':
      tStr += ' - ' + t[6]
    targets += tStr + '\n'
  targets += ''
  return targets, flags, teams

def removeTarget(msg):
  id = re.findall('[0-9]+', msg)
  if len(id) != 1:
    return False
  id = int(id[0])
  tList = loadTargets()
  if id <= len(tList) and id > 0:
    tList.pop(id-1)
    for i in range(len(tList)):
      tList[i][0] = i+1
    return True
  return False

def switchTarget(msg):
  id = re.findall('[0-9]+', msg)
  if len(id) != 2:
    return False
  id1 = int(id[0])-1
  id2 = int(id[1])-1
  tList = loadTargets()
  if id1+1 <= len(tList) and id1+1 > 0 and id2+1 <= len(tList) and id2+1 > 0:
    tList[id1], tList[id2] = tList[id2], tList[id1]
    for i in range(len(tList)):
      tList[i][0] = i+1
    return True
  return False

def time2str(time):
  timeStr = str(time)
  while len(timeStr) < 2:
    timeStr = '0' + timeStr
  return timeStr + ':00'

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))
  loadCogs()
  ###Load eden structure information from csv
  #e_str = pd.read_csv(os.path.join("modules","data","eden_buildings_ALL_3.csv"),sep=";")
  #db["allStructures"] =[]
  #e = []
  #for _,r in e_str.iterrows():
  #  st = Structure(sector=r['SECTOR'],typ=r['TYPE'],lvl=r['LVL'],x=int(r['X']),y=int(r['Y']))
  #  e.append(st.str2db())
  #db["allStructures"] = e
  
#print(os.getenv("REPLIT_DB_URL"))

@client.event
async def on_message(message):
  msg = message.content.lower()
  if message.author == client.user or message.author.bot:
    return
  #Show Teams
  if message.channel.name == 'strategy':
    if msg.startswith('show teams'):
      allMembers = message.guild.members
      wTeam = get(message.guild.roles, name='Team Whiskey')
      tTeam = get(message.guild.roles, name='Team Tango')
      fTeam = get(message.guild.roles, name='Team Foxtrot')
      gTeam = get(message.guild.roles, name='Guild member')
      rTeam = get(message.guild.roles, name='RBC')
      wMembers = []
      wStr = '**Team Whiskey:**'
      tMembers = []
      tStr = '**Team Tango:**'
      fMembers = []
      fStr = '**Team Foxtrot:**'
      rest = []
      rStr = '**Unnasigned:**'
      for m in allMembers:
        if wTeam in m.roles:
          wMembers.append(m)
          wStr += '\n' + m.display_name
        elif tTeam in m.roles:
          tMembers.append(m)
          tStr += '\n' + m.display_name
        elif fTeam in m.roles:
          fMembers.append(m)
          fStr += '\n' + m.display_name
        elif m.bot == False and (gTeam in m.roles or rTeam in m.roles):
          rest.append(m)
          rStr += '\n' + m.display_name
      await message.channel.send(wStr)
      await message.channel.send(tStr)
      await message.channel.send(fStr)
      await message.channel.send(rStr)
    
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

    #Add Target
    elif msg.startswith('add'):
      msg = msg.replace('add','').strip()
      addedTarget, tList = addTarget(msg)
      if addedTarget:
        sentMsg = await message.channel.send("You added the target.")
        
        rEmbed = nextcord.Embed(
          color = nextcord.Colour.red()
        )
        rEmbed.add_field(name='**Target list**',value=getAllTargets(),inline=False)
        sentMsgTL = await message.channel.send(embed=rEmbed)
        if len(db.prefix("msgTargetList")) > 0:
          omID = db["msgTargetList"]
          oldMsgTL = await message.channel.fetch_message(omID)
          await oldMsgTL.delete()
        db["msgTargetList"] = sentMsgTL.id
      else:
        sentMsg = await message.channel.send("No target was added, your request was not correct:\n " + msg)
      if len(db.prefix("msgAddTarget")) > 0:
        omID = db["msgAddTarget"]
        oldMsg = await message.channel.fetch_message(omID)
        await oldMsg.delete()
      db["msgAddTarget"] = sentMsg.id
      await message.delete()
      return
    
    #Reorder Targets
    elif msg.startswith('switch'):
      if switchTarget(msg):
        sentMsg = await message.channel.send("You switched two target.")
        
        rEmbed = nextcord.Embed(
          color = nextcord.Colour.red()
        )
        rEmbed.add_field(name='**Target list**',value=getAllTargets(),inline=False)
        sentMsgTL = await message.channel.send(embed=rEmbed)
        if len(db.prefix("msgTargetList")) > 0:
          omID = db["msgTargetList"]
          oldMsgTL = await message.channel.fetch_message(omID)
          await oldMsgTL.delete()
        db["msgTargetList"] = sentMsgTL.id
      else:
        sentMsg = await message.channel.send("Sorry couldn't process your request: " + msg)
      if len(db.prefix("msgAddTarget")) > 0:
        omID = db["msgAddTarget"]
        oldMsg = await message.channel.fetch_message(omID)
        await oldMsg.delete()
      db["msgAddTarget"] = sentMsg.id
      await message.delete()
      return

    #Remove Target
    elif msg.startswith('remove'):
      if removeTarget(msg):
        sentMsg = await message.channel.send("You removed a target.")
        
        rEmbed = nextcord.Embed(
          color = nextcord.Colour.red()
        )
        rEmbed.add_field(name='**Target list**',value=getAllTargets(),inline=False)
        sentMsgTL = await message.channel.send(embed=rEmbed)
        if len(db.prefix("msgTargetList")) > 0:
          omID = db["msgTargetList"]
          oldMsgTL = await message.channel.fetch_message(omID)
          await oldMsgTL.delete()
        db["msgTargetList"] = sentMsgTL.id
      else:
        sentMsg = await message.channel.send("Sorry couldn't process your request: " + msg)
      if len(db.prefix("msgAddTarget")) > 0:
        omID = db["msgAddTarget"]
        oldMsg = await message.channel.fetch_message(omID)
        await oldMsg.delete()
      db["msgAddTarget"] = sentMsg.id
      await message.delete()
      return
    
    #Publish Targets
    elif "publish" in msg.lower():
      annChannel = get(message.author.guild.channels, name='announcements')
      targets, flags, teams = getAllTargetsWithMention()
      for f in flags:
        flag = []
        for player in client.guilds[0].members:
          if player.bot:
            continue
          if f.lower() in player.display_name.lower():
            flag.append(player)
        if len(flag) == 1:
          targets = targets.replace(f,'<@' + str(flag[-1].id) + '>')
      for t in teams:
        team = []
        for team in client.guids[0].roles:
          print(t.lower() + ' ?=? ' + team.name.lower())
          if t.lower() in team.name.lower():
            team.append(t)
        if len(team) == 1:
          targets = targets.replace(f,'<@' + str(team[-1].id) + '>')
      rEmbed = nextcord.Embed(
        color = nextcord.Colour.red()
      )
      rEmbed.add_field(name='**Target list**',value=targets,inline=False)
      sentMsgTL = await annChannel.send(embed=rEmbed)
      if len(db.prefix("msgPubTargetList")) > 0:
        omID = db["msgPubTargetList"]
        oldMsgTL = await annChannel.fetch_message(omID)
        await oldMsgTL.delete()
      db["msgPubTargetList"] = sentMsgTL.id
      await message.delete()

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
      
      msgDB = db.prefix("msg")
      for dbEntry in msgDB:
        del db[dbEntry]
      await message.delete()
    #Error
    else:
      sentMsg = await message.channel.send("Sorry couldn't process your Request: " + msg)
      if len(db.prefix("msgErrorMessage")) > 0:
        omID = db["msgErrorMessage"]
        oldMsg = await message.channel.fetch_message(omID)
        await oldMsg.delete()
      db["msgErrorMessage"] = sentMsg.id
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
        options.append(emojiAlph[i])
        optionsTxt.append(time2str(i*2) + ' - ' + time2str(i*2+2))
        text += options[-1]+' ' + optionsTxt[-1] + "\n"
        db["avlPoll"+options[-1]] = []
      options.append(emojiAlph[12])
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
    for e in emojiAlph:
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
    for e in emojiAlph:
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