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

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content == '!setup':
        await setup(message)

    if message.content == '!start':
        await start(message)

    if message.content == '!discuss':
        await discuss(message)

    if '!k' in message.content:
        await death(message)

    if message.content == '!cleanup':
        await clean(message)
    
    if message.content == '!restart':
        await restart(message)

async def setup(message):
    guild = message.guild

    # Setting Up the Server for Among Us
    # Create a category and necessary voice channels
    category = next((cat for cat in guild.categories if cat.name == "Among Us"), None)
    if category == None: 
        await guild.create_category("Among Us")
        category = next((cat for cat in guild.categories if cat.name == "Among Us"), None)

    if not any(vc.name == "Among Us Lobby" for vc in guild.voice_channels):
        await guild.create_voice_channel("Among Us Lobby", category=category)

    # Create the dead role
    if not any(role.name == 'dead' for role in guild.roles):
        await guild.create_role(name="dead")

    await message.channel.send("Set up complete. Please joing the Among Us Lobby")

async def start(message):
    guild = message.guild

    # Mute Everyone in the Lobby
    vc_lobby = next((vc for vc in guild.voice_channels if vc.name == "Among Us Lobby"), None)
    if vc_lobby == None:
        print(f'error')

    for member in vc_lobby.members:
        if any(r.name == "dead" for r in member.roles):
            await member.edit(mute=False) 
        else:
            await member.edit(deafen=True)
    
    await message.channel.send("A round of Among Us has begun. Shhhh!")

async def death(message):
    guild = message.guild
    role = next((r for r in guild.roles if r.name == "dead"), None)
    if role == None:
        print('error')

    # Get all users mentioned and mark as dead
    for d in message.mentions:
        await d.edit(mute=True)
        await d.add_roles(role)

async def discuss(message):
    guild = message.guild

    # Unmute Everyone in the Lobby
    vc_lobby = next((vc for vc in guild.voice_channels if vc.name == "Among Us Lobby"), None)
    if vc_lobby == None:
        print(f'error')

    for member in vc_lobby.members:
        if any(r.name == "dead" for r in member.roles):
            await member.edit(mute=True) 
        else:
            await member.edit(deafen=False)
    
    await message.channel.send("Discuss!")

async def restart(message):
    guild = message.guild

    # Unmute Everyone in the Lobby
    vc_lobby = next((vc for vc in guild.voice_channels if vc.name == "Among Us Lobby"), None)
    if vc_lobby == None:
        print(f'error')

    role = next((r for r in guild.roles if r.name == "dead"), None)
    if role == None:
        print('error')

    for member in vc_lobby.members:
        await member.edit(mute=False, deafen=False)
        await member.remove_roles(role)
    
    await message.channel.send("New Game!")

async def clean(message):
    guild = message.guild

    vc_lobby = next((vc for vc in guild.voice_channels if vc.name == "Among Us Lobby"), None)
    if vc_lobby == None:
        print(f'error')
    
    vc_grave = next((vc for vc in guild.voice_channels if vc.name == "Among Us Grave"), None)
    if vc_grave == None:
        print(f'error')

    role = next((r for r in guild.roles if r.name == "dead"), None)
    if role == None:
        print('error')
    
    category = next((c for c in guild.categories if c.name == "Among Us"), None)
    if role == None:
        print('error')

    await vc_lobby.delete()
    await vc_grave.delete()
    await role.delete()
    await category.delete()
    

client.run(TOKEN)