import discord
from discord.ext import commands
from cogs.apis import wikipedia, wolfram, oxford
import json
import pyshorteners

def split_chunks(l, n):
    for i in range(0, len(l), n): 
        yield l[i:i + n]
class HelpDropdown(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(
                label="searchWikiQuery",
                description="Wikipedia from query",
                value="searchWikiQuery"
            ),
            discord.SelectOption(
                label="searchWikiID",
                description="Wikipedia from Page ID",
                value="searchWikiID"
            ),
            discord.SelectOption(
                label="whatIs",
                description="What is...",
                value="whatIs"
            ),
            discord.SelectOption(
                label="dlWikiPDF",
                description='Download Wikipedia in PDF',
                value="dlWikiPDF"
            ),
            discord.SelectOption(
                label="dictionary",
                description="Dictionary",
                value="dictionary"
            ),
            discord.SelectOption(
                label="thesaurus",
                description="Thesaurus",
                value="thesaurus"
            ),
            discord.SelectOption(
                label="todo",
                description="Todo",
                value="todo"
            )
        ]
        super().__init__(placeholder='...', min_values=1, max_values=1, options=options)
    
    async def callback(self, interaction: discord.Interaction):
        sent = False
        if self.values[0] == "searchWikiQuery":
            embed = discord.Embed(title="Wikipedia from query", description="Enter a query to get a Wikipedia article")
            embed.add_field(name="How to use:", value="Add the query after the command.", inline=False)
            embed.add_field(name="Example command:", value="`>wikiFromQuery The Hitchhiker's Guide to the Galaxy`", inline=False)
            embed.add_field(name="Response:", value="The Hitchhiker's Guide to the Galaxy is a comedy science fiction franchise created by Douglas Adams.", inline=False)
            await interaction.response.edit_message(embed=embed)
        elif self.values[0] == "searchWikiID":
            embed = discord.Embed(title="Wikipedia from Page ID", description="Enter a Page ID to get a Wikipedia article")
            embed.add_field(name="How to use:", value="Add the Page ID after the command.", inline=False)
            embed.add_field(name="Example", value="`>wikiFromPage 5472903`", inline=False)
            embed.add_field(name="Response:", value="'Never Gonna Give You Up'is the debut single recorded by English singer and songwriter Rick Astley, released on 27 July 1987.", inline=False)
            await interaction.response.edit_message(embed=embed)
        elif self.values[0] == "whatIs":
            embed = discord.Embed(title="What is...", description="Enter a query to get a Wolfram Alpha answer")
            embed.add_field(name="How to use:", value="Add the query after the command.", inline=False)
            embed.add_field(name="Example", value="`>whatIs the area of circle`", inline=False)
            embed.add_field(name="Response:", value="The area of a circle is πr^2.", inline=False)
            await interaction.response.edit_message(embed=embed)
        elif self.values[0] == "dlWikiPDF":
            embed = discord.Embed(title="Download Wikipedia in PDF", description="Returns a link that redirects you to a direct download link to the Wikipedia article.")
            embed.add_field(name="How to use:", value="Add the query after the command.", inline=False)
            embed.add_field(name="Example", value="`>dlWikiPDF The Hitchhiker's Guide to the Galaxy`", inline=False)
            embed.add_field(name="Response:", value="https://tinyurl.com/xxxxxxxx", inline=False)
            await interaction.response.edit_message(embed=embed)
        elif self.values[0] == "dictionary":
            embed = discord.Embed(title="Dictionary", description="Enter a query to get a dictionary answer")
            embed.add_field(name="How to use:", value="Add the query after the command.", inline=False)
            embed.add_field(name="Example", value="`>dictionary apprentice`", inline=False)
            embed.add_field(name="Response:", value="The word 'apprentice' is a noun.", inline=False)
            await interaction.response.edit_message(embed=embed)
        elif self.values[0] == "thesaurus":
            embed = discord.Embed(title="Thesaurus", description="Enter a query to get a thesaurus answer")
            embed.add_field(name="How to use:", value="Add the query after the command.", inline=False)
            embed.add_field(name="Example", value="`>thesaurus apprentice`", inline=False)
            embed.add_field(name="Response:", value="Synonyms: trainee, learner", inline=False)
            await interaction.response.edit_message(embed=embed)
        elif self.values[0] == "todo":
            embed = discord.Embed(title="Todo", description="Enter a query to get a todo answer")
            embed.add_field(name="How to use:", value="Add the query after the command.", inline=False)
            embed.add_field(name="Actions: ", value="`add: [add, a, +]\nremove: [remove, rm, r, del, delete]\nclear: [clear, clr, c]`")
            embed.add_field(name="Example", value="`>todo add drink water`", inline=False)
            embed.add_field(name="Response:", value="Added drink water to todo list.", inline=False)
            await interaction.response.edit_message(embed=embed)
        elif self.values[0] == "book":
            embed = discord.Embed(title="Book", description="Enter a query to download a book")
            embed.add_field(name="How to use:", value="Add the query after the command.", inline=False)
            embed.add_field(name="Actions: ", value="`search: [search, s]\ndownload: [download, dl]`")
            embed.add_field(name="Example", value="`>book search The Hitchhiker's Guide to the Galaxy`", inline=False)
            embed.add_field(name="Response:", value="The Hitchhiker's Guide to the Galaxy is a comedy science fiction franchise created by Douglas Adams.", inline=False)
            await interaction.response.edit_message(embed=embed)
class HelpView(discord.ui.View):
    def __init__(self, *, timeout=10):
        super().__init__(timeout=timeout)
        self.add_item(HelpDropdown())
        self.timeout = timeout
    
    async def on_timeout(self) -> None:
        await self.message.edit(view=None)

class bookPageEngine(discord.ui.View):
    def __init__(self, *, timeout=10, results=None, query=None, fiction=False):
        super().__init__(timeout=timeout)
        self.results = results
        self.timeout = timeout
        self.page = 1
        self.query = query
        self.fiction = fiction
    async def on_timeout(self) -> None:
        for item in self.children:
            item.disabled = True
        await self.message.edit(view=self)
    
    @discord.ui.button(label="Previous Page", style=discord.ButtonStyle.green, emoji="⬅")
    async def previous_page(self, button:discord.ui.Button,interaction:discord.Interaction):
        if not self.page - 1 == 0:
            self.page -= 1
            embed = discord.Embed(title="Search results for: {}".format(self.query), color=0xFFFFFF)
            if not self.fiction:
                for i in self.results[self.page - 1]:
                    embed.add_field(name=i.get("Title"), value="Author: **`{}`**\nLanguage: **`{}`**\n File Extension: **`{}`**\nMD5 Hash: **`{}`**".format(i.get("Author"), i.get("Language"),i.get("Extension"), i.get("Mirror_1").split("/")[-1]), inline=False)
            else:
                for i in self.results[self.page - 1]:
                    embed.add_field(name=i.get("Title"), value="Author: **`{}`**\nLanguage: **`{}`**\n File Extension: **`{}`**\nMD5 Hash: **`{}`**".format(i.get("Author"), i.get("Language"),i.get("Extension"), i.get("Mirrors")[0].split("/")[-1]), inline=False)
            await interaction.response.edit_message(embed=embed)
        else:
            await interaction.response.send_message('You are on the first page.', ephemeral=True)
    
    @discord.ui.button(label='Next Page', style=discord.ButtonStyle.green, emoji='➡')
    async def next_page(self, button:discord.ui.Button,interaction:discord.Interaction):
        self.page += 1
        if self.page - 1 != len(self.results):
            embed = discord.Embed(title="Search results for: {}".format(self.query), color=0xFFFFFF)
            if not self.fiction:
                for i in self.results[self.page - 1]:
                    embed.add_field(name=i.get("Title"), value="Author: **`{}`**\nLanguage: **`{}`**\n File Extension: **`{}`**\nMD5 Hash: **`{}`**".format(i.get("Author"), i.get("Language"),i.get("Extension"), i.get("Mirror_1").split("/")[-1]), inline=False)
            else:
                for i in self.results[self.page - 1]:
                    embed.add_field(name=i.get("Title"), value="Author: **`{}`**\nLanguage: **`{}`**\n File Extension: **`{}`**\nMD5 Hash: **`{}`**".format(i.get("Author"), i.get("Language"),i.get("Extension"), i.get("Mirrors")[0].split("/")[-1]), inline=False)
            await interaction.response.edit_message(embed=embed)
        else:
            await interaction.response.send_message('You are on the last page.', ephemeral=True)
class wikiPageEngine(discord.ui.View):
    def __init__(self, *, timeout=10, results=None, page=None, title=None, type=None):
        super().__init__()
        self.timeout = timeout
        self.results = results
        self.page = page
        self.title = title
        self.type = type
        
    async def on_timeout(self) -> None:
        for item in self.children:
            item.disabled = True
        await self.message.edit(view=self)
    @discord.ui.button(label="Previous Page", style=discord.ButtonStyle.green, emoji="⬅")
    async def previous_page(self, button:discord.ui.Button,interaction:discord.Interaction):
        if not self.page - 1 == 0:
            self.page -= 1
            new_embed = discord.Embed(title=self.title, color=0xFFFFFF)
            i = self.results[self.page - 1]
            new_embed.add_field(name=i.get('title'), value=i.get("extract"), inline=False)
            new_embed.set_footer(text='Page id: {}'.format(i.get("pageid")))
            await interaction.response.edit_message(view=self, embed=new_embed)
        else:
            await interaction.response.send_message('You are on the first page.', ephemeral=True)
    

    @discord.ui.button(label='Next Page', style=discord.ButtonStyle.green, emoji='➡')
    async def next_page(self, button:discord.ui.Button,interaction:discord.Interaction):
        self.page += 1
        if self.page - 1 != len(self.results):
            
            new_embed = discord.Embed(title=self.title, color=0xFFFFFF)
            i = self.results[self.page - 1]
            new_embed.add_field(name=i.get('title'), value=i.get("extract"), inline=False)
            new_embed.set_footer(text='Page id: {}'.format(i.get("pageid")))
            await interaction.response.edit_message(view=self, embed=new_embed)
        else:
            await interaction.response.send_message('You are on the last page', ephemeral=True)

class wolframPageEngine(discord.ui.View):
    def __init__(self, *, timeout=10, results=None, page=None):
        super().__init__()
        self.timeout = timeout
        self.results = results
        self.page = page
    async def on_timeout(self) -> None:
        for item in self.children:
            item.disabled = True
        await self.message.edit(view=self)
    @discord.ui.button(label="Previous Subpod", style=discord.ButtonStyle.green, emoji="⬅")
    async def previous_page(self, button:discord.ui.Button,interaction:discord.Interaction):
        if not self.page - 1 == 0:
            self.page -= 1
            embed = discord.Embed(title=self.results[self.page - 1].get('dataType'), color=0xFFFFFF)
            for i in self.results[self.page - 1].get("subpods"):
                embed.set_image(url=i.get("img"))
            await interaction.response.edit_message(embed=embed)
        else:
            await interaction.response.send_message('You are on the first subpod.', ephemeral=True)
    
    @discord.ui.button(label='Next Subpod', style=discord.ButtonStyle.green, emoji='➡')
    async def next_page(self, button:discord.ui.Button,interaction:discord.Interaction):
        self.page += 1
        if self.page - 1 != len(self.results):
            embed = discord.Embed(title=self.results[self.page - 1].get('dataType'), color=0xFFFFFF)
            for i in self.results[self.page - 1].get("subpods"):
                embed.set_image(url=i.get("img"))
            await interaction.response.edit_message(embed=embed)
        else:
            await interaction.response.send_message('You are on the last subpod.', ephemeral=True)

class oxfordPageEngine(discord.ui.View):
    def __init__(self, *, timeout=10, results=None, word=None):
        super().__init__()
        self.timeout = timeout
        self.results = results
        self.word = word
        self.page = 1
    async def on_timeout(self) -> None:
        for item in self.children:
            item.disabled = True
        await self.message.edit(view=self)
    @discord.ui.button(label="Previous Result", style=discord.ButtonStyle.green, emoji="⬅")
    async def previous_page(self, button:discord.ui.Button,interaction:discord.Interaction):
        self.page -= 1
        if self.page - 1 == 0:
            #self.results = entry: {...}
            #self.results =         ^^^
            embed = discord.Embed(title=self.word, color=0xFFFFFF)
            i = self.results.get("lexicalEntries")[self.page - 1]
            if i.get("entries")[0].get("lexicalCategory"):
                embed.add_field(name="Category:", value=i.get("entries")[0].get("lexicalCategory"), inline=False)
            if i.get("pronunciations"):
                embed.add_field(name="Pronunciation:", value=i.get("entries")[0].get("pronunciations")[0].get("phoneticSpelling") + "\n" + "[How to pronounce]({})".format(i.get("entries")[0].get("pronunciations")[0].get('audioFile')), inline=False)
            if i.get("entries")[0].get("origin"):
                embed.add_field(name="Origin:", value="".join(i.get("entries")[0].get("origin")), inline=False)
            if i.get("entries")[0].get("senses")[0].get("definitions"):
                embed.add_field(name="Definition:", value="\n".join(i.get("entries")[0].get("senses")[0].get("definitions")), inline=False)
            if i.get("entries")[0].get("senses")[0].get("examples"):
                embed.add_field(name="Examples:", value="\n".join(i.get("entries")[0].get("senses")[0].get("examples")), inline=False)
            if i.get("entries")[0].get("senses")[0].get("synonyms"):
                embed.add_field(name="Synonyms:", value="\n".join(i.get("entries")[0].get("senses")[0].get("synonyms")), inline=False)
            if i.get("entries")[0].get("senses")[0].get("antonyms"):
                embed.add_field(name="Antonyms:", value="\n".join(i.get("entries")[0].get("senses")[0].get("antonyms")), inline=False)
            await interaction.response.edit_message(embed=embed)
        else:
            await interaction.response.send_message('You are on the first result.', ephemeral=True)
    @discord.ui.button(label='Next Result', style=discord.ButtonStyle.green, emoji='➡')
    async def next_page(self, button:discord.ui.Button,interaction:discord.Interaction):
        self.page += 1
        if self.page - 1 != len(self.results.get("lexicalEntries")):
            embed = discord.Embed(title=self.word, color=0xFFFFFF)
            i = self.results.get("lexicalEntries")[self.page - 1]
            if i.get("entries")[0].get("lexicalCategory"):
                embed.add_field(name="Category:", value=i.get("entries")[0].get("lexicalCategory"), inline=False)
            if i.get("pronunciations"):
                embed.add_field(name="Pronunciation:", value=i.get("entries")[0].get("pronunciations")[0].get("phoneticSpelling") + "\n" + "[How to pronounce]({})".format(i.get("entries")[0].get("pronunciations")[0].get('audioFile')), inline=False)
            if i.get("entries")[0].get("origin"):
                embed.add_field(name="Origin:", value="".join(i.get("entries")[0].get("origin")), inline=False)
            if i.get("entries")[0].get("senses")[0].get("definitions"):
                embed.add_field(name="Definition:", value="\n".join(i.get("entries")[0].get("senses")[0].get("definitions")), inline=False)
            if i.get("entries")[0].get("senses")[0].get("examples"):
                embed.add_field(name="Examples:", value="\n".join(i.get("entries")[0].get("senses")[0].get("examples")), inline=False)
            if i.get("entries")[0].get("senses")[0].get("synonyms"):
                embed.add_field(name="Synonyms:", value="\n".join(i.get("entries")[0].get("senses")[0].get("synonyms")), inline=False)
            if i.get("entries")[0].get("senses")[0].get("antonyms"):
                embed.add_field(name="Antonyms:", value="\n".join(i.get("entries")[0].get("senses")[0].get("antonyms")), inline=False)
            await interaction.response.edit_message(embed=embed)
        else:
            await interaction.response.send_message('You are on the last result.', ephemeral=True)

class MainCogs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.wiki = wikipedia.Wikipedia()
        self.wolfram = wolfram.Wolfram()
        self.wolframCalls = 0
        self.oxford = oxford.OxfordDictionaries()
        self.shorten = pyshorteners.Shortener()
    @commands.command()
    async def wiki(self, ctx, action, *, query):
        aliases = {
            "search" : ['search', 's', "query", "q"],
            "download" : ['download', 'd', "dl"],
            "id" : ['id', 'i']
        }
        if action in aliases.get("search"):
            obj = list(self.wiki.fromQuery(query))
            page = 1
            embed = discord.Embed(title="Search Results")
            i = obj[0]
            embed.add_field(name=i.get('title'), value=i.get("extract"), inline=False)
            embed.set_footer(text='Page id: {}'.format(i.get("pageid")))
            view = wikiPageEngine(results=obj, page=page, title="Search Results")
            view.message = await ctx.send(embed=embed, view=view)
        elif action in aliases.get("download"):
            ddl = self.wiki.dlPDF(query)
            embed = discord.Embed(title="Download PDF: {}".format(query))
            embed.add_field(name="Download here", value=f"[Direct Download Link]({ddl})", inline=False)
            await ctx.send(embed=embed)
        elif action in aliases.get("id"):
            obj = list(self.wiki.fromPageID(id))[0]
            embed = discord.Embed(title=obj.get("title"), url="https://en.wikipedia.org/wiki/{}".format(obj.get("title").replace(" ", "_")))
            embed.set_thumbnail(url=obj.get("thumbnail"))
            embed.add_field(name="Contents: ", value=obj.get("extract"), inline=False)
            embed.set_footer(text="Page ID: {}".format(obj.get("pageid")))
            await ctx.send(embed=embed)

    @commands.command()
    async def whatIs(self, ctx, *, query):
        self.wolframCalls += 1
        if self.wolframCalls > 1900:
            await ctx.send("WARNING: The API free calls is running low. Remaining: {}".format(self.wolframCalls, 2000 - self.wolframCalls))
        if self.wolframCalls == 2000:
            await ctx.send("You have exceeded the maximum number of the API free calls using the StudyBot App ID. Switching to `demo` app ID.")
            self.wolfram.setAppID("demo")
            
        obj = self.wolfram.filterResults(query=query)
        pods = obj.get("pods")
        embed = discord.Embed(title=pods[0].get("dataType"), color=0xFFFFFF)
        for i in pods[0].get("subpods"):
            embed.set_image(url=i.get("img"))
        view = wolframPageEngine(results=pods, page=1)
        view.message = await ctx.send(view=view, embed=embed)
    

    @commands.command()
    async def help(self, ctx):
        view = HelpView()
        view.message = await ctx.send("Select a command:", view=view)
    
    @commands.command()
    async def credits(self, ctx):
        embed = discord.Embed(title="Credits")
        embed.add_field(name="Created by: ", value="[dwnppo#8736](https://discord.com/users/897656082313383968)", inline=False)
        embed.add_field(name="Source code: ", value="[GitHub page](https://github.com/dwnppoalt/pyStudy)", inline=False)
        await ctx.send(embed=embed)
    
    @commands.command()
    async def dictionary(self, ctx, *, query):
        obj = self.oxford.dictionary(query)
        embed = discord.Embed(title=query, color=0xFFFFFF)
        i = obj[0].get("lexicalEntries")[0]
        if i.get("entries")[0].get("lexicalCategory"):
                embed.add_field(name="Category:", value=i.get("entries")[0].get("lexicalCategory"), inline=False)
        if i.get("pronunciations"):
            embed.add_field(name="Pronunciation:", value=i.get("entries")[0].get("pronunciations")[0].get("phoneticSpelling") + "\n" + "[How to pronounce]({})".format(i.get("entries")[0].get("pronunciations")[0].get('audioFile')), inline=False)
        if i.get("entries")[0].get("origin"):
            embed.add_field(name="Origin:", value="".join(i.get("entries")[0].get("origin")), inline=False)
        if i.get("entries")[0].get("senses")[0].get("definitions"):
            embed.add_field(name="Definition:", value="\n".join(i.get("entries")[0].get("senses")[0].get("definitions")), inline=False)
        if i.get("entries")[0].get("senses")[0].get("examples"):
            embed.add_field(name="Examples:", value="\n".join(i.get("entries")[0].get("senses")[0].get("examples")), inline=False)
        if i.get("entries")[0].get("senses")[0].get("synonyms"):
            embed.add_field(name="Synonyms:", value="\n".join(i.get("entries")[0].get("senses")[0].get("synonyms")), inline=False)
        if i.get("entries")[0].get("senses")[0].get("antonyms"):
            embed.add_field(name="Antonyms:", value="\n".join(i.get("entries")[0].get("senses")[0].get("antonyms")), inline=False)
        if len(obj[0].get("lexicalEntries")) > 1:
            view = oxfordPageEngine(results=obj[0], word=query)
            view.message = await ctx.send(embed=embed, view=view)
        else:
            await ctx.send(embed=embed)
    
    @commands.command()
    async def thesaurus(self, ctx, *, query):
        obj = self.oxford.thesaurus(query)
        embed = discord.Embed(title=query, color=0xFFFFFF)
        i = obj[0].get("lexicalEntries")[0]
        if i.get("entries")[0].get("lexicalCategory"):
                embed.add_field(name="Category:", value=i.get("entries")[0].get("lexicalCategory"), inline=False)
        if i.get("entries")[0].get("senses")[0].get("synonyms"):
            embed.add_field(name="Synonyms:", value="\n".join(i.get("entries")[0].get("senses")[0].get("synonyms")), inline=False)
        if i.get("entries")[0].get("senses")[0].get("antonyms"):
            embed.add_field(name="Antonyms:", value="\n".join(i.get("entries")[0].get("senses")[0].get("antonyms")), inline=False)
        if len(obj[0].get("lexicalEntries")) > 1:
            view = oxfordPageEngine(results=obj[0], word=query)
            view.message = await ctx.send(embed=embed, view=view)
        else:
            await ctx.send(embed=embed)
    
    @commands.command()
    async def announce(self, ctx, *, message):
        embed = discord.Embed(title="", color=0xFFFFFF)
        embed.add_field(name="From:", value="[Bot Author](https://discord.com/users/897656082313383968)", inline=False)
        embed.add_field(name="Message:", value=message, inline=False)
        if ctx.author.id == 897656082313383968:
            for guild in self.bot.guilds:
                await guild.text_channels[0].send(embed=embed)
        else:
            await ctx.send("You don't have access to this command, {}.".format(ctx.author.mention))

    @staticmethod
    async def setup(bot):
        await bot.add_cog(MainCogs(bot))
    
