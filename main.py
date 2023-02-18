TOKEN = "INSERT TOKEN HERE"

import disnake
from disnake.ext import commands
from disnake import app_commands
from disnake import Webhook
import aiohttp
import os
import requests
import json
import datetime
import random
from datetime import timedelta
import asyncio
import easy_pil
from easy_pil import Editor
from easy_pil import load_image_async
from easy_pil import Font
from disnake import File
discord = disnake
intent = discord.Intents
bot = commands.Bot(command_prefix="?", intents = disnake.Intents.all())

def convert(time):
    pos = ["s","m","h","d",]
    time_dict = {"s": 1,"m": 60,"h": 3600,"d": 3600*24}
    unit = time[-1]
    if unit not in pos:
        return -1
    try:
        val = int(time[:-1])
    except:
        return -2
    
    return val * time_dict[unit]                       
async def status_task():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='Polly server'))
    await asyncio.sleep(10)
    await bot.change_presence(activity=disnake.Activity(type=discord.ActivityType.watching, name="Movies"))
    await asyncio.sleep(10)
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='/setup'))
    await asyncio.sleep(10)
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f'over {len(bot.guilds)} servers'))
    await asyncio.sleep(10)
@bot.event
async def on_ready():
    print('Connected to bot: {}'.format(bot.user.name))
    print('Bot ID: {}'.format(bot.user.id))
    while 1 == 1:
        await status_task()

@bot.slash_command()
async def settings(ctx):
    with open("polly.json", "r") as f:
        guilds = json.load(f)
    if str(ctx.guild.id) in guilds:
        embed = disnake.Embed(title="Polly settings",description=f"{ctx.guild.name}'s settings",color=disnake.Colour.blue(),)
        embed.add_field(name = "Logging Channel", value = guilds[str(ctx.guild.id)]["logging"])
        embed.add_field(name = "Open Tickets", value = guilds[str(ctx.guild.id)]["opentickets"])
        embed.add_field(name = "Closed Tickets", value = guilds[str(ctx.guild.id)]["closedtickets"])
        embed.add_field(name = "Announcement Channel", value = guilds[str(ctx.guild.id)]["announcement"])
        embed.add_field(name = "Welcome Channel", value = guilds[str(ctx.guild.id)]["welcomer"])
        embed.add_field(name = "Goodbye Channel", value = guilds[str(ctx.guild.id)]["bye"])
        await ctx.send(embed=embed)
    else:
        await ctx.send("Server not found in database. Please run /start to add to database")

@bot.slash_command()
@commands.default_member_permissions(administrator=True)
async def start(ctx):
    with open("polly.json", "r") as f:
        guilds = json.load(f)
    if str(ctx.guild.id) in guilds:
        await ctx.send(f"Bot has already started for {ctx.guild.name}")
        return
    else:
        guilds[str(ctx.guild.id)] = {}
        guilds[str(ctx.guild.id)]["logging"] = "disabled"
        guilds[str(ctx.guild.id)]["opentickets"] = "disabled"
        guilds[str(ctx.guild.id)]["closedtickets"] = "disabled"
        guilds[str(ctx.guild.id)]["announcement"] = "disabled"
        guilds[str(ctx.guild.id)]["welcomer"] = "disabled"
        guilds[str(ctx.guild.id)]["bye"] = "disabled"
        with open("polly.json", "w") as f:
            json.dump(guilds,f)
        await ctx.send(f"This server is now ready to be used with {bot.user.name}")
      
@bot.slash_command(description="Sets the logging channel using chanell ID")
@commands.has_permissions(administrator=True)
async def set_logging(ctx, id: str = "disabled"):
    with open("polly.json", "r") as f:
        guilds = json.load(f)
    if id == "disabled":
        guilds[str(ctx.guild.id)]["logging"] = disabled
        await ctx.send("Logging has been disabled")
    elif str(ctx.guild.id) in guilds:
        try:
            channelid = int(id)
        except:
            await ctx.send("Please only use a channel ID", ephemeral=True)
        else:
            try:
                channel = ctx.guild.get_channel(int(id))
            except:
                await ctx.send("Not a valid channel ID")
            else:
                guilds[str(ctx.guild.id)]["logging"] = int(id)
                with open("polly.json", "w") as f:
                    json.dump(guilds,f)
                await ctx.send(f"Set the logs channel to <#{id}>")
                
    else:
        await ctx.send("This server was not found in the database. Please run **/start** to add to the database")
@bot.slash_command(description="Sets the ticket categories using ID")
@commands.has_permissions(administrator=True)
async def set_tickets(ctx, open_channel: str = "disabled", closed_channel: str = "disabled"):
    with open("polly.json", "r") as f:
        guilds = json.load(f)
    if open_channel == "disabled" or closed_channel == "disabled":
        guilds[str(ctx.guild.id)]["opentickets"] = "disabled"
        guilds[str(ctx.guild.id)]["closedtickets"] = "disabled"
        
        await ctx.send("Ticket system has been disabled")
    elif str(ctx.guild.id) in guilds:
        guilds[str(ctx.guild.id)]["opentickets"] = int(open_channel)
        guilds[str(ctx.guild.id)]["closedtickets"] = int(closed_channel)
        with open("polly.json", "w") as f:
            json.dump(guilds,f)
        await ctx.send(f"Set the open tickets category to <#{open_channel}>\nand the ticket archive to <#{closed_channel}>")                
    else:
        await ctx.send("This server was not found in the database. Please run **/start** to add to the database")
@bot.slash_command(description="Sets the announcement channel")
@commands.has_permissions(administrator=True)
async def set_announce(ctx, id: str = "disabled"):
    with open("polly.json", "r") as f:
        guilds = json.load(f)
    if id == "disabled":
        guilds[str(ctx.guild.id)]["announcement"] = "disabled"
        
        await ctx.send("Announcement command has been disabled")
    elif str(ctx.guild.id) in guilds:
        guilds[str(ctx.guild.id)]["announcement"] = int(id)
        with open("polly.json", "w") as f:
            json.dump(guilds,f)
        await ctx.send(f"Set the announcement to <#{id}>")                
    else:
        await ctx.send("**This server was not found in the database. Please run **/start** to add to the database")
@bot.slash_command(description="Sets the welcome channel")
@commands.has_permissions(administrator=True)
async def set_welcomer(ctx, id: str = "disabled"):
    with open("polly.json", "r") as f:
        guilds = json.load(f)
    if id == "disabled":
        guilds[str(ctx.guild.id)]["welcomer"] = "disabled"
        
        await ctx.send("Welcomer has been disabled")
    elif str(ctx.guild.id) in guilds:
        guilds[str(ctx.guild.id)]["welcomer"] = int(id)
        with open("polly.json", "w") as f:
            json.dump(guilds,f)
        await ctx.send(f"Set the welcomer channel to <#{id}>")                
    else:
        await ctx.send("**This server was not found in the database. Please run **/start** to add to the database")

@bot.slash_command()
async def set_goodbye(ctx, id: str = "disabled"):
    with open("polly.json", "r") as f:
        guilds = json.load(f)
    if id == "disabled":
        guilds[str(ctx.guild.id)]["bye"] = "disabled"
        
        await ctx.send("Leave log has been disabled")
    elif str(ctx.guild.id) in guilds:
        guilds[str(ctx.guild.id)]["bye"] = int(id)
        with open("polly.json", "w") as f:
            json.dump(guilds,f)
        await ctx.send(f"Set the Leave logs channel to <#{id}>")                
    else:
        await ctx.send("**This server was not found in the database. Please run **/start** to add to the database")
@bot.slash_command()
async def setup(ctx):
    await ctx.send("`/start` starts the bot when added to a new server\n`/settings` View this servers preferences\n`/set_logging` sets the logs channel for edit and delete logs [USE THE ID ONLY OR LEAVE BLANK TO DISABLE]\n`/set_tickets` set the category that tickets go into [USE THE ID ONLY OR LEAVE BLANK TO DISABLE]\n`/set_announce` sets the announcement channel [USE THE ID ONLY OR LEAVE BLANK TO DISABLE]\n`/set_goodbye` sets the channel for when a user leaves [USE THE ID ONLY OR LEAVE BLANK TO DISABLE]\n`/set_welcomer` sets the channel for welcomer messages")

@bot.command()
async def startmodmail(ctx):
    await ctx.send("Click The Below Button to open a ticket to contact staff",components=[disnake.ui.Button(label="Open Ticket", style=disnake.ButtonStyle.secondary, custom_id="ticket"),],)

@bot.listen("on_button_click")
async def help_listener(inter: disnake.MessageInteraction):
    if inter.component.custom_id == "ticket":
        with open("polly.json", "r") as f:
            guilds = json.load(f)
        if guilds[str(inter.guild.id)]["opentickets"] == "disabled":
            await inter.response.send_message("Ticket system has been disabled for this server, If you are an admin see /setup")
        else:
            tickets_id = int(guilds[str(inter.guild.id)]["opentickets"])
            await inter.response.send_message("Why are you opening a ticket:", ephemeral=True, components=disnake.ui.StringSelect(options= [
                disnake.SelectOption(
                    label="Report a user", description="If a user is mistreating you or breaking rules (You can also use /report)", emoji=None
                ),
                disnake.SelectOption(
                    label="Apply for Staff", description="Your looking for a staff role in the server", emoji=None
                ),
                disnake.SelectOption(
                    label="Appeal a punishment", description="You have been warned/kicked/banned/muted and would like to have it revoked", emoji=None
                ),
                disnake.SelectOption(
                    label="Enquire about punishment", description="You have been warned/kicked/banned/muted and would like to know why", emoji=None
                ),
                disnake.SelectOption(
                    label="Reopen an old ticket", description="You would like a member of staff to reopen an old closed ticket", emoji=None
                ),
                disnake.SelectOption(
                    label="Other", description="Anything not mentioned on this list", emoji=None
                ),
            ], custom_id="ticketreason"),)
            return


@bot.listen("on_dropdown")
async def ticketreason_listener(inter: disnake.MessageInteraction):
    if inter.values[0] == "Other":
        await inter.response.send_modal(
        title="Other Reason",
        custom_id="other_id",
        components=[disnake.ui.TextInput(label="Reason", placeholder="I need help!", custom_id="reason_id", required=True,min_length=3, max_length=100,),],)
    else:
        Ticket = await inter.guild.create_text_channel(f'{inter.user.name}-ticket')
        await inter.response.send_message(f"Ticket Opened <#{Ticket.id}>", ephemeral=True)
        with open("polly.json", "r") as f:
            guilds = json.load(f)
        tickets_id = int(guilds[str(inter.guild.id)]["opentickets"])
        tickets = bot.get_channel(tickets_id)
        await Ticket.edit(category=tickets, sync_permissions=True)
        await Ticket.set_permissions(inter.user, view_channel=True,send_messages=True)
        embed = disnake.Embed(title="New Ticket",description=f"{inter.user.name}'s ticket",color=disnake.Colour.blue(),timestamp=datetime.datetime.now(),)
        embed.add_field(name="Reason", value=f"{inter.values[0]}", inline=True)
        await Ticket.send(f"{inter.user.mention} this is your ticket,", embed=embed, components=[disnake.ui.Button(label="Close Ticket", style=disnake.ButtonStyle.danger, custom_id="close"),],)       

@bot.event
async def on_modal_submit(inter: disnake.ModalInteraction):
    if inter.custom_id == "other_id":
        Ticket = await inter.guild.create_text_channel(f'{inter.user.name}-ticket')
        await inter.response.send_message(f"Ticket Opened <#{Ticket.id}>", ephemeral=True)
        with open("polly.json", "r") as f:
            guilds = json.load(f)
        tickets_id = int(guilds[str(inter.guild.id)]["opentickets"])
        tickets = bot.get_channel(tickets_id)
        await Ticket.edit(category=tickets, sync_permissions=True)
        await Ticket.set_permissions(inter.user, view_channel=True,send_messages=True)
        embed = disnake.Embed(title="New Ticket",description=f"{inter.user.name}'s ticket",color=disnake.Colour.blue(),timestamp=datetime.datetime.now(),)
        embed.add_field(name="Reason", value="Other", inline=True)
        embed.add_field(name="Reason Given", value=inter.text_values["reason_id"], inline=True)
        await Ticket.send(f"{inter.user.mention} this is your ticket,", embed=embed, components=[disnake.ui.Button(label="Close Ticket", style=disnake.ButtonStyle.danger, custom_id="close"),],)        
      

@bot.listen("on_button_click")
async def help_listener(inter: disnake.MessageInteraction):
    if inter.component.custom_id not in ["close"]:
        return

    if inter.component.custom_id == "close":
        with open("polly.json", "r") as f:
            guilds = json.load(f)
        ticketarchiveid = int(guilds[str(inter.guild.id)]["closedtickets"])
        ticketarchive = inter.guild.get_channel(ticketarchiveid)
        await inter.channel.edit(name=f"closed-{inter.channel.name}", category=ticketarchive, sync_permissions=True)
        await inter.response.send_message(f"Ticket closed by {inter.user.mention}", ephemeral=False)

#announce command

@bot.slash_command()
@commands.default_member_permissions(manage_messages=True)
async def announce(
    inter: disnake.ApplicationCommandInteraction,
    announcement: str
):
    """
    Sends An Announcement to #announcements channel

    Parameters
    ----------
    announcement: What would you like to announce
    """


    with open("polly.json", "r") as f:
        guilds = json.load(f)
    if guilds[str(inter.guild.id)]["announcement"] == "disabled":
        await inter.response.send_message("The announce command is disabled for this server, If you are an admin please see /setup")
    announcementid = int(guilds[str(inter.guild.id)]["announcement"])
    announcementchan = bot.get_channel(announcementid)
    await announcementchan.send(f"{announcement}")
    await inter.response.send_message(f"Announcement Sent Successfully :white_check_mark:", ephemeral=True)

                            
#Kick/Ban

@bot.slash_command(description = 'Bans a specified member')
@commands.default_member_permissions(ban_members=True)
async def ban(inter: disnake.ApplicationCommandInteraction, member:discord.User, reason: str = "unspecified reason"):
    if member.id == inter.user.id:
        await inter.response.send_message("You cannot ban yourself, sorry! :)")
        return
    

    else:
        await member.send(f"You have been banned from {inter.guild.name}")
        await member.ban(reason=reason)
        await inter.response.send_message(f"Successfuly Banned {member}")
        
@bot.slash_command(description = 'Kicks a specified member')

@commands.default_member_permissions(kick_members=True)

async def kick(inter: disnake.ApplicationCommandInteraction, member:discord.Member, reason: str = "unspecified reason"):
        
        await member.send(f"You have been kicked from {inter.guild.name}.")
        await member.kick(reason=reason)
        await inter.response.send_message(f"Successfully Kicked {member}")

#webhook send

@bot.slash_command()
async def webhook(
    inter: disnake.ApplicationCommandInteraction,
    message: str,
    url: str,
    username: str,
):
    """
    Sends a specific message to a webhook

    Parameters
    ----------
    message: What would you like to say over the webhook
    url: Webhook URL
    username: Username the message will come from
    """

    await inter.response.send_message(f"Sent :white_check_mark:", ephemeral=true)
    async with aiohttp.ClientSession() as session:
      webhook = Webhook.from_url(url, session=session)
      await webhook.send(message, username=username)

#Avatar/ My avatar commands
 
@bot.slash_command()
async def avatar(
    inter: disnake.ApplicationCommandInteraction,
    user: disnake.Member,
):
    """
    Gets a user's avatar

    Parameters
    ----------
    user: Who's Avatar
    """
    userID = user.id
    user = user
    pfp = user.display_avatar.url
    embed = disnake.Embed(
    title=user,
    description=f"{user}'s avatar",
    color=0x3498db)
    embed.set_image(url=pfp)

    await inter.response.send_message(embed=embed)

@bot.slash_command()
async def myavatar(
    inter: disnake.ApplicationCommandInteraction,
):
    """
    Gets your avatar
    """
    userID = inter.user.id
    user = inter.user
    pfp = inter.user.display_avatar.url
    embed = disnake.Embed(
    title=inter.user,
    description=f"{user}'s avatar",
    color=0x3498db)
    embed.set_image(url=pfp)

    await inter.response.send_message(embed=embed)

#bottag

#role

@bot.slash_command(default_member_permissions=disnake.Permissions(manage_roles=True),description = 'Grants a role')
async def role(inter: disnake.ApplicationCommandInteraction, user:disnake.Member, role:disnake.Role):
    await inter.response.send_message(f"Gave role {role} to {user}", ephemeral=True)
    await user.add_roles(role)

#say 


     
#Delete log

@bot.event
async def on_message_delete(message):
    if message.author == bot.user:
        return
    

    else:
        embed = disnake.Embed(
            title="Message Deleted",
            description=f"**Message:**\n{message.content}",
            color=disnake.Colour.blue())

        embed.set_author(
            name=message.author,
            icon_url=message.author.display_avatar.url)
        with open("polly.json", "r") as f:
            guilds = json.load(f)
        logs_id = int(guilds[str(message.guild.id)]["logging"])
        if guilds[str(message.guild.id)]["logging"] == "disabled":
            return
        else:
            logs = bot.get_channel(logs_id)
            await logs.send(embed=embed)


#Edit Log

@bot.event
async def on_message_edit(before, after):
    if before.author.id == bot.user.id:
        return
     
    embed = disnake.Embed(
        title="Message Edited",
        description=f"**Before:**\n{before.content}\n\n**After:**\n{after.content}",
        color=disnake.Colour.blue())

    embed.set_author(
        name=before.author,
        icon_url=before.author.display_avatar.url)
    with open("polly.json", "r") as f:
        guilds = json.load(f)
    logs_id = int(guilds[str(before.guild.id)]["logging"])
    if logs_id == "disabled":
        return
    else:
        logs = bot.get_channel(logs_id)
        await logs.send(embed=embed)

#Quote

def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return(quote)

@bot.slash_command()
async def quote(inter: disnake.ApplicationCommandInteraction):
    quote = get_quote()
    await inter.response.send_message(quote, ephemeral=False)

@bot.slash_command()
@commands.default_member_permissions(moderate_members=True)
async def timeout(inter: disnake.ApplicationCommandInteraction, user: disnake.Member, time: str, reason: str = "No Reason Given"):
    """
    Times out a user

    Parameters
    ----------
    user: Who do you want to time out?
    time: How long do you want to time them out for s|m|h|d?
    reason: Why are you timing them out?
    """
    sectime = convert(time)
    timeout = timedelta(seconds=sectime)
    await inter.guild.timeout(user, duration=timeout, reason=reason)
    await inter.response.send_message(f"Timed out {user} for {time}", ephemeral=True)

@bot.slash_command()
@commands.default_member_permissions(moderate_members=True)
async def let_the_poor_guy_speak_again(inter: disnake.ApplicationCommandInteraction, user: disnake.Member, reason: str = "No Reason Given"):
    """
    Lets someone speak

    Parameters
    ----------
    user: Who do you want to let speak?
    reason: But Why?
    """
    timeout = timedelta(hours=0,minutes=0)
    await inter.guild.timeout(user, duration=timeout, reason=reason)
    await inter.response.send_message(f"Alr {user.name} you can speak again, I guess", ephemeral=False)


@bot.command()
async def servercount(ctx):
    await ctx.send(f"I am in **{len(bot.guilds)} Servers**")

@bot.command()
@commands.has_permissions(moderate_members=True)
async def giveaway(ctx):
    await ctx.channel.send("Creating Giveaway. You have 20 seconds to answer each question")
    questions = ["What Channel are you hosting the giveaway in?",
                 "How long should the giveaway last?",
                 "What is the prize for the giveaway?"]
    answers = []
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel
    for i in questions:
        await ctx.send(i)
        try:
            msg = await bot.wait_for("message", timeout=60.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send("Timed out. Please try again")
            return
        else:
            if msg.content == "cancel":
                return
            else:
                answers.append(msg.content)
    try:
        c_id = int(answers[0][2:-1])
    except:
        await ctx.send(f"You entered the channel wrong please only include in your message the channnel mention (e.g. {ctx.channel.mention}")
        return
    channel = bot.get_channel(c_id)
    time = convert(answers[1])
    if time == -1:
        await ctx.send("Invalid Time used. Please use the format e.g. 1h for 1 hour")
        return
    elif time == -2:
        await ctx.send("Time must be an integer meaning no decimal points and no letters besides the unit (s/m/h/d)")
        return
    prize = answers[2]
    await ctx.send("Giveaway created")
    embed = disnake.Embed(title = "Giveaway!", description=f"{prize}", color=disnake.Colour.blue())
    embed.add_field(name = "Hosted By:", value = ctx.author.mention)
    embed.set_footer(text = f"Giveaway will last {answers[1]}")
    my_msg = await channel.send(embed = embed)
    await my_msg.add_reaction("🎉")
    await asyncio.sleep(time)
    new_msg = bot.get_message(my_msg.id)
    users = await new_msg.reactions[0].users().flatten()
    users.pop(users.index(bot.user))
    winner = random.choice(users)
    await channel.send(f"Congratulations! {winner.mention} won {prize}")



@bot.command()
@commands.has_permissions(moderate_members=True)
async def poll(ctx):
    questions = ["What Channel do you want to put the poll in?",
                 "What is the question?",
                 "What are the options (seperate by a `;`)"]
    answers = []
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel
    for i in questions:
        await ctx.send(i)
        try:
            msg = await bot.wait_for("message", timeout=60.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send("Timed out. Please try again")
            return
        else:
            if msg.content == "cancel":
                return
            else:
                answers.append(msg.content)
    try:
        c_id = int(answers[0][2:-1])
    except:
        await ctx.send(f"You entered the channel wrong please only include in your message the channnel mention (e.g. {ctx.channel.mention}")
        return
    pollchan = bot.get_channel(c_id)
    question = answers[1]
    alloptions = answers[2]
    options = alloptions.split(";")
    pollemoji = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
    count = len(options)
    if count > 10:
        ctx.send("Sorry you can only have a maximum of 10 options")

    usedemojis = pollemoji[0:count]
    for x, y in zip(usedemojis, options):
        foptions = str('{} {}'.format(x, y))
        optionfile = open("temp.txt", "a")
        optionfile.write(f"\n{foptions}")
        optionfile.close
        optionfile = open("temp.txt", "r")
        embedoptions = optionfile.read()
    embed = disnake.Embed(title=question,description=embedoptions,color=disnake.Colour.blue())
    pollmsg = await pollchan.send(embed=embed)
    optionfile.close
    optionsfile = open("temp.txt", "w")
    optionsfile.write("")
    optionsfile.close
    for i in usedemojis:
        await pollmsg.add_reaction(i)

@bot.event
async def on_member_join(member):
    with open("polly.json", "r") as f:
        guilds = json.load(f)
    if guilds[str(member.guild.id)]["welcomer"] == "disabled":
        return
    else:
        welcome = bot.get_channel(int(guilds[str(member.guild.id)]["welcomer"]))
        background = Editor("bg.png")
        profile_image = await load_image_async(str(member.display_avatar.url))
        profile = Editor(profile_image).resize((150, 150)).circle_image()
        poppins = Font.poppins(size=50, variant="bold")
        poppins_small =Font.poppins(size=20, variant="light")
        background.paste(profile, (405, 90))
        background.ellipse((405, 90), 150, 150, outline="white", stroke_width=5)
        background.text((480, 260), f"WELCOME TO {member.guild.name}", color="white", font=poppins, align="center")
        background.text((480, 325), f"{member}", color="white", font=poppins_small, align="center")
        file = File(fp=background.image_bytes, filename=f"{member}.png")
        await welcome.send(f"{member.mention} WELCOME TO **{member.guild.name}**\nPlease read the rules", file=file)
@bot.event
async def on_member_remove(member):
    with open("polly.json", "r") as f:
        guilds = json.load(f)
    if guilds[str(member.guild.id)]["bye"] == "disabled":
        return
    else:
        welcome = bot.get_channel(int(guilds[str(member.guild.id)]["bye"]))
        background = Editor("bg.png")
        profile_image = await load_image_async(str(member.display_avatar.url))
        profile = Editor(profile_image).resize((150, 150)).circle_image()
        poppins = Font.poppins(size=50, variant="bold")
        poppins_small =Font.poppins(size=20, variant="light")
        background.paste(profile, (405, 90))
        background.ellipse((405, 90), 150, 150, outline="white", stroke_width=5)
        background.text((480, 260), f"Goodbye {member}", color="white", font=poppins, align="center")
        background.text((480, 325), "We will miss you", color="white", font=poppins_small, align="center")
        file = File(fp=background.image_bytes, filename=f"{member}.png")
        await welcome.send(f"GOODBYE **__{member}__**\nWe will miss you", file=file)

@bot.slash_command(description="Changes a users nickname")
@commands.has_permissions(manage_nicknames=True)
async def nick(inter, user: disnake.Member, name: str):
    await user.edit(nick=name)
    await inter.response.send_message(f"Changed {user.mention}'s nickname to {name}", ephemeral=True)

if TOKEN == "INSERT TOKEN HERE":
    print("Please edit main.py and replace INSERT TOKEN HERE with your token")
    return
else:
    bot.run(TOKEN)