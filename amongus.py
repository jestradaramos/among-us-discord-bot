#amongus.py
import os

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.all()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    for guild in client.guilds:
        print(
            f'{client.user} has connected to Discord!\n'
            f'{guild.name}(id: {guild.id})'
        )
        
        members = '\n -'.join([member.name for member in guild.members])
        print(f'Guild Members:\n - {members}')
        print(f'\n')
    

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content == '!start':
        await setup_and_start(message)

    if message.content == '!discuss':
        print('discuss')

    if message.content == '!dead':
        death(message)

    if message.content == '!spectator':
        print('spectator')

async def setup_and_start(message):
    guild = message.guild

    # Setting Up the Server for Among Us
    # Create a category and necessary voice channels
    category = next((cat for cat in guild.categories if cat.name == "Among Us"), None)
    if category == None: 
        await guild.create_category("Among Us")
        category = next((cat for cat in guild.categories if cat.name == "Among Us"), None)

    if not any(vc.name == "Among Us Lobby" for vc in guild.voice_channels):
        await guild.create_voice_channel("Among Us Lobby", category=category)
    if not any(vc.name == "Among Us Grave" for vc in guild.voice_channels):    
        await guild.create_voice_channel("Among Us Grave", category=category)

    # Create the dead role
    if not any(role.name == 'dead' for role in guild.roles):
        await guild.create_role(name="dead")

    # Mute Everyone in the Lobby
    vc = next((vc for vc in guild.voice_channels if vc.name == "Among Us Lobby"), None)
    if vc == None:
        print(f'error')
    for member in vc.members:
        await member.edit(mute=True)  
    
    await message.channel.send("A round of Among Us has begun. Shhhh!")

async def death(message):
    guild = message.guild
    role = next((r for r in guild.roles if r.name == "dead"))

    # Get all users
    dead = message.mentions
    for d in dead:
        d.edit(roles=role)

client.run(TOKEN)