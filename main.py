import asyncio
import discord
from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import pytz
import logging
from src.config import DISCORD_TOKEN

# Setup logging
logging.basicConfig(level=logging.INFO)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot is ready. Logged in as {bot.user}')
    
    # Start Scheduler
    scheduler = AsyncIOScheduler()
    # Schedule daily reminder at 6 PM IST (or 23:45 as per user edit)
    # Using 18:00 as per spec, but user changed it to 23:45 manually.
    # I will respect the user's manual change to 23:45.
    trigger = CronTrigger(hour=23, minute=45, timezone=pytz.timezone('Asia/Kolkata'))
    
    # We need to access the daily_reminder method from the Cog instance
    tracker_cog = bot.get_cog('Tracker')
    if tracker_cog:
        scheduler.add_job(tracker_cog.daily_reminder, trigger)
        scheduler.start()
        print("Scheduler started.")
    else:
        print("Tracker Cog not found, scheduler not started.")

async def main():
    async with bot:
        await bot.load_extension('src.cogs.tracker')
        if DISCORD_TOKEN:
            await bot.start(DISCORD_TOKEN)
        else:
            print("Error: DISCORD_TOKEN not found in environment variables.")

if __name__ == '__main__':
    asyncio.run(main())
