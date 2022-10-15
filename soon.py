from http.client import responses
from itertools import filterfalse
from optparse import Option
from tkinter.messagebox import YES
from urllib import response
import nextcord
from nextcord.ext import commands
from nextcord import member, guild, message, Client, Interaction, SlashOption, ChannelType, FFmpegPCMAudio
from nextcord.abc import GuildChannel
import asyncio
import ffmpeg
import aiohttp
from discord_webhook import DiscordWebhook, DiscordEmbed

client = Client()

## Support  

@client.slash_command(name="support", description="Führe diesen Command aus, um eventuelle Fragen direkt zu klären, ohne eine Ticket zu öffnen.")
async def support(interaction: Interaction):
    embed = nextcord.Embed(title="Häufig gestellte Fragen", description="``❗️❓`` **Hier werden dir häufig gestellte Fragen angezeigt.**", color=0xff0000)
    embed.add_field(name="Erklärung des Auto-Supports", value="Der **Auto Support** ist dafür gedacht, um die große Anzahl von Tickets zu reduzieren. Bevor ein Ticket geöffnet wird, bitten wir dich deine Frage hier zu suchen.\r\n\r\n"
                                                              "Dies kannst du machen, indem du in dem unten angezeigten Menu das Hauptthema deiner Frage auswählst und diese dort suchts. **Falls deine Frage nicht aufgelistet ist, "
                                                              "kannst du ein Ticket öffnen.**\r\n\r\n"
                                                              '*Falls du denkst, dass deine Frage öfters gestellt werden könnten, drückst du ganz einfach in dem Menu auf "Eine Frage beantragen".*', inline=False)
    class ApplyModal(nextcord.ui.Modal):
        def __init__(self):
            super().__init__(
            title="Eine Frage beantragen",
            timeout=1800)

            self.name = nextcord.ui.TextInput(label="Wie lautet dein Roblox Name?", placeholder="z.B. feltil", max_length=25)
            self.topic = nextcord.ui.TextInput(label="Auf welchen Bereich bezieht sich die Frage?", placeholder="z.B. Discord Support", max_length=100)
            self.question = nextcord.ui.TextInput(label="Wie lautet die Frage?", placeholder="z.B. Wie bewerbe ich mich?", max_length=1800)

            self.add_item(self.name)
            self.add_item(self.topic)
            self.add_item(self.question)

        async def callback(self, interaction: Interaction):
             embed = DiscordEmbed(title="New requested Question!", color=0xff0000)
             embed.add_embed_field(name="Roblox name", value=self.name.value, inline=False)
             embed.add_embed_field(name="Topic of the question", value=self.topic.value, inline=False)
             embed.add_embed_field(name="Question", value=self.question.value, inline=False)
             embed.set_thumbnail(url=f"{interaction.user.avatar.url}")
             embed.set_footer(text=f"Request by {interaction.user} ({interaction.user.id})")
             
             webhook = DiscordWebhook(url="https://discord.com/api/webhooks/1024301851568517140/KJFKghXqCfhgv0YPRuAh_Towgz0-l5lgCpZrNdpalDVdZAlpLRTLcZg4SyVjxhgaw6z9")
             webhook.add_embed(embed)
             response = webhook.execute()

    class RateHelp(nextcord.ui.View):
        def __init__(self):
            super().__init__()
            self.Value = None

        @nextcord.ui.button(label="Ja!", style=nextcord.ButtonStyle.gray, emoji="✔️")
        async def yes(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
            await interaction.response.send_message("``✔️`` Danke für dein Feedback!")
            self.Value = False 
            self.stop()

        @nextcord.ui.button(label="Nein!", style=nextcord.ButtonStyle.gray, emoji="❌")
        async def no(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
            await interaction.response.send_message("``✔️`` Danke für dein Feedback!")
            self.Value = False 
            self.stop()
    ########################################################################################################################################################################
    class DropDownMenu(nextcord.ui.Select):
        def __init__(self):
            selectOptions = [
                nextcord.SelectOption(label="Discord Support", description="Hier werden dir oft gestellte Fagen über Discord."),
                nextcord.SelectOption(label="Roblox Support", description="Hier werden dir oft gestellte Fagen über Discord."),
                nextcord.SelectOption(label="Eine Frage beantragen", description="Hier kannst du eine Frage beantragen, die nicht aufgelistet wird.", emoji="❓")
            ]
            super().__init__(placeholder="Wähle das passende Hauptthema deiner Frage!", min_values=1, max_values=1, options=selectOptions)

        async def callback(self, interaction: nextcord.Interaction):
            member = interaction.user
            if self.values[0] == "Discord Support":
                embed = nextcord.Embed(title="Discord Support", color=0xff0000)
                embed.add_field(name="Wie bekomme ich die <@576153071768567850> oder <@768183047627210774>-Rolle?", value="Diese Rollen kriegt man in der Regel vom OC-Team durch Events oder für andere besondere Taten für Berlin.", inline=False)
                embed.set_footer(text="Haben dir diese Fragen weitergeholfen?")
                view=RateHelp()
                await interaction.response.edit_message(embed=embed, view=view)
            elif self.values[0] == "Roblox Support":
                print("soon...")
            elif self.values[0] == "Eine Frage beantragen":
                applymodal = ApplyModal()
                await interaction.response.send_modal(applymodal)
    
    class DropDownMenuView(nextcord.ui.View):
        def __init__(self):
            super().__init__()
            self.add_item(DropDownMenu())

    await interaction.response.send_message(embed=embed, view=DropDownMenuView(), ephemeral=True)




@client.slash_command(name="bugreport", description="Reporte einen Bug, indem du ihn direkt an das Development-Team schickst.")
async def bugreport(interaction: Interaction):
    class BugApplyment(nextcord.ui.Modal):
        def __init__(self):
            super().__init__(
                title="Einen Bug reporten", 
                timeout=1800)

            self.topic = nextcord.ui.TextInput(label="Art des Bugs", placeholder="z.B. UI Bug", min_length=2)
            self.description = nextcord.ui.TextInput(label="Beschreibung des Bugs.", placeholder="z.B. GUI schließt sich nicht mehr.", min_length=2)

            self.add_item(self.topic)
            self.add_item(self.description)

        async def callback(self, interaction: nextcord.Interaction): 
            embed = nextcord.Embed(title="Neuer Bug Report!", description=self.topic.value, color=0xff0000)
            embed.add_field(name="Beschreibung des Bugs (Wie ist der Bug enstanden?/Was hast du gemacht?)", value=self.description.value)
            embed.set_footer(text=f"Bug Report von {interaction.user} ({interaction.user.id})")
            embed.set_thumbnail(url=interaction.user.avatar.url)
            channel = client.get_channel(1023971014629138492)
            await channel.send(embed=embed)
            await interaction.response.send_message("``✔️`` Dein Bug Report wurde an das Development-Team weitergeleitet! Danke für das melden deines Bugs.", ephemeral=True)

    return await interaction.response.send_modal(BugApplyment())