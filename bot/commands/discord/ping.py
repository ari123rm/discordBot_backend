import discord
from bot import bot

@bot.tree.command()
async def ping(interaction: discord.Interaction):
    """Comando de teste que responde com 'Pong!'."""
    await interaction.response.send_message("Pong!")