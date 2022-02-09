from nextcord import SelectOption, Interaction, ButtonStyle
from nextcord.ui import Select, View, Button
from functions import staticValues as sv
from functions import bannerFunc as bf
from replit import db

class DeleteButton(Button):
  """Button to delete a banner"""
  def __init__(self,banner=str):
    super().__init__(label="Delete Banner",emoji=sv.emoji.exp_rabbit,style=ButtonStyle.red,row=1)
    self.banner = banner
  async def callback(self,interaction:Interaction):
    if not(self.view.dataCog.deleteBannerByName(self.banner)):
      await interaction.response.edit_message(content="Something went wrong, try again or ask for support",view=None)
    
    await interaction.response.edit_message(content=f"You deleted the banner **{self.banner}**.",view=None)
    #update List
    embeds = bf.listBanners(self.view.dataCog.members)
    failed = False
    mesID = 0
    try:
      mesID = db[sv.db.bannerList]
    except:
      failed = True
    try:
      mes = await interaction.channel.fetch_message(mesID)
    except:
      print("Failed to fetch Message")
      failed = True
    if failed:
      mes = await interaction.followup.send(content=None,embeds=embeds)
      db[sv.db.bannerList] = mes.id
      return
    await mes.edit(content=None,embeds=embeds)


class CancelButton(Button):
  """Button to cancel deleting a banner"""
  def __init__(self):
    super().__init__(label="Cancel",row=1)

  async def callback(self,interaction:Interaction):
    await interaction.response.edit_message(content="You **did not** deleted a banner.",view=None)


class SelectBanner(Select):
  """Dropdown to select a banner"""
  def __init__(self, banners: [str]):
    super().__init__(placeholder="Select the banner you want to delete",row=0,min_values=1, max_values=1)
    options = []
    for b in banners:
      options.append(SelectOption(label=b))
    self.options = options

  async def callback(self,interaction:Interaction):
    self.view.clear_items()
    self.view.add_item(DeleteButton(self.values[0]))
    self.view.add_item(CancelButton())
    await interaction.response.edit_message(content=f"Do you want really want to delete this banner?\n**{self.values[0]}**",view=self.view)


class BannerDeleteView(View):
  """The view to hold the Dropdown and Buttons"""
  def __init__(self,data):
    super().__init__()
    self.dataCog = data
    self.add_item(SelectBanner(self.dataCog.getBannerNames()))
    self.add_item(CancelButton())