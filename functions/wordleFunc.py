import random
import nextcord
import os
import requests
import json
from PIL import Image, ImageDraw, ImageFont, ImageColor

languages = ["en", "de"]
def popular_words(language: str): 
  return open(f"data/dict-popular-{language}.txt").read().splitlines()

def all_words(language: str):
  return set(word.strip().lower() for word in open(f"data/dict-valid-{language}.txt"))


EMOJI_CODES = {
    "green": {
        "a": "<:1f1e6:942044126717833256>",
        "b": "<:1f1e7:942044126214496278>",
        "c": "<:1f1e8:942044126218711102>",
        "d": "<:1f1e9:942044126810112070>",
        "e": "<:1f1ea:942044126512300083>",
        "f": "<:1f1eb:942044126323544145>",
        "g": "<:1f1ec:942044126638129162>",
        "h": "<:1f1ed:942044126587813919>",
        "i": "<:1f1ee:942044126579400775>",
        "j": "<:1f1ef:942044127070138368>",
        "k": "<:1f1f0:942044126420037743>",
        "l": "<:1f1f1:942044126394859571>",
        "m": "<:1f1f2:942044126675881984>",
        "n": "<:1f1f3:942044126600396840>",
        "o": "<:1f1f4:942044126646505502>",
        "p": "<:1f1f5:942044126701043782>",
        "q": "<:1f1f6:942044126763958272>",
        "r": "<:1f1f7:942044126650703932>",
        "s": "<:1f1f8:942044126717812806>",
        "t": "<:1f1f9:942044126709428264>",
        "u": "<:1f1fa:942044126898163722>",
        "v": "<:1f1fb:942044126713630730>",
        "w": "<:1f1fc:942044126768140341>",
        "x": "<:1f1fd:942044126302572585>",
        "y": "<:1f1fe:942044126726225970>",
        "z": "<:1f1ff:942044126801707098>",
        "ä": "<:1f1e6:942044126717833256>",
        "ö": "<:1f1f4:942044126646505502>",
        "ü": "<:1f1fa:942044126898163722>",
        "ß": "<:1f1f8:942044126717812806>",
    },
    "yellow": {
        "a": "<:1f1e6:942043527045603349>",
        "b": "<:1f1e7:942043527083348038>",
        "c": "<:1f1e8:942043526605201450>",
        "d": "<:1f1e9:942043526986887188>",
        "e": "<:1f1ea:942043526751989761>",
        "f": "<:1f1eb:942043526957514782>",
        "g": "<:1f1ec:942043526949126144>",
        "h": "<:1f1ed:942043526982692875>",
        "i": "<:1f1ee:942043526970081280>",
        "j": "<:1f1ef:942043527020437504>",
        "k": "<:1f1f0:942043527041413130>",
        "l": "<:1f1f1:942043527074955294>",
        "m": "<:1f1f2:942043526953324565>",
        "n": "<:1f1f3:942043527104311346>",
        "o": "<:1f1f4:942043526840062054>",
        "p": "<:1f1f5:942043527280476190>",
        "q": "<:1f1f6:942043527305633884>",
        "r": "<:1f1f7:942043527175618560>",
        "s": "<:1f1f8:942043527024627814>",
        "t": "<:1f1f9:942043527314018335>",
        "u": "<:1f1fa:942043527112712232>",
        "v": "<:1f1fb:942043527444066335>",
        "w": "<:1f1fc:942043527725088788>",
        "x": "<:1f1fd:942043526911393803>",
        "y": "<:1f1fe:942043527544729600>",
        "z": "<:1f1ff:942043527196573786>",
        "ä": "<:1f1e6:942043527045603349>",
        "ö": "<:1f1f4:942043526840062054>",
        "ü": "<:1f1fa:942043527112712232>",
        "ß": "<:1f1f8:942043527024627814>",
    },
    "gray": {
        "a": "<:1f1e6:942043898954530836>",
        "b": "<:1f1e7:942043898900021258>",
        "c": "<:1f1e8:942043899000680508>",
        "d": "<:1f1e9:942043898996478073>",
        "e": "<:1f1ea:942043899013255229>",
        "f": "<:1f1eb:942043898753187861>",
        "g": "<:1f1ec:942043898950328320>",
        "h": "<:1f1ed:942043898971308102>",
        "i": "<:1f1ee:942043898962911242>",
        "j": "<:1f1ef:942043899046793246>",
        "k": "<:1f1f0:942043898988093491>",
        "l": "<:1f1f1:942043898870661171>",
        "m": "<:1f1f2:942043899009048626>",
        "n": "<:1f1f3:942043899252318258>",
        "o": "<:1f1f4:942043899164262400>",
        "p": "<:1f1f5:942043898849673277>",
        "q": "<:1f1f6:942043899051008110>",
        "r": "<:1f1f7:942043899097120768>",
        "s": "<:1f1f8:942043899298472026>",
        "t": "<:1f1f9:942043899101327360>",
        "u": "<:1f1fa:942043899449475193>",
        "v": "<:1f1fb:942043899160035358>",
        "w": "<:1f1fc:942043899004846091>",
        "x": "<:1f1fd:942043899193606204>",
        "y": "<:1f1fe:942043899306860624>",
        "z": "<:1f1ff:942043899080347689>",
        "ä": "<:1f1e6:942043898954530836>",
        "ö": "<:1f1f4:942043899164262400>",
        "ü": "<:1f1fa:942043899449475193>",
        "ß": "<:1f1f8:942043899298472026>",
    },
}


def keyboard(puzzle_id=int,green:str="",yellow:str="",dark:str=""):
  """
  Generate a keyboard image with colored letters according to the previous guesses
  """
  #Image size
  x = 1024
  y = 512
  #keysize
  x_size = round(x/12)
  y_size = round(y/4)
  x_gap = round(2*x_size/11)
  y_gap = round(1*y_size/4)
  #letters
  row1 = ["Q","W","E","R","T","Y","U","I","O","P"]
  row2 = ["A","S","D","F","G","H","J","K","L"]
  row3 = ["Z","X","C","V","B","N","M"]
  #cornerRadius
  radius = 15
  #font
  font = ImageFont.truetype("data/arial/arial.ttf", 35)
  #colors
  gr = (59,188,45)
  ye = (238,201,15)
  da = (102,110,116)
  li = (200,200,200)

  with Image.new("RGB",(x,y)) as im:
    draw = ImageDraw.Draw(im)

    #Row1
    x0 = x_gap
    y0 = y_gap
    x1 = x0 + x_size
    y1 = y0 + y_size
    for i in range(10):
      col = li
      if row1[i].lower() in green.lower():
        col = gr
      elif row1[i].lower() in yellow.lower():
        col = ye
      elif row1[i].lower() in dark.lower():
        col = da
      draw.rounded_rectangle([x0, y0, x1, y1],radius=radius,fill=col)
      draw.text([(x0+x1)/2,(y0+y1)/2],text=row1[i],anchor="mm",font=font)
      x0 = x1+x_gap
      x1 = x0+x_size
    
    #Row2
    y0 = y1 + y_gap
    y1 = y0 + y_size
    x0 = 10 + round(x_size/2)
    x1 = x0 + x_size
    for i in range(9):
      col = li
      if row2[i].lower() in green.lower():
        col = gr
      elif row2[i].lower() in yellow.lower():
        col = ye
      elif row2[i].lower() in dark.lower():
        col = da
      draw.rounded_rectangle([x0, y0, x1, y1],radius=radius,fill=col)
      draw.text([(x0+x1)/2,(y0+y1)/2],text=row2[i],anchor="mm",font=font)
      x0 = x1+x_gap
      x1 = x0+x_size

    #Row3
    y0 = y1 + y_gap
    y1 = y0 + y_size
    x0 = 10 + round(x_size/2) + x_size + x_gap
    x1 = x0 + x_size
    for i in range(7):
      col = li
      if row3[i].lower() in green.lower():
        col = gr
      elif row3[i].lower() in yellow.lower():
        col = ye
      elif row3[i].lower() in dark.lower():
        col = da
      draw.rounded_rectangle([x0, y0, x1, y1],radius=radius,fill=col)
      draw.text([(x0+x1)/2,(y0+y1)/2],text=row3[i],anchor="mm",font=font)
      x0 = x1+x_gap
      x1 = x0+x_size
    dir = "keyboards"
    if not os.path.exists(dir):
        os.makedirs(dir)
    im.save(f"{dir}/keyboard_{puzzle_id}.png")
  img = nextcord.File(f"keyboards/keyboard_{puzzle_id}.png")
  return img

def getDefinition(word_id):
  """get definition of the solution word"""
  #get the base word
  language = "en"
  url= 'https://od-api.oxforddictionaries.com:443/api/v2/lemmas/' + language + '/' + word_id.lower()
  r = requests.get(url, headers = {"app_id": os.environ['OxfordAppID'], "app_key": os.environ['OxfordAppKey']})
  if r.status_code == 200:
    results = r.json()["results"][0]
    lexicalEntries = results["lexicalEntries"][0]
    inflectionOf = lexicalEntries["inflectionOf"][0]
    word_id = inflectionOf["id"]
  else:
    return None
  
  #get the definition
  language_codes = ["en-us","en-gb"]
  for language_code in language_codes:
    url = f"https://od-api.oxforddictionaries.com/api/v2/entries/{language_code}/{word_id.lower()}?fields=definitions&strictMatch=false"
    r = requests.get(url, headers = {"app_id": os.environ['OxfordAppID'], "app_key": os.environ['OxfordAppKey']})
    if r.status_code == 200:
      results = r.json()["results"][0]
      lexicalEntries = results["lexicalEntries"][0]
      entries = lexicalEntries["entries"][0]
      senses = entries["senses"][0]
      definition = senses["definitions"][0]
      return definition
      
  return None

def generate_colored_word(guess: str, answer: str) -> (str,[str],[str],[str]):
    """
    Builds a string of emoji codes where each letter is
    colored based on the key:
    - Same letter, same place: Green
    - Same letter, different place: Yellow
    - Different letter: Gray
    Args:
        word (str): The word to be colored
        answer (str): The answer to the word
    Returns:
        str: A string of emoji codes
    """
    colored_word = [EMOJI_CODES["gray"][letter] for letter in guess]
    guess_letters = list(guess)
    answer_letters = list(answer)
    green = []
    yellow = []
    dark = []
    # change colors to green if same letter and same place
    for i in range(len(guess_letters)):
      if guess_letters[i] == answer_letters[i]:
        green.append(guess_letters[i])
        colored_word[i] = EMOJI_CODES["green"][guess_letters[i]]
        answer_letters[i] = None
        guess_letters[i] = None
    # change colors to yellow if same letter and not the same place
    for i in range(len(guess_letters)):
      if guess_letters[i] is not None and guess_letters[i] in answer_letters:
        yellow.append(guess_letters[i])
        colored_word[i] = EMOJI_CODES["yellow"][guess_letters[i]]
        answer_letters[answer_letters.index(guess_letters[i])] = None
        guess_letters[i] = None
    # get the non matching letters
    for i in range(len(guess_letters)):
      if guess_letters[i] is not None:
        dark.append(guess_letters[i])
    green.sort()
    yellow.sort()
    dark.sort()
    return "".join(colored_word), green, yellow, dark


def generate_blanks() -> str:
    """
    Generate a string of 5 blank white square emoji characters
    Returns:
        str: A string of white square emojis
    """
    return "\N{WHITE MEDIUM SQUARE}" * 5


def generate_puzzle_embed(user: nextcord.User, language: str, puzzle_id: int) -> nextcord.Embed:
    """
    Generate an embed for a new puzzle given the puzzle id and user
    Args:
        user (nextcord.User): The user who submitted the puzzle
        puzzle_id (int): The puzzle ID
    Returns:
        nextcord.Embed: The embed to be sent
    """
    embed = nextcord.Embed(title="Wordle Clone")
    embed.description = "\n".join([generate_blanks()] * 6)
    embed.set_author(name=user.name, icon_url=user.display_avatar.url)
    embed.set_footer(
        text=f"ID: {puzzle_id} ︱{language}︱︱︱︱\n" 
        "To play, use the command /playwordle\n"
        "To guess, reply to this message with a word."
    )
    image = keyboard(puzzle_id,"","","")
    return embed, image


def update_embed(embed: nextcord.Embed, guess: str) -> nextcord.Embed:
    """
    Updates the embed with the new guesses
    Args:
        embed (nextcord.Embed): The embed to be updated
        puzzle_id (int): The puzzle ID
        guess (str): The guess made by the user
    Returns:
        nextcord.Embed: The updated embed
    """
    puzzle_id = int(embed.footer.text.split()[1])
    language = embed.footer.text.split("︱")[1].strip()
    green = list(embed.footer.text.split("︱")[2].strip())
    yellow = list(embed.footer.text.split("︱")[3].strip())
    dark = list(embed.footer.text.split("︱")[4].strip())
    answer = popular_words(language)[puzzle_id].lower()
    colored_word, g, y, d = generate_colored_word(guess, answer)
    for l in g:
      if l in green:
        continue
      green.append(l)
      if l in yellow:
        yellow.remove(l)
    for l in y:
      if l in green or l in yellow:
        continue
      yellow.append(l)
    for l in d:
      if l in dark:
        continue
      dark.append(l)
    empty_slot = generate_blanks()
    # replace the first blank with the colored word
    embed.description = embed.description.replace(empty_slot, colored_word, 1)
    # set footer
    embed.set_footer(
      text=f"ID: {puzzle_id} ︱{language}︱{''.join(green)}︱{''.join(yellow)}︱{''.join(dark)}︱\n" 
      "To play, use the command /playwordle\n"
      "To guess, reply to this message with a word."
    )
    image = keyboard(puzzle_id,"".join(green),"".join(yellow),"".join(dark))
    # check for game over
    num_empty_slots = embed.description.count(empty_slot)
    if guess == answer:
      image = None
      if num_empty_slots == 0:
          embed.description += "\n\nPhew!"
      if num_empty_slots == 1:
          embed.description += "\n\nGreat!"
      if num_empty_slots == 2:
          embed.description += "\n\nSplendid!"
      if num_empty_slots == 3:
          embed.description += "\n\nImpressive!"
      if num_empty_slots == 4:
          embed.description += "\n\nMagnificent!"
      if num_empty_slots == 5:
          embed.description += "\n\nGenius!"
      #get definition
      definition = getDefinition(answer)
      if definition != None:
        embed.description += f"\n**definition:** {definition}"
    elif num_empty_slots == 0:
      image = None
      embed.description += f"\n\nThe answer was {answer}!"
      #get definition
      definition = getDefinition(answer)
      if definition != None:
        embed.description += f"\n**definition:** {definition}"
    return embed, image


def is_valid_word(word: str, language: str) -> bool:
    """
    Validates a word
    Args:
        word (str): The word to validate
    Returns:
        bool: Whether the word is valid
    """
    return word in all_words(language)


def random_puzzle_id(language: str) -> int:
    """
    Generates a random puzzle ID
    Returns:
        int: A random puzzle ID
    """
    return random.randint(0, len(popular_words(language)) - 1)


def is_game_over(embed: nextcord.Embed) -> bool:
    """
    Checks if the game is over in the embed
    Args:
        embed (nextcord.Embed): The embed to check
    Returns:
        bool: Whether the game is over
    """
    return "\n\n" in embed.description



