import cv2
import face_recognition
import requests
import sqlite3
import os
import threading
import winsound
from datetime import datetime
from config import BOT_TOKEN, CHAT_ID

DB_FILE = "intrusions.db"
VIDEO_DURATION_SECONDS = 30
MOTION_THRESHOLD = 5000

# --- DB Setup ---
def init_db():
    conn = sqlite3.connect(DB_FILE)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS intrusions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            photo_path TEXT,
            video_path TEXT,
            location TEXT
        )
    """)
    conn.commit()
    conn.close()

def log_intrusion(timestamp, photo_path, video_path, location):
    conn = sqlite3.connect(DB_FILE)
    conn.execute(
        "INSERT INTO intrusions (timestamp, photo_path, video_path, location) VALUES (?,?,?,?)",
        (timestamp, photo_path, video_path, location)
    )
    conn.commit()
    conn.close()

# --- Location ---
def get_location():
    try:
        r = requests.get("https://ipinfo.io/json", timeout=5)
        data = r.json()
        return f"{data.get('city')}, {data.get('region')}, {data.get('country')} | IP: {data.get('ip')} | Coords: {data.get('loc')}"
    except Exception:
        return "Location unavailable"

# --- Telegram ---
def send_telegram_photo(photo_path, caption=""):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    with open(photo_path, "rb") as photo:
        requests.post(url, data={"chat_id": CHAT_ID, "caption": caption}, files={"photo": photo})

def send_telegram_video(video_path, caption=""):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendVideo"
    with open(video_path, "rb") as video:
        requests.post(url, data={"chat_id": CHAT_ID, "caption": caption}, files={"video": video})

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": text})

# --- Alarm ---
def sound_alarm():
    for _ in range(5):
        winsound.Beep(1000, 500)

# --- Video Recording ---
def record_video(cap, filename, seconds=VIDEO_DURATION_SECONDS):
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    fps = 10
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    out = cv2.VideoWriter(filename, fourcc, fps, (width, height))
    total_frames = fps * seconds
    for _ in range(total_frames):
        ret, frame = cap.read()
        if ret:
            out.write(frame)
    out.release()

# --- Load Known Faces ---
def load_known_faces(folder="known_faces"):
    encodings, names = [], []
    if not os.path.exists(folder):
        os.makedirs(folder)
        print(f"Add known face images to '{folder}/' folder and restart.")
        return encodings, names
    for fname in os.listdir(folder):
        if fname.lower().endswith((".jpg", ".jpeg", ".png")):
            img = face_recognition.load_image_file(os.path.join(folder, fname))
            enc = face_recognition.face_encodings(img)
            if enc:
                encodings.append(enc[0])
                names.append(os.path.splitext(fname)[0])
    return encodings, names

# --- Motion Detection ---
def detect_motion(prev_gray, curr_gray):
    diff = cv2.absdiff(prev_gray, curr_gray)
    _, thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)
    return cv2.countNonZero(thresh) > MOTION_THRESHOLD

# --- Main ---
def main():
    init_db()
    known_encodings, known_names = load_known_faces()

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Camera not accessible.")
        return

    print("Monitoring started. Press ESC to quit.")

    cooldown = {}
    COOLDOWN_SECONDS = 30

    ret, prev_frame = cap.read()
    prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        curr_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        motion_detected = detect_motion(prev_gray, curr_gray)
        prev_gray = curr_gray

        if not motion_detected:
            cv2.imshow("Security Camera", frame)
            if cv2.waitKey(1) == 27:
                break
            continue

        print("Motion detected, scanning for faces...")
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb)
        print(f"Faces found: {len(face_locations)}")
        face_encodings = face_recognition.face_encodings(rgb, face_locations)

        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_encodings, face_encoding) if known_encodings else [False]
            is_known = True in matches

            if not is_known:
                now = datetime.now()
                ts = now.strftime("%Y%m%d_%H%M%S")

                # Cooldown to avoid spam
                last = cooldown.get("last")
                if last and (now - last).seconds < COOLDOWN_SECONDS:
                    continue
                cooldown["last"] = now

                photo_path = f"intruder_{ts}.jpg"
                video_path = f"intruder_{ts}.mp4"
                cv2.imwrite(photo_path, frame)

                location = get_location()
                caption = f"🚨 Intruder detected!\n🕒 {now.strftime('%Y-%m-%d %H:%M:%S')}\n📍 {location}"

                threading.Thread(target=sound_alarm, daemon=True).start()
                send_telegram_photo(photo_path, caption)

                print(f"Intruder detected at {now} | {location}")

                # Record and send video in background
                def record_and_send(cap, video_path, caption):
                    record_video(cap, video_path)
                    send_telegram_video(video_path, f"📹 30s clip\n{caption}")

                threading.Thread(target=record_and_send, args=(cap, video_path, caption), daemon=True).start()

                log_intrusion(str(now), photo_path, video_path, location)

        cv2.imshow("Security Camera", frame)
        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
