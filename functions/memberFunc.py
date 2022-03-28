import nextcord
from functions.generalFunc import Ranking2Embeds
from operator import attrgetter, itemgetter

#List members first to reach X loyalty
def getFirstAbove(membersList, val=int, typ=str):
  memAbove = []
  memBelow = []
  for m in membersList:
    if typ == 'loyalty':
      found, value, dat = m.firstTimeLoyaltyAbove(val)
    elif typ == 'skill':
      found, value, dat = m.firstTimeSkillAbove(val)
      
    if found:
      memAbove.append([m.rName(), value, dat, -value])
    elif value > 0:
      memBelow.append([m.rName(), value, dat, -value])
  memAbove.sort(key=itemgetter(2,1,0))
  memBelow.sort(key=itemgetter(3,2,0))
  ranking = firstToReach2table(memAbove, memBelow, typ)
  header = '**rank        Name                           Timediff**'
  fTitle = 'All ' + str(len(memAbove)) + ' Players that reached ' 

  if typ == 'loyalty':
    fTitle += str(val) + ' Loyalty'
    description = ''
    color = nextcord.Color.red()
  elif typ == 'skill':
    fTitle += 'skill lvl ' + str(val)
    description = ''
    color = nextcord.Color.blue()
  return Ranking2Embeds(ranking,fTitle,description,header,color)

#generate ranking for first to reach
def firstToReach2table(memAbove, memBelow, tpy):
  charLimits = [256,1024]
  i = 1
  rank = 0
  results = []
  rMess = '```'
  referenceValue = memAbove[0][1]
  referenceDate = memAbove[0][2]
  for m in memAbove:# + memBelow:
    #generate Ranking
    rank += 1
    ran = str(rank)
    while len(ran) < 3:
      ran = ' ' + ran
    ran += '. '

    #Name (shorten or fill up with white space)
    name = m[0]
    while len(name) > 15:
      name = name[:-1]
    while len(name) < 16:
      name += ' '

    #Value (shorten or fill up with white space)
    if rank == 1:
      value = str(m[1])
    else:
      delta = referenceDate - m[2]
      hours = str(24-round(delta.seconds/3600))
      while len(hours) < 2:
        hours = ' ' + hours
      hours += 'h'
      value = '+' + str(abs(delta.days)) + 'd ' + hours

    while len(value) > 9:
      value = value[:-1]
    while len(value) < 9:
      value = ' ' + value

    #split message if current line is exceeding charLimit
    if len(rMess + ran + name + value + '\n') + 5 >= charLimits[i]:
      rMess += '```'
      results.append(rMess)
      rMess = '```'
      i = 0 if i == 1 else 1
    rMess = rMess + ran + name + value + '\n'
  rMess += '```'
  results.append(rMess)
  return results
  
def getRankingEmbeds(memberList,typ,above=1,progressSince=None):
  ranking = []
  typPhrase = "Skill lvl"
  color = nextcord.Color.blue()
  for m in memberList:
    #Skill
    if typ == 'skill' and m.currentSkillLvl >= above:
      #Get all skill data greater/equal to given value
      r = [m.rName(), int(m.currentSkillLvl),m.lastSkillUpdate]
      if progressSince != None:
        #Add historic skill value if historic compare date is given
        success, skill, dat = m.historicSkill(progressSince)
        if skill == 0:
          skill = m.currentSkillLvl
        r.append(skill)
        r.append(dat)
        r.append(success)
      ranking.append(r)
    #Loyalty
    elif typ == 'loyalty' and m.currentLoyalty >= above:
      #Get all loyalty data greater/equal to given value
      r = [m.rName(), int(m.currentLoyalty),m.lastLoyaltyUpdate]
      if progressSince != None:
        #Add historic loyalty value if historic compare date is given
        success, loy, dat = m.historicLoyalty(progressSince)
        if loy == 0:
          loy = m.currentLoyalty
        r.append(loy)
        r.append(dat)
        r.append(success)
      ranking.append(r)
  #Sort Ranking
  ranking = sorted(ranking, key=lambda x: (1/x[1],x[2]), reverse=False)
  #Generate Ranking table
  if progressSince == None:
    table = generate_table(ranking)
  else:
    table = generate_table(ranking,True)
  
  #Standard values for skill/loyalty embeds
  if typ == 'skill':
    typPhrase = "Skill lvl"
    color = nextcord.Color.blue()
  elif typ == 'loyalty':
    typPhrase = "Loyalty"
    color = nextcord.Color.red()
  
  #Header for different requests
  if above == 1 and progressSince == None:
    title = str(len(ranking)) + " of " + str(len(memberList)) + " players " + typPhrase + "."
    description = ''
    header = '**Rank     Player                                  ' + typPhrase + '**'
  elif above == 1 and progressSince != None:
    title = 'Members ' + typPhrase + ' compared to ' + progressSince.strftime("%d.%b %Y")
    description = '* marked ' + typPhrase + ' are the oldest availabe data as no data was available for the requested date.'
    header = '**Player                                     ' + typPhrase + '**'
  elif above > 1 and progressSince == None:
    title ="There are " + str(len(ranking)) + " players above " + str(above) + " " + typPhrase + "."
    description = ''
    header = '**Rank     Player                                  ' + typPhrase + '**'
  elif above > 1 and progressSince != None:
    title ='Members that now have ' + typPhrase + ' higher than ' + str(above) + ' compared to ' + progressSince.strftime("%d.%b %Y") 
    description = '* marked ' + typPhrase + ' are the oldest availabe data as no data was available for the requested date.'
    header = '**Rank     Player                                  ' + typPhrase + '**'

  embeds = Ranking2Embeds(table,title,description,header,color)
  return embeds

def generate_table(ranking,compare=False):
  charLimits = [256,1024]
  i = 1
  results = []
  rMess = '```'
  rank = 0
  cRank = 0
  cLvl = 0
  for r in ranking:
    #generate rank no.
    rank += 1
    if cLvl != r[1]:
      cRank = rank
      cLvl = r[1]
    if compare:
      #no rank no. when comparing to old data
      ran = ''
    else:
      ran = str(cRank)
      while len(ran) < 3:
        ran = ' ' + ran
      ran += '. '

    #Player name (shorten and fill up with white space)
    line = r[0]
    while len(line) > 15:
      line = line[:-1]
    while len(line) < 16:
      line += ' '

    #Lengthen rank to 4 digits
    num = str(cLvl)
    while len(num) < 4:
      num = ' ' + num
    if compare:
      tnum = str(r[3])
      if not(r[5]):
        tnum = '*' + tnum
      while len(tnum) < 5:
        tnum = ' ' + tnum
      diff = r[1] - r[3]
      if diff >= 0:
        diff = '+' + str(diff)
      num = tnum + ' ➡ ' + num + ' ' + str(diff)
    
    #split message if current line is exceeding charLimit
    if len(rMess + ran + line +  num + '\n') + 5 >= charLimits[i]:
      rMess += '```'
      results.append(rMess)
      rMess = '```'
      i = 0 if i == 1 else 1
    rMess = rMess + ran + line +  num + '\n'
  rMess += '```'
  results.append(rMess)
  return results