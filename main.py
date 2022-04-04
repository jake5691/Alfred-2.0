##What is what
#main.py - starts the bot and in "sf.loadCogs(client)" all modules of the bot get loaded.
#modules can be found in the "modules" folder, there for every module a folder with its name exists which contains a "cog.py" file. This is the file that gets loaded. (only the exact spelling so if anything is added to the name it is not getting loaded)
#modules/mapHandler/dataHandler.py - this cog is loaded initially and should contain all the data which is shared between different cogs (modules), e.g. Structures, Targets, Members... 
#The data of this can be accessed from anywhere by getting the cog instance "dataCog = client.get_cog('Data')"
#cog.py - a module of the bot that should contain all relevant code for this specific module
#classes - this folder contains custom classes, which are created to handle data, Dropdown Menus and Buttons.
#functions  - this folder contains function files which should be split so each file has only functions of a specific module/part of the bot, this is so they remain independent of each other and modules can be added/removed without effecting each other in a bad way
#functions/staticValues.py - here static values like database keys, Role-IDs, Channel-IDs... are stored so that changes on them can be done with jsut changing a single value and not having to go to all the different places where those values are accessed


import os
import nextcord
from nextcord.ext import commands
import logging
from functions import setupFunc as sf
from replit import db

logging.basicConfig(level=logging.WARNING)

intents = nextcord.Intents.default()
intents.members = True
intents.reactions = True
client = commands.Bot(intents=intents, command_prefix="?A")

#sf.importStructureCSV()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


sf.loadCogs(client)
#coms = client.get_all_application_commands()
#for com in coms:
#  print(f"{com.name} - {com.description}")

#@client.listen('on_message')
#async def on_message(message):
#  pass

@client.event
async def on_application_command_error(interaction, exception):
  print(f"{interaction.user.display_name} tried {interaction.application_command.qualified_name} on {interaction.guild.name} in {interaction.channel.name}:\n{exception}")


client.run(os.environ['TOKEN'])
