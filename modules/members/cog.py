from nextcord.ext import commands
from nextcord import Interaction, slash_command, SlashOption, User
from classes.Member import MemberClass
from functions import staticValues as sv
from functions import memberFunc as mf
#from nextcord.utils import get
import re
from replit import db


class Members(commands.Cog):
  """Manage the member instances, keeping loyalty and skill lvl up to date..."""

  def __init__(self, client: commands.Bot):
    self.client = client
    self.dataCog = client.get_cog('Data')

  @commands.Cog.listener('on_member_update')
  async def add_delete_MemberInstance(self,old,new):
    """Add/Remove a MemberClass instance to dataCog.members when roles are assigned.
    Currently relevant roles are: RBC, Guild Member, Newbie"""
    if old.roles == new.roles:
      return
    oldRoles = [r.id for r in old.roles]
    newRoles = [r.id for r in new.roles]
    relevantRoles = [sv.roles.RBC, sv.roles.GuildMember, sv.roles.Newbie]
    #Added/removed a relevant role -> create/delete Member instance
    if not(any(r in oldRoles for r in relevantRoles)) and any(r in newRoles for r in relevantRoles):
      #Check if already a member existis
      for m in self.dataCog.members:
        if m.id == new.id:
          print('Member already exists.')
          return
      #create a member
      newMember = MemberClass(new)
      newMember.save()
      self.dataCog.members.append(newMember)
      print(f"Added: {newMember.name}")
    elif any(r in oldRoles for r in relevantRoles) and not(any(r in newRoles for r in relevantRoles)):
      #remove member if there exists one
      for m in self.dataCog.members:
        if m.id == new.id:
          print(f"{m.name} was deleted.")
          self.dataCog.deleteMemberByID(m.id)
          return
      print("No Member instance found")
  
  @slash_command(name="updateloyskill",
                      description="Update Loyalty and/or skill lvl of any member",
                      guild_ids=sv.gIDS)
  async def updateloyskill(self,
      interaction: Interaction,
      member:User = SlashOption(
        name = "member",
        description="The Member you want to update",
        required = True),
      loyalty:int = SlashOption(
        description="the current Loyalty",
        required = False
      ),
      skill:int = SlashOption(
        description="the current skill lvl/spec points",
        required = False
      )
  ):
    """Change Loyalty/Skill of any member"""
    #Check if user has Permission
    userRoles = [i.id for i in interaction.user.roles]
    if not(sv.roles.Leadership in userRoles):
      await interaction.response.send_message("Sorry you are not allowed to use that command.", ephemeral = True)
      return
    #check if command is send in correct channel
    if not(sv.channel.loyalty_And_skill_lvl == interaction.channel.id):
      await interaction.response.send_message("Sorry this command can only be used in a specific channel", ephemeral = True)
      return
    #Function
    if loyalty == None and skill == None:
      await interaction.response.send_message(f"Please provide at least one update for {member.display_name}", ephemeral = True)
      return
    
    mem = self.dataCog.getMemberByID(member.id)
    if mem == None:
      await interaction.response.send_message(f"Could not find {member.display_name}", ephemeral = True)
      return
    await interaction.response.send_message(f"Working on your input for {member.display_name}", ephemeral = True)
    if loyalty != None:
      updated,reply = mem.updateLoyalty(loyalty)
      if updated:
        mem.save()
        #Update Ranking
        embeds=mf.getRankingEmbeds(self.dataCog.members,'loyalty')
        try:
          oldMes = await interaction.channel.fetch_message(db[sv.db.loyaltyRanking])
          await oldMes.edit(embeds=embeds)
        except:
          print("couldn't get old message")
        
          loyMes = await interaction.channel.send(embeds=embeds)
          db[sv.db.loyaltyRanking] = loyMes.id
      #Post Personal Reply
      await interaction.channel.send(reply, delete_after = 30)
    if skill != None:
      updated,reply = mem.updateSkill(skill)
      if updated:
        mem.save()
        #Update Ranking
        embeds=mf.getRankingEmbeds(self.dataCog.members,'skill')
        try:
          oldMes = await interaction.channel.fetch_message(db[sv.db.skillRanking])
          await oldMes.edit(embeds=embeds)
        except:
          print("couldn't get old message")
        
          loyMes = await interaction.channel.send(embeds=embeds)
          db[sv.db.skillRanking] = loyMes.id
      #Post Personal Reply
      await interaction.channel.send(reply, delete_after = 30)
    #await interaction.response.send_message(f"You updated the input for {user.display_name}", ephemeral = True)
  
  @commands.Cog.listener('on_member_remove')
  async def remove_memberInstance_on_leaving(self,member):
    """Remove MemberClass instance when person leaves the server."""
    if member.bot:
      return
    for m in self.dataCog.members:
      if m.id == member.id:
        print(f"{m.name} was deleted.")
        self.dataCog.deleteMemberByID(m.id)
        return
  
  @commands.Cog.listener('on_message')
  async def delete_messages(self,message):
    """delete Messages after 5s"""
    if message.author.bot:
      return
    #Loyalty and Skill lvl channel
    if message.channel.id != sv.channel.loyalty_And_skill_lvl:
      return
    try:
      await message.delete(delay=5)
    except:
      print('Message could not be deleted')


  @commands.Cog.listener('on_message')
  async def loy_skill_update(self,message):
    """Update Loyalty and/or skill lvl"""
    if message.author.bot:
      return
    #Loyalty and Skill lvl channel
    if message.channel.id != sv.channel.loyalty_And_skill_lvl:
      return
    msg = message.content.lower()
    #Check if input is for a banner account
    bannerInput = False
    bannerNames = self.dataCog.getBannerNames()
    if any(name.lower() in msg for name in bannerNames):
      bannerName = ''
      for b in bannerNames:
        if b.lower() in msg:
          bannerName = b
          bannerInput = True
          msg = msg.replace(b.lower(),'').strip()
          skLo = re.findall('[0-9]+', msg)
          break
    else:
      skLo = re.findall('[0-9]+', msg)
    skLoo = []
    for s in skLo:
      s = int(s)
      if (s < sv.skillCap and s > 0) or (s >= sv.loyalty_min and s <= sv.loyalty_max):
        skLoo.append(s)
    if len(skLoo) == 0:
      return # do nothing if no correct numbers are inserted
    #Get correct member instance
    if bannerInput:
      infoMsg = await message.channel.send(f"Working on your input {message.author.display_name} for the account: {bannerName}")
      #find banner Instance
      member = self.dataCog.getMemberByID(bannerName)
      if member == None:
        print('Error with ' + bannerName)
        return
    else:
      infoMsg = await message.channel.send(f"Working on your input {message.author.display_name}")
      #Find or create member
      member = self.dataCog.getMemberByID(message.author.id)
      if member == None:
        member = MemberClass(message.author)
        self.dataCog.members.append(member)
        print(f'Member {member.name} created.')

    for s in skLoo:
      if s<= sv.skillCap:
        #Update Skill lvl and post updated list
        print(member.skillData)
        updated, mes = member.updateSkill(newSkill=int(s))
        if updated:
          member.save()
          #Update Ranking
          embeds=mf.getRankingEmbeds(self.dataCog.members,'skill')
          try:
            oldMes = await message.channel.fetch_message(db[sv.db.skillRanking])
            await oldMes.edit(embeds=embeds)
          except:
            print("couldn't get old message")
          
            skillMes = await message.channel.send(embeds=embeds)
            db[sv.db.skillRanking] = skillMes.id
        #Post Personal Reply
        await message.channel.send(mes, delete_after = 30)

      elif s >= sv.loyalty_min and s <= sv.loyalty_max:
        #Offseason Message
        #await infoMsg.delete()
        #await message.channel.send("We do not have an active Reign of Chaos season so there is no way you need to update your loyalty right now.",delete_after = 30)
        #return
        #Update Loyalty and post updated list
        updated, mes = member.updateLoyalty(newLoyalty=int(s))
        if updated:
          member.save()
          #Update Ranking
          embeds=mf.getRankingEmbeds(self.dataCog.members,'loyalty')
          try:
            oldMes = await message.channel.fetch_message(db[sv.db.loyaltyRanking])
            await oldMes.edit(embeds=embeds)
          except:
            print("couldn't get old message")
          
            loyMes = await message.channel.send(embeds=embeds)
            db[sv.db.loyaltyRanking] = loyMes.id
        #Post Personal Reply
        await message.channel.send(mes, delete_after = 30)
    await infoMsg.delete()

  
  @commands.Cog.listener('on_message')
  async def help(self,message):
    """show help"""
    if message.author.bot:
      return
    #Loyalty and Skill lvl channel
    if message.channel.id != sv.channel.loyalty_And_skill_lvl:
      return
    #Help function
    if message.content.lower().startswith('help'):
      #Send Message
      sendText = "**Enter your current loyalty** (e.g. 3701) and/or your **current skill lvl** (e.g. 97) to update it. (Just the number is enough)\n*banner-name* **skill-lvl/loyalty** - to update skill lvl or loyalty your registered banner account enter it's name and then the number\nMore functions comming back soon"
      #\n**skill lvl above *XX*** - to get all players above *XX* skill lvl \n**loyalty above *XX*** - to get all players above *XX* loyalty\n**skill change since ** *dd.mm.yyyy* - show the change to the given date (also works for loyalty)\n**skill** *X* **days ago** - show the change to *X* days ago (also works for loyalty)\n**first at *X* loyalty** - shows a list with time difference of all that reached the loyalty compared to the first one (also works for skill lvl)\n**whose skill is missing?** - Remind players that haven't entered any skill lvl (works also for loyalty)\n**help** - This overview of all commands"
      
      try:
        helpMesID = db[sv.db.skLoHelp]
        oldMes = await message.channel.fetch_message(helpMesID)
        await oldMes.delete()
      except:
        print("couldn't delete old help message")
      
      helpMes = await message.channel.send(content=sendText)
      db[sv.db.skLoHelp] = helpMes.id
  
  


    
    

      


def setup(client: commands.Bot):
  client.add_cog(Members(client))