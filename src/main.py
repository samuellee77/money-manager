from decouple import config
import discord
from discord import app_commands
from src.money_tracker import money_tracker as mt

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# constant/setting  
commands_dict = {}
ERROR_MESSAGE = "The money group does not exist"
ALLOWED_GUILDS = []
for guild_id in config("DISCORD_SERVER_IDS").split(","):
    ALLOWED_GUILDS.append(discord.Object(id=int(guild_id)))

@tree.command(name = "help", description = "help functions", guilds=ALLOWED_GUILDS)
async def help(interaction):
    result_string = 'Commands:\n'
    for key, value in commands_dict:
        result_string += f"/{key}: {value}\n"
    await interaction.response.send_message("Hello!")

@tree.command(name = "create", description = "create the money group with names", guilds=ALLOWED_GUILDS)
async def create(interaction, names:str):
    names = names.replace(" ", "").split(",")
    # if mt.numbers() <= 5:
    global money_group
    money_group =  mt(names)
    # current_group = mt.numbers()
    string = f"The group is created!\n{money_group}"
    # else:
    #     string = "Too many groups! Please delete some other groups to continue!"
    await interaction.response.send_message(string)

@tree.command(name = "delete", description= "delete the money group", guilds=ALLOWED_GUILDS)
async def delete(interaction):
    try:
        money_group.__del__()
        await interaction.response.send_message("The money group is deleted")
    except NameError:
        await interaction.response.send_message(ERROR_MESSAGE)

@tree.command(name = "add", description= "add an expense to the money group", guilds=ALLOWED_GUILDS)
async def add(interaction, expense_name: str, amount: int, payer: str, names: str):
    people = names.replace(" ", "").split(",")
    try:
        money_group.add_expense(expense_name, amount, people, payer)
        await interaction.response.send_message("Success!")
    except NameError:
        await interaction.response.send_message(ERROR_MESSAGE)
    except TypeError:
        await interaction.response.send_message("The types of the args are not correct")

@tree.command(name = "person_owed", description= "get the total amount owed by the person", guilds=ALLOWED_GUILDS)
async def person_owed(interaction, name: str):
    try:
        money_group.update()
        await interaction.response.send_message(f"{name} have to pay: {money_group.get_owed(name.strip())}")
    except NameError:
        await interaction.response.send_message(ERROR_MESSAGE)
    except TypeError:
        await interaction.response.send_message("The types of the args are not correct")

@tree.command(name = "pay_amount", description= "the payer pays the recipient with the amount of money", guilds=ALLOWED_GUILDS)
async def pay_amount(interaction, payer: str, recipient: str, amount: int):
    try:
        flag = money_group.pay(payer, recipient, amount)
        if flag:
            await interaction.response.send_message(f"Success! {recipient} received ${amount} from {payer}!")
        else:
            await interaction.response.send_message(f"Failed to do! Please send {money_group.get_owed(payer.strip())}, not {amount} to {recipient}!")
    except NameError:
        await interaction.response.send_message(ERROR_MESSAGE)
    except TypeError:
        await interaction.response.send_message("The types of the args are not correct")

@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=1032389114957418496))
    print("Ready!")

client.run(config("DISCORD_TOKEN"))