from decouple import config
import discord
from discord import app_commands
from src import money_tracker as mt

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@tree.command(name = "help", description = "help functions", guild=discord.Object(id=config("DISCORD_SERVER_IDS")))
async def help(interaction):
    await interaction.response.send_message("Hello!")

@tree.command(name = "create", description = "help functions", guild=discord.Object(id=config("DISCORD_SERVER_IDS")))
async def create(interaction):
    string = interaction.message
    await interaction.response.send_message(string)

@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=847413071714582528))
    print("Ready!")

client.run(config("DISCORD_TOKEN"))