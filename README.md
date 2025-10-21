
![Python](https://img.shields.io/badge/python-3.6+-blue.svg)
![GNOME](https://img.shields.io/badge/desktop-GNOME-blue.svg)

# Bing Spotlight Wallpaper for GNOME

Automatically download daily Bing wallpapers and set them as your GNOME desktop background. Made with Claude 3.5 Sonnet.


## Features

- 🖼️ Daily wallpaper updates from Bing
- 🔄 Automatic setup via systemd
- 🌓 Supports both light and dark themes
- 📁 Saves all wallpapers to `~/Pictures/Spotlight`
- ⏰ Customizable update schedule
- 🚀 Runs on system boot

## Requirements

- Python 3
- GNOME Desktop Environment
- `requests` library

## Installation

### 1. Install dependencies

```bash
pip3 install requests
```

### 2. Download and install the script

```bash
# Create scripts directory (if it doesn't exist)
mkdir -p ~/.local/bin

# Download the script
curl -o ~/.local/bin/spotlight.py https://raw.githubusercontent.com/delaklo/bing-spotlight-on-gnome/main/spotlight.py

# Make it executable
chmod +x ~/.local/bin/spotlight.py
```

### 3. Configure systemd

Create the systemd user directory:

```bash
mkdir -p ~/.config/systemd/user
```

Create **`~/.config/systemd/user/spotlight-wallpaper.service`** with this content:

```ini
[Unit]
Description=Download and set Bing daily wallpaper
After=network-online.target
Wants=network-online.target

[Service]
Type=oneshot
ExecStart=%h/.local/bin/spotlight.py
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=default.target
```

Create **`~/.config/systemd/user/spotlight-wallpaper.timer`** with this content:

```ini
[Unit]
Description=Daily Bing wallpaper download timer
Requires=spotlight-wallpaper.service

[Timer]
# Run at 9:00 AM every day
OnCalendar=daily
OnCalendar=*-*-* 09:00:00
# Run 5 minutes after boot if missed
OnBootSec=5min
# Allow random delay up to 1 hour to avoid server load
RandomizedDelaySec=1h
Persistent=true

[Install]
WantedBy=timers.target
```

**Quick copy-paste commands:**

```bash
# Create service file
cat > ~/.config/systemd/user/spotlight-wallpaper.service << 'EOF'
[Unit]
Description=Download and set Bing daily wallpaper
After=network-online.target
Wants=network-online.target

[Service]
Type=oneshot
ExecStart=%h/.local/bin/spotlight.py
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=default.target
EOF

# Create timer file
cat > ~/.config/systemd/user/spotlight-wallpaper.timer << 'EOF'
[Unit]
Description=Daily Bing wallpaper download timer
Requires=spotlight-wallpaper.service

[Timer]
OnCalendar=daily
OnCalendar=*-*-* 09:00:00
OnBootSec=5min
RandomizedDelaySec=1h
Persistent=true

[Install]
WantedBy=timers.target
EOF
```

### 4. Enable and start the service

```bash
# Reload systemd configuration
systemctl --user daemon-reload

# Enable timer to start automatically
systemctl --user enable spotlight-wallpaper.timer

# Start the timer
systemctl --user start spotlight-wallpaper.timer
```

### 5. Verify installation

```bash
# Check timer status
systemctl --user status spotlight-wallpaper.timer

# Check when next run is scheduled
systemctl --user list-timers

# Run manually for testing
systemctl --user start spotlight-wallpaper.service

# View logs
journalctl --user -u spotlight-wallpaper.service
```

## Configuration

### Change update time

Edit `~/.config/systemd/user/spotlight-wallpaper.timer`:

```ini
[Timer]
OnCalendar=*-*-* 09:00:00  # Change to desired time (e.g., 15:30:00)
```

After changes:

```bash
systemctl --user daemon-reload
systemctl --user restart spotlight-wallpaper.timer
```

### Change wallpaper directory

Edit `~/.local/bin/spotlight.py`:

```python
wallpaper_dir = os.path.expanduser("~/Pictures/Spotlight")  # Change path
```

## File Structure

```
~/.local/bin/spotlight.py                          # Main script
~/.config/systemd/user/spotlight-wallpaper.service # Systemd service
~/.config/systemd/user/spotlight-wallpaper.timer   # Systemd timer
~/Pictures/Spotlight/                              # Wallpaper storage directory
```

## Uninstallation

```bash
# Stop and disable service
systemctl --user stop spotlight-wallpaper.timer
systemctl --user disable spotlight-wallpaper.timer

# Remove files
rm ~/.local/bin/spotlight.py
rm ~/.config/systemd/user/spotlight-wallpaper.service
rm ~/.config/systemd/user/spotlight-wallpaper.timer

# Reload systemd
systemctl --user daemon-reload

# Optionally remove wallpapers
rm -rf ~/Pictures/Spotlight
```

## Troubleshooting

### Service won't start

```bash
# Check logs for errors
journalctl --user -u spotlight-wallpaper.service -n 50

# Verify script is executable
ls -l ~/.local/bin/spotlight.py

# Run script manually for diagnostics
~/.local/bin/spotlight.py
```

### Wallpaper not setting

- Ensure you're using GNOME desktop environment
- Check if `gsettings` is installed
- View logs: `journalctl --user -u spotlight-wallpaper.service`

### No internet connection

Service will automatically wait for connection thanks to `After=network-online.target`.

### Timer not running

```bash
# Verify timer is enabled
systemctl --user is-enabled spotlight-wallpaper.timer

# Check timer list
systemctl --user list-timers --all

# Re-enable if needed
systemctl --user enable spotlight-wallpaper.timer
systemctl --user start spotlight-wallpaper.timer
```

## How It Works

1. **Timer triggers** the service daily at 9:00 AM (configurable)
2. **Service runs** the Python script
3. **Script downloads** the latest Bing wallpaper
4. **Script sets** the wallpaper using `gsettings`
5. **Logs** are stored in systemd journal


## Author

Claude 3.5 Sonnet and delaklo

---

**Tip:** The timer will automatically handle missed runs if your computer was off, thanks to `Persistent=true`!