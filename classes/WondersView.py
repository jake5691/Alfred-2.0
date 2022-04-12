from nextcord.ui import View, Button
from nextcord import Interaction, ButtonStyle, PartialEmoji
from replit import db

from classes.Member import MemberClass
from functions import staticValues as sv 
from functions import wondersFunc as wf

class WonderLvlButton(Button):
  """Button to de/increase lvl of a Wonder"""
  def __init__(self, name:str, step:int, row:int=0):
    super().__init__(style=ButtonStyle.grey, row=row)
    self.step = step
    self.name = name
    if step > 0:
      self.label = "+" + str(step)
    else:
      self.label = str(step)
    if row == 0 or row == 2:
      self.style = ButtonStyle.blurple

  async def callback(self, interaction:Interaction):
    #Increase the lvl of that Wonder for the Member that pressed the button
    member = self.view.dataCog.getMemberByID(interaction.user.id)
    newLvl = member.updateWonder(self.name, increment=self.step)
    member.save()
    await interaction.send(content=f"Updated the lvl of **{self.name}** for {interaction.user.display_name} to {newLvl}", ephemeral=True)
    #Update Ranking
    embeds=wf.getWonderRankingEmbeds(self.view.dataCog.members, self.name)
    wonderDBKey = sv.db.WONDER_RANKING + self.name.replace(" ", "")
    try:
      oldMes = await interaction.channel.fetch_message(db[wonderDBKey][str(interaction.guild.id)])
      await oldMes.edit(embeds=embeds)
      return
    except:
      print("couldn't get old message")
      wonderMes = await interaction.channel.send(embeds=embeds)
      if db.prefix(wonderDBKey) == ():
        db[wonderDBKey] = {}
      db[wonderDBKey][str(interaction.guild.id)] = wonderMes.id
    
class WonderButton(Button):
  """Button to put in specific lvl of a Wonder"""
  def __init__(self, name:str, emoji:str=None, row:int=0):
    super().__init__(label=name, style=ButtonStyle.grey, row=row)
    if emoji != None:
      em = PartialEmoji.from_str(emoji)
      self.emoji = em
    self.name = name
    if row == 0 or row == 2:
      self.style = ButtonStyle.blurple

  async def callback(self, interaction:Interaction):
    """Show the numpad to enter the lvl of the wonder"""
    member = self.view.dataCog.getMemberByID(interaction.user.id)
    await interaction.send(content=f"Enter the lvl of **{self.name}** for {interaction.user.display_name}:\n*(press save when done)*", view=WonderLvlSelectView(member, self.name, self.emoji, self.view.dataCog), ephemeral=True)


class WondersView(View):
  """The view to hold the Wonders Buttons"""
  def __init__(self, dataCog):
    super().__init__(timeout=None)
    self.dataCog = dataCog
    self._wonders = [
      "Mayan Pyramid", 
      "Moai Statue", 
      "Statue of Victory", 
      "Statue of General"
    ]
    self._wonderEmoji = [sv.emoji.MayanPyramid, sv.emoji.MoaiStatue, sv.emoji.StatueOfVictory, sv.emoji.StatueOfGeneral]
    for idx, wonder in enumerate(self._wonders):
      self.add_item(WonderButton(wonder, emoji=self._wonderEmoji[idx], row=idx))
      self.add_item(WonderLvlButton(wonder, 1, idx))
      self.add_item(WonderLvlButton(wonder, 5, idx))
      #self.add_item(WonderLvlButton(wonder, -1, idx))

#########################NUMBERPAD#########################
class WonderName(Button):
  """Button to display the name the wonder"""
  def __init__(self, name:str, emoji:str=None, row:int=0):
    super().__init__(label=name, emoji=emoji, style=ButtonStyle.blurple, row=row)
    self.disabled = True

class NumberButton(Button):
  """Button to put in a number"""
  def __init__(self, number:int, row:int):
    super().__init__(label=number, style=ButtonStyle.grey, row=row)

  async def callback(self, interaction:Interaction):
    self.view.lvl += str(self.label)
    await interaction.response.edit_message(content=f"*{self.view.member.name}*: lvl **{self.view.lvl}** for *{self.view.wonder}*, press **SAVE** when finished.")

class SaveButton(Button):
  """Button to set the put in number as the wonders lvl"""
  def __init__(self):
    super().__init__(label="SAVE", style=ButtonStyle.green, row=4)

  async def callback(self, interaction:Interaction):
    newLvl = self.view.member.updateWonder(self.view.wonder, lvl=int(self.view.lvl))
    self.view.member.save()
    await interaction.response.edit_message(content=f"You put in **lvl {newLvl}** {self.view.wonder} for *{self.view.member.name}*", view=None)
    #Update Ranking
    embeds=wf.getWonderRankingEmbeds(self.view.dataCog.members, self.view.wonder)
    wonderDBKey = sv.db.WONDER_RANKING + self.view.wonder.replace(" ", "")
    try:
      oldMes = await interaction.channel.fetch_message(db[wonderDBKey][str(interaction.guild.id)])
      await oldMes.edit(embeds=embeds)
      return
    except:
      print("couldn't get old message")
      wonderMes = await interaction.channel.send(embeds=embeds)
      if db.prefix(wonderDBKey) == ():
        db[wonderDBKey] = {}
      db[wonderDBKey][str(interaction.guild.id)] = wonderMes.id
    
class WonderLvlSelectView(View):
  """The view to hold the numberpad to put in a wonder lvl"""
  def __init__(self, member:MemberClass, wonder:str, emoji, dataCog):
    super().__init__(timeout=None)
    self.dataCog = dataCog
    self.member = member
    self.wonder = wonder
    self.lvl = ""
    
    self.add_item(WonderName(self.wonder, emoji))
    self.add_item(NumberButton(7,1))
    self.add_item(NumberButton(8,1))
    self.add_item(NumberButton(9,1))
    self.add_item(NumberButton(4,2))
    self.add_item(NumberButton(5,2))
    self.add_item(NumberButton(6,2))
    self.add_item(NumberButton(1,3))
    self.add_item(NumberButton(2,3))
    self.add_item(NumberButton(3,3))
    self.add_item(NumberButton(0,4))
    self.add_item(SaveButton())
