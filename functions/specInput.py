from classes.Spec import specInfo
from functions.assignSpecFunc import specAdvice
from functions.blueSpecFunc import *
from functions.greenSpecFunc import *
from functions.redSpecFunc import *

async def specInput(channel, view):
    specinfo = specInfo()

    #if view.specinfo.preset == 
    if view.specinfo.loyalty == 'NO':
    
      notes = "Your focus is upgrading CBCs, so you should have 90% food and marble tiles. Depending on the number of resets you have, you will occasionally switch to green left to upgrade Frontline Workshops.\n \n"
      list1 = ('LoyaltySpeedGroup', 'CBCMat', 'OneExtQ')
      list2 = ('ExtraTile', 'TileHonour', 'UpgradeBuild')
    elif view.specinfo.fulliw == 'NO':
     
      notes = "Your focus is getting high level wood and iron tiles. You may wish to keep a few CBC material tiles if you wish to increase loyalty. You can always take more iron/wood and upgrade later using land development.\n\nIf you think you will fill up on iron/wood before next specialisation reset, ask in alliance chat for advice.\n\n"
      list1 = ('LoyaltySpeedGroup', 'FWMat', 'OneExtQ')
      list2 = ('ExtraTile', 'TileHonour', 'TwoExtQs')
    elif view.specinfo.fwmax == 'NO':
      notes = "Your focus is on upgrading your Frontline Workshops and getting the maximum honour bonus from these upgrades.\n\n"
      list1 = ('UpgradeBuild', 'FWMat', 'OneExtQ')
      list2 = ('ExtraTile', 'TileHonour', 'TwoExtQs', 'Land')
    else:
      notes = "Your focus is on maximising honour from tiles. You will sometimes switch to green left and extra queues to upgrade Assault and Guardian Fortresses.\n\nIn the last week, you may need to put extra points on processing queues to ensure that you process all of your materials.  Depending on resets you may also prioritise having 49 points on green left (building honour).  Land development and extra tiles might not be necessary.\n.\n"
      list1 = ('TileHonour', 'FWMat', 'ExtraTile')
      list2 = ('UpgradeBuild', 'TwoExtQs', 'Land')

      #run spec advice
    spec = 120
    try:
      specAdvice(specinfo.banner,list1, list2, spec, groups_bl, groups_gr)
      
    #send advice
      await channel.send(content =notes)
      if specInfo.language != 'en':
        notes_trans = GoogleTranslator(source='auto', target=target_lang).translate(text=notes)
        await channel.send(content =notes_trans) 
      await channel.send(file=File('blueSpec.png'))
      await channel.send(file=File('greenSpec.png'))
      await channel.send(file=File('redSpec.png'))
    except:
      await channel.send(content = "Oops, something went wrong")

('Loyalty', 'FillIW', 'Upgrade buildings', 'Tile Honour')
async def presetInput(channel, view):
    specinfo = specInfo()
    
    #if view.specinfo.preset == 
    if view.specinfo.preset == 'Loyalty':
    
      notes = "Your focus is upgrading CBCs, so you should have 90% food and marble tiles. Depending on the number of resets you have, you will occasionally switch to green left to upgrade Frontline Workshops.\n \n"
      list1 = ('LoyaltySpeedGroup', 'CBCMat', 'OneExtQ')
      list2 = ('ExtraTile', 'TileHonour', 'UpgradeBuild')
    
    elif view.specinfo.preset == 'FillIW':
     
      notes = "Your focus is getting high level wood and iron tiles. You may wish to keep a few CBC material tiles if you wish to increase loyalty. You can always take more iron/wood and upgrade later using land development.\n\nIf you think you will fill up on iron/wood before next specialisation reset, ask in alliance chat for advice.\n\n"
      list1 = ('LoyaltySpeedGroup', 'FWMat', 'OneExtQ')
      list2 = ('ExtraTile', 'TileHonour', 'TwoExtQs')
    elif view.specinfo.preset == 'Upgrade buildings':
      notes = "Your focus is on upgrading your Frontline Workshops and getting the maximum honour bonus from these upgrades.\n\n"
      list1 = ('UpgradeBuild', 'FWMat', 'OneExtQ')
      list2 = ('ExtraTile', 'TileHonour', 'TwoExtQs', 'Land')
    elif view.specinfo.preset == 'Tile Honour':
      notes = "Your focus is on maximising honour from tiles. You will sometimes switch to green left and extra queues to upgrade Assault and Guardian Fortresses.\n\nIn the last week, you may need to put extra points on processing queues to ensure that you process all of your materials.  Depending on resets you may also prioritise having 49 points on green left (building honour).  Land development and extra tiles might not be necessary.\n.\n"
      list1 = ('TileHonour', 'FWMat', 'ExtraTile')
      list2 = ('UpgradeBuild', 'TwoExtQs', 'Land')

      #run spec advice
    try:
      specAdvice(specinfo.banner,list1, list2, specinfo.spec, groups_bl, groups_gr)
      
    #send advice
      await channel.send(content =notes)
      if specInfo.language != 'en':
        notes_trans = GoogleTranslator(source='auto', target=target_lang).translate(text=notes)
        await channel.send(content =notes_trans) 
      await channel.send(file=File('blueSpec.png'))
      await channel.send(file=File('greenSpec.png'))
      await channel.send(file=File('redSpec.png'))
    except:
      await channel.send(content = "Oops, something went wrong")
