##What is what
#main.py - starts the bot and in "sf.loadCogs(client)" all modules of the bot get loaded.
#modules can be found in the "modules" folder, there for every module a folder with its name exists which contains a "cog.py" file. This is the file that gets loaded. (only the exact spelling so if anything is added to the name it is not getting loaded)
#modules/mapHandler/data-cog.py - this cog is loaded initially and should contain all the data which is shared between different cogs (modules), e.g. Structures, Targets, Members...  ***** JAKE do you mean dataHandler?****
#The data of this can be accessed from anywhere by getting the cog instance "dataCog = client.get_cog('Data')"
#cog.py - a module of the bot that should contain all relevant code for this specific module
#classes - this folder contains custom classes, which are created to handle data, Dropdown Menus and Buttons.
#functions  - this folder contains function files which should be split so each file has only functions of a specific module/part of the bot, this is so they remain independent of each other and modules can be added/removed without effecting each other in a bad way
#functions/staticValues.py - here static values like database keys, Role-IDs, Channel-IDs... are stored so that changes on them can be done with jsut changing a single value and not having to go to all the different places where those values are accessed
#keep-alive.py - this file is to create a wegserver which can be pinged by "https://uptimerobot.com/" so the bot remains online even when this replit page is not currently opened by a user

### loving the comments!!!!!!  Just like a proper coder...
### Glad you like it, documentation is a pain in the ass though, so forgive me if I miss to comment everything but you are welcome to do what I missed ;) - Jake
import os
import nextcord
from keep_alive import keep_alive
from nextcord.ext import commands
import logging
from functions import setupFunc as sf

logging.basicConfig(level=logging.WARNING)

intents = nextcord.Intents.default()
intents.members = True
intents.reactions = True
client = commands.Bot(intents=intents, command_prefix="??")

sf.importStructureCSV()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


sf.loadCogs(client)


@client.listen('on_message')
async def on_message(message):
    msg = message.content.lower()
    if message.author == client.user or message.author.bot:
        return


keep_alive()
client.run(os.environ['TOKEN'])
