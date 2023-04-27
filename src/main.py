from calendar import month_name
from threading import currentThread
from decouple import config
import discord
from discord import app_commands
from money_tracker import money_tracker as mt

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

#constant/setting
current_group = 0
group_count = 0
commands_dict = {}
ALLOWED_GUILDS = []
for guild_id in config("DISCORD_SERVER_IDS").split(","):
    ALLOWED_GUILDS.append(discord.Object(id=int(guild_id)))

@tree.command(name = "help", description = "help functions", guilds=ALLOWED_GUILDS)
async def help(interaction):
    result_string = 'Commands:\n'
    for key, value in commands_dict:
        result_string += f"/{key}: {value}\n"
    await interaction.response.send_message("Hello!")

@tree.command(name = "create", description = "help functions", guilds=ALLOWED_GUILDS)
async def create(interaction, names:str):
    names = names.strip().split(",")
    if mt.numbers() <= 5:
        key = str("money_group_" + str(group_count + 1))
        money_group_1 = mt(names)
        print(money_group_1)
        commands_dict["Sam"] = "Hsa"
        global group_count 
        # exec("money_group_" + str(mt.numbers() + 1) + " = mt(names)")
        # print(money_group_1)
        string = f"The group with {', '.join(names)} is created!\nCurrent count of the group is {current_group}"
    else:
        string = "Too many groups! Please delete some other groups to continue!"
    await interaction.response.send_message(string)

@client.event
async def on_ready():
    await tree.sync()
    print("Ready!")

client.run(config("DISCORD_TOKEN"))