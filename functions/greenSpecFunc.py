from functions.drawSpecFunc import  getPoint_gr, x_center, y_center
from classes.Spec import Spec
#define different radius


#isn't used at the moment
radiusDict_gr_old = {
1:int((1-9.5/11)*y_center),
2:int((1-8.5/11)*y_center),
3:int((1-7.5/11)*y_center),
4:int((1-6/11)*y_center),
5:int((1-4.5/11)*y_center),
6:int((1-3/11)*y_center),
7:int((1-2/11)*y_center),
8:int((1-1/11)*y_center),
9:int((1-0/11)*y_center),
10:int((1+1/11)*y_center),

}

#defines green and green light
gr = (50,188,50)
gr_l = (160,188,160)


#Define all specs
#UP
CombatExUp1 = Spec("Combat Experience 1",getPoint_gr(12,1),3)
CombatExUp1.activatable = True
CombatExUp2 = Spec("Combat Experience 2",getPoint_gr(12,2),3)
CombatExUp3 = Spec("Combat Experience 3",getPoint_gr(12,3),3)
CombatExUp4 = Spec("Combat Experience 4",getPoint_gr(12,5),3)
AgricuTeUp1 = Spec("Agricultural Technology 1",getPoint_gr(12,2,-(1-10/11)*x_center),3)
AgricuTeUp2 = Spec("Agricultural Technology 2",getPoint_gr(12,3,-(1-10/11)*x_center),3)
AgricuTeUp3 = Spec("Agricultural Technology 3",getPoint_gr(12,5,-(1-10/11)*x_center),3)
MiningTeUp1 = Spec("Mining Technology 1",getPoint_gr(12,2,(1-10/11)*x_center),3)
MiningTeUp2 = Spec("Mining Technology 2",getPoint_gr(12,3,(1-10/11)*x_center),3)
MiningTeUp3 = Spec("Mining Technology 3",getPoint_gr(12,5,(1-10/11)*x_center),3)
Training = Spec("Training",getPoint_gr(12,4),5,True)
ResourCella = Spec("Resource Cellar",getPoint_gr(12),5,True)
CombatExLe1 = Spec("Combat Experience 5L",getPoint_gr(-11),3)
CombatExLe2 = Spec("Combat Experience 6L",getPoint_gr(-10),3)
CombatExLe3 = Spec("Combat Experience 7L",getPoint_gr(-9),3)
CombatExRi1 = Spec("Combat Experience 5R",getPoint_gr(11),3)
CombatExRi2 = Spec("Combat Experience 6R",getPoint_gr(10),3)
CombatExRi3 = Spec("Combat Experience 7R",getPoint_gr(9),3)
TerritCapaL = Spec("Territory Capacity L",getPoint_gr(-8),5,True)
TerritCapaR = Spec("Territory Capacity R",getPoint_gr(8),5,True)
TerritCapaL.activatable = True
TerritCapaR.activatable = True
#RIGHT
BattleHoRi1 = Spec("Battle Honors 1",getPoint_gr(4,1),3)
BattleHoRi1.activatable = True
BattleHoRi2 = Spec("Battle Honors 2",getPoint_gr(4,2),3)
BattleHoRi3 = Spec("Battle Honors 3",getPoint_gr(4,3),3)
BattleHoRi4 = Spec("Battle Honors 4",getPoint_gr(4,5),3)
BuildiNaRi1 = Spec("Building Navigation 1",getPoint_gr(4,2,-(1-10/11)*x_center),3)
BuildiNaRi2 = Spec("Building Navigation 2",getPoint_gr(4,3,-(1-10/11)*x_center),3)
BuildiNaRi3 = Spec("Building Navigation 3",getPoint_gr(4,5,-(1-10/11)*x_center),3)
FieldCarRi1 = Spec("Field Cartography 1",getPoint_gr(4,2,(1-10/11)*x_center),3)
FieldCarRi2 = Spec("Field Cartography 2",getPoint_gr(4,3,(1-10/11)*x_center),3)
FieldCarRi3 = Spec("Field Cartography 3",getPoint_gr(4,5,(1-10/11)*x_center),3)
TimeReduRi1 = Spec("Time Reduction 1",getPoint_gr(4,7,(1-10/11)*x_center),3)
TimeReduRi2 = Spec("Time Reduction 2",getPoint_gr(4,8,(1-9.5/11)*x_center),3)
TimeReduRi3 = Spec("Time Reduction 3",getPoint_gr(4,9,(1-10/11)*x_center),3)
CostReduRi1 = Spec("Cost Reduction 1",getPoint_gr(4,7,-(1-10/11)*x_center),3)
CostReduRi2 = Spec("Cost Reduction 2",getPoint_gr(4,8,-(1-9.5/11)*x_center),3)
CostReduRi3 = Spec("Cost Reduction 3",getPoint_gr(4,9,-(1-10/11)*x_center),3)
LandReclama = Spec("Land Reclamation",getPoint_gr(4,4),5,True)
LandDevelo1 = Spec("Land Development 1",getPoint_gr(4),5,True)
LandDevelo2 = Spec("Land Development 2",getPoint_gr(4,10),4,True)
LandDevelo2.activatable = True
BattleHoUp1 = Spec("Battle Honor 5U",getPoint_gr(5),3)
BattleHoUp2 = Spec("Battle Honor 6U",getPoint_gr(6),3)
BattleHoUp3 = Spec("Battle Honor 7U",getPoint_gr(7),3)
BattleHoDo1 = Spec("Battle Honor 5D",getPoint_gr(3),3)
BattleHoDo2 = Spec("Battle Honor 6D",getPoint_gr(2),3)
BattleHoDo3 = Spec("Battle Honor 7D",getPoint_gr(1),3)
TerritCapaD = Spec("Territory Capacity D",getPoint_gr(0),5,True)
TerritCapaD.activatable = True
#LEFT
ContruHoLe1 = Spec("Construction Honors 1",getPoint_gr(-4,1),3)
ContruHoLe1.activatable = True
ContruHoLe2 = Spec("Construction Honors 2",getPoint_gr(-4,2),3)
ContruHoLe3 = Spec("Construction Honors 3",getPoint_gr(-4,3),3)
ContruHoLe4 = Spec("Construction Honors 4",getPoint_gr(-4,5),3)
ResourCoLe1 = Spec("Resource Conservation 1",getPoint_gr(-4,2,(1-10/11)*x_center),3)
ResourCoLe2 = Spec("Resource Conservation 2",getPoint_gr(-4,3,(1-10/11)*x_center),3)
ResourCoLe3 = Spec("Resource Conservation 3",getPoint_gr(-4,5,(1-10/11)*x_center),3)
ComposPrLe1 = Spec("Composite process 1",getPoint_gr(-4,2,-(1-10/11)*x_center),3)
ComposPrLe2 = Spec("Composite process 2",getPoint_gr(-4,3,-(1-10/11)*x_center),3)
ComposPrLe3 = Spec("Composite process 3",getPoint_gr(-4,5,-(1-10/11)*x_center),3)
CivilEngine = Spec("Civil Engineering",getPoint_gr(-4,4),5,True)
CivilEngine.activatable = True
HonorAward = Spec("Honor Award",getPoint_gr(-4),5,True)
HonorAward.activatable = True
ContruHoUp1 = Spec("Construction Honor 5U",getPoint_gr(-5),3)
ContruHoUp2 = Spec("Construction Honor 6U",getPoint_gr(-6),3)
ContruHoUp3 = Spec("Construction Honor 7U",getPoint_gr(-7),3)
ContruHoDo1 = Spec("Construction Honor 5U",getPoint_gr(-3),3)
ContruHoDo2 = Spec("Construction Honor 6U",getPoint_gr(-2),3)
ContruHoDo3 = Spec("Construction Honor 7U",getPoint_gr(-1),3)

#group Specs
#UP
CombatExUpGroup = [CombatExUp1, CombatExUp2, CombatExUp3, Training, CombatExUp4, ResourCella]
AgricuTeUpGroup = [CombatExUp1, AgricuTeUp1, AgricuTeUp2, Training, AgricuTeUp3, ResourCella]
MiningTeUpGroup = [CombatExUp1, MiningTeUp1, MiningTeUp2, Training, MiningTeUp3, ResourCella]
TerritCapaLGroup = [ResourCella, CombatExLe1, CombatExLe2, CombatExLe3, TerritCapaL]
TerritCapaRGroup = [ResourCella, CombatExRi1, CombatExRi2, CombatExRi3, TerritCapaR]
#RIGHT
BattleHoRiGroup = [BattleHoRi1, BattleHoRi2, BattleHoRi3, LandReclama, BattleHoRi4, LandDevelo1]
BuildiNaRiGroup = [BattleHoRi1, BuildiNaRi1, BuildiNaRi2, LandReclama, BuildiNaRi3, LandDevelo1]
FieldCarRiGroup = [BattleHoRi1, FieldCarRi1, FieldCarRi2, LandReclama, FieldCarRi3, LandDevelo1]
LandDeveloGroup = [LandDevelo1, LandDevelo2]
TimeReduRiGroup = [LandDevelo1, TimeReduRi1, TimeReduRi2, TimeReduRi3, LandDevelo2]
CostReduRiGroup = [LandDevelo1, CostReduRi1, CostReduRi2, CostReduRi3, LandDevelo2]
BattleHoUpGroup = [LandDevelo1, BattleHoUp1, BattleHoUp2, BattleHoUp3, TerritCapaR]
BattleHoDoGroup = [LandDevelo1, BattleHoDo1, BattleHoDo2, BattleHoDo3, TerritCapaD]
#LEFT
ContruHoLeGroup = [ContruHoLe1, ContruHoLe2, ContruHoLe3, CivilEngine, ContruHoLe4, HonorAward]
ResourCoLeGroup = [ContruHoLe1, ResourCoLe1, ResourCoLe2, CivilEngine, ResourCoLe3, HonorAward]
ComposPrLeGroup = [ContruHoLe1, ComposPrLe1, ComposPrLe2, CivilEngine, ComposPrLe3, HonorAward]
ContruHoUpGroup = [HonorAward, ContruHoUp1, ContruHoUp2, ContruHoUp3, TerritCapaL]
ContruHoDoGroup = [HonorAward, ContruHoDo1, ContruHoDo2, ContruHoDo3, TerritCapaD]

#groups
groups_gr = [
#UP
CombatExUpGroup, AgricuTeUpGroup, MiningTeUpGroup, TerritCapaLGroup, TerritCapaRGroup,
#Right
BattleHoRiGroup, BuildiNaRiGroup, FieldCarRiGroup, LandDeveloGroup, TimeReduRiGroup, CostReduRiGroup, BattleHoUpGroup, BattleHoDoGroup,
#Left
ContruHoLeGroup, ResourCoLeGroup, ComposPrLeGroup, ContruHoUpGroup, ContruHoDoGroup
]

#additional groups for assigning spec points
TileSpeed = [BattleHoRi1, FieldCarRi1, FieldCarRi2, LandReclama, FieldCarRi3]
UpgradeBuild = [ContruHoLe1, ContruHoLe2, ContruHoLe3, CivilEngine, ContruHoLe4, HonorAward,  ComposPrLe1, ComposPrLe2, ComposPrLe3, ContruHoUp1, ContruHoUp2, ContruHoUp3,ContruHoDo1, ContruHoDo2, ContruHoDo3]
BuildExTile = [TerritCapaL,TerritCapaD]
TileHonour = [BattleHoRi1, BattleHoRi2, BattleHoRi3, LandReclama, BattleHoRi4, LandDevelo1, BattleHoUp1, BattleHoUp2, BattleHoUp3, BattleHoDo1, BattleHoDo2, BattleHoDo3]
TileHoExTile = [TerritCapaR, TerritCapaD]
CBCMat = [CombatExUp1, AgricuTeUp1, AgricuTeUp2, Training, AgricuTeUp3]
FWMat = [CombatExUp1, MiningTeUp1, MiningTeUp2, Training, MiningTeUp3]
LandTS = [BattleHoRi1, FieldCarRi1, FieldCarRi2, LandReclama, FieldCarRi3, LandDevelo1, LandDevelo2]
LandTH = [BattleHoRi1, BattleHoRi2, BattleHoRi3, LandReclama, BattleHoRi4, LandDevelo1, LandDevelo2]

#groups for where there are multiple options

ExtraTileLHon = [ContruHoLe1, ContruHoLe2, ContruHoLe3, CivilEngine, ContruHoLe4, HonorAward, ContruHoUp1, ContruHoUp2, ContruHoUp3, TerritCapaL]
ExtraTileLCBC = [CombatExUp1, AgricuTeUp1, AgricuTeUp2, Training, AgricuTeUp3, ResourCella, CombatExLe1, CombatExLe2, CombatExLe3, TerritCapaL]
ExtraTileLFW = [CombatExUp1, MiningTeUp1, MiningTeUp2, Training, MiningTeUp3, ResourCella, CombatExLe1, CombatExLe2, CombatExLe3, TerritCapaL]
ExtraTileRCBC = [CombatExUp1, AgricuTeUp1, AgricuTeUp2, Training, AgricuTeUp3, ResourCella, CombatExRi1, CombatExRi2, CombatExRi3, TerritCapaR]
ExtraTileRFW = [CombatExUp1, MiningTeUp1, MiningTeUp2, Training, MiningTeUp3, ResourCella, CombatExRi1, CombatExRi2, CombatExRi3, TerritCapaR]

ExtraTileRTS = [BattleHoRi1, FieldCarRi1, FieldCarRi2, LandReclama, FieldCarRi3, LandDevelo1, BattleHoUp1, BattleHoUp2, BattleHoUp3, TerritCapaR]

ExtraTileRTH = [BattleHoRi1, BattleHoRi2, BattleHoRi3, LandReclama, BattleHoRi4, LandDevelo1, BattleHoUp1, BattleHoUp2, BattleHoUp3, TerritCapaR]
ExtraTileDTS = [BattleHoRi1, FieldCarRi1, FieldCarRi2, LandReclama, FieldCarRi3,LandDevelo1, BattleHoDo1, BattleHoDo2, BattleHoDo3, TerritCapaD]
ExtraTileDTH = [BattleHoRi1, BattleHoRi2, BattleHoRi3, LandReclama, BattleHoRi4, LandDevelo1,BattleHoDo1, BattleHoDo2, BattleHoDo3, TerritCapaD]
ExtraTileDHon = [ContruHoLe1, ContruHoLe2, ContruHoLe3, CivilEngine, ContruHoLe4, HonorAward, ContruHoDo1, ContruHoDo2, ContruHoDo3, TerritCapaD]



#points for each group
#issue BuildExTile and TileHoExTile use some Node
greenSpec_gr = {
  "UpgradeBuild":(UpgradeBuild, 49), 
  "TileSpeed":(TileSpeed, 17),
  "BuildExTile":(BuildExTile, 10), 
  "TileHonour":(TileHonour, 49),
  "TileHoExTile":(TileHoExTile, 10),
  "CBCMat":(CBCMat, 17),
  "FWMat":(FWMat, 17),
  "MatExTileL":(TerritCapaLGroup,19),
  "MatExTileR":(TerritCapaRGroup,19),
  "LandTS":(LandTS,0),
  "LandTH":(LandTH,0),
  "ExtraTileLHon": (ExtraTileLHon, 0),
  "ExtraTileLCBC": (ExtraTileLCBC, 0),
  "ExtraTileLFW":(ExtraTileLFW , 0),
  "ExtraTileRCBC":(ExtraTileRCBC, 0),
  "ExtraTileRFW":(ExtraTileRFW , 0),
  "ExtraTileRTS":(ExtraTileRTS , 0),
  "ExtraTileRTH":(ExtraTileRTH , 0),
  "ExtraTileDTS": (ExtraTileDTS , 0),
  "ExtraTileDTH": (ExtraTileDTH ,0),
  "ExtraTileDHon": (ExtraTileDHon ,0)

 
  }


#First Spec from Center
firstSpecs_gr = [
    
    BattleHoRi1, ContruHoLe1, CombatExUp1
  ]