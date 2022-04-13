from nextcord.ext import commands, application_checks
from nextcord import Interaction, slash_command, SlashOption, User
import re
from replit import db
from nextcord.utils import get
from datetime import datetime, timedelta, timezone

from classes.Member import MemberClass

from functions import staticValues as sv
from functions import memberFunc as mf


class Members(commands.Cog):
  """Manage the member instances, keeping loyalty and skill lvl up to date..."""

  def __init__(self, client: commands.Bot):
    self.client = client
    self.dataCog = client.get_cog('Data')

  async def checkcheck(interaction):
    featureName = "Members"
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
    
  @commands.Cog.listener('on_member_update')
  async def add_delete_MemberInstance(self,old,new):
    """Add/Remove a MemberClass instance to dataCog.members when roles are assigned.
    Currently relevant roles are: RBC, Guild Member, Newbie"""
    if old.roles == new.roles:
      return
    oldRoles = [r.id for r in old.roles]
    newRoles = [r.id for r in new.roles]
    #Added/removed a relevant role -> create/delete Member instance
    if not(any(r in oldRoles for r in sv.relRoles)) and any(r in newRoles for r in sv.relRoles):
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
    elif any(r in oldRoles for r in sv.relRoles) and not(any(r in newRoles for r in sv.relRoles)):
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
  @application_checks.check(checkcheck)
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

  
  @commands.Cog.listener('on_ready')
  async def on_ready(self):
    """Read missed messages"""
    guild = None
    for g in self.client.guilds:
      if g.id == sv.gIDS[0]:
        guild = g
        break
    loySkillChannel = get(guild.channels, id=sv.channel.loyalty_And_skill_lvl)
    if loySkillChannel == None:
      return
    async for message in loySkillChannel.history(limit=200,oldest_first=True):
      if message.author.bot:
        #Skip if message is from a bot
        continue
      #print(f"{message.author.display_name}: {message.content}")
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
        await message.delete()
        return # do nothing if no correct numbers are inserted
      #Get correct member instance
      if bannerInput:
        #find banner Instance
        member = self.dataCog.getMemberByID(bannerName)
        if member == None:
          print('Error with ' + bannerName)
          await message.delete()
          return
      else:
        #Find or create member
        member = self.dataCog.getMemberByID(message.author.id)
        if member == None:
          member = MemberClass(message.author)
          self.dataCog.members.append(member)
          print(f'Member {member.name} created.')
  
      for s in skLoo:
        if s<= sv.skillCap:
          #Update Skill lvl and post updated list
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
      await message.delete()


  
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
    #First to reach certain lvl/Loyalty and time diff of the rest to get there
    elif "first at" in msg:
      skLo = re.findall('[0-9]+', msg)
      if any(word in msg for word in ["skill", "spec"]):
        typ = "skill"
      elif any(word in msg for word in ["loyalty"]):
        typ = "loyalty"
      else:
        await message.channel.send("Cannot process your Input",delete_after = 30)
        await message.delete()
        return
      if len(skLo) != 1:
        await message.channel.send("Cannot process your Input",delete_after = 30)
        await message.delete()

      for e in mf.getFirstAbove(self.dataCog.members,int(skLo[0]),typ):
        await message.channel.send(embed=e,delete_after=300)
      return
        
    #Loyalty/skill Ranking above certain lvl
    elif any(word in msg for word in ["above", ">","higher","greater"]):
      if any(word in msg for word in ["skill", "spec"]):
        typ = "skill"
      elif any(word in msg for word in ["loyalty"]):
        typ = "loyalty"
      else:
        await message.channel.send("Cannot process your Input",delete_after = 30)
        await message.delete()
        return
      skLo = re.findall('[0-9]+', msg)
      if len(skLo) == 1:
        embeds = mf.getRankingEmbeds(self.dataCog.members, typ, above=int(skLo[0]))
        #Post Ranking
        for e in embeds:
          await message.channel.send(embed=e, delete_after = 240)
      else:
        print('Unprocessable message: ' + msg)
      return
      
    #Compare skill/loyalty to old data
    elif any(k in msg for k in ['since','compare','ago','change']):
      typ = ''
      skLo = re.findall('[0-9]+', msg)
      #which typ to compare 
      if any(l in msg for l in ['skill','spec']):
        typ = 'skill'
      elif any(l in msg for l in ['loyalty']):
        typ = 'loyalty'
      else:
        await message.channel.send('Sorry cannot process your input, please use a correct request. Type Help to get more information', delete_after = 20)
        await message.delete()
        return
      if len(skLo) == 3:
        #Date was given
        if len(skLo[2]) == 2:
          skLo[2] = '20' + skLo[2]
        try:
          t = datetime(int(skLo[2]), int(skLo[1]), int(skLo[0]), tzinfo=timezone.utc)
        except:
            try:
              t = datetime(int(skLo[2]), int(skLo[0]), int(skLo[1]), tzinfo=timezone.utc)
            except:
              await message.channel.send('Sorry cannot process your input, please use a correct date format **dd.mm.yyyy**', delete_after = 45)
              await message.delete()
              return
      elif len(skLo) == 1:
        #Number of days was given
        now = datetime.now((timezone.utc))
        t = now - timedelta(days = int(skLo[0]), hours=now.hour, minutes=now.minute)
      else:
        await message.channel.send('Sorry cannot process your input, please use a correct date format **dd.mm.yyyy**', delete_after = 45)
        await message.delete()
        return
      res = mf.getRankingEmbeds(self.dataCog.members, typ, progressSince=t)
      for e in res:
        await message.channel.send(embed=e,delete_after=300)
      return
      
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
      #infoMsg = await message.channel.send(f"Working on your input {message.author.display_name} for the account: {bannerName}")
      #find banner Instance
      member = self.dataCog.getMemberByID(bannerName)
      if member == None:
        print('Error with ' + bannerName)
        return
    else:
      #infoMsg = await message.channel.send(f"Working on your input {message.author.display_name}")
      #Find or create member
      member = self.dataCog.getMemberByID(message.author.id)
      if member == None:
        member = MemberClass(message.author)
        self.dataCog.members.append(member)
        print(f'Member {member.name} created.')

    for s in skLoo:
      if s<= sv.skillCap:
        #Update Skill lvl and post updated list
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
    #await infoMsg.delete()

  
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
      sendText = "**Enter your current loyalty** (e.g. 3701) and/or your **current skill lvl** (e.g. 97) to update it. (Just the number is enough)\n*banner-name* **skill-lvl/loyalty** - to update skill lvl or loyalty your registered banner account enter it's name and then the number\nMore functions comming back soon\n**skill lvl above *XX*** - to get all players above *XX* skill lvl \n**loyalty above *XX*** - to get all players above *XX* loyalty\n**skill change since ** *dd.mm.yyyy* - show the change to the given date (also works for loyalty)\n**skill** *X* **days ago** - show the change to *X* days ago (also works for loyalty)\n**first at *X* loyalty** - shows a list with time difference of all that reached the loyalty compared to the first one (also works for skill lvl)\n**help** - This overview of all commands"
      #\n**whose skill is missing?** - Remind players that haven't entered any skill lvl (works also for loyalty)\n**help** - This overview of all commands"
      
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