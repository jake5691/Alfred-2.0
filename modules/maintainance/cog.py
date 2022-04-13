from nextcord.ext import commands
from nextcord.utils import get

from classes.Member import MemberClass

from functions import staticValues as sv


class Maintainance(commands.Cog):
  """Handle server maintainance, like welcomming members, waving goodby, assigning roles..."""

  def __init__(self, bot: commands.Bot):
    self.bot = bot
    self.dataCog = bot.get_cog('Data')
  
  @commands.Cog.listener('on_member_join')
  async def welcome_message(self,member):
    if member.bot:
      return
    newbie = get(member.guild.roles, id=sv.roles.Newbie)
    await member.add_roles(newbie)
    welChannel = get(member.guild.channels, id=sv.channel.welcome)
    genChannel = get(member.guild.channels, id=sv.channel.guests)
    lasChannel = get(member.guild.channels, id=sv.channel.loyalty_And_skill_lvl)
    avlChannel = get(member.guild.channels, id=sv.channel.availability)
    await genChannel.send(f"Welcome {member.display_name} to our Server, role assignment pending, please be patient.")
    flags = ''
    for fl in sv.reac:
      if fl != '⏰':
        flags += fl
    welMessage = f"Hey {member.mention}, welcome to **{member.guild.name}**!\n\n1) Please take the time to **change your server nickname** to reflect your in-game name. People that can not be mapped to players will be removed from the server eventually. You can do it by clicking your image and select manage, there you'll find the option to change nickname.\n\n2) Please **update** your current loyalty and skill lvl in {lasChannel.mention} channel. This information is crucial for planning building attacks, so help the leadership by keeping this information up to date.\n\n3) Please fill the {avlChannel.mention} poll, so we know when we can plan structures the best and make teams.\n\n4) React to this message to get:\n⏰ - Reminders to shield for KE, traiing hourlies, when super tickets are on sale in VIP shop and more\n{flags} - to get according translation channel."
    sentMsg = await welChannel.send(welMessage)
    for e in sv.reac:
      await sentMsg.add_reaction(e)
  
  @commands.Cog.listener('on_raw_reaction_add')
  async def translation_reminder_role_add(self,payload):
    """Add translation and reminder by reacting to a welcome message"""
    if payload.member.bot:
      return
    #Welcome Message Roles add
    if payload.channel_id == sv.channel.welcome:
      for r in sv.reac:
        if payload.emoji.name == r:
          if r == '⏰':
            role = get(payload.member.guild.roles, id=sv.roles.RemindMe)
          else:
            role = get(payload.member.guild.roles, name=r)
          await payload.member.add_roles(role)
          return
  
  @commands.Cog.listener('on_raw_reaction_remove')
  async def translation_reminder_role_remove(self,payload):
    """Remove translation and reminder by removing reaction to a welcome message"""
    guild = next ((x for x in self.bot.guilds if x.id == payload.guild_id), None)
    if guild == None:
      return
    member = get(guild.members, id = payload.user_id)
    if member == None:
      return
    if member.bot:
      return
    #Welcome Message Roles remove
    if payload.channel_id == sv.channel.welcome:
      for r in sv.reac:
        if payload.emoji.name == r:
          if r == '⏰':
            role = get(guild.roles, id=sv.roles.RemindMe)
          else:
            role = get(guild.roles, name=r)
          await member.remove_roles(role)
          return

  @commands.Cog.listener('on_member_update')
  async def change_name(self,old,new):
    """Recognize Players name changes and update them"""
    if old.bot:
      return
    if old.display_name == new.display_name:
      return
    member = self.dataCog.getMemberByID(old.id)
    member.name = new.display_name
    member.save()


  @commands.Cog.listener('on_member_update')
  async def add_delete_MemberInstance(self,old,new):
    """Add/Remove a MemberClass instance to dataCog.members when roles are assigned.
    
    Currently relevant roles are: RBC, Guild Member, Newbie"""
    if old.bot:
      return
    if old.roles == new.roles:
      return
    oldRoles = [r.id for r in old.roles]
    newRoles = [r.id for r in new.roles]
    relevantRoles = [sv.roles.RBC, sv.roles.GuildMember, sv.roles.Guest, sv.roles.Future_232]
    #remove newbie role if other role is assigned
    if (sv.roles.Newbie in oldRoles) and any(r in newRoles for r in relevantRoles):
      await new.remove_roles(get(old.roles, id=sv.roles.Newbie))

    #Remove translation roles for guests and future232
    if any(r in newRoles for r in [sv.roles.Guest, sv.roles.Future_232]):
      removeRoles = []
      for r in new.roles:
        if r.name in sv.reac:
          removeRoles.append(r)
      await new.remove_roles(removeRoles)
    
    relevantRoles = [sv.roles.RBC, sv.roles.GuildMember, sv.roles.Guest]
    #Add Member instance if role newbie, rbc, guild is assigned
    if not(any(r in oldRoles for r in relevantRoles)) and any(r in newRoles for r in relevantRoles):
      print('role assigned')
      m = MemberClass(new)
      m.save()
      self.dataCog.members.append(m)
    #Remove Member instance if no newbie, rbc, guild role anymore
    if any(r in oldRoles for r in relevantRoles) and not(any(r in newRoles for r in relevantRoles)):
      print('role removed')
      self.dataCog.deleteMemberByID(new.id)

  
  @commands.Cog.listener('on_member_remove')
  async def announce_leaving(self,member):
    """Announce leaving"""
    if member.bot:
      return
    
    #Announce leaving depending on the role the user had
    channelID = sv.channel.general
    roles = [r.id for r in member.roles]
    if sv.roles.RBC in roles:
      channelID = sv.channel.general
      pass
    elif sv.roles.GuildMember in roles:
      #Say goodby in #eden-english
      channelID = sv.channel.eden_english
    elif sv.roles.Guest in roles:
      #Say goodby in #guest
      channelID = sv.channel.guests
    farewellChannel = get(member.guild.channels, id=channelID)
    await farewellChannel.send(f"{member.display_name} just left our Server!")

    #Remove Member instance if any existed
    self.dataCog.deleteMemberByID(member.id)
    
    

      


def setup(bot: commands.Bot):
  bot.add_cog(Maintainance(bot))