# Discord Personal Task Tracker Bot

A Discord bot to manage daily tasks, track history, generate productivity heatmaps, and sync with Notion.

## Features

- **Personal Task List**: `!addtask`, `!removetask`, `!tasks`
- **Daily Tracking**: `!done`, `!undone`
- **Productivity Heatmap**: `!heatmap [days]`
- **Daily Reminders**: 6 PM IST
- **Notion Sync**: Automatically syncs daily progress to a Notion database.

## Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Environment Variables**:
   Create a `.env` file or set the following variables:
   - `DISCORD_TOKEN`: Your Discord Bot Token
   - `NOTION_TOKEN`: Your Notion Integration Token
   - `NOTION_DB_ID`: ID of the Notion Database
   - `REMIND_CHANNEL_ID`: Channel ID for daily reminders
   - `HEATMAP_DAYS`: Default days for heatmap (default: 30)

3. **Notion Setup**:
   - Create a Database in Notion.
   - Ensure it has a **Title** property named `Name`.
   - Ensure it has a **Date** property named `Date`.
   - Share the database with your Notion Integration.

4. **Run the Bot**:
   ```bash
   python bot.py
   ```

## Commands

- `!addtask <task>`: Add a new task.
- `!removetask <task>`: Remove a task.
- `!tasks`: View today's tasks.
- `!done <task/index>`: Mark a task as done.
- `!undone <task/index>`: Mark a task as undone.
- `!heatmap [days]`: Generate a productivity heatmap.
