# -*- coding: utf-8 -*-
"""
Created on Fri Oct 13 22:11:28 2023

@author: 12133
"""

import datetime
import pyttsx3
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
import numpy as np
#import sys
#sys.path.append(r'C:\Users\12133\Desktop\weather_forecast')

from get_weatherinfo import HtmlParser, Write_to_csv

search_key = '晋江'

global picture, city_select_list_select, time_select, photo_select, info_select,\
    text_read, info_1day, info_7day, info_15day, city_select_list_list, time_list, canvas,\
        photo_list, weather_list, weather_1day
        








class Outputer(object):
    
    def say_text(self):
        global info_1day, info_7day, info_15day, search_key, text_read
        text_read = search_key + "市" + str(info_15day[0][0]) + "日" + str(info_1day[0][0]) + "时" + "天气" + \
            info_15day[0][1]
        if info_15day[0][3] == None:
            text_read = "最高气温" + "暂无" + "最低气温" + str(info_15day[0][2]) + "度" + "当前温度" + str(info_1day[0][1]) + '度' + \
                info_1day[0][2] + str(info_1day[0][3]) + "级"
        else:
            text_read = "最高气温" + str(info_15day[0][3]) + "最低气温" + str(info_15day[0][2]) + "度" + "当前温度" + str(info_1day[0][1]) + '度' + \
                info_1day[0][2] + str(info_1day[0][3]) + "级"

        if info_1day[0][6] == '':
            text_read = "降水" + str(info_1day[0][4]) +"相对湿度" + str(info_1day[0][5]) + "空气质量" + "暂无"
        else:
            text_read = "降水" + str(info_1day[0][4]) +"相对湿度" + str(info_1day[0][5]) + "空气质量" + str(info_1day[0][6]) 
        print(text_read)
        
        
    
    def say_voice(self):
        self.say_text()
        voice = pyttsx3.init()
        voice.say(self.say_text)
        voice.runAndWait()
    
        
    #save data
    def save_message(self):
        global info_1day, info_7day, info_15day
        info_1day, info_7day, info_15day = HtmlParser.get_city_all_weather_info(search_key)
        now_time = datetime.datetime.now().strftime('%T')
        now_time = now_time.replace(':', '-')
        now_date = datetime.datetime.now().strftime('%F')
        if info_select == '24h':
            file_name = search_key +"24小时的天气数据-" + now_date + '-' + now_time + ".csv"
            Write_to_csv.write_info_to_csv(file_name, info_1day, day=1)
            tk.messagebox.showinfo("提示", "24小时数据保存完成")
        elif info_select == '7天':
            file_name = search_key +"7天的天气数据-" + now_date + '-' + now_time + ".csv"
            Write_to_csv.write_info_to_csv(file_name, info_7day, day=7)
            tk.messagebox.showinfo("提示", "7天数据保存完成")
        else:
            file_name = search_key +"15天的天气数据-" + now_date + '-' + now_time + ".csv"
            Write_to_csv.write_info_to_csv(file_name, info_15day, day=15)
            tk.messagebox.showinfo("提示", "15天数据保存完成")
            
        

    #Image display interface and image toolbar
    def draw_map(self):
        global canvas
        draw = tk.Canvas(screen, bd=0, bg='grey', width=450, height=300)
        draw.place(x=520, y=288)
        tool = tk.Canvas(screen, bd=0, bg='grey', width=100, height=30)
        tool.place(x=610, y=238)
        canvas = FigureCanvasTkAgg(picture, master=draw)
        canvas.draw()
        toolbar = NavigationToolbar2Tk(canvas, tool)
        toolbar.update()
        canvas.get_tk_widget().place(x=2, y=2)
        
        
    #Generate menus, buttons, selections
    def draw_menu(self):
        #City search
        city_select_listtext = tk.Label(screen, text="搜索城市", font=("楷体", 15), width=8, height=1)
        city_select_listtext.place(x=50, y=50)
       
        entry = tk.Entry(screen, font=("楷体", 15))
        entry.place(x=150, y=50)
        city = entry.get()
        button = tk.Button(screen, text="确定", font=("楷体", 15), command=lambda: print("搜索的城市是{}".format(city)))
        button.place(x=200, y=50)
           
           
        #time selection
        timed_h = tk.Label(screen, text="时间选择", font=("楷体", 15), width=8, height=1)
        timed_h.place(x=260, y=50)
        global time_list
        time_list = ttk.Combobox(screen, font={"楷体", 15}, width=9, state="randonly", values=time_select)
        time_list.set("24h")
        time_list.place(x=350, y=50)
           
        #Image selection
        photo_label = tk.Label(screen, text= "图像选择", font=("楷体", 15), width=8, height=1)
        photo_label.place(x=50, y=120)
        global photo_list
        photo_list = ttk.Combobox(screen, font={"楷体", 15}, width=9, state="randonly", values=photo_select_list)
        photo_list.set(photo_label)
        photo_list.place(x=150, y=120)
           
        #Button selection
        #switch
        ok_label = tk.Label(screen, text="数据更新", font=("楷体", 15), width=8, height=1)
        ok_label.place(x=260, y=120)
        ok = tk.Button(screen, text= "确认更新", command=self.city_select_listselect, font=("楷体", 15), width=10, height=1)
        ok.place(x=347, y=115)
        #function
        menu = tk.Label(screen, text="功能按钮", font=("楷体", 15), width=8, height=1)
        menu.place(x=50,y=190)
        say = tk.Button(screen, text= "语音播报", command=self.say_voice, font=("楷体", 15), width=10, height=1)
        say.place(x=150, y=185)
        save = tk.Button(screen, text= "数据保存", command=self.save_message, font=("楷体", 15), width=10, height=1)
        save.place(x=347, y=185)
  
        
        
    #Weather list display(text)
    def draw_weather_text(self):
        global weather_list, weather_1day
        weather_1day = tk.Canvas(screen, bd=2, bg='white', width=300, height=200)
        weather_1day.place(x=580, y=20)
        frame = tk.Frame(screen, width=400, height=350)
        frame.place(x=60, y=225)
        weather_list = tk.Canvas(frame, bd=0, bg='white', width=400, height=350, scrollregion=(0, 0, 850, 1500))
        hbar = tk.Scrollbar(frame, orient=tk.HORIZONTAL)
        hbar.pack(side=tk.BOTTOM, fill=tk.X)
        hbar.config(command=weather_list.xview)
        vbar = tk.Scrollbar(frame, orient=tk.VERTICAL)
        vbar.place(side=tk.RIGHT, fill=tk.Y)
        vbar.config(command=weather_list.yview)
        weather_list.config(width=400, height=350)
        weather_list.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
        weather_list.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
      
        
    #Weather list display(table)
    def draw_weather_list(self):
        weather_list.delete(tk.ALL)
        weather_1day.delete(tk.ALL)
        weather_1day.create_text(40, 20, text=search_key + ':', font=('宋体', 16), fill='red')
        weather_1day.create_text(150, 20, text=info_15day[0][0] + '号' + info_1day[0][0] + '时' , font=('宋体', 14), fill='red')
        weather_1day.create_text(150, 48, text=info_15day[0][1], font=('宋体', 14), fill='red')
        if info_15day[0][3] !=None:
            weather_1day.create_text(150, 76, text=info_15day[0][3] + '/' + info_15day[0][2] + '℃' + '——' + info_1day + '℃',
                                    font=('宋体', 14), fill='red')
        else:
            weather_1day.create_text(150, 76, text=' ' + '/' + info_15day[0][2] + '℃' + '——' + info_1day + '℃',
                                    font=('宋体', 14), fill='red')
        weather_1day.create_text(150, 104, text=info_1day[0][2] + '——' + info_1day[0][3] + '级', font=('宋体', 14), fill='red')
        weather_1day.create_text(150, 132, text='降水' + '——' + info_1day[0][4], font=('宋体', 14), fill='red')
        weather_1day.create_text(150, 160, text='相对湿度' + '——' + info_1day[0][5], font=('宋体', 14), fill='red')
        weather_1day.create_text(150, 188, text='空气质量' + '——' + info_1day[0][6], font=('宋体', 14), fill='red')
        
        if info_select == '24h':
            weather_list.create_text(50, 20, text='时间/h', font=('宋体', 15))
            weather_list.create_text(150, 20, text='温度', font=('宋体', 15))
            weather_list.create_text(250, 20, text='风向', font=('宋体', 15))
            weather_list.create_text(350, 20, text='风速', font=('宋体', 15))
            weather_list.create_text(450, 20, text='降水', font=('宋体', 15))
            weather_list.create_text(550, 20, text='湿度', font=('宋体', 15))
            weather_list.create_text(650, 20, text='空气质量', font=('宋体', 15))
            for i in range(25):
                weather_list.create_text(50,70 + i * 50, text=str(info_1day[i][0],font=('宋体',18)))
                weather_list.create_text(150,70 + i * 50, text=str(info_1day[i][1],font=('宋体',18)))
                weather_list.create_text(250,70 + i * 50, text=str(info_1day[i][2],font=('宋体',18)))
                weather_list.create_text(350,70 + i * 50, text=str(info_1day[i][3],font=('宋体',18)))
                weather_list.create_text(450,70 + i * 50, text=str(info_1day[i][4],font=('宋体',18)))
                weather_list.create_text(550,70 + i * 50, text=str(info_1day[i][5],font=('宋体',18)))
                weather_list.create_text(650,70 + i * 50, text=str(info_1day[i][6],font=('宋体',18)))
                
        elif info_select == "15天":
            weather_list.create_text(50, 20, text='时间/Day', font=('宋体', 15))
            weather_list.create_text(150, 20, text='天气', font=('宋体', 15))
            weather_list.create_text(250, 20, text='最低温度', font=('宋体', 15))
            weather_list.create_text(350, 20, text='最高温度', font=('宋体', 15))
            weather_list.create_text(450, 20, text='风向1', font=('宋体', 15))
            weather_list.create_text(600, 20, text='风向2', font=('宋体', 15))
            weather_list.create_text(700, 20, text='风级', font=('宋体', 15))
            for i in range(15):
                weather_list.create_text(50,70 + i * 50, text=str(info_15day[i][0],font=('宋体',18)))
                weather_list.create_text(150,70 + i * 50, text=str(info_15day[i][1],font=('宋体',18)))
                weather_list.create_text(250,70 + i * 50, text=str(info_15day[i][2],font=('宋体',18)))
                weather_list.create_text(350,70 + i * 50, text=str(info_15day[i][3],font=('宋体',18)))
                weather_list.create_text(450,70 + i * 50, text=str(info_15day[i][4],font=('宋体',18)))
                weather_list.create_text(600,70 + i * 50, text=str(info_15day[i][5],font=('宋体',18)))
                weather_list.create_text(700,70 + i * 50, text=str(info_15day[i][6],font=('宋体',18)))
                

    def draw_image_select(self):
        if photo_select == photo_select_list[0]:
            tem_curve_24()
        elif photo_select == photo_select_list[1]:
            hum_curve_24()
        elif photo_select == photo_select_list[2]:
            if search_key in ("澳门", "香港", "台北"):
                tk.messagebox.showwarning("提示", "港澳台空气质量无法获取")
            else:
                air_curve_24()
        
        elif photo_select == photo_select_list[3]:
            wind_radar_24()
        elif photo_select == photo_select_list[4]:
            tem_curve_15()
        elif photo_select == photo_select_list[5]:
            wind_radar_15()
        elif photo_select == photo_select_list[6]:
            weather_pie()
                
        
                

        
        
    #Refresh the interface and draw the elements in the interface
    def screen_model(self):
        screen.after(2000, self.draw_menu);
        screen.after(2000, self.draw_map);
        screen.after(2000, self.draw_weather_text);
        screen.after(2000, self.draw_weather_list);
        screen.after(2000, self.draw_image_select);
        
    

        
        
        
picture = plt.figure(figsize=(4.5, 3), dpi=100)
plt.subplot(1, 1, 1)
city_select_list_select = "重庆"
time_select = ("24h", "7天", "15天")
info_select = "24h"
photo_select = "过去24小时温度变化曲线图"
photo_select_list = ("过去24小时温度变化曲线图", "过去24小时相对湿度变化曲线图", 
                     "过去24小时空气质量柱状图", "过去24小时风向雷达图", 
                     "未来15天高温低温变换曲线图", "未来15天风向雷达图",
                     "未来15天气候分布饼状图")



#Setup window interface
screen = tk.Tk()
#screen.iconbitmap(r"./logo.ico")
screen.title("天气预报系统")
screen.geometry('1000x600')


#Drop down property Settings
combostyle = ttk.Style()
combostyle.theme_create('combostyle', parent='alt')
combostyle.configure('TCombobox', **{'selectbackground': 'white',
                                     'background':'green',
                                     'selectforeground':'black',
                                     'selectborderwidth': 0})
combostyle.theme_use('combostyle')


#Set the Chinese display in matplotlib
plt.rcParams['font.sans-serif'] = 'SimHei'
plt.rcParams['axes.unicode_minus'] = False


#Start static images to avoid whiteboards due to data loading
photo = Image.open("Image.jpg")
photo = photo.resize((1000, 600))
img_jpg = ImageTk.PhotoImage(photo)
h1 = tk.Label(screen, image=img_jpg)
h1.place(x=0, y=0)
screen.after(3000, h1.place_forget)


#Capture data during the animation display and draw interface elements
info_1day, info_7day, info_15day = HtmlParser.get_city_all_weather_info(search_key)
Outputer.screen_model()


#The information is updated automatically every 30 minutes
screen.after(30 * 60 * 1000, infoGet)
screen.mainloop()











