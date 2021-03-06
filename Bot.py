import discord, discord.utils
from discord.ext import commands
from discord.utils import get
from Functions import getdiscord, key

#TODO Implement Guild Role check
#Discord Key used to run the Bot
KEY = key.key()
#The Prefix of the Bot
PREFIX = "v!"
#The Role it gives People 
ROLE = "Hypixel Verified"



# Sets Command Prefix 
client = commands.Bot(command_prefix = PREFIX)

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game("https://github.com/Lulonaut/Hypixel-Verify"))
    print("Ready")

@client.command()
async def verify(ctx, name):
    #defines Member
    member = ctx.message.author
    #trys getting Output
    rank = None
    nickname = None
    guildrole = None
    grole = None
    Output = None

    Output = getdiscord.discordlinked(name)
    rank = getdiscord.rank(name)
    nickname = getdiscord.name(name)
#    guildrole = getdiscord.guild(name)
    
    if Output == "API_ERROR":
        #Abort
        await ctx.send("There was an Error while contacting the API, please try again later or contact an Admin!")
        pass
    elif Output == "DISCORD_ERROR":
        #Abort
        await ctx.send(f"There is currently no Discord linked to the IGN: {name}. If you just updated it in game, try again in a few minutes!")
        pass
    if rank == "RANK_ERROR":
        #Continue without Rank info
        await ctx.send("There was an Error while getting your rank info, maybe you are a Staff Member?")
    
    if name == "NAME_ERROR":
        #Abort
        print("There was an Error getting your Name, try again and if this keeps happening contact an Admin")
        pass


    member2 = str(member).replace("#", "")
    Output2 = str(Output).replace("#", "")

    if member2 == Output2 and ROLE != None:
        role = None
        rankrole = None
        try:
            role = discord.utils.get(ctx.guild.roles, name=ROLE)
            rankrole = discord.utils.get(ctx.guild.roles, name=rank)
#            grole = discord.utlis.get(ctx.guild.roles, name = "Guild Member")
        except:
            pass
        try:
            await member.add_roles(role)
            await member.add_roles(rankrole)
#            if guildrole == True:
#                await member.add_roles(grole)
            
        except:
            pass
        try:
            await member.edit(nick = nickname)
            await ctx.send(f"You now have the Role `{ROLE}` and i changed your Nickname")
        except:
            await ctx.send("Sorry, i cant change your Nickname :( Maybe you have higher permissions than me?")
        

    elif Output2 == "Error":
        await ctx.send("Something went wrong, please try again! If this keeps happening the Api is probably down.")
        


    elif Output2 != member2 and ROLE != None:
        await ctx.send(f"The current Discord set on the Account `{Output}` doesnt match your discord name `{member}`. If you just changed wait a few minutes and try again.")
    
    else:
        await ctx.send("Error, maybe try again in a bit")

client.run(KEY)
