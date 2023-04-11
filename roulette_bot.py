import discord
from discord.ext import commands
import random

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

TOKEN = 'YOUR BOT TOKEN'

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

# Dictionary to store user balances
user_balances = {}

# Function to check if a user has enough balance to place a bet
def check_balance(user_id, bet_amount):
    if user_id not in user_balances:
        user_balances[user_id] = 100
    if user_balances[user_id] < bet_amount:
        return False
    return True

# Command to place a bet on a specific number (0-36)
@bot.command(name="number_bet")
async def bet_number(ctx, number: int, bet_amount: int):
    try:
        user_id = ctx.author.id
        if not check_balance(user_id, bet_amount):
            await ctx.send(f"{ctx.author.mention}, you don't have enough balance to place this bet.")
            return
        if number < 0 or number > 36:
            await ctx.send(f"{ctx.author.mention}, please enter a number between 0 and 36.")
            return
        user_balances[user_id] -= bet_amount
        outcome_number, outcome_color = spin_roulette()
        if outcome_number == number:
            winnings = bet_amount * 36
            user_balances[user_id] += winnings
            await ctx.send(f"{ctx.author.mention}, the outcome is {outcome_number} {outcome_color}. You won {winnings} coins!. your balance is {user_balances[user_id]}")
        else:
            await ctx.send(f"{ctx.author.mention}, the outcome is {outcome_number} {outcome_color}. You lost {bet_amount} coins. your balance is {user_balances[user_id]}")
    except Exception as e:
        print(f"Error: {e}")
        await ctx.send(f"{ctx.author.mention}, an error occurred while processing your bet. Please try again later.")

@bot.command(name="color_bet")
async def bet_color(ctx, color: str, bet_amount: int):
    try:
        user_id = ctx.author.id
        if not check_balance(user_id, bet_amount):
            await ctx.send(f"{ctx.author.mention}, you don't have enough balance to place this bet.")
            return
        if color.lower() not in ['red', 'black']:
            await ctx.send(f"{ctx.author.mention}, please enter a valid color (red or black).")
            return
        user_balances[user_id] -= bet_amount
        outcome_number, outcome_color = spin_roulette()
        if (color.lower() == 'red' and outcome_color == 'red') or (color.lower() == 'black' and outcome_color == 'black'):
            winnings = bet_amount * 2
            user_balances[user_id] += winnings
            await ctx.send(f"{ctx.author.mention}, the outcome is {outcome_number} {outcome_color}. You won {winnings} coins!. your balance is {user_balances[user_id]}")
        else:
            await ctx.send(f"{ctx.author.mention}, the outcome is {outcome_number} {outcome_color}. You lost {bet_amount} coins. your balance is {user_balances[user_id]}")
    except Exception as e:
        print(f"Error: {e}")
        await ctx.send(f"{ctx.author.mention}, an error occurred while processing your bet. Please try again later.")


def spin_roulette():
    # define dictionary of roulette numbers and their colors
    roulette_numbers = {
        'red': [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36],
        'black': [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35],
        'green': [0]
    }
    
    # generate random outcome number between 0 and 36
    outcome_number = random.choice(range(37))
    
    # determine outcome color based on outcome number
    if outcome_number == 0:
        outcome_color = 'green'
    elif outcome_number in roulette_numbers['red']:
        outcome_color = 'red'
    else:
        outcome_color = 'black'
        
    # return tuple of outcome number and color
    return (outcome_number, outcome_color)

#help command
@bot.command(name="game_help")
async def help_command(ctx):
    help_message = """
    **Roulette Bot**
    
    This bot allows you to play roulette and bet on the outcome of the spin. You can place two types of bets:
    
    1. Number bet: You can bet on a specific number between 0 and 36. If the ball lands on your chosen number, you win 36 times your bet amount.
    Command: `!number_bet <number> <bet_amount>`
    Example: `!number_bet 17 10`
    
    2. Color bet: You can bet on either red or black. If the ball lands on your chosen color, you win 2 times your bet amount.
    Command: `!color_bet <color> <bet_amount>`
    Example: `!color_bet red 20`
    
    You start with 100 coins, and you can place bets as long as you have enough coins in your balance. Good luck!
    """
    await ctx.send(help_message)


#Running the bot
bot.run(TOKEN)