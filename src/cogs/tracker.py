import discord
from discord.ext import commands
from src.data.database import load_db, save_db, get_user_data, ensure_today_history, resolve_task
from src.services.notion import sync_to_notion
from src.services.heatmap import generate_heatmap_image
from src.utils import get_today_str
from src.config import HEATMAP_DAYS, REMIND_CHANNEL_ID

class Tracker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def addtask(self, ctx, *, task: str):
        data = load_db()
        user_data = get_user_data(data, ctx.author.id)
        
        if task in user_data["tasks"]:
            await ctx.send(f"Task '{task}' already exists.")
            return

        user_data["tasks"].append(task)
        ensure_today_history(user_data)
        
        save_db(data)
        await ctx.send(f"Added task: {task}")

    @commands.command()
    async def removetask(self, ctx, *, task: str):
        data = load_db()
        user_data = get_user_data(data, ctx.author.id)
        
        target_task = None
        if task in user_data["tasks"]:
            target_task = task
        else:
            matches = [t for t in user_data["tasks"] if task.lower() in t.lower()]
            if len(matches) == 1:
                target_task = matches[0]
            elif len(matches) > 1:
                await ctx.send(f"Multiple tasks match '{task}': {', '.join(matches)}. Be more specific.")
                return
        
        if target_task:
            user_data["tasks"].remove(target_task)
            today = get_today_str()
            if today in user_data["history"] and target_task in user_data["history"][today]:
                del user_data["history"][today][target_task]
                
            save_db(data)
            await ctx.send(f"Removed task: {target_task}")
        else:
            await ctx.send(f"Task '{task}' not found.")

    @commands.command()
    async def tasks(self, ctx):
        data = load_db()
        user_data = get_user_data(data, ctx.author.id)
        today_history = ensure_today_history(user_data)
        save_db(data)

        if not user_data["tasks"]:
            await ctx.send("You have no tasks. Use `!addtask <task>` to add one.")
            return

        msg = "Your tasks:\n"
        for i, task in enumerate(user_data["tasks"], 1):
            status = "[x]" if today_history.get(task, False) else "[ ]"
            msg += f"{i}. {status} {task}\n"
        
        await ctx.send(f"```\n{msg}\n```")

    @commands.command()
    async def done(self, ctx, *, task_ref: str):
        data = load_db()
        user_data = get_user_data(data, ctx.author.id)
        ensure_today_history(user_data)
        
        task, error = resolve_task(user_data, task_ref)
        if error:
            await ctx.send(error)
            return
            
        today = get_today_str()
        user_data["history"][today][task] = True
        save_db(data)
        
        await sync_to_notion(ctx.author.id, user_data)
        await ctx.send(f"Marked as done: {task}")

    @commands.command()
    async def undone(self, ctx, *, task_ref: str):
        data = load_db()
        user_data = get_user_data(data, ctx.author.id)
        ensure_today_history(user_data)
        
        task, error = resolve_task(user_data, task_ref)
        if error:
            await ctx.send(error)
            return
            
        today = get_today_str()
        user_data["history"][today][task] = False
        save_db(data)
        
        await sync_to_notion(ctx.author.id, user_data)
        await ctx.send(f"Marked as undone: {task}")

    @commands.command()
    async def heatmap(self, ctx, days: int = HEATMAP_DAYS):
        data = load_db()
        user_data = get_user_data(data, ctx.author.id)
        
        if not user_data["history"]:
            await ctx.send("No history found.")
            return
            
        buf = generate_heatmap_image(user_data, days)
        file = discord.File(buf, filename="heatmap.png")
        await ctx.send(file=file)

    async def daily_reminder(self):
        print("Running daily reminder...")
        if not REMIND_CHANNEL_ID:
            print("REMIND_CHANNEL_ID not set, skipping reminder.")
            return
            
        channel = self.bot.get_channel(int(REMIND_CHANNEL_ID))
        if channel:
            await channel.send("⏰ Reminder: Update your daily tasks with `!tasks` and mark them as done.")
        else:
            print(f"Could not find channel with ID {REMIND_CHANNEL_ID}")

async def setup(bot):
    await bot.add_cog(Tracker(bot))
