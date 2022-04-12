from nextcord.ext import commands, application_checks
from nextcord import Interaction, slash_command, Embed, Color, SlashOption, Message
from functions import staticValues as sv
from classes.SpecView import SpecView, LeaderSpecView
from replit import db






class specAdv2(commands.Cog):
  """Handle spec advice"""

  def __init__(self, bot: commands.Bot):
    self.bot = bot
    self.flags = sv.flags
    self.dataCog = bot.get_cog('Data')

  async def checkcheck(interaction):
    featureName = "specAdv2"
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
  
  @slash_command(name="leaderspec", description="Press to specify a spec priority for all players", guild_ids=sv.gIDS)
  @application_checks.check(checkcheck)
  async def leaderspec(self,
      interaction: Interaction):
    """Leaders can specify a priority for specialisation points for all players"""
    channel = interaction.channel     
        
    view  = LeaderSpecView(channel)
    

    await interaction.response.send_message(content="select a leader priority:",view=view,ephemeral = True)

  
        
  @slash_command(name="specadvice",
                      description="Press for spec advice.",
                      guild_ids=sv.gIDS)
  @application_checks.check(checkcheck)
  async def specadvice(self,
      interaction: Interaction):
    """Provides advice on where to place your specialisation points"""   
    channel = interaction.channel
    user = interaction.user
    try:
      member = self.dataCog.getMemberByID(user.id)
      points = member.currentSkillLvl
      if points < 10:
        await interaction.response.send_message("Please enter your specialisation points in the #loyalty skill channel", ephemeral = True)
        
        return
    except:
      await interaction.response.send_message("Please enter your specialisation points in the #loyalty skill channel", ephemeral = True)
      return
      
    redFile = f"drawings/red{user.id}.png"
    blueFile = f"drawings/blue{user.id}.png"
    greenFile = f"drawings/green{user.id}.png"
        
    view  = SpecView( self.flags, channel, blueFile, greenFile, redFile, member, user)
    

    await interaction.response.send_message(content="select a language:",view=view,ephemeral = True)
    #waitUntil(view.specinfo.ready == True, specInput(channel, view)) #runs function  
    
    
  @commands.Cog.listener('on_message')
  async def delete_messages(self,message):
    """delete Messages after 10s"""
    if message.author.bot:
      return
    #Loyalty and Skill lvl channel
    if message.channel.id != sv.channel.skill_point_advice:
      return
    try:
      await message.delete(delay=10)
    except:
      print('Message could not be deleted') 

  @commands.Cog.listener('on_ready')
  async def load_leaderspec(self):
    view = LeaderSpecView(None)
    if view.leaderspec == None:
      return
    try:
      view.leaderspec = db['leaderspec']
    except:
      view.leaderspec = None
  
    print(view.leaderspec)
    
    

def setup(bot: commands.Bot):
  bot.add_cog(specAdv2(bot))
  