import discord
from discord import Interaction,app_commands
import random
from discord.ext import commands
from discord import app_commands
import asyncio
import time
import datetime
import re
from discord import app_commands, Interaction, Member

class Client(commands.Bot):
    async def on_ready(self):
        print(f"Logged in as {self.user} (ID: {self.user.id})")
    
        try:
            guild = discord.Object(id=1398401093809213504)
            synced =  await self.tree.sync()
            print(f'Synced {len(synced)} global command(s).')
        except Exception as e:
            print(f'Error syncing commands: {e}')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = Client(command_prefix = '!', intents=intents)



@bot.tree.command(name = "dice-roll", description= "Allows you to pick how many dice and roll (1-6)")
async def diceroll(interaction: discord.Interaction, amountofdice: int):
    if amountofdice < 1 or amountofdice > 6:
        await interaction.response.send_message("Please input a whole positive number from 1-6")
        return
    if amountofdice == 1:
        roll1 = random.randint(1, 6)
    if amountofdice == 2:
        roll1 = random.randint(2, 12)
    if amountofdice == 3:
        roll1 = random.randint(3, 18)
    if amountofdice == 4:
        roll1 = random.randint(4, 24)
    if amountofdice == 5:
        roll1 = random.randint(5, 30)
    if amountofdice == 6:
        roll1 = random.randint(1, 36)
    
    await interaction.response.send_message(f'You rolled {roll1}')

@bot.tree.command(name = "coin-flip", description="Flip a coin")
async def coinflip(interaction: discord.Interaction):
    whichside = random.randint(1, 2)
    if whichside == 1:
        side = "Heads"
    if whichside == 2:
        side = "Tails"
    interaction.response.send_message(f'{side} was flipped')


@bot.tree.command(name= "random-meme", description="Sends a random meme")
async def randommeme(interaction: discord.Interaction):
    memes = [
        "https://i.imgflip.com/a6wibc.jpg",
        "https://i.imgflip.com/2/a6whyi.jpg",
        "https://i.imgflip.com/2/a6whra.jpg",
        "https://i.imgflip.com/2/a6whez.jpg"
    ]
    thememe = random.choice(memes)
    await interaction.response.send_message(thememe)

@bot.tree.command(name="closer", description="Who can get closer to the number 1 to 100 inclusive")
async def closer(interaction: Interaction, yourguess: int, player2: Member):
    if player2 == interaction.user:
        await interaction.response.send_message("You can't challenge yourself")
        return
    if not 1 <= yourguess <= 100:
        await interaction.response.send_message("Pick a number between 1 and 100")
        return

    answer = random.randint(1, 100)
    await interaction.response.send_message(
        f'{interaction.user.mention} challenged {player2.mention} to a game of Closer (guess a number between 1-100)!')

    def check(m):
        return (
            m.author == player2 and 
            m.channel == interaction.channel and
            m.content.isdigit() and
            1 <= int(m.content) <= 100
        )

    try:
        guess2_msg = await bot.wait_for("message", check=check, timeout=30)
        guess2 = int(guess2_msg.content)

        diff1 = abs(answer - yourguess)
        diff2 = abs(answer - guess2)

        await interaction.followup.send(f'The target number was **{answer}**... drumroll please...')
        await asyncio.sleep(2)

        if diff1 < diff2:
            winner_msg = f"The winner is {interaction.user.mention} with a guess of {yourguess}!"
        elif diff2 < diff1:
            winner_msg = f"The winner is {player2.mention} with a guess of {guess2}!"
        else:
            winner_msg = "It's a tie! What are the odds?"

        await interaction.followup.send(winner_msg)

    except asyncio.TimeoutError:
        await interaction.followup.send("Game canceled: the other player took too long to guess.")

@bot.tree.command(name= "8-ball", description="Let all your questions be answered")
async def guesses(interaction: discord.Interaction, question: str):
    guess = [
        "It is certain",
        "It is decidedly so",
        "Without a doubt",
        "Yes definitely",
        "You may rely on it",
        "As I see it, yes",
        "Most likely",
        "Outlook good",
        "Yes",
        "Signs point to yes",
        "Reply hazy, try again",
        "Ask again later",
        "Better not tell you now",
        "Cannot predict now",
        "Concentrate and ask again",
        "Don't count on it",
        "My reply is no",
        "My sources say no",
        "Outlook not so good",
        "Very doubtful"
    ]
    truth = random.choice(guess)
    await interaction.response.send_message(f'{question} --- {truth}')



@bot.tree.command(name="math-battles", description="See who can solve the math problem faster")
async def mathbattles(interaction: discord.Interaction, player2: discord.Member):
    if player2 == interaction.user:
        await interaction.response.send_message("You can't challenge yourself!")
        return
    num1 = random.randint(1, 12)
    num2 = random.randint(1, 12)
    operator = random.choice(['+', '-', '*'])
    if operator == '+':
        answer = num1 + num2
    elif operator == '-':
        answer = num1 - num2
    else:
        answer = num1 * num2

    await interaction.response.send_message(f"{interaction.user} challenged {player2} to Math Battles!")
    time.sleep(1)
    await interaction.followup.send(f"{num1} {operator} {num2}")

    def check(m):
        return (
            m.author in [interaction.user, player2] and 
            m.channel == interaction.channel and 
            m.content.isdigit()
        )

    try:
        msg = await bot.wait_for("message", check=check, timeout=30)
    except asyncio.TimeoutError:
        await interaction.followup.send("No answer in time. Game cancelled.")
        return

    if int(msg.content) == answer:
        winner = msg.author
        await interaction.followup.send(f"Correct! The answer is {answer}. {winner.mention} wins the Math Battle!")
    else:
        await interaction.followup.send(f"Wrong answer. The correct answer was {answer}.")
   
@bot.tree.command(name= "reaction_duel", description="compete and see who can type the word faster")
@app_commands.choices(version =[
    app_commands.Choice(name= "Normal", value = "normal"),
    app_commands.Choice(name= "Hacklub", value = "hackclub")
])
async def reactword(interaction: discord.Interaction, challenger: discord.Member, version: str):
    normal = [
        "banana",
        "thunder",
        "lightning",
        "galaxy",
        "matrix",
        "cyber",
    ]
    hackclub = [
        "hacklub",
        "coding",
        "teens",
        "community",
        "Stickers",
        "Events"
        ]
    if version == "normal":
        word = random.choice(normal)
    if version == "hackclub":
        word = random.choice(hackclub)
    
    await interaction.response.send_message("Type the following word as fast as you can it will send in 1 to 10 seconds")
    sleeptime = random.randint(1, 10)
    await asyncio.sleep(sleeptime)
    await interaction.followup.send(f"{word}")

    def check(m):
        return (
            m.author in [interaction.user, challenger] and 
            m.channel == interaction.channel
        )
    
    try:
        msg = await bot.wait_for("message", check=check, timeout=30)
    except asyncio.TimeoutError:
        await interaction.followup.send("No answer in time. Game cancelled.")
        return
    
    if str(msg.content) == word:
        winner = msg.author
        await interaction.followup.send(f"Correct! The word was {word}. {winner.mention} wins the Reaction Duel")
        


@bot.tree.command(name="blackjack", description="Play a game of blackjack")
async def blackjack(interaction: discord.Interaction):
    your_total = random.randint(4, 21)
    dealer_first = random.randint(2, 11)

    await interaction.response.send_message(f'Your cards have a total value of {your_total}')
    await asyncio.sleep(1)
    await interaction.followup.send(f'The dealer\'s first card has a value of {dealer_first}')
    await asyncio.sleep(1)
    await interaction.followup.send("Would you like to **Hit** or **Stand**?")

    def check(m):
        return m.author == interaction.user and m.channel == interaction.channel

    try:
        msg = await bot.wait_for("message", check=check, timeout=30)
    except asyncio.TimeoutError:
        await interaction.followup.send("No answer in time. Game cancelled.")
        return

    # ---------------- Player loop ----------------
    while msg.content.lower() == "hit":
        new_card = random.randint(1, 10)
        your_total += new_card
        await interaction.followup.send(f"You draw a {new_card}. Your total is now {your_total}.")
        await asyncio.sleep(1)

        if your_total > 21:
            await interaction.followup.send("You busted! Dealer wins.")
            return
        elif your_total == 21:
            await interaction.followup.send("You got 21! Let's see what the dealer has...")
            break
        else:
            await interaction.followup.send("Would you like to **Hit** again or **Stand**?")
            try:
                msg = await bot.wait_for("message", check=check, timeout=30)
            except asyncio.TimeoutError:
                await interaction.followup.send("No answer in time. Game cancelled.")
                return

    # ---------------- Dealer's turn ----------------
    dealer_second = random.randint(1, 10)
    dealer_total = dealer_first + dealer_second
    await interaction.followup.send(
        f"The dealer's second card has a value of {dealer_second}, "
        f"making their total {dealer_total}."
    )
    await asyncio.sleep(1)

    while dealer_total < your_total and dealer_total < 22:
        await interaction.followup.send("The dealer decides to hit again...")
        next_card = random.randint(1, 10)
        dealer_total += next_card
        await asyncio.sleep(1)
        await interaction.followup.send(
            f"The dealer draws a card with value {next_card}, making their new total {dealer_total}."
        )

    # ---------------- Outcome ----------------
    if dealer_total > 21:
        await interaction.followup.send("The dealer busted! You win!")
    elif dealer_total == your_total:
        await interaction.followup.send("It's a tie!")
    elif dealer_total > your_total:
        await interaction.followup.send("The dealer has a higher total. You lose!")
    else:
        await interaction.followup.send("You win!")



@bot.tree.command(name="slots", description="Its a slot machine maybe you will get a cool role")
async def slots(interaction: discord.Interaction):
    emojis = [ "🍎", "🍊", "🍋", "🍉", "🍇", "🍓", "🍒",]
    slot1 = random.choice(emojis)
    slot2 = random.choice(emojis)
    slot3 = random.choice(emojis)
    await interaction.response.send_message(f'{slot1}|{slot2}|{slot3}')
    if slot1 == slot2 == slot3:
        role = discord.utils.get(interaction.guild.roles, name="Winner", color=discord.Color.gold())
        await interaction.followup.send("YOU WIN")
        if role is None:
            role = await interaction.guild.create_role(name="Winner", color=discord.Color.gold)
        await interaction.user.add_roles(role)
    else:
        await interaction.followup.send("Sorry your not a winner ")

@bot.tree.command(name="highs-or-lows", description="roll two dice will it roll lower(2-6) or high (8-12) or equal(7)")
@app_commands.choices(highlowequal =[
    app_commands.Choice(name= "High", value = "high"),
    app_commands.Choice(name= "Low", value = "low"),
    app_commands.Choice(name= "Equal", value = "equal")
])
async def highlow(interaction: discord.Interaction, highlowequal: str):
    roll1 = random.randint(1, 6)
    roll2 = random.randint(1, 6)
    total = roll1 + roll2
    await interaction.response.send_message(f'Your first die rolled a {roll1}')
    await asyncio.sleep(1)
    await interaction.followup.send(f'Your second die rolled a {roll2}')
    await interaction.followup.send(f'Your total is {total}')
    if total >= 8 and highlowequal == "high":
        await interaction.followup.send("You win")
    if total <= 6 and highlowequal == "low":
        await interaction.followup.send("You win")
    if total == 7 and highlowequal == "equal":
        role = discord.utils.get(interaction.guild.roles, name="Risky7", color=discord.Color.red())
        await interaction.followup.send("Dang you really risk it all and won that deserves somthing special")
        if role is None:
            role = await interaction.guild.create_role(name="Risky7", color=discord.Color.red())
        await interaction.user.add_roles(role)
bot.run('MTQxOTExMjE5ODI0ODMzMzM3Mg.G6dZGJ.PoEmJANZ2c9X7pPjYQMCbZlXqGYVJQA9WzL7l8')

