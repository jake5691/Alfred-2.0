import os
from nextcord.ext import commands, application_checks
from nextcord import Interaction, slash_command, SlashOption, Message

from functions import staticValues as sv
from functions import wordleFunc as wf


class Wordle(commands.Cog):
  """Play wordle"""

  def __init__(self, bot: commands.Bot):
    self.bot = bot
    self.command_variables = []
    self.feature_variables = []

  async def checkcheck(interaction):
    featureName = "Wordle"
    features = interaction.client.get_cog(sv.SETTINGS_COG).Features
    feature = next((x for x in features if x.name == featureName), None)
    #feature
    if feature == None:
      await interaction.response.send_message(f"**ERROR:** couldn't find the feature *{featureName}*, please reach out to the developers.", ephemeral=True)
      return False
    #enabled
    if not feature.isEnabled(interaction.guild.id):
      await interaction.response.send_message(f"This feature is not enabled on your server, please reach out to your Leaders for clarification.", ephemeral=True)
      return False
    #command
    command = next((x for x in feature.commands if x.name == interaction.application_command.qualified_name), None)
    if command == None:
      await interaction.response.send_message(f"**ERROR:** couldn't find the command *{interaction.application_command.qualified_name}*, please reach out to the developers.", ephemeral=True)
      return False
    #roles
    if not command.isAllowedByMember(interaction.guild.id, interaction.user):
      await interaction.response.send_message(f"You are not allowed to use this command *{command.name}*.", ephemeral=True)
      return False
    #channels
    if not command.isAllowedInChannel(interaction.guild.id, interaction.channel.id):
      await interaction.response.send_message(f"The command *{command.name}* is not allowed in this channel.", ephemeral=True)
      return False
    return True
    
  @slash_command(description="Play a game of Wordle Clone", guild_ids=sv.gIDS)
  @application_checks.check(checkcheck)
  async def playwordle(self,
      interaction: Interaction,
      language: str = SlashOption(
          description="Select the language you want to play (default = en)",required=False
      ),
      puzzle_id: int = SlashOption(
          description="Puzzle ID, leave out for a random puzzle", required=False
      ),
  ):
      # get language
      language = language.lower() if language != None else "en"
      if language not in wf.languages:
        await interaction.response.send_message("Please select an available language to play!", ephemeral=True)
        return
      # generate a puzzle
      puzzle_id = puzzle_id or wf.random_puzzle_id(language)
      # create the puzzle to display
      embed, keyboard = wf.generate_puzzle_embed(interaction.user, language, puzzle_id)
      # send the puzzle as an interaction response
      await interaction.response.send_message(embed=embed)
      await interaction.followup.send(file=keyboard)

  @playwordle.on_autocomplete("language")
  async def bannerName(self,interaction: Interaction, lang: str):
    if not lang:
        # send the full autocomplete list
        await interaction.response.send_autocomplete(wf.languages)
        return
    # send a list of nearest matches from the list of dog breeds
    get_near_lang = [
        langb for langb in wf.languages if langb.lower().startswith(lang.lower())
    ]
    await interaction.response.send_autocomplete(get_near_lang)

        
  @commands.Cog.listener('on_message')
  async def on_message(self,message: Message):
      """
      When a message is sent, check if it is a reply to the bot's message.
      If so, validate the guess and update the bot's message.
      """
      # get the message replied to
      ref = message.reference
      if not ref or not isinstance(ref.resolved, Message):
          return
      parent = ref.resolved

      # if the parent message is not the bot's message, ignore it
      if parent.author.id != self.bot.user.id:
          return
      if message.author == self.bot.user:
        return

      # check that the message has embeds
      if not parent.embeds:
          return
        
      embed = parent.embeds[0]
      # check that the embed is a wordle game
      if not("wordle" in embed.title.lower()):
        return
      

      guess = message.content.lower()

      # check that the user is the one playing
      if (
          embed.author.name != message.author.name
          or embed.author.icon_url != message.author.display_avatar.url
      ):
          reply = "Start a new game with /playwordle"
          if embed.author:
              reply = f"This game was started by {embed.author.name}. " + reply
          await message.reply(reply, delete_after=5)
          try:
              await message.delete(delay=5)
          except Exception:
              pass
          return

      # check that the game is not over
      if wf.is_game_over(embed):
        await message.reply("The game is already over. Start a new game with /playwordle", delete_after=5)
        puzzle_id = int(embed.footer.text.split()[1])
        if os.path.exists(f"keyboards/keyboard_{puzzle_id}.png"):
          os.remove(f"keyboards/keyboard_{puzzle_id}.png")
        async for m in parent.channel.history(limit=200,after=parent.created_at):
          if len(m.attachments) == 1:
            if m.attachments[0].filename == f"keyboard_{puzzle_id}.png":
              await m.delete()
        try:
            await message.delete(delay=5)
        except Exception:
            pass
        return

      # check that a single word is in the message
      if len(message.content.split()) > 1:
          await message.reply(
              "Please respond with a single 5-letter word.", delete_after=5
          )
          try:
              await message.delete(delay=5)
          except Exception:
              pass
          return

      # check that the word is valid
      language = embed.footer.text.split("︱")[1].strip()
      if not wf.is_valid_word(guess, language):
          await message.reply("That is not a valid word", delete_after=5)
          try:
              await message.delete(delay=5)
          except Exception:
              pass
          return

      # update the embed
      puzzle_id = int(embed.footer.text.split()[1])
      embed, keyboard = wf.update_embed(embed, guess)
    # send the puzzle as an interaction response
      await parent.edit(embed=embed)
      async for m in parent.channel.history(limit=200,after=parent.created_at):
        if len(m.attachments) == 1:
          if m.attachments[0].filename == f"keyboard_{puzzle_id}.png":
            await m.delete()
            if not(wf.is_game_over(embed)) and keyboard != None:
              await parent.reply(content=message.author.display_name,file=keyboard)
            os.remove(f"keyboards/keyboard_{puzzle_id}.png")
            break
            
      # attempt to delete the message
      try:
          await message.delete()
      except Exception:
          pass

def setup(bot: commands.Bot):
  bot.add_cog(Wordle(bot))