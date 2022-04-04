from nextcord.ext import commands
from nextcord import Interaction, slash_command, Embed, Color, SlashOption, Message
from functions import staticValues as sv
from classes.SpecView import SpecView





class specAdv2(commands.Cog):
  """Handle spec advice"""

  def __init__(self, bot: commands.Bot):
    self.bot = bot
    self.flags = sv.flags
    self.dataCog = bot.get_cog('Data')

  @slash_command(name="specadvice",
                      description="Press for spec advice.",
                      guild_ids=sv.gIDS)
  async def specadvice(self,
      interaction: Interaction):
    """Provides advice on where to place your specialisation points"""
    #Check if advice is asked for in the right channel
    if not(sv.channel.skill_point_advice == interaction.channel.id):
      await interaction.response.send_message("Sorry this command can only be used in a specific channel", ephemeral = True)
      return
    
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
    """delete Messages after 5s"""
    if message.author.bot:
      return
    #Loyalty and Skill lvl channel
    if message.channel.id != sv.channel.skill_point_advice:
      return
    try:
      await message.delete(delay=5)
    except:
      print('Message could not be deleted')    

def setup(bot: commands.Bot):
  bot.add_cog(specAdv2(bot))
  