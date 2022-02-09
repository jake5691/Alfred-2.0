from nextcord.ext import commands
from nextcord import Interaction, slash_command, SlashOption, Role, File
from operator import attrgetter
from functions import staticValues as sv
from datetime import date
import csv



gIDS = [895003315883085865]

class Evaluation(commands.Cog):
  """Evaluate members, roles and more"""

  def __init__(self, client: commands.Bot):
    self.client = client
    self.dataCog = client.get_cog('Data')
  
  @slash_command(name="rolemembers",
                      description="Shows a list of all Members with the selected role",
                      guild_ids=gIDS)
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
                      description="Export members to a csv-file",
                      guild_ids=gIDS)
  async def exportrole(self, interaction: Interaction,
      role: Role = SlashOption(
          name="role",
          description="Role to export members of",
          required=True)):
    """Exports a list of all Members with the selected role"""
    #Check if user has Permission
    userRoles = [i.id for i in interaction.user.roles]
    if not(sv.roles.Leadership in userRoles):
      await interaction.response.send_message("Sorry you are not allowed to use that command.", ephemeral = True)
      return
    await interaction.response.send_message("*please be patient while I'm creating your csv-file*",ephemeral=True)
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