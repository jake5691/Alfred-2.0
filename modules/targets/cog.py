from nextcord.ext import commands, tasks, application_checks
from nextcord import Interaction, slash_command, Embed, Color, SlashOption, Message
from functions import staticValues as sv
from functions import targetFunctions as tf
from classes.TargetEdit import TargetEditView
from classes.TargetDelete import TargetDeleteView
from classes.TargetAdd import TargetAddView
from classes.TargetComment import TargetCommentView
from operator import attrgetter
from nextcord.utils import get


class Targets(commands.Cog):
  """Target planning and announcing"""

  def __init__(self, bot: commands.Bot):
    self.bot = bot
    #Load Structures
    self.dataCog = bot.get_cog('Data')
    self.structures = self.dataCog.structures
    self.remindTarget.start()

  async def checkcheck(interaction):
    featureName = "Targets"
    features = interaction.client.get_cog(sv.SETTINGS_COG).Features
    feature = next((x for x in features if x.name == featureName), None)
    #feature
    if feature == None:
      await interaction.response.send_message(f"**ERROR:** couldn't find the feature *{featureName}*, please reach out to the developers.", ephemeral=True)
      return False
    #enabled
    if not feature.isEnabled(interaction.guild.id):
      await interaction.response.send_message(f"This feature is not enabled on your server, please reach out to your Leaders for clarification.", ephemeral=True)
      return False
    #command
    command = next((x for x in feature.commands if x.name == interaction.application_command.qualified_name), None)
    if command == None:
      await interaction.response.send_message(f"**ERROR:** couldn't find the command *{interaction.application_command.qualified_name}*, please reach out to the developers.", ephemeral=True)
      return False
    #roles
    if not command.isAllowedByMember(interaction.guild.id, interaction.user):
      await interaction.response.send_message(f"You are not allowed to use this command *{command.name}*.", ephemeral=True)
      return False
    #channels
    if not command.isAllowedInChannel(interaction.guild.id, interaction.channel.id):
      await interaction.response.send_message(f"The command *{command.name}* is not allowed in this channel.", ephemeral=True)
      return False
    return True
  
  @tasks.loop(seconds = 10)
  async def remindTarget(self):
    """Loop to check if it is time to remind everyone that a target is about to be atacked"""
    reminded = False
    for target in self.dataCog.targets:
      needRemind, remindStr = target.needsReminder()
      if needRemind:
        guild = next((x for x in self.bot.guilds if x.id == sv.gIDS[0]), None)
        if guild == None:
          return
        edenChat = get(guild.channels, id=sv.channel.eden_english)
        rbcRole = get(guild.roles, id=sv.roles.RBC)
        guildRole = get(guild.roles, id=sv.roles.GuildMember)
        await edenChat.send(remindStr + rbcRole.mention + guildRole.mention)
        reminded = True
    if reminded:
      tf.saveTargets(self.dataCog.targets,self.dataCog.getFlags())

  
  @slash_command(name="addtarget",
                      guild_ids=sv.gIDS)
  @application_checks.check(checkcheck)
  async def addTarget(self,
      interaction: Interaction):
    """Add Target from the structure list and assign time and flag"""
    #Function
    view = TargetAddView(self.structures, self.dataCog.getFlags(),self.dataCog.targets)
    await interaction.response.send_message(content="Please select a sector:",view=view,ephemeral = True)
  
  @slash_command(name="listtargets",
                      guild_ids=sv.gIDS)
  @application_checks.check(checkcheck)
  async def listTargets(self,
      interaction: Interaction):
    """List all current targets (not publish)"""
    #Function
    tList = "**Current Targets:**\n"
    targets = self.dataCog.targets
    targets = sorted(targets, key=attrgetter('hour', 'minute'))
    for t in targets:
      tList += t.targetStr() + "\n"
    if targets == []:
      tList = "No targets in list."
    await interaction.response.send_message(content=tList)
  
  @slash_command(name="publishtargets",
                      description="Press send to publish the targets",
                      guild_ids=sv.gIDS)
  @application_checks.check(checkcheck)
  async def publishTargets(self,
      interaction: Interaction,
      infotext: str = SlashOption(
        description="If you want a custom text as header for the Embed put it here",
        required = False
      )):
    """Add Target from the structure list and assign time and flag"""
    #Function
    targets = self.dataCog.targets
    if targets == []:
      await interaction.response.send_message(content="Currently no targets scheduled, please add targets first before publishing the list", ephemeral = True)
    targets = sorted(targets, key=attrgetter('hour', 'minute'))
    if infotext == None:
      infotext = "our current plan for the next attacks, please keep in mind that we might have to react on events and have short notice changes"
    infotext += f"\n<@&{sv.roles.RBC}><@&{sv.roles.GuildMember}>"
    rEmbed = Embed(
      title = "**Target list:**",
      description = infotext,
      color = Color.random()
    )
    for t in targets:
      h,v = t.embedFieldValue()
      rEmbed.add_field(name=h,value=v,inline=False)
    
    await interaction.response.send_message(embed=rEmbed)
  
  @slash_command(name="edittargets",
                      guild_ids=sv.gIDS)
  @application_checks.check(checkcheck)
  async def editTargets(self,
      interaction: Interaction):
    """Edit Target Time and Flag"""
    #Function
    targets = self.dataCog.targets
    if targets == []:
      await interaction.response.send_message(content="There are no targets, please use */addtarget* to create the first one.",ephemeral = True)
      return
    view = TargetEditView(self.dataCog)
    await interaction.response.send_message(content="Select a target to change time and/or flag",view=view,ephemeral = True)
  
  @slash_command(name="commenttarget",
                      description="Add/Replace a comment to a target (selected after entering the comment)",
                      guild_ids=sv.gIDS)
  @application_checks.check(checkcheck)
  async def commentTarget(self,
      interaction: Interaction,
      comment: str = SlashOption(
          name="comment",
          description="comment to a target (which you will select after sinding this command)",
          required=True)):
    """Add comment to a target"""
    #Function
    targets = self.dataCog.targets
    targets = sorted(targets, key=attrgetter('hour', 'minute'))
    if targets == []:
      await interaction.response.send_message(content="There are no targets set, so nothing to comment on...", ephemeral = True)
      return
    view = TargetCommentView(targets,self.dataCog.getFlags(),comment)
    await interaction.response.send_message(content=f"Please select the target where you want to add your comment:\n*{comment}*",view=view, ephemeral = True)
  
  @slash_command(name="deletetargets",
                      guild_ids=sv.gIDS)
  @application_checks.check(checkcheck)
  async def deleteTargets(self,
      interaction: Interaction):
    """Delete all current targets"""
    #Function
    content = "Do you really want to **delete all targets**?\n*Current Targets:*\n"
    targets = self.dataCog.targets
    targets = sorted(targets, key=attrgetter('hour', 'minute'))
    for t in targets:
      content += t.targetStr() + "\n"
    if targets == []:
      await interaction.response.send_message(content="There are no targets set, so nothing to delete...", ephemeral = True)
      return
    view = TargetDeleteView(self.dataCog)
    await interaction.response.send_message(content=content,view=view, ephemeral = True)
  
  @slash_command(name="structureinfo",
                      guild_ids=sv.gIDS)
  @application_checks.check(checkcheck)
  async def structureinfo(self, interaction: Interaction,
      structure: str = SlashOption(
          description="Select a structure from the list",
          required=True),
        avgdestruction: int = SlashOption(
          description="The average destruction value you want to consider",
          required=False),
        private: bool = SlashOption(
          description="should the reply be only for you (default) or public",
          required=False)):
    """Show Information of structures"""
    #Function
    private = True if private == None else private

    struct = next((x for x in self.structures if x.name == structure), None)
    if struct == None:
      await interaction.response.send_message(f"Could not find a strcture with this name", ephemeral = True)
      return
    mes = f"Here is your info for {struct.name}:\nLoyalty: {struct.loyalty:,} ({struct.damagedLoyalty:,})\nDurability: {struct.durability:,} ({int(struct.durability*0.8):,})\nPoints: {struct.points}"
    embed=None
    if avgdestruction != None:
      embed = tf.attackersEmbed(struct.durability,avgdestruction)
      await interaction.response.send_message(mes,embed=embed, ephemeral = private)
      return
    await interaction.response.send_message(mes, ephemeral = private)
  
  @structureinfo.on_autocomplete("structure")
  async def structureName(self,interaction: Interaction, structure: str):
    """Autocomplete the structure name"""
    if not structure:
        # send the full autocomplete list
        await interaction.response.send_autocomplete(self.dataCog.strucNames)
        return
    # send a list of nearest matches from the list structures
    get_near_name = [
        nameb for nameb in self.dataCog.strucNames if nameb.lower().startswith(structure.lower())
    ]
    await interaction.response.send_autocomplete(get_near_name)
  
  @commands.Cog.listener('on_message')
  async def update_avgdestruction(self,message):
    # get the message replied to
    ref = message.reference
    if not ref or not isinstance(ref.resolved, Message):
        return
    parent = ref.resolved

    # if the parent message is not the bot's message, ignore it
    if parent.author.id != self.bot.user.id:
        return

    # check that the message has embeds
    if not parent.embeds:
        return

    embed = parent.embeds[0]
    #check that the message is not the wordle game
    if embed.title == "Wordle Clone":
      return
    try:
      avgdestruction = int(message.content.strip())
    except:
      await message.reply(
          "Please respond just with an integer", delete_after=5
      )
      try:
          await message.delete(delay=5)
      except Exception:
          pass
      return
    durability = int(embed.footer.text.split(":")[1].strip())
    try:
      durability = int(embed.footer.text.split(":")[1].strip())
    except:
      return
    embed = tf.attackersEmbed(durability,avgdestruction)
    await parent.edit(embed=embed)
    try: 
      await message.delete()
    except:
      pass
  

def setup(bot: commands.Bot):
  bot.add_cog(Targets(bot))