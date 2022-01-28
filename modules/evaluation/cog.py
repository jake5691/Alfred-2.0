from nextcord.ext import commands
from nextcord import Interaction, slash_command, SlashOption, Role
from functions import staticValues as sv



class Evaluation(commands.Cog):
  """Evaluate members, roles and more"""

  def __init__(self, client: commands.Bot):
    self.client = client
  
  @slash_command(name="rolemembers",
                      description="Shows a list of all Members with the selected role",
                      guild_ids=sv.gIDS)
  async def rolemembers(self, interaction: Interaction,
      role: Role = SlashOption(
          name="role",
          description="Role to show members of",
          required=True)):
    allMembers = interaction.guild.members
    roleMembers = []
    for m in allMembers:
      if role in m.roles and m.bot == False:
        roleMembers.append(m)
    res = f"**{role.name}:**"
    for m in roleMembers:
      res += f"\n{m.display_name}"
    await interaction.response.send_message(res)


def setup(client: commands.Bot):
  client.add_cog(Evaluation(client))