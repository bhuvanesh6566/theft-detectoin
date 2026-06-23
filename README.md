# Laptop Theft Detection System

## Setup

### 1. Install Dependencies
```
pip install -r requirements.txt
```
> Note: `face-recognition` requires CMake and Visual C++ Build Tools on Windows.
> Install from: https://visualstudio.microsoft.com/visual-cpp-build-tools/

### 2. Add Known Faces
Create a `known_faces/` folder and add photos named after each person:
```
known_faces/
    owner.jpg
    family_member.png
```

### 3. Configure Telegram
- Create a bot via @BotFather on Telegram → get your `BOT_TOKEN`
- Get your `CHAT_ID`: visit `https://api.telegram.org/botYOUR_TOKEN/getUpdates` after sending any message to your bot
- Set `BOT_TOKEN` and `CHAT_ID` in `theft_detection.py`

### 4. Run
```
python theft_detection.py
```

### 5. Auto-Start on Windows Boot
1. Press `Win + R` → type `shell:startup` → press Enter
2. Copy `startup.bat` into that folder

## How It Works
| Feature | Details |
|---|---|
| Motion detection | Skips face scan when no movement, saves CPU |
| Face recognition | Matches against all images in `known_faces/` |
| Alarm | Beeps 5 times via system speaker |
| Telegram alert | Sends photo + location caption immediately |
| 30s video | Records and sends clip in background thread |
| Location | Uses IP geolocation (city, country, coordinates) |
| Database | Logs all intrusions to `intrusions.db` (SQLite) |
| Cooldown | 30-second cooldown per detection to prevent spam |

## Database Schema
```sql
intrusions(id, timestamp, photo_path, video_path, location)
```
Query with any SQLite viewer or:
```python
import sqlite3
conn = sqlite3.connect("intrusions.db")
for row in conn.execute("SELECT * FROM intrusions"):
    print(row)
```
