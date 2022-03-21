from functions.drawSpecFunc import Spec, getPoint_bl, x_center, y_center

bl = (70,175,225)
bl_l = (165,200,220)

radiusDict_bl = {
  1:int((1-9.6/11)*y_center),
  2:int((1-8.9/11)*y_center),
  3:int((1-8.2/11)*y_center),
  4:int((1-7.4/11)*y_center),
  5:int((1-6.6/11)*y_center),
  6:int((1-5.9/11)*y_center),
  7:int((1-5.1/11)*y_center),
  8:int((1-4.3/11)*y_center),
  9:int((1-3.6/11)*y_center),
  10:int((1-2.8/11)*y_center),
  11:int((1-2.0/11)*y_center),
  12:int((1-1.3/11)*y_center),
  13:int((1-0.5/11)*y_center),
}
#specPoints = specB
#Define all specs
#UP
DemoUp1 = Spec("Demolition 1",getPoint_bl(12,1),3)
DemoUp1.activatable = True
DemoUp2 = Spec("Demolition 2",getPoint_bl(12,2),3)
DemoUp3 = Spec("Demolition 3",getPoint_bl(12,3),3)
DemoUp4 = Spec("Demolition 4",getPoint_bl(12,5),3)
DemoUp5 = Spec("Demolition 5",getPoint_bl(12,6),3)
DemoUp6 = Spec("Demolition 6",getPoint_bl(12,8),3)
DemoUp7 = Spec("Demolition 7",getPoint_bl(12,9),3)
DemoUp8 = Spec("Demolition 8",getPoint_bl(12,11),3)
DemoUp9 = Spec("Demolition 9",getPoint_bl(12,12),3)
InstRe = Spec("Instant Recall", getPoint_bl(12,4),5,True)
InstaReCoUpl1 = Spec("Instant recall cost 1 ",getPoint_bl(12,5,-(1-10/11)*x_center),3)
InstaReCoUpl2 = Spec("Instant recall cost 2",getPoint_bl(12,6,-(1-10/11)*x_center),3)
InstaReCoUpr3 = Spec("Instant recall cost 3",getPoint_bl(12,5,(1-10/11)*x_center),3)
InstaReCoUpr4 = Spec("Instant recall cost 4",getPoint_bl(12,6,(1-10/11)*x_center),3)
TruceProtect = Spec("Honor Structure Protection", getPoint_bl(12,7),5,True)
TruceDur1 = Spec("Truce Duration 1",getPoint_bl(12,8,-(1-10/11)*x_center),3)
TruceDur2 = Spec("Truce Duration 2",getPoint_bl(12,9,-(1-10/11)*x_center),3)
TrucePrep1 = Spec("Truce Prep 1",getPoint_bl(12,8,(1-10/11)*x_center),3)
TrucePrep2 = Spec("Truce Prep 2",getPoint_bl(12,9,(1-10/11)*x_center),3)
DemoSkill = Spec("Demolition bonus skill",getPoint_bl(12,10),5,True)
  
DemoEff1 = Spec("Demolition Effect 1",getPoint_bl(12,11,-(1-10/11)*x_center),3)
DemoEff2 = Spec("TDemolition Effect  2",getPoint_bl(12,12,-(1-10/11)*x_center),3)
DemoPrep1 = Spec("Demolition Prep 1",getPoint_bl(12,11,(1-10/11)*x_center),3)
DemoPrep2 = Spec("TDemolition Prep  2",getPoint_bl(12,12,(1-10/11)*x_center),3)
SiegeHammer = Spec("Extra durability damage skill",getPoint_bl(12,13),5,True)

#LEFT
Process1 = Spec("Processing Speed 1",getPoint_bl(18,1),3)
Process1.activatable = True
Process2 = Spec("Processing Speed 2",getPoint_bl(18,2,(1-10/11)*x_center),3)
Process3 = Spec("Processing Speed 3",getPoint_bl(18,3,(1-10/11)*x_center),3)
Process4 = Spec("Processing Speed 4",getPoint_bl(18,5,(1-10/11)*x_center),3)
Process5 = Spec("Processing Speed 5",getPoint_bl(18,6,(1-10/11)*x_center),3)
Process6 = Spec("Processing Speed 6",getPoint_bl(18,8,(1-10/11)*x_center),3)
Process7 = Spec("Processing Speed 7",getPoint_bl(18,9,(1-10/11)*x_center),3)
Process8 = Spec("Processing Speed 8",getPoint_bl(18,11,(1-10/11)*x_center),3)
Process9 = Spec("Processing Speed 9",getPoint_bl(18,12,(1-10/11)*x_center),3)


Capacity1 = Spec("Capacity 1",getPoint_bl(18,2,-(1-10/11)*x_center),3)
Capacity2 = Spec("Capacity 2",getPoint_bl(18,3,-(1-10/11)*x_center),3)
Capacity3 = Spec("Capacity 3",getPoint_bl(18,5,-(1-10/11)*x_center),3)
Capacity4 = Spec("Capacity 4",getPoint_bl(18,6,-(1-10/11)*x_center),3)
Capacity5 = Spec("Capacity 5",getPoint_bl(18,8,-(1-10/11)*x_center),3)
Capacity6 = Spec("Capacity 6",getPoint_bl(18,9,-(1-10/11)*x_center),3)
Capacity7 = Spec("Capacity 7",getPoint_bl(18,11,-(1-10/11)*x_center),3)
Capacity8 = Spec("Capacity 8",getPoint_bl(18,12,-(1-10/11)*x_center),3)

ExtraQ1 = Spec("Processing Queue 1",getPoint_bl(18,4),1,True)
ExtraQ2 = Spec("Processing Queue 2",getPoint_bl(18,7),1,True)
ExtraQ3 = Spec("Processing Queue 3",getPoint_bl(18,10),1,True)
ExtraQ4 = Spec("Processing Queue 4",getPoint_bl(18,13),1,True)
ExtraQ1.activatable = True
ExtraQ2.activatable = True
ExtraQ3.activatable = True
ExtraQ4.activatable = True

#RIGHT
HealSp1 = Spec("Healing Speed 1",getPoint_bl(6,1),3)
HealSp1.activatable = True
HealSp2 = Spec("Healing Speed 2",getPoint_bl(6,2,(1-10/11)*x_center),3)
HealSp3 = Spec("Healing Speed 3",getPoint_bl(6,3,(1-10/11)*x_center),3)
HealSp4 = Spec("Healing Speed 4",getPoint_bl(6,5,(1-10/11)*x_center),3)
HealSp5 = Spec("Healing Speed 5",getPoint_bl(6,6,(1-10/11)*x_center),3)
HealSp6 = Spec("Healing Speed 6",getPoint_bl(6,8,(1-10/11)*x_center),3)
HealSp7 = Spec("Healing Speed 7",getPoint_bl(6,9,(1-10/11)*x_center),3)
HealSp8 = Spec("Healing Speed 8",getPoint_bl(6,11,(1-10/11)*x_center),3)
HealSp9 = Spec("Healing Speed 9",getPoint_bl(6,12,(1-10/11)*x_center),3)


HealCo1 = Spec("Healing Cost 1",getPoint_bl(6,2,-(1-10/11)*x_center),3)
HealCo2 = Spec("Healing Cost 2",getPoint_bl(6,3,-(1-10/11)*x_center),3)
HealCo3 = Spec("Healing Cost 3",getPoint_bl(6,5,-(1-10/11)*x_center),3)
HealCo4 = Spec("Healing Cost 4",getPoint_bl(6,6,-(1-10/11)*x_center),3)
HealCo5 = Spec("Healing Cost 5",getPoint_bl(6,8,-(1-10/11)*x_center),3)
HealCo6 = Spec("Healing Cost 6",getPoint_bl(6,9,-(1-10/11)*x_center),3)
HealCo7 = Spec("Healing Cost 7",getPoint_bl(6,11,-(1-10/11)*x_center),3)
HealCo8 = Spec("Healing Cost 8",getPoint_bl(6,12,-(1-10/11)*x_center),3)

Loyalty1 = Spec("Loyalty 1",getPoint_bl(6,4),5,True)
Loyalty2 = Spec("Loyalty 2",getPoint_bl(6,7),5,True)
Loyalty3 = Spec("Loyalty 3",getPoint_bl(6,10),5,True)
Loyalty4 = Spec("Loyalty 4",getPoint_bl(6,13),5,True)
Loyalty1.activatable = True
Loyalty2.activatable = True
Loyalty3.activatable = True
Loyalty4.activatable = True
#DOWN

BuildSp1 = Spec("Healing Cost 2",getPoint_bl(0,2,(1-10/11)*x_center),3)

BuildSp2 = Spec("Healing Cost 3",getPoint_bl(0,3,(1-10/11)*x_center),3)
BuildSp3 = Spec("Healing Cost 4",getPoint_bl(0,5,(1-10/11)*x_center),3)
BuildSp4 = Spec("Healing Cost 5",getPoint_bl(0,6,(1-10/11)*x_center),3)
BuildSp5 = Spec("Healing Cost 6",getPoint_bl(0,8,(1-10/11)*x_center),3)
BuildSp6 = Spec("Healing Cost 7",getPoint_bl(0,9,(1-10/11)*x_center),3)
BuildSp7 = Spec("Healing Cost 8",getPoint_bl(0,11,(1-10/11)*x_center),3)
BuildSp8 = Spec("Healing Cost 9",getPoint_bl(0,12,(1-10/11)*x_center),3)

BuildDur1 = Spec("Building Durability 1",getPoint_bl(0,1),3)
BuildDur1.activatable = True
BuildDur2 = Spec("Building Durability 2",getPoint_bl(0,2,-(1-10/11)*x_center),3)
BuildDur3= Spec("Building Durability 3",getPoint_bl(0,3,-(1-10/11)*x_center),3)
BuildDur4 = Spec("Building Durability 4",getPoint_bl(0,5,-(1-10/11)*x_center),3)
BuildDur5 = Spec("Building Durability 5",getPoint_bl(0,6,-(1-10/11)*x_center),3)
BuildDur6 = Spec("Building Durability 6",getPoint_bl(0,8,-(1-10/11)*x_center),3)
BuildDur7 = Spec("Building Durability 7",getPoint_bl(0,9,-(1-10/11)*x_center),3)
BuildDur8 = Spec("Building Durability 8",getPoint_bl(0,11,-(1-10/11)*x_center),3)
BuildDur9 = Spec("Building Durability 9",getPoint_bl(0,12,-(1-10/11)*x_center),3)

Fortress1 = Spec("Fortress 1",getPoint_bl(0,4),1,True)
Fortress2 = Spec("Fortress 2",getPoint_bl(0,7),1,True)
Fortress3 = Spec("Fortress 3",getPoint_bl(0,10),1,True)
Fortress4 = Spec("Fortress 4",getPoint_bl(0,13),1,True)

#Define Groups
#UP
DemoGroup = [DemoUp1, DemoUp2, DemoUp3, InstRe, DemoUp4, DemoUp5, TruceProtect, DemoUp6, DemoUp7, DemoSkill, DemoUp8,DemoUp9, SiegeHammer ]
InstaReCoRGroup = [InstRe, InstaReCoUpr3, InstaReCoUpr4, TruceProtect]
InstaReCoLGroup = [InstRe, InstaReCoUpl1, InstaReCoUpl2, TruceProtect]
TruceDurGroup = [TruceProtect, TruceDur1, TruceDur2, DemoSkill]
TrucePrepGroup = [TruceProtect, TrucePrep1, TrucePrep2, DemoSkill]
DemoEffGroup = [DemoSkill, DemoEff1, DemoEff2, SiegeHammer]
DemoPrepGroup = [DemoSkill, DemoPrep1, DemoPrep2, SiegeHammer]
#LEFT
ProcessGroup = [Process1, Process2, Process3, ExtraQ1, Process4, Process5, ExtraQ2, Process6, Process7, ExtraQ3, Process8, Process9, ExtraQ4 ]
CapacityGroup = [Process1, Capacity1, Capacity2, ExtraQ1, Capacity3, Capacity4, ExtraQ2, Capacity5, Capacity6, ExtraQ3, Capacity7, Capacity8, ExtraQ4 ]

#RIGHT
LoyaltyCostGroup = [HealSp1, HealCo1, HealCo2, Loyalty1, HealCo3, HealCo4, Loyalty2, HealCo5, HealCo6, Loyalty3, HealCo7, HealCo8, Loyalty4 ]
LoyaltySpeedGroup = [HealSp1, HealSp2, HealSp3, Loyalty1, HealSp4, HealSp5, Loyalty2, HealSp6, HealSp7, Loyalty3, HealSp8, HealSp9, Loyalty4 ]
#DOWN
BuildingSpeedGroup = [BuildDur1, BuildSp1, BuildSp2, Fortress1, BuildSp3, BuildSp4, Fortress2, BuildSp5, BuildSp6, Fortress3, BuildSp7, BuildSp8, Fortress4]

BuildingDurGroup = [BuildDur1, BuildDur2, BuildDur3, Fortress1, BuildDur4, BuildDur5, Fortress2, BuildDur6, BuildDur7, Fortress3, BuildDur8, BuildDur9, Fortress4]

groups_bl = [
#UP
DemoGroup, InstaReCoRGroup, InstaReCoLGroup, TruceDurGroup, TrucePrepGroup, DemoEffGroup, DemoPrepGroup,
#LEFT
ProcessGroup, CapacityGroup,
#RIGHT
LoyaltyCostGroup, LoyaltySpeedGroup,
#DOWN
BuildingSpeedGroup, BuildingDurGroup
]

#additiona groups for assigning spec points
OneExtQ = [Process1, Process2, Process3, ExtraQ1]
TwoExtQs = [Process1, Process2, Process3, ExtraQ1, Process4, Process5, ExtraQ2]
MaxQs = [Process1, Process2, Process3, ExtraQ1, Process4, Process5, ExtraQ2, Process6, Process7, ExtraQ3]

blueSpec_gr = {
  "OneExtQ":(OneExtQ, 10), 
  "TwoExtQs":(TwoExtQs, 17),
  "MaxQs":(MaxQs, 31), 
  "LoyaltySpeedGroup":(LoyaltySpeedGroup, 47)
  }

#First Spec from Center
firstSpecs = [
    
    BuildDur1, HealSp1, Process1, DemoUp1
  ]