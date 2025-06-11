import tkinter as tk
import requests
from PIL import Image,ImageTk #pip install pillow 

root=tk.Tk()
root.title("Weather App")
root.geometry("600x500")

def format_res(weather):
    try:
         city=(weather['name'])
         condition=(weather['weather'][0][ 'description'])
         temp=(weather['main']['temp'])
         final_str='City:%s\nCondition:%s\nTemperature:%s'%(city,condition,temp)
    except:
         final_str='There was a problem while retriving the information'
    return  final_str     

def get_weather(city):
    weather_key='a9d96161ca37b34dd529d5a3592939e6'
    url='https://api.openweathermap.org/data/2.5/weather' 
    params={'APPID':weather_key,'q':city,'units':'imperial'}
    response=requests.get(url,params)
    weather=response.json()         
    result['text']=format_res(weather)                             

img=Image.open('./bg.png')
img=img.resize((600,500),Image.Resampling.LANCZOS)
img_photo=ImageTk.PhotoImage(img)

bg_label=tk.Label(root,image=img_photo)
bg_label.place(x=0,y=0,width=600,height=500)

head_title=tk.Label(bg_label,text='Earth including over 2,00,000 cities',fg='green',font=('times new roman',16,'bold'))
head_title.place(x=80,y=18)

frame1=tk.Frame(bg_label,bg="light blue",bd=5)
frame1.place(x=80,y=50,width=450,height=50)

txt1=tk.Entry(frame1,font=('times new roman',25),width=17)
txt1.grid(row=0,column=0,sticky='w')

btn=tk.Button(frame1,text="get weather",fg='green',font=('times new roman',16,'bold'),command=lambda:get_weather(txt1.get()))
btn.grid(row=0,column=1,padx=10)

frame2=tk.Frame(bg_label,bg="light blue",bd=5)
frame2.place(x=80,y=130,width=450,height=300)

result=tk.Label(frame2,font=40,bg='white',justify='left',anchor='nw')
result.place(relheight=1,relwidth=1)

root.mainloop()