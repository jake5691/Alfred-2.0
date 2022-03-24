from nextcord.ext import commands
from functions import staticValues as sv

class Settings(commands.Cog):
  """Settings"""

  def __init__(self, bot: commands.Bot):
    self.bot = bot
    self.catName = "Alfred"
    self.chanName = "Overview"

  def isDev(ctx):
    userRoles = [i.id for i in ctx.author.roles]
    if not(sv.roles.Developers in userRoles):
      print(f"{ctx.author.display_name} is not allowed to use this.")
      return False
    return True
  
  @commands.command()
  @commands.check(isDev)
  async def settings(self, ctx):
    """Displaying of all Alfred variables"""
    #Random Reply
    aChannels = [sv.channel.migration_to_232, sv.channel.guests, sv.channel.eden_english, sv.channel.general]
    channels = ""
    for ca in aChannels:
      channels += f"<#{ca}>, "
    channels = channels[:-2]
    r = "**Random Reply**\n"
    r += f"*_channels_* = {channels}\n"
    r += "*_Keywords:_*\n"
    for k in sv.keywords:
      r += f"`{k}`, "
    r = r[:-2]
    r += "\n*_Replies_:*\n"
    for k in sv.reply:
      r += f"`{k}`, "
    r = r[:-2]
    await ctx.send(r)

    #coffee
    r = "**Coffee**\n"
    aChannels = [sv.channel.migration_to_232, sv.channel.guests, sv.channel.eden_english, sv.channel.general, sv.channel.guild_leadership]
    channels = ""
    for ca in aChannels:
      channels += f"<#{ca}>, "
    channels = channels[:-2]
    r += f"*_channels_* = {channels}"
    
    
    #reaction role
    r = "**Reaction roles**\n"
    for k in sv.reac:
      r += f"`{k}`, "
    r = r[:-2]
    await ctx.send(r)

    #Skill and Loyalty
    relR = ""
    for ro in sv.relRoles:
      relR += f"<@&{ro}>, "
    relR = relR[:-2]
    r = "**Skill and Loyalty**\n"
    r += f"relevant roles = {relR}\n"
    r += f"skillCap = `{sv.skillCap}`\n"
    r += f"min loyalty = `{sv.loyalty_min}`\n"
    r += f"max loyalty = `{sv.loyalty_max}`"
    await ctx.send(r)

    #Roles
    a = sv.roles()
    r = "**Roles**"
    pp = [ab for ab in dir(a) if not ab.startswith('__')]
    for p in pp:
      r += f"\n{p} = <@&{getattr(a, p)}>"
    #await ctx.send(r)

    #category
    a = sv.category()
    r = "**Categories**"
    pp = [ab for ab in dir(a) if not ab.startswith('__')]
    for p in pp:
      r += f"\n{p} = <#{getattr(a, p)}>"
    #await ctx.send(r)

    #channel
    a = sv.channel()
    r = "**Channels**"
    pp = [ab for ab in dir(a) if not ab.startswith('__')]
    for p in pp:
      r += f"\n{p} = <#{getattr(a, p)}>"
    #await ctx.send(r)


    ##commands
    commands = []
    arguments = []
    allowedRoles = []
    allowedChannels = []
    #availability
    commands.append("/startavailabilitysurvey")
    arguments.append(["interval"])
    allowedRoles.append([sv.roles.Leadership])
    allowedChannels.append([sv.channel.availability])
    
    commands.append("/evalavailability")
    arguments.append([])
    allowedRoles.append([sv.roles.Leadership])
    allowedChannels.append([sv.channel.availability])

    #banners
    commands.append("/newbanner")
    arguments.append(["name", "isflag", "owner"])
    allowedRoles.append([sv.roles.GuildMember, sv.roles.RBC])
    allowedChannels.append([sv.channel.banners])
    
    commands.append("/deletebanner")
    arguments.append([])
    allowedRoles.append([sv.roles.GuildMember, sv.roles.RBC])
    allowedChannels.append([sv.channel.banners])
    
    commands.append("/editbanner")
    arguments.append(["name", "isflag", "newname", "owner"])
    allowedRoles.append([sv.roles.GuildMember, sv.roles.RBC])
    allowedChannels.append([sv.channel.banners])
    
    commands.append("/changeflagspec")
    arguments.append(["member", "isflag"])
    allowedRoles.append([sv.roles.GuildMember, sv.roles.RBC])
    allowedChannels.append([sv.channel.banners])

    #evaluation
    commands.append("/rolemembers")
    arguments.append(["role"])
    allowedRoles.append([])
    allowedChannels.append([])

    commands.append("/exportrole")
    arguments.append(["role"])
    allowedRoles.append([sv.roles.Leadership])
    allowedChannels.append([])

    #Members
    commands.append("/updateloyskill")
    arguments.append(["member", "loyalty", "skill"])
    allowedRoles.append([sv.roles.Leadership])
    allowedChannels.append([sv.channel.loyalty_And_skill_lvl])
    
    #Seasons 
    commands.append("/createseason")
    arguments.append(["name", "type", "startyear", "startmonth", "startday", "endyear", "endmonth", "endday"])
    allowedRoles.append([sv.roles.Leadership])
    allowedChannels.append([sv.channel.test_channel])

    commands.append("/seasoncsv")
    arguments.append(["season"])
    allowedRoles.append([sv.roles.Leadership])
    allowedChannels.append([])

    #Targets 
    commands.append("/addtarget")
    arguments.append([])
    allowedRoles.append([sv.roles.Leadership, sv.roles.GuildLeader])
    allowedChannels.append([sv.channel.test_channel, sv.channel.strategy])
    
    commands.append("/listtargets")
    arguments.append([])
    allowedRoles.append([sv.roles.Leadership, sv.roles.GuildLeader])
    allowedChannels.append([sv.channel.test_channel, sv.channel.strategy])
    
    commands.append("/publishtargets")
    arguments.append(["infotext"])
    allowedRoles.append([sv.roles.Leadership, sv.roles.GuildLeader])
    allowedChannels.append([sv.channel.test_channel, sv.channel.strategy])
    
    commands.append("/edittargets")
    arguments.append([])
    allowedRoles.append([sv.roles.Leadership, sv.roles.GuildLeader])
    allowedChannels.append([sv.channel.test_channel, sv.channel.strategy])
    
    commands.append("/commenttarget")
    arguments.append(["comment"])
    allowedRoles.append([sv.roles.Leadership, sv.roles.GuildLeader])
    allowedChannels.append([sv.channel.test_channel, sv.channel.strategy])
    
    commands.append("/deletetargets")
    arguments.append([])
    allowedRoles.append([sv.roles.Leadership, sv.roles.GuildLeader])
    allowedChannels.append([sv.channel.test_channel, sv.channel.strategy])

    commands.append("/structureinfo")
    arguments.append(["structure", "avgdestruction", "private"])
    allowedRoles.append([])
    allowedChannels.append([])

    #Wordle 
    commands.append("/playwordle")
    arguments.append(["puzzle_id"])
    allowedRoles.append([])
    allowedChannels.append([])

    ##Publish the command
    print(len(commands))
    for idx, c in enumerate(commands):
      args = ""
      for a in arguments[idx]:
        args += f" *{a}*"
      roles = ""
      for r in allowedRoles[idx]:
        roles += f"<@&{r}>, "
      roles = roles[:-2]
      channels = ""
      for ca in allowedChannels[idx]:
        channels += f"<#{ca}>, "
      channels = channels[:-2]
      com = f"__{c}__{args}\n"
      com += f"allowed roles = {roles}\n"
      com += f"allowed channels = {channels}\n"
      await ctx.send(com)
    
    
    
    

def setup(bot: commands.Bot):
  bot.add_cog(Settings(bot))