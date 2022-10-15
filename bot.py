from urllib import response
import nextcord
from nextcord.ext import commands, activities
from nextcord import member, guild, message, Client, Interaction, SlashOption, ChannelType, FFmpegPCMAudio
from nextcord.abc import GuildChannel
import asyncio
import ffmpeg
import aiohttp
from discord_webhook import DiscordWebhook, DiscordEmbed
from pytube import YouTube
import random
import os

client = Client()

@client.event
async def on_ready():
    print("Ready!")
    client.loop.create_task(status_task())
    await client.sync_application_commands()
    
async def status_task():
    while True:
        servers = len(client.guilds)
        members = 0
        for guild in client.guilds:
            members += guild.member_count - 1
        await client.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.watching, name='/help'))
        await asyncio.sleep(5)
        await client.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.listening, name=f"{members} members"))
 
#####################################################################################################################
@client.event
async def on_voice_state_update(member, before, after):
    if member.bot:
        return print("Member is a bot.")
    else:
        if after.channel is not None:
            if after.channel.id == 1023806524650422302:
                logchannel = client.get_channel(1023806902657896540)
                embed = nextcord.Embed(description=f"Ein User benötigt Hilfe!", color=0xff0000)
                await logchannel.send(embed=embed)
                return
            else:
                return
                        
#####################################################################################################################

@client.slash_command(name="help", description="Shows you a panel, which contains every command.")
async def help(interaction: Interaction):
    embed = nextcord.Embed(title="Berlin, Deutschland", color=0xff0000)
    embed.add_field(name="**Slash-Commands**", value="```diff\r\n"
                                                     "+ /help - Zeigt dir dieses Panel an.\r\n"
                                                     "+ /startradio - Starte das Radio.\r\n"
                                                     "+ /stopradio - Stoppe das Radio.\r\n"
                                                     "+ /activity - Spiele Minigames in einem Talk.\r\n"
                                                     "+ /ytinfo - Erhalte Informationen.\r\n"
                                                     "+ /rbxwhois - Erhalte eine Userinfo über einen Roblox User.\r\n"
                                                     "+ /userinfo - Schaue dir Informationen über einen User an.\r\n"
                                                     "+ /serverinfo - Schaue dir Informationen über den Server an.\r\n"
                                                     "+ /8ball - Frage das Orakel\r\n"
                                                     "+ /emojify - Der Bot zeigt deinen Text in Emojis an.```", inline=False)
    await interaction.response.send_message(embed=embed,  ephemeral=True)

#####################################################################################################################

@client.slash_command(name="startradio", description="[ONLY FOR STAFFS] Starte das Radio.")
async def startradio(interaction: Interaction, channel:nextcord.VoiceChannel):
     await interaction.response.send_message("``✔️`` Ich habe das Radio **gestartet**.", ephemeral=True)
     while True:
        player = await channel.connect()
        player.play(FFmpegPCMAudio("https://streams.ilovemusic.de/iloveradio109.mp3"))
        await asyncio.sleep(3600)
        await interaction.guild.voice_client.disconnect()


@client.slash_command(name="stopradio", description="[ONLY FOR STAFFS] Stoppe das Radio.")
async def stopradio(interaction: Interaction):
     while True:
        global player
        player = await interaction.guild.voice_client.disconnect()
        await interaction.response.send_message("``✔️`` Ich habe das Radio **gestoppt**.", ephemeral=True)

#####################################################################################################################

@client.slash_command(name="activity")
async def activity(interaction: Interaction, channel: nextcord.VoiceChannel):
    class DropdownMenu(nextcord.ui.Select):
        def __init__(self):
            selectOptions = [
                nextcord.SelectOption(label="Poker Night"),
                nextcord.SelectOption(label="Chess in the Park"),
                nextcord.SelectOption(label="Sketch Heads"),
                nextcord.SelectOption(label="Letter League"),
                nextcord.SelectOption(label="Checkers in the Park"),
                nextcord.SelectOption(label="SpellCast"),
                nextcord.SelectOption(label="Blazing 8s"),
                nextcord.SelectOption(label="Land-io"),
                nextcord.SelectOption(label="Putt Party"),
                nextcord.SelectOption(label="Watch Together"),
                nextcord.SelectOption(label="Bobble League")
            ]
            super().__init__(placeholder="Wähle ein Spiel aus!", min_values=1, max_values=1, options=selectOptions)

        async def callback(self, interaction: nextcord.Interaction):
            if self.values[0] == "Poker Night":
                invite_link = await channel.create_activity_invite(activities.Activity.poker)
                embed = nextcord.Embed(description=f"``✔️`` {invite_link}", color=0xff0000)
                await interaction.response.edit_message(embed=embed)
            elif self.values[0] == "Chess in the Park":
                invite_link = await channel.create_activity_invite(activities.Activity.chess)
                embed = nextcord.Embed(description=f"``✔️`` {invite_link}", color=0xff0000)
                await interaction.response.edit_message(embed=embed)
            elif self.values[0] == "Sketch Heads":
                invite_link = await channel.create_activity_invite(activities.Activity.sketch)
                embed = nextcord.Embed(description=f"``✔️`` {invite_link}", color=0xff0000)
                await interaction.response.edit_message(embed=embed)
            elif self.values[0] == "Letter League":
                invite_link = await channel.create_activity_invite(activities.Activity.letter_league)
                embed = nextcord.Embed(description=f"``✔️`` {invite_link}", color=0xff0000)
                await interaction.response.edit_message(embed=embed)
            elif self.values[0] == "Checkers in the Park":
                invite_link = await channel.create_activity_invite(activities.Activity.checkers)
                embed = nextcord.Embed(description=f"``✔️`` {invite_link}", color=0xff0000)
                await interaction.response.edit_message(embed=embed)
            elif self.values[0] == "SpellCast":
                invite_link = await channel.create_activity_invite(activities.Activity.spellcast)
                embed = nextcord.Embed(description=f"``✔️`` {invite_link}", color=0xff0000)
                await interaction.response.edit_message(embed=embed)
            elif self.values[0] == "Blazing 8s":
                invite_link = await channel.create_activity_invite(activities.Activity.blazing)
                embed = nextcord.Embed(description=f"``✔️`` {invite_link}", color=0xff0000)
                await interaction.response.edit_message(embed=embed)
            elif self.values[0] == "Land-io":
                invite_link = await channel.create_activity_invite(activities.Activity.land_io)
                embed = nextcord.Embed(description=f"``✔️`` {invite_link}", color=0xff0000)
                await interaction.response.edit_message(embed=embed)
            elif self.values[0] == "Putt Party":
                invite_link = await channel.create_activity_invite(activities.Activity.putt_party)
                embed = nextcord.Embed(description=f"``✔️`` {invite_link}", color=0xff0000)
                await interaction.response.edit_message(embed=embed)
            elif self.values[0] == "Watch Together":
                invite_link = await channel.create_activity_invite(activities.Activity.youtube)
                embed = nextcord.Embed(description=f"``✔️`` {invite_link}", color=0xff0000)
                await interaction.response.edit_message(embed=embed)
            elif self.values[0] == "Bobble League":
                invite_link = await channel.create_activity_invite(activities.Activity.bobble)
                embed = nextcord.Embed(description=f"``✔️`` {invite_link}", color=0xff0000)
                await interaction.response.edit_message(embed=embed)

    class DropdownView(nextcord.ui.View):
        def __init__(self):
            super().__init__()
            self.add_item(DropdownMenu())

    embed = nextcord.Embed(description="``⌛️`` Wähle ein Spiel aus, was du spielen willst.", color=0xff0000)
    await interaction.response.send_message(embed=embed, view=DropdownView())

#####################################################################################################################

@client.slash_command(name="ytinfo", description="Erhalte Informationen über ein YouTube Video.")
async def ytdownload(interaction: Interaction, link:str):
    yt = YouTube(link)
    
    embed = nextcord.Embed(title=yt.title, description=f"``⏱`` {yt.length} Sekunden\r\n"
                                                       f"``🎥`` {yt.author}\r\n"
                                                       f"``👀`` {yt.views}\r\n"
                                                       f"``⏰`` {yt.publish_date}\r\n", color=0xff0000)
    embed.set_image(url=yt.thumbnail_url)
    await interaction.response.send_message(embed=embed)

#####################################################################################################################

@client.slash_command(name="userinfo", description="Bekomme Informationen über einen User.")
async def userinfo(interaction: Interaction, user:nextcord.Member = SlashOption(required=False)):
    if user == None: 
        user = interaction.user

    embed=nextcord.Embed(title=f'Userinfo für {user.name}', description=f'Hier sind ein paar Informationen über {user.mention}', color=0xff0000)
    embed.add_field(name="Server beigetreten", value=f"{user.joined_at.day}.{user.joined_at.month}.{user.joined_at.year}, {user.joined_at.hour}:{user.joined_at.minute}")
    embed.add_field(name="Discord beigetreten", value=f"{user.created_at.day}.{user.created_at.month}.{user.created_at.year}, {user.created_at.hour}:{user.created_at.minute}")
    if len(user.roles) > 1:
        role_string = ' '.join([r.mention for r in user.roles][1:])
        embed.add_field(name="Rollen [{}]".format(len(user.roles)-1), value=role_string, inline=False)
    perm_string = ', '.join([str(p[0]).replace("_", " ").title() for p in user.guild_permissions if p[1]])
    embed.add_field(name="Server Berechtigungen", value=perm_string, inline=False)
    embed.set_footer(text=f"ID: {user.id}")
    embed.set_thumbnail(url=user.avatar.url)
    await interaction.response.send_message(embed=embed)

@client.slash_command(name="serverinfo", description="Bekomme Informationen über den Server.")
async def serverinfo(interaction: Interaction):
    embed=nextcord.Embed(color=0xff0000)
    embed.set_author(name=f"{interaction.guild.name}", icon_url=str(interaction.guild.icon.url))
    embed.add_field(name="Owner", value=str(interaction.guild.owner.mention))
    embed.add_field(name="Sprach-Kanäle", value=len(interaction.guild.categories))
    embed.add_field(name="Text-Kanäle", value=len(interaction.guild.text_channels))
    embed.add_field(name="Sprach-Kanäle", value=len(interaction.guild.voice_channels))
    embed.add_field(name="Mitglieder", value=interaction.guild.member_count)
    embed.add_field(name="Rollen", value=len(interaction.guild.roles))
    embed.set_thumbnail(url=str(interaction.guild.icon.url))
    embed.set_footer(text=f"ID: {interaction.guild_id}")
    await interaction.response.send_message(embed=embed)

@client.slash_command(name="8ball", description="Frage das Orakel.")
async def _8ball(interaction: Interaction, question:str):
    answers = ["Ja", "Nein", "Vielleicht", "Wahrscheinlich", "Sehr wahrscheinlich", "Sehr unwahrscheinlich", "Mir egal. Nicht mein Bier"]
    message = await interaction.response.send_message(content=f"``❓`` Ich versuche die Frage **{question}** zu beantworten...")
    await asyncio.sleep(1)
    await message.edit(content=f"``🌌`` Ich kontaktiere das Orakel...")
    await asyncio.sleep(1)
    await message.edit(content=f"``❗️`` Die Antwort auf deine Frage **{question}** lautet **{random.choices(answers)}**.")

@client.slash_command(name="emojify")
async def emojif(interaction: Interaction, text:str):
    emojis = []
    for s in text.lower():
        if s.isdecimal():
            num2emo = {"0":"zero", "1":"one", "2":"two",
                       "3":"three", "4":"four", "5":"five",
                       "6":"six", "7":"seven", "8":"eight", "9":"nine"}
            emojis.append(f":{num2emo.get(s)}:")
        elif s.isalpha():
            emojis.append(f":regional_indicator_{s}:")
        else:
            emojis.append(s)
    await interaction.response.send_message(content=" ".join(emojis))

#####################################################################################################################

import ro_py
from ro_py import Client
from ro_py.thumbnails import ThumbnailFormat, ThumbnailSize, ThumbnailType
roblox = Client("_4D1753360586FC31A2E7817FC1BCA2BC6C526284A7F554898DF92EA036702FB74BDEAC32C3EF1AF1E3465A25647B3BCDC73203EE52F00C33420E7DBF9E55C8EC11882B072B1EB2F2C752DF904B5FC6CD1328995B5496EF262700C095C87E29793DEC1EEDCCD703F64F53E1A41A0E083283E428304FC05E8EDE491B6B6FF04AC570A9FBC2F8476982E0D0A0AA55D0C809DDB2AF4011CA6CF64979A18AA839817D95F211276137F7B094F3A1C82CE42286F0CAC2B6AA13B853E982B6701A7F268C5A8690E69A70B2DFF92F3DE8D8C03D9BF06591FE9F05045AE690F97A5CB4F78CCBA18B4C621C2A8ADD93A82C541CA1EC68C6A46DB253E8800413ECE940059CD395739F83E6A4FA7DC8F40607D36B67B0814FADE23FDC03FA65680CDA7D227C656980445D66D4729DECEEA6E5DAD32A815E9DFA0875BAACA4FAC8AA207B2306E47971956FDFA73B505199B17B6BDEE967F4429A3C")

@client.slash_command(name="rbxwhois", description="Get information about a user!")
async def rbxwhois(interaction: Interaction, username):
    user = await roblox.get_user_by_username(username)
    avatar = await user.thumbnails.get_avatar_image(
        shot_type=ThumbnailType.avatar_headshot,
        size=ThumbnailSize.size_420x420,
        is_circular=False
    )
    day = user.created.day
    month = user.created.month
    year = user.created.year
    
    embed=nextcord.Embed(title=f"{user.display_name}", color=0xff0000)
    embed.add_field(name="Username", value=f"[@{user.name}](https://www.roblox.com/users/{user.id}/profile)", inline=True)
    embed.add_field(name="ID", value=user.id, inline=True)
    embed.add_field(name="Friends", value=await user.get_friends_count(), inline=False)
    embed.add_field(name="Followers", value=await user.get_followers_count(), inline=False)
    embed.add_field(name="Created at", value=f"{month}/{day}/{year}")
    embed.add_field(name="Description", value=f'{user.description or "No Description!"}', inline=False)
    embed.set_thumbnail(url=avatar)
    await interaction.response.send_message(embed=embed)


if __name__ == "__main__":
    client.run(os.environ["DISCORD_TOKEN"])