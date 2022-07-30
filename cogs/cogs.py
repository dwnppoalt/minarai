import discord
from discord.ext import commands
from cogs.apis import wikipedia, wolfram
from tinq import Tinq

class HelpDropdown(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(
                label="wikiFromQuery",
                description="Wikipedia from query",
                value="wikiFromQuery"
            ),
            discord.SelectOption(
                label="wikiFromID",
                description="Wikipedia from Page ID",
                value="wikiFromID"
            ),
            discord.SelectOption(
                label="whatIs",
                description="What is...",
                value="whatIs"
            ),
        ]
        super().__init__(placeholder='...', min_values=1, max_values=1, options=options)
    
    async def callback(self, interaction: discord.Interaction):
        sent = False
        if self.values[0] == "wikiFromQuery":
            embed = discord.Embed(title="Wikipedia from query", description="Enter a query to get a Wikipedia article")
            embed.add_field(name="How to use:", value="Add the query after the command.", inline=False)
            embed.add_field(name="Example command:", value="`?wikiFromQuery The Hitchhiker's Guide to the Galaxy`", inline=False)
            embed.add_field(name="Response:", value="The Hitchhiker's Guide to the Galaxy is a comedy science fiction franchise created by Douglas Adams.", inline=False)
            await interaction.response.edit_message(embed=embed)
        elif self.values[0] == "wikiFromID":
            embed = discord.Embed(title="Wikipedia from Page ID", description="Enter a Page ID to get a Wikipedia article")
            embed.add_field(name="How to use:", value="Add the Page ID after the command.", inline=False)
            embed.add_field(name="Example", value="`?wikiFromPage 5472903`", inline=False)
            embed.add_field(name="Response:", value="'Never Gonna Give You Up'is the debut single recorded by English singer and songwriter Rick Astley, released on 27 July 1987.", inline=False)
            await interaction.response.edit_message(embed=embed)
        elif self.values[0] == "whatIs":
            embed = discord.Embed(title="What is...", description="Enter a query to get a Wolfram Alpha answer")
            embed.add_field(name="How to use:", value="Add the query after the command.", inline=False)
            embed.add_field(name="Example", value="`?whatIs the area of circle`", inline=False)
            embed.add_field(name="Response:", value="The area of a circle is πr^2.", inline=False)
            await interaction.response.edit_message(embed=embed)

class HelpView(discord.ui.View):
    def __init__(self, *, timeout=10):
        super().__init__(timeout=timeout)
        self.add_item(HelpDropdown())
        self.timeout = timeout
    
    async def on_timeout(self) -> None:
        await self.message.edit(view=None)


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
    async def previous_page(self, interaction:discord.ui.Button,button:discord.Interaction):
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
    async def next_page(self,interaction:discord.ui.Button,button:discord.Interaction):
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
    async def previous_page(self, interaction:discord.ui.Button,button:discord.Interaction):
        if not self.page - 1 == 0:
            self.page -= 1
            embed = discord.Embed(title=self.results[self.page - 1].get('dataType'), color=0xFFFFFF)
            for i in self.results[self.page - 1].get("subpods"):
                embed.set_image(url=i.get("img"))
            await interaction.response.edit_message(embed=embed)
        else:
            await interaction.response.send_message('You are on the first subpod.', ephemeral=True)
    
    @discord.ui.button(label='Next Subpod', style=discord.ButtonStyle.green, emoji='➡')
    async def next_page(self,interaction:discord.ui.Button,button:discord.Interaction):
        self.page += 1
        if self.page - 1 != len(self.results):
            embed = discord.Embed(title=self.results[self.page - 1].get('dataType'), color=0xFFFFFF)
            for i in self.results[self.page - 1].get("subpods"):
                embed.set_image(url=i.get("img"))
            await interaction.response.edit_message(embed=embed)
        else:
            await interaction.response.send_message('You are on the last subpod.', ephemeral=True)


class MainCogs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.wiki = wikipedia.Wikipedia()
        self.wolfram = wolfram.Wolfram()
        self.wolframCalls = 0
        self.tinq = Tinq(api_key="key-8c91a43e-bfa9-4491-8a07-23834efb3482-62e4e7fee88df")
    
    
    @commands.command()
    async def wikiFromQuery(self, ctx, *, query):
        obj = list(self.wiki.fromQuery(query))
        page = 1
        embed = discord.Embed(title="Search Results")
        i = obj[0]
        embed.add_field(name=i.get('title'), value=i.get("extract"), inline=False)
        embed.set_footer(text='Page id: {}'.format(i.get("pageid")))
        view = wikiPageEngine(results=obj, page=page, title="Search Results")
        view.message = await ctx.send(embed=embed, view=view)
    
    @commands.command()
    async def wikiDLPDF(self, ctx, *, query):
        ddl = self.wiki.dlPDF(query)
        embed = discord.Embed(title="Download PDF: {}".format(query))
        embed.add_field(name="Download here", value=f"[Direct Download Link]({ddl})", inline=False)
        await ctx.send(embed=embed)
    @commands.command()
    async def wikiFromID(self, ctx, *, id):
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

    async def setup(self, bot):
        await bot.add_cog(MainCogs(bot))