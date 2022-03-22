#maximise usefulness score given the contraint of user spec points
#allocate usefulness points to specific nodes based on user priorities

from functions.blueSpecFunc import *
from functions.greenSpecFunc import *
from functions.drawSpecFunc import *
import pandas as pd
import itertools
import datetime 


# if extra tiles is selected, puts a group for each extra tile node in the list of priorities
def extra_tile(priorities_list):
  if "ExtraTile" in priorities_list:
    extra_list = []
    D = False
    L = False
    R = False
  
    if   "Land" in priorities_list or "TileHonour" in priorities_list:
      if D == False:
        extra_list.append("ExtraTileDTH")
        D = True
      if R == False:
        extra_list.append("ExtraTileRTH")
        R = True
    if  "TileSpeed" in priorities_list:
      if D == False:
        extra_list.append("ExtraTileDTS")
        D = True
      if R == False:
        extra_list.append("ExtraTileRTS")
        R = True
    if "UpgradeBuild" in priorities_list:
      if D == False:
        extra_list.append("ExtraTileDHon")
        D = True
      if L == False:
        extra_list.append("ExtraTileLHon")
        L = True
    if "FWMat" in priorities_list:
      if R == False:
        extra_list.append("ExtraTileRFW")
        R = True
      if L == False:
        extra_list.append("ExtraTileLFW")
        L = True
    if  "CBCMat" in priorities_list:
      if R == False:
        extra_list.append("ExtraTileRCBC")
        R = True
      if L == False:
        extra_list.append("ExtraTileLCBC")
        L = True
    if D == False:
      extra_list.append("ExtraTileDTS")
    if L == False:
      extra_list.append("ExtraTileLCBC")
    if R == False:
      extra_list.append("ExtraTileRCBC")
  
  return(extra_list)
  
#gets a full list of nodes to fulfil priorities
def getNodes(priorities_list_full):
  nodes_list = []
  node_priority =[]
  print(priorities_list_full)
  for p in priorities_list_full:

    if p in blueSpec_gr:
      l = blueSpec_gr[p][0]
    elif p in greenSpec_gr:
      l= greenSpec_gr[p][0]
    else:
      print ("l not assigned")
    for node in l:
      #if node not in nodes_list:
      nodes_list.append(node)
      node_priority.append(p)

  score = []
  title = []
  maxLevel = []
  
  for node in nodes_list:
    score.append(node.usefulScore)
    title.append(node.title)
    maxLevel.append(node.maxLvl)
    
  data = {'Node':nodes_list, 'Score':score, 'Title':title,'maxLvl':maxLevel, 'Priority':node_priority}
  df = pd.DataFrame(data)
  return(nodes_list, df)

### this is where you might want to tweak things to get better advice.  
def useful_assign(priorities_list):
  priorities_list_full = priorities_list
  nodes_list2 = getNodes(priorities_list_full)[1]
  #if LoyaltySpeedGroup is in the priorities, it should have a higher weighting than other priorities
  for index, row in nodes_list2.iterrows():
    if row['Priority'] in ('LoyaltySpeedGroup'):
      if row['Node'].activatable == True:
        nodes_list2.at[index, 'Score'] = 50
      else:
        nodes_list2.at[index, 'Score'] = 10
    else:
      if row['Node'].activatable == True:
        nodes_list2.at[index, 'Score'] = 20
      else:
        nodes_list2.at[index, 'Score'] = 5
      
  #assign to actual nodes
  for index, row in nodes_list2.iterrows():
    row['Node'].usefulScore = row['Score']


def sumPoints(x):
  Points = 0
  nodes = []
  for i in x:
    try: 
      if i in nodes:
        pass
      else:
        Points += i.maxLvl - i.currentLvl
        nodes.append(i)
    except:
      for n in i:
        if n in nodes:
          pass
        else:
          Points += n.maxLvl - n.currentLvl
          nodes.append(n)

  return(Points)

def useScore(score_dict):
  useScore = 0
  for i in score_dict:
    try:
      useScore += i.usefulScore
    except:
      for x in i:
        useScore += x.usefulScore
  return(useScore)


def combinations (df):
  df['match'] = df.Priority.eq(df.Priority.shift())

  df['req_nodes'] = ""
  #get required nodes for each node
  for index, row in df.iterrows():
    if row['match'] == False:
      df.at[index,'req_nodes'] = df.at[index, 'Node']
    else:
      prev = df.at[index -1,'req_nodes']
      group =[]

      try:
        for i in prev:
          if i not in group:
            group.append(i)
      except:
        group.append(prev)
      try:
        if row['Node'] not in prev:
          group.append(row['Node'])
      except:
        group.append(row['Node'])
      df.at[index,'req_nodes'] = group
      
  #get list of possible combinations of nodes for each main priority
  mp_list = df['Priority'].unique()
  possibleCombSets = []
  for mp in mp_list:
    mp_combs = []
    mp_combs=df.query('Priority==@mp')['req_nodes'].to_list()
    possibleCombSets.append(mp_combs)

  possibleComb =[]
  #gets all possible combinations (only 1 from each set, but does not have to be one from every set)
  for L in range(0, len(possibleCombSets)+1):
    for subset in itertools.combinations(possibleCombSets, L):
      c = list(itertools.product(*subset))
      for i in c:
        possibleComb.append(i)
          #print(possibleComb)
  print("num poss comb", len(possibleComb))
  return (possibleComb)

def evaluate(Nodes, df, userSpecPoints):
  possibleSets = []
  setPoints = []
  setScores = []
  print("comb", datetime.datetime.now())
  possibleComb  = combinations(df)
  print("eval sets", datetime.datetime.now())
  for comb in possibleComb:
    pointsReq = sumPoints(comb)
    if userSpecPoints - 10 <= pointsReq <= userSpecPoints:
      setScore = useScore(comb)
      possibleSets.append(comb)
      setPoints.append(pointsReq)
      setScores.append(setScore)
  data = {'NodeSets':possibleSets, 'PointsReq':setPoints, 'UseScore':setScores}
  
  print("create df", datetime.datetime.now())
  print(f"valid combos: {len(setScores)}")
  df_eval = pd.DataFrame(data)
  
  idxMaxScore = df_eval['UseScore'].idxmax()
  nodeset = df_eval['NodeSets'][idxMaxScore]
  pt = df_eval['PointsReq'][idxMaxScore]
  us = df_eval['UseScore'][idxMaxScore]
 
  print("points", pt)
  print("Useful Score", us)
  print("spec points available", userSpecPoints)
  userSpecPoints -= pt

  return(nodeset, userSpecPoints)

def assignPoints(nodeset,userSpecPoints):
  for x in nodeset:
    try:
      for node in x:
        while userSpecPoints > 0 and node.currentLvl < node.maxLvl: 
          node.currentLvl += 1
          userSpecPoints -= 1
    except:
      while userSpecPoints > 0 and x.currentLvl < x.maxLvl: 
          x.currentLvl += 1
          userSpecPoints -= 1
      


def most_use(priorities_list_full, userSpecPoints):
  print("start", datetime.datetime.now())
  df = getNodes(priorities_list_full)[1]
  Nodes = list(df['Node'])
  nodePoints = sumPoints(Nodes)
  print("node points", nodePoints)
  if nodePoints <= userSpecPoints:
    print("assign p straight away")
    assignPoints(Nodes, userSpecPoints)
    userSpecPointsNew = userSpecPoints - nodePoints
  else:
    print("eval", datetime.datetime.now())
    eval = evaluate(Nodes, df, userSpecPoints)
    nodeset = eval[0]
    userSpecPointsNew = eval[1]
    print("assign p", datetime.datetime.now())
    assignPoints(nodeset, userSpecPoints)
  print("finished", datetime.datetime.now())
  return(userSpecPointsNew)
 

def specAdvice(list1, list2, userSpecPoints, groups_bl, groups_gr):
  priorities_list = list1
  finished = False
  while finished == False:
    priorities = []
    for i in priorities_list:

  #gets dependencies for Extra tiles depending on other selections
      if i == "ExtraTile":
        eval_list = []
        for i in list1:
          eval_list.append(i)
        for i in list2:
          eval_list.append(i)
        ExTiles = extra_tile(eval_list)
        for g in ExTiles:
          priorities.append(g)
  ## gets dependencies for Land based on other selections
      elif  i == "Land":
        if "TileSpeed" in priorities_list:
          priorities.append("LandTS")
        else:
          priorities.append("LandTH")
      else:
        priorities.append(i)

 
    print(priorities)

    useful_assign(priorities)
    userSpecPoints  = most_use(priorities, userSpecPoints)
 
    print("updates sp", userSpecPoints)
    if userSpecPoints > 0:
      if priorities_list == list2:
        finished = True
      else:
        priorities_list = list2
    else:
      finished = True
  
  print(list1, list2)
  draw(groups_bl,bl,bl_l,"blueSpec.png", firstSpecs_bl)
  draw(groups_gr,gr,gr_l,"greenSpec.png", firstSpecs_gr)

  #set all nodes back to zero
  for group in groups_bl:
      #Loop specs in group
    for s in group:
      s.currentLvl  = 0
  for group in groups_gr:
      #Loop specs in group
    for s in group:
      s.currentLvl  = 0
        