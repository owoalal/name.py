import requests
import pygame
import time
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from geopy.geocoders import Nominatim

# Initialize pygame for audio
pygame.mixer.init()

# Default API selection
API_SELECTION = "Aladhan"

# Online Athan MP3 URL
ATHAN_MP3_URL = "https://server8.mp3quran.net/saud/001.mp3"

# Function to get user's location (latitude, longitude)
def get_location():
    try:
        geolocator = Nominatim(user_agent="athan_app")
        location = geolocator.geocode("New York")  # Default to NY if GPS fails
        return location.latitude, location.longitude
    except:
        return 40.7128, -74.0060  # Default to NYC

# Function to fetch prayer times
def get_prayer_times():
    lat, lon = get_location()
    url = f"https://api.aladhan.com/v1/timings/{int(time.time())}"
    params = {"latitude": lat, "longitude": lon, "method": 2}

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        timings = data["data"]["timings"]
        return {
            "Fajr": timings["Fajr"][:-3],  # Remove seconds
            "Dhuhr": timings["Dhuhr"][:-3],
            "Asr": timings["Asr"][:-3],
            "Maghrib": timings["Maghrib"][:-3],
            "Isha": timings["Isha"][:-3],
        }
    else:
        return None

# Function to play Athan
def play_athan():
    pygame.mixer.music.load(ATHAN_MP3_URL)
    pygame.mixer.music.play()

# Function to check & play Athan at prayer times
def check_prayer_times():
    prayer_times = get_prayer_times()
    if prayer_times:
        now = datetime.now().strftime("%H:%M")
        for prayer, time in prayer_times.items():
            if now == time:
                messagebox.showinfo("Athan Alert", f"Time for {prayer}!")
                play_athan()
    app.after(60000, check_prayer_times)  # Check again in 1 minute

# Function to stop Athan
def stop_athan():
    pygame.mixer.music.stop()
    messagebox.showinfo("Athan App", "Athan Stopped!")

# Function to update prayer times on the screen
def update_prayer_times():
    times = get_prayer_times()
    if times:
        for prayer, time in times.items():
            prayer_labels[prayer].config(text=f"{prayer}: {time}")
    else:
        messagebox.showerror("Error", "Failed to fetch prayer times.")

# Function for Thikr (Dhikr) Tab
def show_thikr():
    thikr_window = tk.Toplevel(app)
    thikr_window.title("Thikr & Supplications")
    thikr_window.geometry("400x300")
    tk.Label(thikr_window, text="Thikr & Supplications", font=("Arial", 14)).pack(pady=10)

    thikr_list = [
        "SubhanAllah - 33 times",
        "Alhamdulillah - 33 times",
        "Allahu Akbar - 34 times",
        "La ilaha illallah",
        "Astaghfirullah"
    ]

    for thikr in thikr_list:
        tk.Label(thikr_window, text=thikr, font=("Arial", 12)).pack(pady=2)

# GUI Setup
app = tk.Tk()
app.title("Athan & Prayer App")
app.geometry("400x400")

# Tabs
notebook = ttk.Notebook(app)
tab1 = ttk.Frame(notebook)
tab2 = ttk.Frame(notebook)

notebook.add(tab1, text="Prayer Times")
notebook.add(tab2, text="Settings")
notebook.pack(expand=True, fill="both")

# Prayer Times UI
tk.Label(tab1, text="Prayer Times", font=("Arial", 14)).pack(pady=10)
prayer_labels = {}
for prayer in ["Fajr", "Dhuhr", "Asr", "Maghrib", "Isha"]:
    label = tk.Label(tab1, text=f"{prayer}: --:--", font=("Arial", 12))
    label.pack()
    prayer_labels[prayer] = label

tk.Button(tab1, text="Refresh Times", command=update_prayer_times).pack(pady=5)
tk.Button(tab1, text="Stop Athan", command=stop_athan).pack(pady=5)

# Thikr Button
tk.Button(app, text="Thikr & Supplications", command=show_thikr).pack(pady=5)

# Start checking for prayer times every minute
app.after(1000, check_prayer_times)

# Update prayer times on startup
update_prayer_times()

app.mainloop()
