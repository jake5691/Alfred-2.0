from nextcord.ext import commands, application_checks
from nextcord import Interaction, slash_command, SlashOption, Role, File
from operator import attrgetter
import csv

from functions import staticValues as sv



class Evaluation(commands.Cog):
  """Evaluate members, roles and more"""

  def __init__(self, client: commands.Bot):
    self.client = client
    self.dataCog = client.get_cog('Data')

  async def checkcheck(interaction):
    featureName = "Evaluation"
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
  
  @slash_command(name="rolemembers",
                      guild_ids=sv.gIDS)
  @application_checks.check(checkcheck)
  async def rolemembers(self, interaction: Interaction,
      role: Role = SlashOption(
          name="role",
          description="Role to show members of",
          required=True)):
    """Shows a list of all Members with the selected role"""
    allMembers = interaction.guild.members
    roleMembers = []
    for m in allMembers:
      if role in m.roles and m.bot == False:
        roleMembers.append(m)
    roleMembers = sorted(roleMembers, key=attrgetter('display_name'))
    res = []
    first = False
    await interaction.response.send_message(f"Fetching your requested data for {role.name}",ephemeral=True)
    resStr = f"{len(roleMembers)} Members in **{role.name}:**"
    for m in roleMembers:
      tpmStr = f"\n{m.display_name} "
      member = self.dataCog.getMemberByID(m.id)
      if member:
        tpmStr += f" *({member.currentSkillLvl} skill points)*"
      if len(resStr) + len(tpmStr) >= sv.limits.charInMessage:
        if first:
          
          first = False
        else:
          res.append(resStr)
        resStr = tpmStr
      else:
        resStr += tpmStr
    res.append(resStr)
    
    for i in range(len(res)):
      await interaction.followup.send(res[i])
  
  @slash_command(name="exportrole",
                      guild_ids=sv.gIDS)
  @application_checks.check(checkcheck)
  async def exportrole(self, interaction: Interaction,
      role: Role = SlashOption(
          name="role",
          description="Role to export members of",
          required=True)):
    """Exports a list of all Members as csv-file with the selected role"""
    await interaction.send("*please be patient while I'm creating your csv-file*",ephemeral=True)
    memberData = []
    for m in role.members:
      tpm = [m.display_name]
      mem = self.dataCog.getMemberByID(m.id)
      tpm.append(mem.currentSkillLvl)
      tpm.append(mem.currentLoyalty)
      
      memberData.append(tpm)
    # open the file in the write mode
    f = open(f"data/{role.name}_data.csv", 'w')
    # create the csv writer
    writer = csv.writer(f)
    # write a row to the csv file
    writer.writerow(["Name","Skill lvl","Loyalty"])
    for row in memberData:
      writer.writerow(row)
    # close the file
    f.close()
    with open(f"data/{role.name}_data.csv", 'rb') as f:
      await interaction.followup.send("Here is your csv file",ephemeral=True,file=File(f, f"{role.name}_data.csv"))




def setup(client: commands.Bot):
  client.add_cog(Evaluation(client))