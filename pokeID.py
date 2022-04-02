# pokeID.py
import os
import random
import discord
import json
from discord.ext import commands
from dotenv import load_dotenv
from pokeList import poke_list

load_dotenv()
TOKEN = 'DISCORD_TOKEN'

with open("trainer_list.json", 'rb') as file:
    if file.read(2) != '{}':
        file.seek(0)
        trainer_dict = json.load(file)
    else:
        trainer_dict = {}

bot = commands.Bot(command_prefix='p~')
bot.remove_command('help')

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.command(name='wild')
async def wild(ctx):
    curr_pokemon = random.choice(poke_list)
    curr_png = poke_list.index(curr_pokemon) + 1
    curr_png = str(curr_png) + ".png"
    embed = discord.Embed()
    file = discord.File("./Poke_PNG/" + curr_png, filename = curr_png)
    embed.set_image(url="attachment://" + curr_png)

    await ctx.send(file=file, embed=embed)

    def check(msg):
        return msg.channel == ctx.channel
    
    msg = await bot.wait_for("message", check=check)
    msg_author = msg.author
    msg_author_str = str(msg_author)
    msg = msg.content.lower()
    msg = msg.capitalize()
    if msg == curr_pokemon:
        if msg_author_str in trainer_dict:
            if (msg_author_str, curr_pokemon) not in trainer_dict.items():
                trainer_dict[msg_author_str].append(curr_pokemon)
        else:
            trainer_dict[msg_author_str] = [curr_pokemon]
        await ctx.send("Correct! Congrats " + str(msg_author.mention) + ", you caught " + curr_pokemon + "!")
    else:
        await ctx.send("Wrong! Sorry the Pokemon got away!")
    
@bot.command(name='pokemon')
async def caught(ctx):
    trainer = str(ctx.author)
    if trainer in trainer_dict:
        pokemon_caught = str(len(trainer_dict[trainer]))
        response = "You've caught " + pokemon_caught + " Pokemon: " + str(trainer_dict[trainer]) + "\n"
        if pokemon_caught == "151":
            response += "Congrats! You've caught all original 151 Pokemon!"
        await ctx.send(response)
    else:
        await ctx.send("You haven't caught any Pokemon!")

@bot.command(name='help')
async def ayuda(ctx):
    response = "PokeID is a fun little game for you to guess the name of a random Pokemon in order for you to 'catch' it! PokeID currently only has the original 151 Pokemon and will soon have a battle feature!\n\n"
    response += "Here are the current commands:\n\n"
    response += "**p~wild**" + " will bring up a random Pokemon for you to guess. Careful though! Someone else can guess it and steal it! Or make it run away if they guess incorrectly... WARNING: pinging p~wild or sending a message without guessing the current Pokemon on screen will cause it to run away!\n\n"
    response += "**p~pokemon**" + " will bring up how many Pokemon you've caught so far. Try to catch all of the original 151 Pokemon!"

    await ctx.send(response)

@bot.command(name='save')
async def loading(ctx):
    global trainer_dict
    f = open("trainer_list.json", "r+") 
    f.seek(0) 
    f.truncate() 

    with open("trainer_list.json", "w") as file:
        json.dump(trainer_dict, file)


bot.run(TOKEN)
