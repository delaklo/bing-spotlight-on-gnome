#!/usr/bin/env python3
# Script to download Bing daily wallpaper and set it as GNOME wallpaper

import os
import requests
from datetime import datetime
import subprocess

# Directory to save wallpapers
wallpaper_dir = os.path.expanduser("~/Pictures/Spotlight")
os.makedirs(wallpaper_dir, exist_ok=True)

# URL for Bing daily wallpaper (resolution 1920x1080)
bing_url = "https://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=en-US"

try:
    # Fetch JSON data
    response = requests.get(bing_url, timeout=10)
    response.raise_for_status()
    data = response.json()
    img_url = "https://www.bing.com" + data['images'][0]['url']

    # Create unique file name based on date
    file_name = datetime.now().strftime("%Y-%m-%d") + ".jpg"
    file_path = os.path.join(wallpaper_dir, file_name)

    # Download image if it doesn't exist
    if not os.path.exists(file_path):
        img_data = requests.get(img_url, timeout=10).content
        with open(file_path, "wb") as f:
            f.write(img_data)
        print(f"Downloaded: {file_path}")
    else:
        print(f"Already exists: {file_path}")

    # Set the image as GNOME wallpaper (both light and dark mode)
    subprocess.run([
        "gsettings", "set", "org.gnome.desktop.background", "picture-uri", f"file://{file_path}"
    ], check=True)
    
    subprocess.run([
        "gsettings", "set", "org.gnome.desktop.background", "picture-uri-dark", f"file://{file_path}"
    ], check=True)

    print(f"Wallpaper set successfully: {file_path}")

except Exception as e:
    print(f"Error: {e}")
    exit(1)
