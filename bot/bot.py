import discord
import os  # Importe a biblioteca os
from dotenv import load_dotenv # Importe a função
from discord.ext import commands

load_dotenv()  # Carrega as variáveis de ambiente do arquivo .env



# --- CONFIGURAÇÃO BÁSICA DO BOT ---
intents = discord.Intents.default()
intents.message_content = True # Exemplo de intent
bot = commands.Bot(command_prefix='!', intents=intents)
BOT_TOKEN = os.getenv("DISCORD_TOKEN") # Coloque seu token aqui 