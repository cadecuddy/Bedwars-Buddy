import asyncio
import discord
from discord import emoji
from discord.ext import commands
from discord.utils import get
from random import randrange
import bedwars
import config #Contains my API Key and Bot Token
import shop

TOKEN = config.bot_token
BOT_prefix = '.'
bot = commands.Bot(command_prefix=BOT_prefix)

@bot.event
async def on_ready():
	print("ONLINE as: " + bot.user.name + "\n")

def makeEmbeds(data, username, level):
    embedHome = discord.Embed(title=f"{username}'s Stats || Overall", description="==============================================" ,color=0xF9E5BC)
    embedHome.set_thumbnail(url=f"https://minotar.net/avatar/{username}")
    
    embedHome.add_field(name="Final K/D", value=f"{str(bedwars.getKD(data, 0))}", inline=True)
    embedHome.add_field(name="Bed Ratio", value=f"{str(bedwars.getBedRatio(data, 0))}", inline=True)
    embedHome.add_field(name="Wins", value=f"{bedwars.getStatMode(data, 'wins_bedwars', 0)}", inline=True)

    embedHome.add_field(name="Winstreak", value=f"{str(bedwars.getStatMode(data, 'winstreak', 0))}", inline=True)
    embedHome.add_field(name="Level", value=f"{str(level)}", inline=True)
    embedHome.add_field(name="Games Played", value=f"{str(bedwars.getStatMode(data, 'games_played_bedwars', 0))}", inline=True)
    
    embedSolos = discord.Embed(title=f"{username}'s Stats || Solos", description="==============================================" ,color=0xF9E5BC)
    embedSolos.set_thumbnail(url=f"https://minotar.net/avatar/{username}")

    embedSolos.add_field(name="Final K/D", value=f"{str(bedwars.getKD(data, 1))}", inline=True)
    embedSolos.add_field(name="Bed Ratio", value=f"{str(bedwars.getBedRatio(data, 1))}", inline=True)
    embedSolos.add_field(name="Wins", value=f"{bedwars.getStatMode(data, 'wins_bedwars', 1)}", inline=True)

    embedSolos.add_field(name="Winstreak", value=f"{str(bedwars.getStatMode(data, 'winstreak', 1))}", inline=True)
    embedSolos.add_field(name="Win Rate", value=f"{bedwars.getWinRatio(data,1)}%", inline=True)
    embedSolos.add_field(name="Games Played", value=f"{str(bedwars.getStatMode(data, 'games_played_bedwars', 1))}", inline=True)

    embedDuos = discord.Embed(title=f"{username}'s Stats || Duos", description="==============================================" ,color=0xF9E5BC)
    embedDuos.set_thumbnail(url=f"https://minotar.net/avatar/{username}")

    embedDuos.add_field(name="Final K/D", value=f"{str(bedwars.getKD(data, 2))}", inline=True)
    embedDuos.add_field(name="Bed Ratio", value=f"{str(bedwars.getBedRatio(data, 2))}", inline=True)
    embedDuos.add_field(name="Wins", value=f"{bedwars.getStatMode(data, 'wins_bedwars', 2)}", inline=True)

    embedDuos.add_field(name="Winstreak", value=f"{str(bedwars.getStatMode(data, 'winstreak', 2))}", inline=True)
    embedDuos.add_field(name="Win Rate", value=f"{bedwars.getWinRatio(data,2)}%", inline=True)
    embedDuos.add_field(name="Games Played", value=f"{str(bedwars.getStatMode(data, 'games_played_bedwars', 2))}", inline=True)

    embedTrios = discord.Embed(title=f"{username}'s Stats || 3v3v3v3s", description="==============================================" ,color=0xF9E5BC)
    embedTrios.set_thumbnail(url=f"https://minotar.net/avatar/{username}")

    embedTrios.add_field(name="Final K/D", value=f"{str(bedwars.getKD(data, 3))}", inline=True)
    embedTrios.add_field(name="Bed Ratio", value=f"{str(bedwars.getBedRatio(data, 3))}", inline=True)
    embedTrios.add_field(name="Wins", value=f"{bedwars.getStatMode(data, 'wins_bedwars', 3)}", inline=True)

    embedTrios.add_field(name="Winstreak", value=f"{str(bedwars.getStatMode(data, 'winstreak', 3))}", inline=True)
    embedTrios.add_field(name="Win Rate", value=f"{bedwars.getWinRatio(data,3)}%", inline=True)
    embedTrios.add_field(name="Games Played", value=f"{str(bedwars.getStatMode(data, 'games_played_bedwars', 3))}", inline=True)

    embedQuads = discord.Embed(title=f"{username}'s Stats || 4v4v4v4s", description="==============================================" ,color=0xF9E5BC)
    embedQuads.set_thumbnail(url=f"https://minotar.net/avatar/{username}")

    embedQuads.add_field(name="Final K/D", value=f"{str(bedwars.getKD(data, 4))}", inline=True)
    embedQuads.add_field(name="Bed Ratio", value=f"{str(bedwars.getBedRatio(data, 4))}", inline=True)
    embedQuads.add_field(name="Wins", value=f"{bedwars.getStatMode(data, 'wins_bedwars', 4)}", inline=True)

    embedQuads.add_field(name="Winstreak", value=f"{str(bedwars.getStatMode(data, 'winstreak', 4))}", inline=True)
    embedQuads.add_field(name="Win Rate", value=f"{bedwars.getWinRatio(data,4)}%", inline=True)
    embedQuads.add_field(name="Games Played", value=f"{str(bedwars.getStatMode(data, 'games_played_bedwars', 4))}", inline=True)

    return [embedHome, embedSolos, embedDuos, embedTrios, embedQuads]

@bot.command(pass_context=True, aliases=['bw', 'stats'])
async def getstats(ctx, username):
    print(f"{ctx.message.author} called the bot")
    if ctx.message.author.bot:
        return
    
    data = bedwars.getData(username)
    
    if "ERROR" not in data:
        level = data['achievements']['bedwars_level']
        data = data['stats']['Bedwars']
        buttons = ['🛏️', "1\N{COMBINING ENCLOSING KEYCAP}"
                        , "2\N{COMBINING ENCLOSING KEYCAP}"
                        , "3\N{COMBINING ENCLOSING KEYCAP}"
                        , "4\N{COMBINING ENCLOSING KEYCAP}"]
        current_page = 0

        bot.pages = makeEmbeds(data, username, level)
        msg =  await ctx.send(embed=bot.pages[current_page])

        for button in buttons:
            await msg.add_reaction(button)
        while True:
            try:
                reaction, user = await bot.wait_for("reaction_add", check=lambda reaction, user: user == ctx.author and reaction.emoji in buttons, timeout=9.5)

            except asyncio.TimeoutError:
                embed = bot.pages[current_page]
                await msg.delete()
                break
            else:
                previous_page = current_page
                current_page = buttons.index(reaction.emoji)

                await msg.remove_reaction(reaction.emoji, ctx.author)
                
                if current_page != previous_page:
                    await msg.edit(embed=bot.pages[current_page])
    else:
        embed=discord.Embed(title=f"Stats for {username}", description=str(data), color=0xF9E5BC)
        await ctx.send(embed=embed)

@bot.command(pass_context=True, aliases=['shop'])
async def getShop(ctx, username):
    print(f"{ctx.message.author} called the bot")

    if ctx.message.author.bot:
        return
    
    data = bedwars.getData(username)

    if "ERROR" not in data:
        data = data['stats']['Bedwars']

        if "favourites_2" in data:
            shop.createShopImage(data['favourites_2'])
            embed=discord.Embed(title=f"{username}'s Shop", color=0xF9E5BC)
            await ctx.send(embed=embed)
            await ctx.send(file=discord.File('shop.png'))

        else:
            embed=discord.Embed(title=f"{username}'s Shop", description=f"Couldn't find a shop for {username}", color=0xF9E5BC)
            await ctx.send(embed=embed)

    else:
        embed=discord.Embed(title=f"Stats for {username}", description=str(data), color=0xF9E5BC)
        await ctx.send(embed=embed)

bot.run(TOKEN)