import asyncio
import discord
from io import StringIO
import sys
from discord.ext import commands

class Productivity(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.to_do = {}
    
    @commands.command()
    async def todo(self, ctx, action=None, *, task=None):
        serverID = ctx.guild.id
        userID = ctx.author.id
        if serverID not in self.to_do:
            self.to_do[serverID] = {}
        
        if userID not in self.to_do[serverID]:
            self.to_do[serverID][userID] = []
        obj = self.to_do[serverID][userID]
        aliases = {
            "add": ["add", "a", "+"],
            "remove": ["remove", "rm", "-", "del", "delete"],
            "clear" : ["clear", "c", "clr"],
        }
        if not action:
            embed = discord.Embed(title="To-Do List", description="Add a task to the to-do list", color=0x00ff00)
            if obj:
                for x, i in enumerate(obj):
                    embed.add_field(name=f"Task {x}", value="`{}. {}`".format(x, i), inline=False)
            else:
                embed.add_field(name="No tasks!", value="You don't have tasks currently. Congratulations!", inline=False)
            await ctx.send(embed=embed)
        elif action in aliases["add"]:
            obj.append(task)
            await ctx.send(f"Added task `{task}` to to-do list")
        elif action in aliases["remove"]:
            try:
                task = int(task)
                await ctx.send(f"Removed task `{obj[task]}` from to-do list")
                obj.pop(int(task))
            except ValueError:
                await ctx.send(f"When using `>todo remove`, you must specify the index of the task you wish to remove.\nFor example: `>todo remove 1`")
            except IndexError:
                await ctx.send(f"Task `{task}` does not exist in the to-do list")
        elif action in aliases["clear"]:
            obj.clear()
            await ctx.send("Cleared all tasks from the to-do list.")
        elif action == "viewraw":
            await ctx.send(f"```{self.to_do[serverID]}```")
        else:
            await ctx.send("Invalid action. Valid actions are: `add`, `remove`, and `clear`")