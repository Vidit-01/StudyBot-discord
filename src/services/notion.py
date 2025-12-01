from notion_client import Client
from src.config import NOTION_TOKEN, NOTION_DB_ID
from src.utils import get_today_str

async def sync_to_notion(user_id, user_data):
    if not NOTION_TOKEN or not NOTION_DB_ID:
        return # Notion not configured
        
    try:
        notion = Client(auth=NOTION_TOKEN)
        today_str = get_today_str()
        today_history = user_data["history"].get(today_str, {})
        
        query = notion.databases.query(
            **{
                "database_id": NOTION_DB_ID,
                "filter": {
                    "and": [
                        {
                            "property": "Date",
                            "date": {
                                "equals": today_str
                            }
                        },
                        {
                            "property": "Name",
                            "title": {
                                "contains": str(user_id)
                            }
                        }
                    ]
                }
            }
        )
        
        results = query.get("results")
        
        # Construct blocks for tasks
        children = []
        for task, is_done in today_history.items():
            children.append({
                "object": "block",
                "type": "to_do",
                "to_do": {
                    "rich_text": [{"type": "text", "text": {"content": task}}],
                    "checked": is_done
                }
            })
            
        if results:
            page_id = results[0]["id"]
            notion.pages.update(page_id, archived=True)
            
        # Create new page
        notion.pages.create(
            parent={"database_id": NOTION_DB_ID},
            properties={
                "Name": {"title": [{"text": {"content": f"Tasks for {user_id} on {today_str}"}}]},
                "Date": {"date": {"start": today_str}}
            },
            children=children
        )
        
    except Exception as e:
        print(f"Error syncing to Notion: {e}")
