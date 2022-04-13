from replit import db
from nextcord.ext import commands, application_checks
from nextcord import Interaction, slash_command
import jsons

from classes.SettingsView import SettingsView
from classes.Settings import Feature, Command
from functions import staticValues as sv
from functions import setupFunc as sf

class Settings(commands.Cog):
  """Settings"""

  def __init__(self, bot: commands.Bot):
    self.bot = bot
    self.Features = sf.allFeatures()

  @commands.Cog.listener('on_ready')
  async def on_ready(self):
    """load/set default settings for all servers where Alfred is present"""
    commands_ = self.bot.get_all_application_commands()
    commands_grouped = {}
    for c in commands_:
      group = c.self_argument.qualified_name
      if group in commands_grouped:
        commands_grouped[group].append(c)
      else:
        commands_grouped[group] = [c]
        
    #Get all Features and commands that are in the bot
    for g in commands_grouped:
      f = next((x for x in self.Features if x.name == g), None)
      if f == None:
        f = Feature(g, self.bot.cogs[g].description, f"feature{g}")
        self.Features.append(f)
      else:
        f.description = self.bot.cogs[g].description
      for c in commands_grouped[g]:
        co = next((x for x in f.commands if x.name == c.name), None)
        if co == None:
          co = Command(c.name, c.description, "Slash Command")
          f.commands.append(co)
        else:
          co.description = c.description
          
    #Check for db entries that no longer are a feature
    toDelete = []
    for idx, f in enumerate(self.Features):
      if f.name not in commands_grouped and f.name != "Fun":
        del db[f.dbKey]
        toDelete.append(idx)
    for idx in toDelete:
      del self.Features[idx]
        
    #Make sure default values for all guilds are set 
    for guild in self.bot.guilds:
      for f in self.Features:
        if guild.id not in f.enabled:
          f.enabled[guild.id] = False #set feature per default to False
          db[f.dbKey] = jsons.dumps(f)
          #print(f"{guild.name} has {f.name} values NOT stored")
        for c in f.commands:
          if guild.id not in c.allowedChannels:
            c.allowedChannels[guild.id] = []
            db[f.dbKey] = jsons.dumps(f)
          if guild.id not in c.excludedChannels:
            c.excludedChannels[guild.id] = []
            db[f.dbKey] = jsons.dumps(f)
          if guild.id not in c.allowedRoles:
            c.allowedRoles[guild.id] = []
            db[f.dbKey] = jsons.dumps(f)
          if guild.id not in c.excludedRoles:
            c.excludedRoles[guild.id] = []
            db[f.dbKey] = jsons.dumps(f)

  async def checkcheck(interaction):
    featureName = "Settings"
    features = interaction.client.get_cog(sv.SETTINGS_COG).Features
    feature = next((x for x in features if x.name == featureName), None)
    #feature
    if feature == None:
      await interaction.send(f"**ERROR:** couldn't find the feature *{featureName}*, please reach out to the developers.", ephemeral=True)
      return False
    #enabled
    #if not feature.isEnabled(interaction.guild.id):
    #  await interaction.send(f"This feature is not enabled on your server, please reach out to your Leaders for clarification.", ephemeral=True)
    #  return False
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


  @slash_command(name="settings",
                      guild_ids=sv.gIDS)
  @application_checks.check(checkcheck)
  async def settingsSlashCommand(self, interaction: Interaction):
    """
    View and change the settings for Alfred and all his features and commands.
    """
    await interaction.send("**Settings**\nSelect the feature you want to view.", view=SettingsView(self.Features, interaction.guild), ephemeral=True)
    
  def isDev(ctx):
    userRoles = [i.id for i in ctx.author.roles]
    if not(sv.roles.Developers in userRoles):
      print(f"{ctx.author.display_name} is not allowed to use this.")
      return False
    return True
  
  @commands.command()
  @commands.check(isDev)
  async def setting(self, ctx):
    """Displaying of all Alfred variables"""
    commands_ = self.bot.get_all_application_commands()
    for cog in self.bot.cogs:
      print(cog)
      cog = self.bot.cogs[cog]
      for command in cog.get_commands():
        print(f" {command}")
    return
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