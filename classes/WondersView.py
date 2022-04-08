from nextcord.ui import View, Button
from nextcord import Interaction, ButtonStyle

from classes.Member import MemberClass

class WonderLvlUpButton(Button):
  """Button to increase lvl of a Wonder"""
  def __init__(self, name=str, emoji:str=None, row:int=0):
    super().__init__(label=name, emoji=emoji, style= ButtonStyle.grey, row=row)
    

  async def callback(self, interaction:Interaction):
    #Increase the lvl of that Wonder for the Member that pressed the button
    newLvl = self.view.member.updateWonder(self.label, increment=1)
    self.view.member.save()
    await interaction.send(content=f"Upgraded the lvl of **{self.label}** for {interaction.user.display_name} to {newLvl}", ephemeral=True)


class WondersView(View):
  """The view to hold the Wonders Buttons"""
  def __init__(self, member:MemberClass):
    super().__init__(timeout=None)
    self.member = member
    self.add_item(WonderLvlUpButton("Mayan Pyramid",row=0))
    self.add_item(WonderLvlUpButton("Moai Statue",row=1))
    self.add_item(WonderLvlUpButton("Statue of Victory",row=2))
    self.add_item(WonderLvlUpButton("Statue of General",row=3))
    