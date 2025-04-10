# InactivityTray

A minimalist macOS tray application that starts a bundled `xmrig` binary after 10 seconds of user inactivity and stops it when activity resumes. A tray icon visually reflects the state: paused or active (running).

## 🔧 Features

- Detects keyboard and mouse inactivity using macOS APIs.
- Starts/stops a local `xmrig` binary accordingly.
- Tray icon updates dynamically to reflect the state.
- Menu bar option to pause/resume monitoring or quit.
- Built with Python 3 and PyObjC.

---

## 🧱 Prerequisites

- macOS (Apple Silicon supported)
- [Python 3 (via Homebrew)](https://brew.sh/)
- [Platypus](https://sveinbjorn.org/platypus) (for creating the `.app` bundle)
- The `xmrig` binary compiled for Apple Silicon

---

## 📦 Setup

### 1. Clone or Download

```
git clone https://github.com/yourname/InactivityTray.git
cd InactivityTray
```

### 2. Create a Python virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install pyobjc
```

---

## 🚀 Run Without Packaging

While developing:

```bash
source venv/bin/activate
python tray_inactivity_monitor.py
```

---

## 🛠 Create `.app` with Platypus

1. Open Platypus or install it via:

```bash
brew install --cask platypus
```

2. In Platypus:

- Script: `tray_inactivity_monitor.py`
- Interface: `None` (background)
- App Name: `InactivityTray`
- Interpreter: Use full path to `venv/bin/python`
- Check `Remain running after execution`
- Add these files/folders under “Files to be bundled”:
  - `Resources/icon_paused.png`
  - `Resources/icon_running.png`
  - `xmrig/` (folder containing your Apple Silicon `xmrig` binary)

3. Click **Create App**.

---

## 📁 Project Structure

```
InactivityTray/
├── tray_inactivity_monitor.py
├── Resources/
│   ├── icon_paused.png
│   └── icon_running.png
├── xmrig/
│   └── xmrig  # your binary here
├── venv/      # your virtual environment
└── README.md
```

---

## ✅ Tips

- To auto-launch on login, add the `.app` to System Preferences → Users & Groups → Login Items.
- You can create a `@2x` version of icons for Retina displays if needed.

---

## 🧼 License

MIT License (or adapt if needed)