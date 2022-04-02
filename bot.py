# bot.py
import os
import random

import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.event
async def on_member_join(member):
    channel = bot.get_channel(895583116259885070)
    await channel.send(
        f'Hi {member.mention}, welcome to The Shop!'
    )

@bot.command(name='8ball')
async def ball(ctx):
    eight_ball = ['Yes', 'No', 'Maybe', 'Try asking later!', 'Uhhh....']
    await ctx.send(random.choice(eight_ball))

bot.run(TOKEN)