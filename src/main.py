from decouple import config
import discord
from discord import app_commands
from src.money_tracker import money_tracker as mt

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# constant/setting
commands_dict = {
"/help_command": "help function",

"/create": "create the money group with the given names\nParam(s):\n\
\'names (str)\': the names should be in the group (need to be separated by comma!)",

"/delete": "delete the money group",

"/calculate": "calculate the price after tax and tip\nParams(s):\n\
\'amount (float)\': the original price\n\
\'tax_rate (float)\': the tax rate \n\
\'tip (float)\': the tip given",

"/add": "add the expense to the record\nParam(s):\n\
\'expense_name (str)\': the name of the expense\n\
\'amount (float)\': the amount of the expense\n\
\'names (str)\': the names who share this expense(need to be separated by comma!)\n\
\'payer (str)\': the person who pay this expense",

"/person_owed": "get the total amount owed by/to the person\nParam(s):\n\
\'name (str)\': the name of the person",

"/pay_amount": "the payer pays the recipient with the amount of money\nParam(s):\n\
\'payer (str)\': the person who pay his/her owed amount\n\
\'recipient (str)\': the person who should recieve the amount\n\
\'amount (float)\': the amount of the payment"
}

NONEXIST_ERROR_MESSAGE = "The money group does not exist"
BUG_MESSAGE = "BUGGGGGG!!!!!!!!!!!!!!!!"
ALLOWED_GUILDS = []
for guild_id in config("DISCORD_SERVER_IDS").split(","):
    ALLOWED_GUILDS.append(discord.Object(id=int(guild_id)))

@tree.command(name = "help_command", 
              description = "help functions\n", guilds=ALLOWED_GUILDS)
async def help_command(interaction):
    result_string = 'Commands:\n'
    for key, value in commands_dict.items():
        result_string += f"{key}: {value}\n\n"
    await interaction.response.send_message(result_string)

@tree.command(name = "create", description = "create the money group with names", guilds=ALLOWED_GUILDS)
async def create(interaction, names:str):
    names = names.replace(" ", "").split(",")
    global money_group
    money_group = mt(names)
    string = f"The group is created!\n{money_group}"
    await interaction.response.send_message(string)

@tree.command(name = "delete", description = "delete the money group", guilds=ALLOWED_GUILDS)
async def delete(interaction):
    try:
        money_group.__del__()
        await interaction.response.send_message("The money group is deleted")
    except NameError:
        await interaction.response.send_message(NONEXIST_ERROR_MESSAGE)
    except:
        await interaction.response.send_message(BUG_MESSAGE)
@tree.command(name = 'get_record', description = "get the record", guilds=ALLOWED_GUILDS)
async def get_record(interaction):
    await interaction.response.send_message(str(money_group.expenses))

@tree.command(name = 'get_payment', description = "get the payment record", guilds=ALLOWED_GUILDS)
async def get_payment(interaction):
    await interaction.response.send_message(str(money_group.members_payment))

@tree.command(name = "calculate", description = "calculate the price after tax and tip", guilds=ALLOWED_GUILDS)
async def calculate(interaction, amount: float, tax_rate: float, tip: float):
    try:
        await interaction.response.send_message(str(money_group.price_after_tax_and_tip(amount, tax_rate, tip)))
    except NameError:
        await interaction.response.send_message(NONEXIST_ERROR_MESSAGE)
    except:
        await interaction.response.send_message(BUG_MESSAGE)

@tree.command(name = "add", description= "add an expense to the money group", guilds=ALLOWED_GUILDS)
async def add(interaction, expense_name: str, amount: float, names: str, payer: str):
    people = names.replace(" ", "").split(",")
    try:
        money_group.add_expense(expense_name, amount, people, payer)
        money_group.update()
        string = ", ".join(people)
        await interaction.response.send_message(f"Success!\n{expense_name}: {str(amount)}, shared by {string} and paid by {payer}, is stored!")
    except NameError:
        await interaction.response.send_message(NONEXIST_ERROR_MESSAGE)
    except:
        await interaction.response.send_message(BUG_MESSAGE)

@tree.command(name = "person_owed", description= "get the total amount owed by the person", guilds=ALLOWED_GUILDS)
async def person_owed(interaction, name: str):
    try:
        await interaction.response.send_message(f"{name} have to pay/receive: {money_group.get_owed(name.strip())}")
    except NameError:
        await interaction.response.send_message(NONEXIST_ERROR_MESSAGE)
    except:
        await interaction.response.send_message(BUG_MESSAGE)

@tree.command(name = "pay_amount", description= "the payer pays the recipient with the amount of money", guilds=ALLOWED_GUILDS)
async def pay_amount(interaction, payer: str, recipient: str, amount: float):
    try:
        flag = money_group.pay(payer, recipient, amount)
        if flag:
            await interaction.response.send_message(f"Success! {recipient} received ${amount} from {payer}! The record has been cleared!")
        else:
            await interaction.response.send_message(f"Failed to do! Please send {money_group.get_owed(payer.strip())}, not {amount} to {recipient}!")
    except NameError:
        await interaction.response.send_message(NONEXIST_ERROR_MESSAGE)
    except:
        await interaction.response.send_message(BUG_MESSAGE)

@client.event
async def on_ready():
    await tree.sync(guild=ALLOWED_GUILDS[1])
    print("Ready!")

client.run(config("DISCORD_TOKEN"))
