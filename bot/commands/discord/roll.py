import discord
import sys
import random
from bot import bot



@bot.tree.command()
async def roll(interaction: discord.Interaction, sides: int = 6, quantity: int = 1):
    """
    Comando que simula o lançamento de um dado.
    
    Args:
        sides (int): Número de lados do dado. Padrão é 6.
    """
    if sides < 1:
        await interaction.response.send_message("O número de lados deve ser pelo menos 1.")
        return
    if quantity < 1:
        await interaction.response.send_message("A quantidade de dados deve ser pelo menos 1.")
        return
    results = []
    for _ in range(quantity):
        result = random.randint(1, sides)
        results.append(result)
    
    await interaction.response.send_message(f"`{quantity}D{sides}` : `{results}`")

