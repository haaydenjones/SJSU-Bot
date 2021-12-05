from re import search
import discord
import json
import os
import DiscordUtils
from discord import member
from discord import user
from discord.ext import commands
from discord.flags import Intents


client = commands.Bot(command_prefix='!')
os.chdir(r'C:\Users\15623\Desktop\Code Projects\BOT')
music = DiscordUtils.Music()

@client.event
async def on_ready():
    print('bot is ready!')

#Welcoming
@client.event()
async def on_member_join():
    server = client.get_guild('827023107557556264')
    welcome_channel = client.get_channel('827030397358702652')
    intros = client.get_channel('827030448660152340')
    await welcome_channel.send(f"Welcome to the SJSU '25 Discord, {user.mention}! Please go to {intros.mention} and introduce yourself in order to access the rest of the server!")

#General Moderation

#kicks
@client.command()
async def kick(ctx, member: discord.Member, *, reason=None):
    if (not ctx.author.guild_permissions.manage_messages):
        await ctx.send('Get some perms first, bud')
    await member.kick(reason=reason)

#bans
@client.command()
async def ban(ctx, member: discord.Member, *, reason=None):
    if (not ctx.author.guild_permissions.manage_messages):
        await ctx.send('Get some perms first, bud')
    await member.ban(reason=reason)

#Unbans
@client.command(aliases = ['redemption'])
async def unban(ctx, member: discord.Member):
    if (not ctx.author.guild_permissions.manage_messages):
        await ctx.send('Get some perms first, bud')
    bannedUser = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban in bannedUser:
        user = ban.user

        if(user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'{member.mention} has been forgiven!')
            return

#Purging Chat + Za Warudo/Nuke
@client.command(aliases=['purge'])
async def clear(ctx, amount=11):
    if (not ctx.author.guild_permissions.manage_messages):
        await ctx.send('Get some perms first, bud')
    new_amount = amount + 1
    if amount > 300:
        await ctx.send('cannot delete more than 300 messages')
    else:
        await ctx.channel.purge(limit=amount)
        await ctx.send('Purge Complete')

#SJSU Help Commands go here

@client.command()
async def sjsu_help(ctx):
    await ctx.send('ap, covid, pre_enroll, moveinday, reg, roadmap')

@client.command()
async def moveinday(ctx):
    await ctx.send('Move-In Day is August 14th-15th!')

@client.command()
async def roadmap(ctx):
    await ctx.send("Roadmaps are an example of a schedule designed to help you graduate in 4 years. For the roadmap to your major, go to https://catalog.sjsu.edu/content.php?catoid=10&navoid=741 and look for your major!")

@client.command()
async def covid(ctx):
    await ctx.send('A COVID-19 Vaccination will be required by August 19 in order to live in on-campus housing. https://www.sjsu.edu/housing/how-we-can-help/covid-19-information.php')

@client.command()
async def reg(ctx):
    await ctx.send('Class registration will take place on the day of your orientation!')

@client.command()
async def ap(ctx):
    await ctx.send('https://catalog.sjsu.edu/content.php?catoid=2&navoid=127&hl=%22ap%22&returnto=search')

@client.command()
async def pre_enroll(ctx):
    ctx.send("If you see classes registered for you already, don't worry! Certain classes are registered for you in advance to insure that you are able to take that class during your first semester. These classes, regarding date and time, cannot be changed.")
#Level System for SJSU Discord

#Create User Data upon joining server
@client.event
async def on_member_join(member):
    with open('users.json' 'r') as f:
        users = json.load(f)

    await update_data(users, member)

    with open('users.json', 'w') as f:
        json.dump(users, f, indent=4)

#Give EXP from a message
@client.event
async def on_message(message):
    if message.author.bot == False:
        with open('users.json', 'r') as f:
            users = json.load(f)

        await update_data(users, message.author)
        await add_exp(users, message.author, 5)
        await LevelUp(users, message.author, message)

        with open('users.json', 'w') as f:
            json.dump(users, f, indent=4)

    await client.process_commands(message)

#User Functions
async def update_data(users, user):
    if not f'{user.id}' in users:
        users[f'{user.id}'] = {}
        users[f'{user.id}']['experience'] = 0
        users[f'{user.id}']['level'] = 1

async def add_exp(users, user, exp):
    users[f'{user.id}']['experience'] += exp

async def LevelUp(users, user, message):
    with open('levels.json', 'r') as g:
        levels = json.load(g)
    experience = users[f'{user.id}']['experience']
    lvlStart = users[f'{user.id}']['level']
    lvlEnd = int(experience ** (1/3.8))
    if lvlStart < lvlEnd:
        await message.channel.send(f'{user.mention} has leveled up to level {lvlEnd}')
        users[f'{user.id}']['level'] = lvlEnd

#Improved Level Command
@client.command()
async def level(ctx, member: discord.Member = None):
    if not member:
        id = ctx.message.author.id
        with open('users.json', 'r') as f:
            users = json.load(f)
        lvl = users[str(id)]['level']
        await ctx.send(f'You are at level {lvl}!')
    else:
        id = member.id
        with open('users.json', 'r') as f:
            users = json.load(f)
        lvl = users[str(id)]['level']
        await ctx.send(f'{member} is at level {lvl}!')
#End of Level System

#Reminder: all functions must be before this comment in order to work
client.run('ODYwMzQ5NDY3MjcwMzE2MDMy.YN584Q.TYBt0Lo1CXAQdRp8p9kMY-K_lwo')