import pytz
from datetime import datetime

def get_today_str():
    # Use IST for consistency
    tz = pytz.timezone('Asia/Kolkata')
    return datetime.now(tz).strftime('%Y-%m-%d')
