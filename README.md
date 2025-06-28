#GoogleMeet-Extension

An AI-powered **real-time face mesh + concentration bar overlay** that floats above your screen and tracks if you're focused during live video calls (Google Meet, Zoom, etc.).

> Designed for teachers, presenters, or productivity nerds who want to **track attention** during online sessions like a boss.  
> Bonus: ✅ Gen-Z vibes + smooth transparent UI + no mouse interaction.

---

## 🧠 What It Does

- ✅ Uses **MediaPipe Face Mesh** to detect facial landmarks in real time  
- 👀 Estimates **user's concentration %** based on head alignment (are they looking at the screen?)  
- 🟧 Displays a **transparent overlay bar** above all windows — works during Google Meet / Zoom calls  
- 🧼 Doesn't block mouse or keyboard (it's non-interactive)

---

## 🖥️ Demo

_(Add GIF/screenshot here if available)_

---

## 🔧 Requirements

- macOS (tested on M1 MacBook)
- Python 3.8+
- Webcam (built-in or external)

### 🧪 Python Dependencies

Install with pip:

```bash
pip install opencv-python mediapipe pillow pyobjc
```

---

## 🚀 How to Run

1. Clone/download this repo
2. Run the main script:

```bash
python googlemeet.py
```

3. Open **Google Meet or Zoom**, and keep your face in frame.  
You'll see a floating **focus bar** + mesh tracking over your face 👁️‍🗨️

Press `Esc` to quit anytime.

---

## ⚙️ How It Works

- Uses MediaPipe to detect 468 facial landmarks
- Estimates **head alignment** using eye + nose landmark distances
- Maps head orientation → concentration %
- Draws a floating bar on macOS using `NSWindow` (fully transparent and non-blocking)

---

## 🧪 Upcoming Features

- 🎭 Support for **multiple people on screen** (like student tiles in Meet)
- 🔊 Optional **sound alerts** when focus drops
- 🧠 More intelligent concentration detection (e.g., blinking, yawning, head nodding)
- 💬 Emoji reactions when someone is super focused 🔥

---

## 🤝 Credits

- [MediaPipe](https://github.com/google/mediapipe) for landmark detection  
- Apple `pyobjc` for making transparent overlay possible on macOS  
- Built with love & coffee ☕ by **Omkar Patkar**

---

## ⚠️ Disclaimer

> This tool runs only **locally** and does **not send or store any data**.  
Use responsibly during class, meetings, or personal productivity — no surveillance vibes here 🙅‍♂️.
