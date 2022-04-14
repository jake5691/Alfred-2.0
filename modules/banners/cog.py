from nextcord.ext import commands, application_checks
from nextcord import Interaction, slash_command, SlashOption, User
from replit import db
import asyncio

from classes.Member import MemberClass
from classes.BannerDelete import BannerDeleteView

from functions import staticValues as sv
from functions import bannerFunc as bf


class Banners(commands.Cog):
  """Handle banner data/commands"""

  def __init__(self, client: commands.Bot):
    self.client = client
    #Load Members
    self.dataCog = client.get_cog('Data')
    self.command_variables = []
    self.feature_variables = []

  async def checkcheck(interaction):
    featureName = "Banners"
    features = interaction.client.get_cog(sv.SETTINGS_COG).Features
    feature = next((x for x in features if x.name == featureName), None)
    #feature
    if feature == None:
      await interaction.send(f"**ERROR:** couldn't find the feature *{featureName}*, please reach out to the developers.", ephemeral=True)
      return False
    #enabled
    if not feature.isEnabled(interaction.guild.id):
      await interaction.send(f"This feature is not enabled on your server, please reach out to your Leaders for clarification.", ephemeral=True)
      return False
    #command
    command = next((x for x in feature.commands if x.name == interaction.application_command.qualified_name), None)
    if command == None:
      await interaction.send(f"**ERROR:** couldn't find the command *{interaction.application_command.qualified_name}*, please reach out to the developers.", ephemeral=True)
      return False
    #roles
    if not command.isAllowedByMember(interaction.guild.id, interaction.user):
      await interaction.send(f"You are not allowed to use this command *{command.name}*.", ephemeral=True)
      return False
    #channels
    if not command.isAllowedInChannel(interaction.guild.id, interaction.channel.id):
      await interaction.send(f"The command *{command.name}* is not allowed in this channel.", ephemeral=True)
      return False
    return True
  
  #Keep channel clean and show the help
  @commands.Cog.listener('on_message')
  async def banner_channel_messages(self,message):
    if message.author.bot:
      return
    if message.channel.id == sv.channel.banners:
      #Banner handling
      if message.content.lower().startswith('help'):
        loySkillChan = message.guild.get_channel(sv.channel.loyalty_And_skill_lvl)
        sendText = f"**This channel is to manage which flags are active and to be able to put in their loyalty and skill lvl in the regular {loySkillChan.mention} channel**\n**/newbanner** - follow instructions of Alfred 2.0\n**/editbanner** - you can change the *name*, *owner* and set it as *(de)active*\n**/deletebanner** - deletes your banner account (no more entering skill and loyalty and not listed here), do not use this to mark the account as no flag\n**/changeflagspec** - (de)activate any main account as flag specced"
        try:
          helpMesID = db[sv.db.bannerHelp]
          oldMes = await message.channel.fetch_message(helpMesID)
          await oldMes.delete()
        except:
          print("couldn't delete old help message")
        
        helpMes = await message.channel.send(content=sendText)
        db[sv.db.bannerHelp] = helpMes.id
        await message.delete()
      else:
        #Delete Messages that are sent in this channel after a 60s delay
        await asyncio.sleep(60)
        try:
          await message.delete()
        except:
          print('Message could not be deleted')
  
  #Command to create a new banner
  @slash_command(name="newbanner",
    guild_ids=sv.gIDS)
  @application_checks.check(checkcheck)
  async def addBanner(self, interaction: Interaction,
    name:str=SlashOption(
        name="name",
        description="Name of the Banner",
        required=True
      ),
    isflag:bool=SlashOption(
        name="isflag",
        description="If this account is currently specced as flag (can be changed any time)",
        required=True
      ),
    owner:User=SlashOption(
        name="owner",
        description="owener if not owned by yourself",
        required=False
      )):
    """Create a new banner"""
    #Function
    if owner == None:
      owner = interaction.user
    if name in self.dataCog.getBannerNames():
      await interaction.send(f"There already exists a banner account with the name **{name}**, please provide a unique name for each banner account.", ephemeral=True)
      return
    banner = MemberClass(m=owner,banner=True,bannerName=name)
    if isflag:
      flag = "as active flag"
    else:
      flag = "not as active flag"
      banner.bannerActive = False
    
    banner.save()
    self.dataCog.members.append(banner)
    
    await interaction.send(f"**{name}** was created as Banner account and registered {flag}. You can now add loyalty and skill points in <#{sv.channel.loyalty_And_skill_lvl}> by writing the exact banner name in front of the value.", ephemeral=True)
  	#Update Banner list
    embeds = bf.listBanners(self.dataCog.members)
    failed = False
    mesID = 0
    try:
      mesID = db[sv.db.bannerList]
    except:
      failed = True
    try:
      mes = await interaction.channel.fetch_message(mesID)
    except:
      failed = True
    if failed:
      mes = await interaction.followup.send(content=None,embeds=embeds)
      db[sv.db.bannerList] = mes.id
      return
    await mes.edit(content=None,embeds=embeds)
  
  #Delete Banner
  @slash_command(name="deletebanner",
    guild_ids=sv.gIDS)
  @application_checks.check(checkcheck)
  async def deletebanner(self,interaction:Interaction):
    """Delete a banner account"""
    #Function
    view = BannerDeleteView(self.dataCog)
    await interaction.response.send_message(content="Select the Banner you want to delete.", view=view, ephemeral=True)
  
  #Edit Banner
  @slash_command(name="editbanner",
    guild_ids=sv.gIDS)
  @application_checks.check(checkcheck)
  async def editbanner(self,interaction:Interaction,
      name:str=SlashOption(
        name="name",
        description="Current name of the Banner",
        required=True
      ),
      isflag:bool=SlashOption(
        name="isflag",
        description="Is currently specced as flag",
        required=False
      ),
      newname:str=SlashOption(
        name="newname",
        description="New name of the Banner",
        required=False
      ),
      owner:User=SlashOption(
        name="owner",
        description="Change the owner of this banner account",
        required=False
      )):
    """Edit a banner account"""
    #Function
    if not(name in self.dataCog.getBannerNames()):
      await interaction.send(f"There exists no banner account with the name **{name}**, to edit a banner use the correct spelling.", ephemeral=True)
      return
    banner = None
    for m in self.dataCog.members:
      if m.banner and m.name == name:
        banner = m
        break
    if banner == None:
      await interaction.send("Something went wrong, try again or ask for support", ephemeral = True)
      return

    replyStr = f"You changed *{name}*"
    if newname != None:
      banner.name = newname
      banner.id = newname
      replyStr += f" to **{newname}**"
    if isflag != None:
      banner.bannerActive = isflag
      if isflag:
        replyStr += " - **activated** as flag"
      else:
        replyStr += " - **deactivated** flag"
    if owner != None:
      replyStr += f" - changed owner from *{banner.ownerName}* to **{owner.display_name}**"
      banner.ownerID = owner.id
      banner.ownerName = owner.name
      
    
    del db[sv.db.memberPrefix + name]
    banner.save()
    
    await interaction.send(content=replyStr, ephemeral = True)
    #Update Banner list
    embeds = bf.listBanners(self.dataCog.members)
    failed = False
    mesID = 0
    try:
      mesID = db[sv.db.bannerList]
    except:
      failed = True
    try:
      mes = await interaction.channel.fetch_message(mesID)
    except:
      failed = True
    if failed:
      mes = await interaction.followup.send(content=None,embeds=embeds)
      db[sv.db.bannerList] = mes.id
      return
    await mes.edit(content=None,embeds=embeds)
  
  @editbanner.on_autocomplete("name")
  async def bannerName(self,interaction: Interaction, name: str):
    if not name:
        # send the full autocomplete list
        await interaction.response.send_autocomplete(self.dataCog.getBannerNames())
        return
    # send a list of nearest matches from the list of dog breeds
    get_near_name = [
        nameb for nameb in self.dataCog.getBannerNames() if nameb.lower().startswith(name.lower())
    ]
    await interaction.response.send_autocomplete(get_near_name)
  
  @slash_command(name="changeflagspec",
                      description="(de)activate the flag spec for a member",
                      guild_ids=sv.gIDS)
  @application_checks.check(checkcheck)
  async def changeflagspec(self,
      interaction: Interaction,
      member: User = SlashOption(
        description="The Member you want to (de)activate the flag spec",
        required=True),
      isflag: bool = SlashOption(
        description="Is specced as flag?",
        required=True)):
    """Change a member to be set as flag"""
    #Function
    m = self.dataCog.getMemberByID(member.id)
    print(m.bannerActive)
    m.bannerActive = isflag
    m.save()

    if isflag:
      resFlag = "**activated**"
    else:
      resFlag = "**deactivated**"
    await interaction.response.send_message(f"The flag was {resFlag} for {member.display_name}", ephemeral = True)
    #Update Banner list
    embeds = bf.listBanners(self.dataCog.members)
    failed = False
    mesID = 0
    try:
      mesID = db[sv.db.bannerList]
    except:
      failed = True
    try:
      mes = await interaction.channel.fetch_message(mesID)
    except:
      failed = True
    if failed:
      mes = await interaction.followup.send(content=None,embeds=embeds)
      db[sv.db.bannerList] = mes.id
      return
    await mes.edit(content=None,embeds=embeds)

    


def setup(client: commands.Bot):
  client.add_cog(Banners(client))