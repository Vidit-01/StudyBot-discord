import matplotlib.pyplot as plt
import io
import pandas as pd
import pytz
from datetime import datetime, timedelta
from src.config import HEATMAP_DAYS

def generate_heatmap_image(user_data, days=HEATMAP_DAYS):
    history = user_data.get("history", {})
    
    # Generate date range
    end_date = datetime.now(pytz.timezone('Asia/Kolkata'))
    start_date = end_date - timedelta(days=days-1)
    
    date_range = pd.date_range(start=start_date.date(), end=end_date.date())
    
    data = []
    for d in date_range:
        d_str = d.strftime('%Y-%m-%d')
        day_tasks = history.get(d_str, {})
        if not day_tasks:
            completion = 0.0
        else:
            total = len(day_tasks)
            done_count = sum(1 for v in day_tasks.values() if v)
            completion = done_count / total if total > 0 else 0.0
        data.append(completion)
        
    # Pad data to align with weeks
    start_weekday = start_date.weekday()
    padded_data = [None] * start_weekday + data
    
    while len(padded_data) % 7 != 0:
        padded_data.append(None)
        
    grid = []
    for i in range(7):
        row = padded_data[i::7]
        grid.append(row)
        
    fig, ax = plt.subplots(figsize=(10, 3))
    im = ax.imshow(grid, cmap="Greens", vmin=0, vmax=1)
    
    days_labels = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    ax.set_yticks(range(7))
    ax.set_yticklabels(days_labels)
    ax.set_xlabel('Weeks')
    ax.set_title(f'Productivity Heatmap (Last {days} Days)')
    
    cbar = ax.figure.colorbar(im, ax=ax)
    cbar.ax.set_ylabel("Completion Rate", rotation=-90, va="bottom")
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    plt.close(fig)
    return buf
