##added here to make sure we don't lose it
#need to update to get to work

def redSpec():
  print('Red Spec')
  global radius_v, Prio1, Prio2, Prio3, blueSpec_gr, specPoints, specB
  radius_v = radiusDict_red
  specPoints = specB
  print(specPoints)
  #colors
  grey = (200,200,200)
  white = (255,255,255)
  red = (200,50,50)
  red_1 = (200,150,150)
  #Define all specs
  #UP
  ArchReignMightUp1 = Spec("Archer Reign Might 1",getPoint(12,1),3)
  ArchReignMightUp2 = Spec("Archer Reign Might 2",getPoint(12,2,(1-10.5/11)*x_center),3)
  ArchReignMightUp3 = Spec("Archer Reign Might 3",getPoint(12,5),3)
  ArchReignMightUp4 = Spec("Archer Reign Might 4",getPoint(12,7),3)
  ArchReignMightUp5 = Spec("Archer Reign Might 5",getPoint(12,8,(1-10.5/11)*x_center),3)
  ArchReignMightUp6 = Spec("Archer Reign Might 6",getPoint(12,11),3)
  ArchReignMightUp7 = Spec("Archer Reign Might 4",getPoint(12,13),3)
  ArchReignMightUp8 = Spec("Archer Reign Might 5",getPoint(12,14,(1-10.5/11)*x_center),3)
  ArchReignMightUp9 = Spec("Archer Reign Might 6",getPoint(12,15),3)
  ArchReignResisUp1 = Spec("Archer Reign Resistance 1",getPoint(12,2,-(1-10.5/11)*x_center),3)
  ArchReignResisUp2 = Spec("Archer Reign Resistance 2",getPoint(12,8,-(1-10.5/11)*x_center),3)
  ArchReignResisUp3 = Spec("Archer Reign Resistance 3",getPoint(12,14,-(1-10.5/11)*x_center),3)

  CavReignMightUp1 = Spec("Cavalry Reign Might 1",getPoint(12,3,(1-9/11)*x_center),3)
  CavReignMightUp2 = Spec("Cavalry Reign Might 2",getPoint(12,4,(1-8.5/11)*x_center),3)
  CavReignMightUp3 = Spec("Cavalry Reign Might 3",getPoint(12,6,(1-9/11)*x_center),3)
  CavReignMightUp4 = Spec("Cavalry Reign Might 4",getPoint(12,9,(1-8.5/11)*x_center),3)
  CavReignMightUp5 = Spec("Cavalry Reign Might 5",getPoint(12,10,(1-8/11)*x_center),3)
  CavReignMightUp6 = Spec("Cavalry Reign Might 6",getPoint(12,12,(1-8.5/11)*x_center),3)
  CavReignMightUp7 = Spec("Cavalry Reign Might 7",getPoint(12,13,(1-8.5/11)*x_center),3)
  CavReignMightUp8 = Spec("Cavalry Reign Might 8",getPoint(12,14,(1-8/11)*x_center),3)
  CavReignMightUp9 = Spec("Cavalry Reign Might 9",getPoint(12,15,(1-8.5/11)*x_center),3)
  CavReignResisUp1 = Spec("Cavalry Reign Resistance 1",getPoint(12,4,(1-9.5/11)*x_center),3)
  CavReignResisUp2 = Spec("Cavalry Reign Resistance 2",getPoint(12,10,(1-9/11)*x_center),3)
  CavReignResisUp3 = Spec("Cavalry Reign Resistance 3",getPoint(12,14,(1-9/11)*x_center),3)

  FooReignMightUp1 = Spec("Footmen Reign Might 1",getPoint(12,3,-(1-9/11)*x_center),3)
  FooReignMightUp2 = Spec("Footmen Reign Might 2",getPoint(12,4,-(1-8.5/11)*x_center),3)
  FooReignMightUp3 = Spec("Footmen Reign Might 3",getPoint(12,6,-(1-9/11)*x_center),3)
  FooReignMightUp4 = Spec("Footmen Reign Might 4",getPoint(12,9,-(1-8.5/11)*x_center),3)
  FooReignMightUp5 = Spec("Footmen Reign Might 5",getPoint(12,10,-(1-8/11)*x_center),3)
  FooReignMightUp6 = Spec("Footmen Reign Might 6",getPoint(12,12,-(1-8.5/11)*x_center),3)
  FooReignMightUp7 = Spec("Footmen Reign Might 7",getPoint(12,13,-(1-8.5/11)*x_center),3)
  FooReignMightUp8 = Spec("Footmen Reign Might 8",getPoint(12,14,-(1-8/11)*x_center),3)
  FooReignMightUp9 = Spec("Footmen Reign Might 9",getPoint(12,15,-(1-8.5/11)*x_center),3)
  FooReignResisUp1 = Spec("Footmen Reign Resistance 1",getPoint(12,4,-(1-9.5/11)*x_center),3)
  FooReignResisUp2 = Spec("Footmen Reign Resistance 2",getPoint(12,10,-(1-9/11)*x_center),3)
  FooReignResisUp3 = Spec("Footmen Reign Resistance 3",getPoint(12,14,-(1-9/11)*x_center),3)
  
  ChaosExpertise = Spec("Chaos Expertise",getPoint(12,6),5,True)
  ChaosMaster = Spec("Chaos Master",getPoint(12,12),5,True)
  PioneerBanner = Spec("Pioneer Banner",getPoint(12,16,(1-9/11)*x_center),5,True)
  RaiderBanner = Spec("Raider Banner",getPoint(12,16,-(1-9/11)*x_center),5,True)
  CoalitionCommander = Spec("Coalition Commander",getPoint(12,17),5,True)

  #Right
  ArchSiegeMightRi1 = Spec("Archer Siege Might 1",getPoint(4,1),3)
  ArchSiegeMightRi2 = Spec("Archer Siege Might 2",getPoint(4,2,(1-10.5/11)*x_center),3)
  ArchSiegeMightRi3 = Spec("Archer Siege Might 3",getPoint(4,5),3)
  ArchSiegeMightRi4 = Spec("Archer Siege Might 4",getPoint(4,7),3)
  ArchSiegeMightRi5 = Spec("Archer Siege Might 5",getPoint(4,8,(1-10.5/11)*x_center),3)
  ArchSiegeMightRi6 = Spec("Archer Siege Might 6",getPoint(4,11),3)
  ArchSiegeMightRi7 = Spec("Archer Siege Might 4",getPoint(4,13),3)
  ArchSiegeMightRi8 = Spec("Archer Siege Might 5",getPoint(4,14,(1-10.5/11)*x_center),3)
  ArchSiegeMightRi9 = Spec("Archer Siege Might 6",getPoint(4,15),3)
  ArchSiegeResisRi1 = Spec("Archer Siege Resistance 1",getPoint(4,2,-(1-10.5/11)*x_center),3)
  ArchSiegeResisRi2 = Spec("Archer Siege Resistance 2",getPoint(4,8,-(1-10.5/11)*x_center),3)
  ArchSiegeResisRi3 = Spec("Archer Siege Resistance 3",getPoint(4,14,-(1-10.5/11)*x_center),3)

  CavSiegeMightRi1 = Spec("Cavalry Siege Might 1",getPoint(4,3,(1-9/11)*x_center),3)
  CavSiegeMightRi2 = Spec("Cavalry Siege Might 2",getPoint(4,4,(1-8.5/11)*x_center),3)
  CavSiegeMightRi3 = Spec("Cavalry Siege Might 3",getPoint(4,6,(1-9/11)*x_center),3)
  CavSiegeMightRi4 = Spec("Cavalry Siege Might 4",getPoint(4,9,(1-8.5/11)*x_center),3)
  CavSiegeMightRi5 = Spec("Cavalry Siege Might 5",getPoint(4,10,(1-8/11)*x_center),3)
  CavSiegeMightRi6 = Spec("Cavalry Siege Might 6",getPoint(4,12,(1-8.5/11)*x_center),3)
  CavSiegeMightRi7 = Spec("Cavalry Siege Might 7",getPoint(4,13,(1-8.5/11)*x_center),3)
  CavSiegeMightRi8 = Spec("Cavalry Siege Might 8",getPoint(4,14,(1-8/11)*x_center),3)
  CavSiegeMightRi9 = Spec("Cavalry Siege Might 9",getPoint(4,15,(1-8.5/11)*x_center),3)
  CavSiegeResisRi1 = Spec("Cavalry Siege Resistance 1",getPoint(4,4,(1-9.5/11)*x_center),3)
  CavSiegeResisRi2 = Spec("Cavalry Siege Resistance 2",getPoint(4,10,(1-9/11)*x_center),3)
  CavSiegeResisRi3 = Spec("Cavalry Siege Resistance 3",getPoint(4,14,(1-9/11)*x_center),3)

  FooSiegeMightRi1 = Spec("Footmen Siege Might 1",getPoint(4,3,-(1-9/11)*x_center),3)
  FooSiegeMightRi2 = Spec("Footmen Siege Might 2",getPoint(4,4,-(1-8.5/11)*x_center),3)
  FooSiegeMightRi3 = Spec("Footmen Siege Might 3",getPoint(4,6,-(1-9/11)*x_center),3)
  FooSiegeMightRi4 = Spec("Footmen Siege Might 4",getPoint(4,9,-(1-8.5/11)*x_center),3)
  FooSiegeMightRi5 = Spec("Footmen Siege Might 5",getPoint(4,10,-(1-8/11)*x_center),3)
  FooSiegeMightRi6 = Spec("Footmen Siege Might 6",getPoint(4,12,-(1-8.5/11)*x_center),3)
  FooSiegeMightRi7 = Spec("Footmen Siege Might 7",getPoint(4,13,-(1-8.5/11)*x_center),3)
  FooSiegeMightRi8 = Spec("Footmen Siege Might 8",getPoint(4,14,-(1-8/11)*x_center),3)
  FooSiegeMightRi9 = Spec("Footmen Siege Might 9",getPoint(4,15,-(1-8.5/11)*x_center),3)
  FooSiegeResisRi1 = Spec("Footmen Siege Resistance 1",getPoint(4,4,-(1-9.5/11)*x_center),3)
  FooSiegeResisRi2 = Spec("Footmen Siege Resistance 2",getPoint(4,10,-(1-9/11)*x_center),3)
  FooSiegeResisRi3 = Spec("Footmen Siege Resistance 3",getPoint(4,14,-(1-9/11)*x_center),3)
  
  SiegeExpertise = Spec("Siege Expertise",getPoint(4,6),5,True)
  IronWarriors = Spec("Iron Warriors",getPoint(4,12),5,True)
  Invisibility = Spec("Invisibility",getPoint(4,16,(1-9/11)*x_center),5,True)
  Taunt = Spec("Taunt",getPoint(4,16,-(1-9/11)*x_center),5,True)
  PrecisionShout = Spec("Precision Shout",getPoint(4,17),5,True)
  
  #Left
  ArchSiegeDefResisLe1 = Spec("Archer Siege Defense Resistance 1",getPoint(-4,1),3)
  ArchSiegeDefResisLe2 = Spec("Archer Siege Defense Resistance 2",getPoint(-4,2,(1-10.5/11)*x_center),3)
  ArchSiegeDefResisLe3 = Spec("Archer Siege Defense Resistance 3",getPoint(-4,5),3)
  ArchSiegeDefResisLe4 = Spec("Archer Siege Defense Resistance 4",getPoint(-4,7),3)
  ArchSiegeDefResisLe5 = Spec("Archer Siege Defense Resistance 5",getPoint(-4,8,(1-10.5/11)*x_center),3)
  ArchSiegeDefResisLe6 = Spec("Archer Siege Defense Resistance 6",getPoint(-4,11),3)
  ArchSiegeDefResisLe7 = Spec("Archer Siege Defense Resistance 4",getPoint(-4,13),3)
  ArchSiegeDefResisLe8 = Spec("Archer Siege Defense Resistance 5",getPoint(-4,14,(1-10.5/11)*x_center),3)
  ArchSiegeDefResisLe9 = Spec("Archer Siege Defense Resistance 6",getPoint(-4,15),3)
  ArchSiegeDefMightLe1 = Spec("Archer Siege Defence Might 1",getPoint(-4,2,-(1-10.5/11)*x_center),3)
  ArchSiegeDefMightLe2 = Spec("Archer Siege Defence Might 2",getPoint(-4,8,-(1-10.5/11)*x_center),3)
  ArchSiegeDefMightLe3 = Spec("Archer Siege Defence Might 3",getPoint(-4,14,-(1-10.5/11)*x_center),3)

  CavSiegeDefResisLe1 = Spec("Cavalry Siege Defense Resistance 1",getPoint(-4,3,(1-9/11)*x_center),3)
  CavSiegeDefResisLe2 = Spec("Cavalry Siege Defense Resistance 2",getPoint(-4,4,(1-8.5/11)*x_center),3)
  CavSiegeDefResisLe3 = Spec("Cavalry Siege Defense Resistance 3",getPoint(-4,6,(1-9/11)*x_center),3)
  CavSiegeDefResisLe4 = Spec("Cavalry Siege Defense Resistance 4",getPoint(-4,9,(1-8.5/11)*x_center),3)
  CavSiegeDefResisLe5 = Spec("Cavalry Siege Defense Resistance 5",getPoint(-4,10,(1-8/11)*x_center),3)
  CavSiegeDefResisLe6 = Spec("Cavalry Siege Defense Resistance 6",getPoint(-4,12,(1-8.5/11)*x_center),3)
  CavSiegeDefResisLe7 = Spec("Cavalry Siege Defense Resistance 7",getPoint(-4,13,(1-8.5/11)*x_center),3)
  CavSiegeDefResisLe8 = Spec("Cavalry Siege Defense Resistance 8",getPoint(-4,14,(1-8/11)*x_center),3)
  CavSiegeDefResisLe9 = Spec("Cavalry Siege Defense Resistance 9",getPoint(-4,15,(1-8.5/11)*x_center),3)
  CavSiegeDefMightLe1 = Spec("Cavalry Siege Defence Might 1",getPoint(-4,4,(1-9.5/11)*x_center),3)
  CavSiegeDefMightLe2 = Spec("Cavalry Siege Defence Might 2",getPoint(-4,10,(1-9/11)*x_center),3)
  CavSiegeDefMightLe3 = Spec("Cavalry Siege Defence Might 3",getPoint(-4,14,(1-9/11)*x_center),3)

  FooSiegeDefResisLe1 = Spec("Footmen Siege Defense Resistance 1",getPoint(-4,3,-(1-9/11)*x_center),3)
  FooSiegeDefResisLe2 = Spec("Footmen Siege Defense Resistance 2",getPoint(-4,4,-(1-8.5/11)*x_center),3)
  FooSiegeDefResisLe3 = Spec("Footmen Siege Defense Resistance 3",getPoint(-4,6,-(1-9/11)*x_center),3)
  FooSiegeDefResisLe4 = Spec("Footmen Siege Defense Resistance 4",getPoint(-4,9,-(1-8.5/11)*x_center),3)
  FooSiegeDefResisLe5 = Spec("Footmen Siege Defense Resistance 5",getPoint(-4,10,-(1-8/11)*x_center),3)
  FooSiegeDefResisLe6 = Spec("Footmen Siege Defense Resistance 6",getPoint(-4,12,-(1-8.5/11)*x_center),3)
  FooSiegeDefResisLe7 = Spec("Footmen Siege Defense Resistance 7",getPoint(-4,13,-(1-8.5/11)*x_center),3)
  FooSiegeDefResisLe8 = Spec("Footmen Siege Defense Resistance 8",getPoint(-4,14,-(1-8/11)*x_center),3)
  FooSiegeDefResisLe9 = Spec("Footmen Siege Defense Resistance 9",getPoint(-4,15,-(1-8.5/11)*x_center),3)
  FooSiegeDefMightLe1 = Spec("Footmen Siege Defence Might 1",getPoint(-4,4,-(1-9.5/11)*x_center),3)
  FooSiegeDefMightLe2 = Spec("Footmen Siege Defence Might 2",getPoint(-4,10,-(1-9/11)*x_center),3)
  FooSiegeDefMightLe3 = Spec("Footmen Siege Defence Might 3",getPoint(-4,14,-(1-9/11)*x_center),3)

  TotalDefence = Spec("Total Defence",getPoint(-4,6),5,True)
  ImperialFists = Spec("Imperial Fists",getPoint(-4,12),5,True)
  FightToTheDeath = Spec("Fight to the Death",getPoint(-4,16,(1-9/11)*x_center),5,True)
  UnBreachable = Spec("Un-Breachable",getPoint(-4,16,-(1-9/11)*x_center),5,True)
  SwitchARooney = Spec("switch-a-rooney",getPoint(-4,17),5,True)

  #Define Groups
  #UP
  ArchReignMightUpGroup = [ArchReignMightUp1, ArchReignMightUp2, ArchReignMightUp3, ChaosExpertise, ArchReignMightUp4, ArchReignMightUp5, ArchReignMightUp6, ChaosMaster, ArchReignMightUp7, ArchReignMightUp8, ArchReignMightUp9, PioneerBanner]
  ArchReignResisUpGroup = [ArchReignMightUp1, ArchReignResisUp1, ArchReignMightUp3, ChaosExpertise, ArchReignMightUp4, ArchReignResisUp2, ArchReignMightUp6, ChaosMaster, ArchReignMightUp7, ArchReignResisUp3, ArchReignMightUp9, RaiderBanner]
  CavReignMightUpGroup = [CavReignMightUp1, CavReignMightUp2, CavReignMightUp3, ChaosExpertise, CavReignMightUp4, CavReignMightUp5, CavReignMightUp6, ChaosMaster, CavReignMightUp7, CavReignMightUp8, CavReignMightUp9, PioneerBanner]
  CavReignResisUpGroup = [CavReignMightUp1, CavReignResisUp1, CavReignMightUp3, ChaosExpertise, CavReignMightUp4, CavReignResisUp2, CavReignMightUp6, ChaosMaster, CavReignMightUp7, CavReignResisUp3, CavReignMightUp9]
  FooReignMightUpGroup = [FooReignMightUp1, FooReignMightUp2, FooReignMightUp3, ChaosExpertise, FooReignMightUp4, FooReignMightUp5, FooReignMightUp6, ChaosMaster, FooReignMightUp7, FooReignMightUp8, FooReignMightUp9, RaiderBanner]
  FooReignResisUpGroup = [FooReignMightUp1, FooReignResisUp1, FooReignMightUp3, ChaosExpertise, FooReignMightUp4, FooReignResisUp2, FooReignMightUp6, ChaosMaster, FooReignMightUp7, FooReignResisUp3, FooReignMightUp9]
  
  BannerGroup = [PioneerBanner, RaiderBanner]
  CoalitionCommanderPGroup =[PioneerBanner, CoalitionCommander]
  CoalitionCommanderRGroup =[RaiderBanner, CoalitionCommander]
  #Right
  ArchSiegeMightRi = [ArchSiegeMightRi1, ArchSiegeMightRi2, ArchSiegeMightRi3, SiegeExpertise, ArchSiegeMightRi4, ArchSiegeMightRi5, ArchSiegeMightRi6, IronWarriors, ArchSiegeMightRi7, ArchSiegeMightRi8, ArchSiegeMightRi9, Invisibility]
  ArchSiegeResisRi = [ArchSiegeMightRi1, ArchSiegeResisRi1, ArchSiegeMightRi3, SiegeExpertise, ArchSiegeMightRi4, ArchSiegeResisRi2, ArchSiegeMightRi6, IronWarriors, ArchSiegeMightRi7, ArchSiegeResisRi3, ArchSiegeMightRi9, Taunt]
  CavSiegeMightRi = [CavSiegeMightRi1, CavSiegeMightRi2, CavSiegeMightRi3, SiegeExpertise, CavSiegeMightRi4, CavSiegeMightRi5, CavSiegeMightRi6, IronWarriors, CavSiegeMightRi7, CavSiegeMightRi8, CavSiegeMightRi9, Invisibility, Taunt]
  CavSiegeResisRi = [CavSiegeMightRi1, CavSiegeResisRi1, CavSiegeMightRi3, SiegeExpertise, CavSiegeMightRi4, CavSiegeResisRi2, CavSiegeMightRi6, IronWarriors, CavSiegeMightRi7, CavSiegeResisRi3, CavSiegeMightRi9]
  FooSiegeMightRi = [FooSiegeMightRi1, FooSiegeMightRi2, FooSiegeMightRi3, SiegeExpertise, FooSiegeMightRi4, FooSiegeMightRi5, FooSiegeMightRi6, IronWarriors, FooSiegeMightRi7, FooSiegeMightRi8, FooSiegeMightRi9, Taunt]
  FooSiegeResisRi = [FooSiegeMightRi1, FooSiegeResisRi1, FooSiegeMightRi3, SiegeExpertise, FooSiegeMightRi4, FooSiegeResisRi2, FooSiegeMightRi6, IronWarriors, FooSiegeMightRi7, FooSiegeResisRi3, FooSiegeMightRi9]

  ShoutTauntGroup = [Taunt, PrecisionShout]
  ShoutInvisGroup = [Invisibility, PrecisionShout]
  #Left
  ArchSiegeDefResLeGroup = [ArchSiegeDefResisLe1, ArchSiegeDefResisLe2, ArchSiegeDefResisLe3, TotalDefence, ArchSiegeDefResisLe4, ArchSiegeDefResisLe5, ArchSiegeDefResisLe6, ImperialFists, ArchSiegeDefResisLe7, ArchSiegeDefResisLe8, ArchSiegeDefResisLe9, FightToTheDeath, UnBreachable]
  ArchSiegeDefMightLeGroup = [ArchSiegeDefResisLe1, ArchSiegeDefMightLe1, ArchSiegeDefResisLe3, TotalDefence, ArchSiegeDefResisLe4, ArchSiegeDefMightLe2, ArchSiegeDefResisLe6, ImperialFists, ArchSiegeDefResisLe7, ArchSiegeDefMightLe3, ArchSiegeDefResisLe9, UnBreachable]
  CavSiegeDefResisLeGroup = [CavSiegeDefResisLe1, CavSiegeDefResisLe2, CavSiegeDefResisLe3, TotalDefence, CavSiegeDefResisLe4, CavSiegeDefResisLe5, CavSiegeDefResisLe6, ImperialFists, CavSiegeDefResisLe7, CavSiegeDefResisLe8, CavSiegeDefResisLe9, FightToTheDeath]
  CavSiegeDefMightLeGroup = [CavSiegeDefResisLe1, CavSiegeDefMightLe1, CavSiegeDefResisLe3, TotalDefence, CavSiegeDefResisLe4, CavSiegeDefMightLe2, CavSiegeDefResisLe6, ImperialFists, CavSiegeDefResisLe7, CavSiegeDefMightLe3, CavSiegeDefResisLe9]
  FooSiegeDefResisLeGroup = [FooSiegeDefResisLe1, FooSiegeDefResisLe2, FooSiegeDefResisLe3, TotalDefence, FooSiegeDefResisLe4, FooSiegeDefResisLe5, FooSiegeDefResisLe6, ImperialFists, FooSiegeDefResisLe7, FooSiegeDefResisLe8, FooSiegeDefResisLe9, UnBreachable]
  FooSiegeDefMightLeGroup = [FooSiegeDefResisLe1, FooSiegeDefMightLe1, FooSiegeDefResisLe3, TotalDefence, FooSiegeDefResisLe4, FooSiegeDefMightLe2, FooSiegeDefResisLe6, ImperialFists, FooSiegeDefResisLe7, FooSiegeDefMightLe3, FooSiegeDefResisLe9]
  FightRooneyGroup = [FightToTheDeath, SwitchARooney]
  UnBreachableRooneyGroup = [UnBreachable, SwitchARooney]

  #Groups
  groups = [
    #UP
    ArchReignMightUpGroup, BannerGroup, CoalitionCommanderPGroup, CoalitionCommanderRGroup, ArchReignResisUpGroup, CavReignMightUpGroup, CavReignResisUpGroup, FooReignMightUpGroup, FooReignResisUpGroup,
    #Right
    ArchSiegeMightRi, ArchSiegeResisRi, CavSiegeMightRi, CavSiegeResisRi, FooSiegeMightRi, FooSiegeResisRi, ShoutTauntGroup, ShoutInvisGroup,
    #Left
    ArchSiegeDefResLeGroup, ArchSiegeDefMightLeGroup, CavSiegeDefResisLeGroup, CavSiegeDefMightLeGroup, FooSiegeDefResisLeGroup, FooSiegeDefMightLeGroup, FightRooneyGroup, UnBreachableRooneyGroup
  ]

  #First Spec from Center
  firstSpecs = [
    #Up
    CavReignMightUp1, FooReignMightUp1, ArchReignMightUp1,
    #Right
    CavSiegeMightRi1, FooSiegeMightRi1, ArchSiegeMightRi1,
    #Left
    CavSiegeDefResisLe1, FooSiegeDefResisLe1, ArchSiegeDefResisLe1
  ]

  ##Dummy Fill Spec Points
  specPoints = 15
  assignPoints(ArchReignMightUpGroup)

  #Create the Image
  with Image.new("RGB",(x,y),color = (255,255,255)) as im:
    draw = ImageDraw.Draw(im)
    #Draw the connections
    for fiSpec in firstSpecs:
      draw.line(
            [(x_center, y_center), fiSpec.center],
            fill = grey,
            width = 3
          )
      fiSpec.activatable = True
    #Loop groups 
    for group in groups:
      start = None
      #Loop specs in group
      for s in group:
        #draw connecting line
        if start != None:
          draw.line(
            [start, s.center],
            fill = grey,
            width = 3
          )
          pass
        start = s.center

    #Draw the Center
    draw.ellipse(
      [x_center-30,
       y_center-30,
       x_center+30,
       y_center+30],
      outline = red,
      fill = red,
      width=3
    )

    #Draw Specs
    #Loop groups 
    for group in groups:
      start = None
      precondition = False
      #Loop specs in group
      for s in group:
        if precondition:
          s.activatable = True
        fill_color = white
        if s.currentLvl  == s.maxLvl:
          fill_color = red
        elif s.currentLvl > 0:
          fill_color = red_1
        #Define the size of the circle
        if s.bigCircle:
          size = 18
        else: 
          size = 12
        tl = (s.center[0]-size,s.center[1]-size)
        br = (s.center[0]+size,s.center[1]+size)
        #draw the circle
        draw.ellipse(
          [tl,br],
          outline = red,
          fill=fill_color,
          width=2
        )
        text = str(s.currentLvl) if s.currentLvl < s.maxLvl else str(s.maxLvl)
        if text == "0" and not(s.activatable):
          text = ""
        fill = grey if s.currentLvl == 0 else white
        draw.text(s.center, text=text, fill=fill, font=font,anchor="mm")

        if s.currentLvl == s.maxLvl:
          precondition = True
        else:
          precondition = False
          
      
    im.save("redSpec.png")
  
  return


  