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
        print(guild.member_count)
        print(f'Guild Members:\n - {members}')
        print(f'\n')
    

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content == '!start':
        guild = message.guild
        
        category = next((cat for cat in guild.categories if cat.name == "Among Us"), None)
        if category == None: 
            await guild.create_category("Among Us")
            category = next((cat for cat in guild.categories if cat.name == "Among Us"), None)

        if not any(vc.name == "Among Us Lobby" for vc in guild.voice_channels):
            await guild.create_voice_channel("Among Us Lobby", category=category)
        if not any(vc.name == "Among Us Grave" for vc in guild.voice_channels):    
            await guild.create_voice_channel("Among Us Grave", category=category)

        await message.channel.send("A round of Among Us has begun. Shhhh!")


client.run(TOKEN)