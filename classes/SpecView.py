import os
from replit import db
from nextcord import SelectOption, Interaction, File, ButtonStyle
from nextcord.ui import Select, View, Button
from classes.Spec import specInfo
from deep_translator import (GoogleTranslator)

from functions.specFunctions.assignSpecFunc import specAdvice
from functions.specFunctions.blueSpecFunc import groups_bl
from functions.specFunctions.greenSpecFunc import groups_gr
from functions.generalFunc import target_lang


class DoneButton(Button):
  """Button to exit the editing"""
  def __init__(self):
    super().__init__(label="Exit",style=ButtonStyle.red, row=4)
    
  
  async def callback(self,interaction:Interaction):
    
    self.view.content = f"leaderspec changed to {self.view.leaderspec}"
    self.view.clear_items()
    await interaction.response.edit_message(content=self.view.content,view=None)
    
class SelectLeaderSpec(Select):
  """Dropdown to select which preset option"""
  def __init__(self, leaderoptions, leadergroups, leaderspec):
    super().__init__(placeholder = "Please select a priority",row=0,min_values=1, max_values=1)

    self.placeholder = f"leaderspec is current {leaderspec}.  Please select a new option."
    lookup = list(zip(leaderoptions, leadergroups))
    options =[]
    for o in lookup:
      options.append(SelectOption(label=o[0], value=o[1], default=False))
    #self.placeholder = content
    self.options = options
    
  async def callback(self, interaction:Interaction):
    self.view.leaderspec = self.values[0]
    db['leaderspec'] = self.view.leaderspec
    content = f"leader priority changed to {self.view.leaderspec}"
    await interaction.response.edit_message(content = content)
    

class LeaderSpecView(View):
  """The view to hold the Dropdown and Buttons for the leader spec setting"""
  def __init__(self, channel):
    super().__init__()
    if db.prefix('leaderspec') == ():
      db['leaderspec'] = ""
    self.leaderspec = db['leaderspec']
    self.leaderoptions = ['Season Start (place buildings)','Tile Speed', 'None']
    self.leadergroups = ['PlaceBuild','TileSpeed', 'None']
    self.content ="."
    self.add_item(SelectLeaderSpec(self.leaderoptions, self.leadergroups, self.leaderspec))
    self.add_item(DoneButton())
    


class SelectLanguage(Select):
  """Dropdown for language for translation"""
  def __init__(self,flags:[str]):
    super().__init__(placeholder = "Select the language",row=0,min_values=1, max_values=1)
    options = []
    for f in flags:
      options.append(SelectOption(label=f, default=False))
    self.options = options
  
  async def callback(self, interaction:Interaction):
    self.view.specinfo.language = target_lang(self.values[0])
    self.view.whatNext()
    await interaction.response.edit_message(content=self.view.content, view = self.view)

class SelectAdvOpt(Select):
  """Dropdown for whether user wants to select their own or use preset values"""
  def __init__(self,pathopt, content):
    super().__init__(row=0,min_values=1, max_values=1)
    options = []
    for p, t in pathopt:
      options.append(SelectOption(label=p, description=t, default=False))
    self.placeholder = content
    self.options = options
    
  async def callback(self, interaction:Interaction):
    self.view.pathway = self.values[0]
    print("pathway", self.values[0])
    self.view.whatNext()
    await interaction.response.edit_message(content=self.view.content, view = self.view)  

class SelectPreset(Select):
  """Dropdown to select which preset option"""
  def __init__(self, opt, content):
    super().__init__(placeholder = ".",row=0,min_values=1, max_values=1)
    options = []
    for o, t in list(opt):
      options.append(SelectOption(label=o, description=t, default=False))
    self.placeholder = content
    self.options = options
    
  async def callback(self, interaction:Interaction):
    self.view.specinfo.preset = self.values[0]
    self.view.clear_items()
    self.view.whatNext()
    await interaction.response.edit_message(content=self.view.content, view = self.view)
    
class SelectBanner(Select):
  """Dropdown for banner question"""
  def __init__(self,banner, content):
    super().__init__(row=0,min_values=1, max_values=1)
    options = []
    print(banner)
    for e, t in banner:
      options.append(SelectOption(label=e, description = t))
    self.options = options
    self.placeholder = content
  async def callback(self, interaction:Interaction):
    self.view.specinfo.specialCastle = self.values[0]
    self.view.whatNext()
    await interaction.response.edit_message(content=self.view.content, view = self.view)

class SelectTop3(Select):
  """Dropdown for the top three priorities selection"""
  def __init__(self, opt, lookup, content):
    super().__init__(placeholder = "select three options", min_values=3, max_values=3)
    options = []
    
    for p, t in opt:  
      options.append(SelectOption(label=p, value=lookup[p], description=t, default=False)) 
    self.placeholder = content
    self.options = options
    
  async def callback(self, interaction:Interaction):
    for p in self.values:
      self.view.specinfo.list1.append(p)
    self.view.whatNext()
    await interaction.response.edit_message(content=self.view.content, view = self.view)

class SelectNext3(Select):
  """Dropdown for the next three priorities selection"""
  def __init__(self, opt, lookup, content, list1):
    super().__init__(placeholder = "select three options", min_values=1, max_values=3)
    options = []
    for p, t in opt:
      if lookup[p] not in list1:
        options.append(SelectOption(label=p, value=lookup[p], description=t, default=False))  
    self.placeholder = content
    self.options = options

  async def callback(self, interaction:Interaction):
    for p in self.values:
      self.view.specinfo.list2.append(p)
    self.view.specinfo.notes = "You selected your own areas of focus"
    self.view.whatNext()
    await interaction.response.edit_message(content=self.view.content, view = self.view)
  

class SelectOutput(Button):
  """Dropdown to calculate and produce the drawings"""
  def __init__(self, content):
    super().__init__(label="OK", style=ButtonStyle.secondary)
    options = []
    options.append(SelectOption(label="OK", default=False))
    self.placeholder = content
   
    #self.options = options

  async def callback(self, interaction:Interaction):
    self.disabled = True
    self.view.specinput()
    await interaction.response.edit_message(content=self.view.content, view = self.view)
    spec = self.view.specinfo.spec
    helpText = 'Type "/specadvice" to get advice on where to use your specialisation points'
    try:
      summary = await specAdvice(self.view, spec, groups_bl, groups_gr)
      blueFile = self.view.bluefile
      greenFile = self.view.greenfile
      redFile = self.view.redfile
      notes = self.view.specinfo.notes
    #send advice
      await self.view.channel.send(content =f"{self.view.author.mention}: {notes}")
      if self.view.specinfo.language != 'english':
        try:
          notes_trans = GoogleTranslator(source='english', target=self.view.specinfo.language).translate(text=notes)
        except:
          notes_trans = ""
        summary = summary +   GoogleTranslator(source='auto', target=self.view.specinfo.language).translate(text=summary)
        await self.view.channel.send(content =f"{self.view.author.mention}: {notes_trans}") 
      await self.view.channel.send(file=File(blueFile))
      await self.view.channel.send(file=File(greenFile))
      await self.view.channel.send(file=File(redFile))
      await self.view.channel.send(content=summary)
      await self.view.channel.send(content=helpText)
    except:
      await self.view.channel.send(content = f"{self.view.author.mention},Oops, something went wrong")
      await self.view.channel.send(content=helpText)

    os.remove(redFile)
    os.remove(blueFile)
    os.remove(greenFile)


class SpecView(View):
  """The view to hold the Dropdown and Buttons"""
  def __init__(self,flags, channel, blueFile, greenFile, redFile,  member, user):
    super().__init__()
    
    self.specinfo = specInfo()
    self.author = user
    self.channel = channel
    self.flags = flags
    self.bluefile = blueFile
    self.greenfile = greenFile
    self.redfile = redFile
    self.member = member
    self.pathway = None
    self.priorityoptions = ['Loyalty', 'Extra tiles', 'One extra queue', 'Upgrade buildings', 'Tile honour', 'Income from food/marble tiles', 'Income from wood/iron tiles', 'Land development', 'Two extra queues', 'Three extra queues']
    self.prioritygroups = ['Loyalty', 'ExtraTile', 'OneExtQ', 'UpgradeBuild', 'TileHonour', 'CBCMat', 'FWMat', 'Land','TwoExtQs', 'MaxQs']
    self.selectrans = []
    self.ready = False
    self.output = False
    self.specinfo.spec = self.member.currentSkillLvl
    self.content = "."
    self.whatNext()
    self.specinput()

    
  def whatNext(self):
    """Function that selects the next Dropdown to present"""
    self.clear_items()
    if self.specinfo.language == None:
      #get languages from those in staticvalues
      languages = []
      for l in self.flags:
        if not(l in languages):
          languages.append(l)
      languages = sorted(languages)
      if len(languages) > 1:
        self.content = "Language:"
        self.add_item(SelectLanguage(languages))
        return
      self.specinfo.language = 'english'

    if self.specinfo.specialCastle == None:
      opt = []
      specialCastleOpt = ('Banner', 'Tile fighting','None')
      for o in specialCastleOpt:
        trans = GoogleTranslator(source='auto', target=self.specinfo.language).translate(text=o)
        item =(o, trans)
        opt.append(item)
      text = 'Does your castle have a special function?\n\n'
      trans = GoogleTranslator(source='auto', target=self.specinfo.language).translate(text=text)
      if self.specinfo.language != 'english':
        content = text + trans
      else:
        content = text
      self.content = content
      self.add_item(SelectBanner(opt, trans))
      return
      
    if self.pathway == None:
      opt = []
      for p in ('Preset', 'Select'):
        trans = GoogleTranslator(source='auto', target=self.specinfo.language).translate(text=p)
        item =(p, trans)
        opt.append(item)
      text = "Use Preset recommendations or Select your own Priorities?\n\n"
      trans = GoogleTranslator(source='auto', target=self.specinfo.language).translate(text=text)
      if self.specinfo.language != 'english':
        content = text + trans
      else:
        content = text
      self.content = content
      self.add_item(SelectAdvOpt(opt, trans))
      return

    if self.pathway == "Preset" and self.ready ==False:
      trans =[]
      #preset = ('Start', 'Week1', 'Week2', 'Loyalty', 'FillIW', 'FW', 'Tile Honour')
      #p_text =('Place buildings at start of season', 'Week 1 loyalty', 'Week 2 loyalty and tilespeed', 'Increasing loyalty', 'Keep loyalty while filling on iron/wood tiles', 'Upgrading Frontline Workshops or Fortresses', 'Maximum points from tile honour')
      preset = ('Loyalty', 'Iron/Wood', 'Upgrade buildings', 'Tile Honour', 'War Cavalry', 'War Archers')
      p_text =('Increasing loyalty', 'Keep loyalty high while taking iron and wood tiles', 'Upgrading Frontline Workshops or Fortresses', 'Maximum points from tile honour', 'Fun with my horses', 'Fun with my shooters')
      if self.specinfo.language == 'english':
        trans = ['Increasing loyalty', 'Keep loyalty high while taking iron and wood tiles', 'Upgrading Frontline Workshops or Fortresses', 'Maximum points from tile honour', 'Fun with my horses', 'Fun with my shooters']
      elif self.specinfo.language == 'spanish':
        trans = ['Aumento de la lealtad', 'Mantenga alta la lealtad mientras toma fichas de hierro y madera.', 'Mejora de talleres o fortalezas de primera línea', 'Puntos máximos de honor de ficha', 'Divertirme con mis caballos', 'Diversión con mis tiradores']
      elif self.specinfo.language == 'russian':
        trans = ['Повышение лояльности', 'Поддерживайте высокую лояльность, беря железные и деревянные плитки.', 'Улучшение передовых мастерских или крепостей', 'Максимальное количество очков за плитку чести', 'Веселье с моими лошадьми', 'Веселье с моими стрелками']
      elif self.specinfo.language == 'indonesian':
        trans =['Meningkatkan loyalitas', 'Jaga loyalitas tinggi saat mengambil ubin besi dan kayu', 'Meningkatkan Lokakarya atau Benteng Garis Depan', 'Poin maksimum dari kehormatan ubin', 'Bersenang-senang dengan kuda saya', 'Bersenang-senang dengan penembak saya']
      elif self.specinfo.language == 'german':
        trans = ['Loyalität steigern', 'Halten Sie die Loyalität hoch, während Sie Eisen- und Holzfliesen nehmen', 'Upgrade von Frontwerkstätten oder Festungen', 'Maximale Punktzahl von Kachelehre', 'Spaß mit meinen Pferden', 'Spaß mit meinen Schützen']
      elif self.specinfo.language == 'korean':
        trans = ['충성도 증가', '철 및 나무 타일을 사용하면서 충성도를 높게 유지하십시오.', '최전방 작업장 또는 요새 업그레이드', '타일 \u200b\u200b명예의 최대 포인트', '내 말과 함께하는 재미', '내 저격수와 함께 재미']
      elif self.specinfo.language == 'french':
        trans = ['Accroître la fidélité', 'Gardez une loyauté élevée tout en prenant des tuiles en fer et en bois', 'Améliorer les ateliers ou les forteresses de première ligne', "Points maximum de l'honneur des tuiles", "S'amuser avec mes chevaux", 'Amusez-vous avec mes tireurs']
      elif self.specinfo.language == 'dutch':
        trans = ['Loyaliteit vergroten', 'Houd de loyaliteit hoog terwijl je ijzeren en houten tegels neemt', 'Eerstelijnsworkshops of forten upgraden', 'Maximum aantal punten van tegel eer', 'Plezier met mijn paarden', 'Plezier met mijn shooters']
      elif self.specinfo.language == 'chinese':
        trans = ['提高忠诚度', '在拿铁和木瓦时保持高忠诚度', '升级前线工坊或堡垒', '瓷砖荣誉的最高分', '和我的马一起玩', '和我的射手一起玩']
      elif self.specinfo.language == 'romanian':
        trans = ['Creșterea loialității', 'Păstrați loialitatea ridicată în timp ce luați plăci de fier și lemn', 'Modernizarea atelierelor sau fortărețelor din prima linie', 'Puncte maxime din onoarea țiglă', 'Distracție cu caii mei', 'Distracție cu trăgătorii mei']
      else:
        trans = GoogleTranslator(source='english', target=self.specinfo.language).translate_batch(batch=p_text)
        print(trans)
      opt = list(zip(preset, trans))
      text = "Select Preset option?"
      trans = GoogleTranslator(source='auto', target=self.specinfo.language).translate(text=text)
      if self.specinfo.language != 'english':
        content = text + trans
      else:
        content = text
      self.content = content
      self.ready = True
      self.add_item(SelectPreset(opt, trans))
      return

    if self.pathway == "Select" and self.specinfo.list1 == []:
      
      #opt = []

      #for p in self.priorityoptions:
      if self.specinfo.language == 'spanish':
        self.selecttrans = ['Lealtad', 'Azulejos adicionales', 'Una cola extra', 'Mejorar edificios', 'honor del azulejo', 'Ingresos por alimentos/baldosas de mármol', 'Renta de tejas de madera/hierro', 'Desarrollo de la tierra', 'Dos colas extra', 'Tres colas extra']
      elif self.specinfo.language == 'english':
        self.selecttrans = self.priorityoptions
      elif self.specinfo.language == 'russian':
        self.selecttrans = ['Верность', 'Дополнительные плитки', 'Одна дополнительная очередь', 'Улучшайте здания', 'Плитка честь', 'Доход от еды/мраморных плиток', 'Доход от деревянных/железных плиток', 'Землеустройство', 'Две дополнительные очереди', 'Три дополнительные очереди']
      elif self.specinfo.language == 'korean':
        self.selecttrans = ['충의', '추가 타일', '하나의 추가 대기열', '건물 업그레이드', '타일 \u200b\u200b명예', '음식/대리석 타일 수입', '목재/철 타일 수입', '토지 개발', '두 개의 추가 대기열', '3개의 추가 대기열']
      elif self.specinfo.language == 'german':
        self.selecttrans = ['Loyalität', 'Zusätzliche Kacheln', 'Eine zusätzliche Warteschlange', 'Werte Gebäude auf', 'Fliese Ehre', 'Einkommen aus Nahrung/Marmorfliesen', 'Einkommen aus Holz-/Eisenfliesen', 'Landesentwicklung', 'Zwei zusätzliche Warteschlangen', 'Drei zusätzliche Warteschlangen']
      elif self.specinfo.language == 'chinese':
        self.selecttrans = ['忠诚', '额外的瓷砖', '一个额外的队列', '升级建筑', '瓷砖荣誉', '食品/大理石瓷砖收入', '木/铁瓦收入', '土地开发', '两个额外的队列', '三个额外的队列']
      elif self.specinfo.language == 'dutch':
        self.selecttrans = ['Loyaliteit', 'Extra tegels', 'Een extra wachtrij', 'Gebouwen upgraden', 'Tegel eer', 'Inkomsten uit eten/marmeren tegels', 'Inkomsten uit hout/ijzeren tegels', 'Land ontwikkeling', 'Twee extra wachtrijen', 'Drie extra wachtrijen']
      elif self.specinfo.language == 'romanian':
        self.selecttrans = ['Loialitate', 'Placi suplimentare', 'O coadă în plus', 'Actualizați clădiri', 'Onoare de țiglă', 'Venituri din alimente/placi de marmură', 'Venituri din faianta din lemn/fier', 'Dezvoltarea terenului', 'Două cozi în plus', 'Trei cozi în plus']
      elif self.specinfo.language == 'french':
        self.selecttrans = ['Loyauté', 'Tuiles supplémentaires', "Une file d'attente supplémentaire", 'Améliorez les bâtiments', 'Honneur de la tuile', 'Revenu de la nourriture/tuiles de marbre', 'Revenu des tuiles en bois/fer', 'Développement agraire', "Deux files d'attente supplémentaires", "Trois files d'attente supplémentaires"]
      else:
        trans = GoogleTranslator(source='english', target=self.specinfo.language).translate_batch(batch=self.priorityoptions)
        print(trans)
        #item =(p, trans)
        #opt.append(item)
      opt = list(zip(self.priorityoptions, self.selecttrans))
        #priorityOptTrans.append(trans)
      lookup = dict(zip(self.priorityoptions, self.prioritygroups))
      #text = "Sorry, this is still a work in progress.  Send jj coffee so that she can finish this more quickly.\n\n"
      text = "Please select your top three priorities.\n\n"
      trans = GoogleTranslator(source='auto', target=self.specinfo.language).translate(text=text)
      if self.specinfo.language != 'english':
        content = text + trans
      else:
        content = text
      self.content = content
      self.add_item(SelectTop3(opt, lookup, trans))
      return

    if self.pathway == 'Select' and self.specinfo.list2 == []:
      
      opt = list(zip(self.priorityoptions, self.selecttrans))
        #priorityOptTrans.append(trans)
      lookup = dict(zip(self.priorityoptions, self.prioritygroups))
      #text = "Sorry, this is still a work in progress.  Send jj coffee so that she can finish this more quickly.\n\n"
      text = "Please select your next priorities \n(min 1, max 3.\n\n"
      trans = GoogleTranslator(source='auto', target=self.specinfo.language).translate(text=text)
      if self.specinfo.language != 'english':
        content = text + trans
      else:
        content = text
      self.content = content
      self.ready = True
      self.add_item(SelectNext3(opt, lookup, trans, self.specinfo.list1))
      return
      
      
      

    if self.output == False:
      opt = []
      opt.append("OK")
      if len(opt) > 0:
        text = "Press OK to continue...this could take a few moments so please have a cup of coffee.\n\n"
        trans = GoogleTranslator(source='auto', target=self.specinfo.language).translate(text=text)
        if self.specinfo.language != 'english':
            content = text + trans
        else:
          content = text
        self.content = content
        self.add_item(SelectOutput(GoogleTranslator(source='auto', target=self.specinfo.language).translate(text="Press ok to continue")))
        return
      


  def specinput(self):
  
    if self.specinfo.preset == 'Loyalty':
    
      self.specinfo.notes = "Your focus is upgrading CBCs, so you should have 90% food and marble tiles. Depending on the number of resets you have, you will occasionally switch to green left to upgrade Frontline Workshops.\n\n"
      self.specinfo.list1 = ('Loyalty', 'CBCMat', 'TwoExtQs')
      self.specinfo.list2 = ('ExtraTile', 'TileHonour', 'UpgradeBuild')

    
    elif self.specinfo.preset == 'Iron/Wood':
     
      self.specinfo.notes = "Your focus is getting high level wood and iron tiles. You may wish to keep a few CBC material tiles if you wish to increase loyalty. You can always take more iron/wood and upgrade later using land development.\n\nIf you think you will fill up on iron/wood before next specialisation reset, ask in alliance chat for advice.\n\n"
      self.specinfo.list1 = ('Loyalty', 'FWMat', 'OneExtQ')
      self.specinfo.list2 = ('ExtraTile', 'TileHonour', 'TwoExtQs')
    elif self.specinfo.preset == 'Upgrade buildings':
      self.specinfo.notes = "Your focus is on upgrading your Frontline Workshops and getting the maximum honour bonus from these upgrades.\n\n"
      self.specinfo.list1 = ('UpgradeBuild', 'FWMat', 'TwoExtQs')
      self.specinfo.list2 = ('ExtraTile', 'TileHonour', 'Land')
    elif self.specinfo.preset == 'Tile Honour':
      self.specinfo.notes = "Your focus is on maximising honour from tiles. You will sometimes switch to green left and extra queues to upgrade Assault and Guardian Fortresses.\n\nIn the last week, you may need to put extra points on processing queues to ensure that you process all of your materials.  Depending on resets you may also prioritise having 49 points on green left (building honour).  Land development and extra tiles might not be necessary.\n.\n"
      self.specinfo.list1 = ('TileHonour', 'FWMat', 'ExtraTile')
      self.specinfo.list2 = ('UpgradeBuild', 'TwoExtQs', 'Land')
    else:
      print(self.specinfo.preset)



      #run spec advice
    

    
      
      
    