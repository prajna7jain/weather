import tkinter as tk
from tkinter import ttk
import requests
from PIL import Image, ImageTk
import io

WEATHER_KEY = 'a9d96161ca37b34dd529d5a3592939e6'
WEATHER_URL = 'https://api.openweathermap.org/data/2.5/weather'
ICON_URL = "http://openweathermap.org/img/wn/{}@2x.png"
GEOLOCATE_URL = 'https://ipinfo.io/json'

# Main 
root = tk.Tk()
root.title("🌤 Weather App")
root.geometry("600x520")
root.resizable(False, False)

unit = tk.StringVar(value='imperial')  #

def format_res(weather, unit):
    try:
        city = weather['name']
        condition = weather['weather'][0]['description'].capitalize()
        temp = weather['main']['temp']
        icon_code = weather['weather'][0]['icon']

        unit_symbol = "°F" if unit == 'imperial' else "°C"
        temp = round(temp, 1)

        # Display icon
        icon_response = requests.get(ICON_URL.format(icon_code))
        icon_img = Image.open(io.BytesIO(icon_response.content))
        icon_photo = ImageTk.PhotoImage(icon_img)
        icon_label.config(image=icon_photo)
        icon_label.image = icon_photo

        return f"📍 City: {city}\n🌦️ Condition: {condition}\n🌡️ Temperature: {temp} {unit_symbol}"
    except:
        return "⚠️ Unable to retrieve weather information."

def get_weather(city, unit_mode):
    params = {'APPID': WEATHER_KEY, 'q': city, 'units': unit_mode}
    response = requests.get(WEATHER_URL, params)
    weather = response.json()
    result_label.config(text=format_res(weather, unit_mode))

def search_weather():
    city = city_entry.get()
    get_weather(city, unit.get())

def get_location_and_weather():
    try:
        geo_res = requests.get(GEOLOCATE_URL).json()
        city = geo_res['city']
        city_entry.delete(0, tk.END)
        city_entry.insert(0, city)
        get_weather(city, unit.get())
    except:
        result_label.config(text="🌐 Location fetch failed.")

# Background
bg_img = Image.open('./bg.png').resize((600, 520), Image.Resampling.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_img)
bg_label = tk.Label(root, image=bg_photo)
bg_label.place(x=0, y=0, width=600, height=520)

# Title
title = tk.Label(bg_label, text='🌍 Weather for 200,000+ Cities!', fg='green',
                 bg='lightyellow', font=('Helvetica', 16, 'bold'))
title.place(x=100, y=15)

# Input frame
frame = tk.Frame(bg_label, bg='white', bd=3, relief='ridge')
frame.place(x=80, y=60, width=440, height=60)

city_entry = tk.Entry(frame, font=('Helvetica', 18), width=18, bd=0, relief='flat')
city_entry.grid(row=0, column=0, padx=10, pady=10)

search_btn = tk.Button(frame, text="🔍", font=("Helvetica", 14),
                       command=search_weather, bg='#c8e6c9', relief='groove')
search_btn.grid(row=0, column=1, padx=5)

loc_btn = tk.Button(frame, text="📍", font=("Helvetica", 14),
                    command=get_location_and_weather, bg='#fff9c4', relief='groove')
loc_btn.grid(row=0, column=2)

# Unit switch
unit_frame = tk.Frame(bg_label, bg='lightblue', bd=2, relief='ridge')
unit_frame.place(x=80, y=130, width=440, height=40)

tk.Radiobutton(unit_frame, text="°F", variable=unit, value='imperial',
               font=('Helvetica', 12), bg='lightblue', command=search_weather).pack(side='left', padx=20)
tk.Radiobutton(unit_frame, text="°C", variable=unit, value='metric',
               font=('Helvetica', 12), bg='lightblue', command=search_weather).pack(side='left')

# Result 
result_frame = tk.Frame(bg_label, bg='white', bd=3, relief='ridge')
result_frame.place(x=80, y=180, width=440, height=300)

icon_label = tk.Label(result_frame, bg='white')
icon_label.pack(pady=10)

result_label = tk.Label(result_frame, font=('Helvetica', 14), bg='white',
                        fg='black', justify='left', anchor='nw')
result_label.pack(fill='both', expand=True, padx=10, pady=10)
root.mainloop()
