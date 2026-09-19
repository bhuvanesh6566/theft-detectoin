# Laptop Theft Detection System 🔐

A computer-vision project that detects motion/face activity and can send alerts through Telegram.

## Setup
```bash
pip install -r requirements.txt
```
Create `known_faces/` and add authorized reference photos. Configure Telegram credentials through environment/configuration rather than committing secrets.

## Run
```bash
python theft_detection.py
```

## Workflow
1. Monitor for movement
2. Perform face recognition when needed
3. Trigger an alarm for suspicious activity
4. Send an alert/photo through Telegram

> Use only on devices and environments you own or are authorized to monitor.