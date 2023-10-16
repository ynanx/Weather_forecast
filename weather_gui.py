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
        

class Drawer(object):
    #Temperature curves were drawn for 15 days
    def tem_curve_15(self):
        tem_low = []
        tem_high = []
        data = info_15day
        
        #Save data
        for i in range(15):
            if data[i][2] != None:
                tem_low.append(int(data[i][2]))
            else:
                tem_low.append(data[i][2])
            if data[i][3] != None:
                tem_high.append(int(data[i][3]))
            else:
                tem_high.append(data[i][3])
                
        tem_high_sum = 0
        tem_low_sum = 0
        low_sum = 15
        high_sum = 15
        for i in range(15):
            if tem_high[i] != None:
                tem_high_sum += tem_high[i]
            else:
                high_sum -= 1
            if tem_low[i] !=None:
                tem_low_sum += tem_low[i]
            else:
                low_sum -= 1
        tem_high_ave = tem_high_sum / high_sum #average temperature
        tem_low_ave = tem_low_sum / low_sum
        
        while tem_high.count(None):
            tem_high[tem_high.index(None)] = tem_high_ave
        while tem_low.count(None):
            tem_low[tem_low.index(None)] = tem_low_ave
        tem_max = max(tem_high)
        tem_max_date = tem_high.index(tem_max)
        tem_min = min(tem_low)
        tem_min_date = tem_low.index(tem_min)
        global picture_a, canvas
        x = range(1, 16)
        plt.clf()
        plt.plot(x, tem_high, color='red', label='高温')
        plt.scatter(x, tem_high, color='red')
        plt.plot(x, tem_low, color='blue', label='低温')
        plt.scatter(x, tem_low, color='blue')
        plt.plot([1,15],[tem_high_ave, tem_high_ave], c='black', linestyle = '--')
        plt.plot([1,15],[tem_low_ave, tem_low_ave], c='black', linestyle = '--')
        plt.legend() 
        plt.text(tem_max_date + 0.15, tem_max +0.15, str(tem_max), ha='center', va='top', fontsize=10.5)
        plt.text(tem_min_date + 0.15, tem_min +0.15, str(tem_min), ha='center', va='top', fontsize=10.5)
        plt.text(1, round(tem_high_ave, 2), str(round(tem_high_ave, 2)), ha='center', va='top', fontsizw=10.5)
        plt.text(1, round(tem_low_ave, 2), str(round(tem_low_ave, 2)), ha='center', va='top', fontsizw=10.5)
        plt.xticks(x)
        plt.title('未来15天高温低温变化曲线图')
        canvas.draw()
    
    #Temperature curves are drawn for 24 hours
    def tem_curve_24(self):
        hour = []
        tem = []
        data = info_1day
        
        for i in range(25):
            hour.append(int(data[i][0]))
            if data[i][1] != None:
                tem.append(int(data[i][0]))
            else:
                tem.append(data[i][0])
        tem_sum = 0
        t_sum=25
        for i in range(25):
            if tem[i] != None:
                tem_sum += tem[i]
            else:
                t_sum -= 1
        tem_ave = tem_sum / t_sum
        while tem.count(None):
            tem[tem.index(None)] = tem_ave
        tem_max = max(tem)
        tem_min = min(tem)
        tem_max_hour = tem.index(tem_max)
        tem_min_hour = tem.index(tem_min)
        plt.clf()
        x=range(1, 26)
        plt.clf()
        x= range(1, 26)
        plt.plot(x, tem, color='red', label='温度')
        plt.scatter(x, tem, color='red')
        plt.plot([0, 25],[tem_ave, tem_ave], c='blue', linestyle = '--', label = '平均温度')
        plt.text(tem_max_hour + 0.15, tem_max +0.15, str(tem_max), ha='center', va='top', fontsize=10.5)
        plt.text(tem_min_hour + 0.15, tem_min +0.15, str(tem_min), ha='center', va='top', fontsize=10.5)
        plt.text(1, tem_ave, str(round(tem_ave, 2)), ha='center', va='top', fontsizw=10.5)
        plt.xticks(range(1, 26), hour)
        plt.legend()
        plt.title("过去24小时温度变化曲线图")
        canvas.draw()
    
    #Plot a 24-hour air quality graph
    def air_curve_24(self):
        hour = []
        air = []
        data = info_1day
        
        for i in range(25):
            hour.append(int(data[i][0]))
            if data[i][6] != '':
                air.append(int(data[i][6]))
            else:
                air.append(data[i][6])
        air_sum = 0
        t_sum = 25
        for i in range(25):
            if air [i] != '':
                air_sum += air[i]
            else:
                t_sum -= 1
        air_ave = air_sum / t_sum
        while air.count(''):
            air[air.index('')] = air_ave
        air_max = max(air)
        air_min = min(air)
        air_max_hour = air.index(air_max)
        air_min_hour = air.index(air_min)
        global picture_a, canvas, picture
        plt.clf()
        x=range(1, 26)
        for i in range(0, 25):
            if air[i] <= 50:
                plt.bar(x[i], air[i], color='lightgreen', width=0.7) #1 level
            elif air[i] <= 100:
                plt.bar(x[i], air[i], color='wheat', width=0.7) #2 level
            elif air[i] <= 150:
                plt.bar(x[i], air[i], color='orange', width=0.7) #3level
            elif air[i] <= 200:
                plt.bar(x[i], air[i], color='orangered', width=0.7) #4 level
            elif air[i] <= 300:
                plt.bar(x[i], air[i], color='darkviolet', width=0.7) #5 level
            elif air[i] > 300:
                plt.bar(x[i], air[i], color='maroon', width=0.7) #6 level
        plt.plot([0, 25],[air_ave, air_ave], c='blue', linestyle = '--')
        plt.text(air_max_hour + 0.15, air_max +0.15, str(air_max), ha='center', va='top', fontsize=10.5)
        plt.text(air_min_hour + 0.15, air_min +0.15, str(air_min), ha='center', va='top', fontsize=10.5)
        plt.text(1, round(air_ave, 2), str(round(air_ave, 2)), ha='center', va='top', fontsizw=10.5)
        plt.xticks(x, hour)
        plt.title("过去24小时空气质量柱状图")
        canvas.draw()
        
        
                
    #Plot a 24-hour wind curve
    def wind_radar_24(self):
        wind = []
        wind_speed = []
        for i in range(25):
            wind.append(info_1day[i][2])
            wind.speed.append(int(info_1day[i][3]))
        for i in range(0, 25):
            if wind[i] == '北风':
                wind[i] = 90
            elif wind[i] == '南风':
                wind[i] =270
            elif wind[i] == '西风':
                wind[i] =180
            elif wind[i] == '东风':
                wind[i] =360
            elif wind[i] == '东北风':
                wind[i] =45
            elif wind[i] == '西北风':
                wind[i] =135
            elif wind[i] == '西南风':
                wind[i] =225
            elif wind[i] == '东南风':
                wind[i] =315
            degs = np.arange(45, 361, 45)
            temp = []
            for deg in degs:
                speed = []
                for i in range(0,25):
                    if wind[i] == deg:
                        speed.append(wind_speed[i])
                if len(speed) == 0:
                    temp.append(0)
                else:
                    temp.append(sum(speed) / len(speed))
            N = 8
            theta = np.arange(0 + np.pi / 8, 2 * np.pi + np.pi /8, 2 * np.pi /8)
            radii = np.array(temp)
            
        plt.clf()
        plt.axes(polar=True)
        
        colors = [(1- x /max(temp), 1- x /max(temp), 0.6) for x in radii]
        plt.bar(theta, radii, width=(2 * np.pi / N), bottom=0.0, color=colors)
        plt.title("过去24小时风向雷达图", x=1, y=1, fontsize=10)
        canvas.draw()


    #Plot the relative humidity over 24 hours
    def hum_curve_24(self):
        hour = []
        hum = []
        data = info_1day
        
        for i in range(25):
            hour.append(int(data[i][0]))
            if data[i][5] != '':
                hum.append(int(data[i][5]))
            else:
                hum.append(data[i][5])
        hum_sum = 0
        t_sum = 25
        for i in range(25):
            if hum[i] != None:
                hum_sum += hum[i]
            else:
                t_sum -= 1
        hum_ave = hum_sum / t_sum
        while hum.count(None):
            hum[hum.index(None)] = hum_ave
        hum_max = max(hum)
        hum_min = min(hum)
        hum_max_hour = hum.index(hum_max)
        hum_min_hour = hum.index(hum_min)
        plt.clf()
        x=range(1, 26)
        plt.plot(x, hum, color='blue', label='相对湿度')
        plt.scatter(x, hum, color='blue')
        plt.plot([0, 25],[hum_ave, hum_ave], c='red', linestyle = '--', label='平均相对湿度')
        plt.text(hum_max_hour + 0.15, hum_max +0.15, str(hum_max), ha='center', va='top', fontsize=10.5)
        plt.text(hum_min_hour + 0.15, hum_min +0.15, str(hum_min), ha='center', va='top', fontsize=10.5)
        plt.text(1, round(hum_ave, 2), str(round(hum_ave, 2)), ha='center', va='top', fontsizw=10.5)
        plt.xticks(x, hour)
        plt.title("过去24小时相对湿度变化曲线图")
        canvas.draw()
   
    #Change of the wind direction
    def change_wind(wind):
        for i in range(0, 15):
            if wind[i] == '北风':
                wind[i] = 90
            elif wind[i] == '南风':
                wind[i] =270
            elif wind[i] == '西风':
                wind[i] =180
            elif wind[i] == '东风':
                wind[i] =360
            elif wind[i] == '东北风':
                wind[i] =45
            elif wind[i] == '西北风':
                wind[i] =135
            elif wind[i] == '西南风':
                wind[i] =225
            elif wind[i] == '东南风':
                wind[i] =315
        return wind

    #15 day wind radar chart
    def wind_radar_15(self):
        wind1 = []
        wind2 = []
        wind_speed = []
        for i in range(15):
            wind1.append(info_15day[i][4])
            wind2.append(info_15day[i][5])
            wind_speed.append(int(info_15day[i][6]))
        wind1 = self.change_wind(wind1)
        wind2 = self.change_wind(wind2)
        degs = np.arange(45, 361, 45)
        temp = []
        for deg in degs:
            speed = []
            for i in range(0,15):
                if wind1[i] == deg:
                    speed.append(wind_speed[i])
                if wind2[i] == deg:
                    speed.append(wind_speed[i])
            if len(speed) == 0:
                temp.append(0)
            else:
                temp.append(sum(speed) / len(speed))
        N = 8
        theta = np.arange(0 + np.pi / 8, 2 * np.pi + np.pi / 8, 2 * np.pi /8)
        radii = np.array(temp)
        plt.clf()
        plt.axes(polar=True)
        
        colors = [(1- x /max(temp), 1- x /max(temp), 0.6) for x in radii]
        plt.bar(theta, radii, width=(2 * np.pi / N), bottom=0.0, color=colors)
        plt.title("未来15天风向雷达图", x=1, y=1, fontsize=10)
        canvas.draw()
        
    #15-day weather pie chart
    def weather_pie(self):
        weather = []
        for i in range(15):
            weather.append(info_15day[i][1])
        dic_wea = {}
        for i in range(0, 25):
            if weather[i] in dic_wea.keys():
                dic_wea[weather[i]] += 1
            else:
                dic_wea[weather[i]] = 1
        plt.clf()
        explode = [0.01] * len(dic_wea.key())
        color = ['lightskyblue', 'silver', 'yellow', 'salmon', 'grey', 'lime', 'gold', 'red', 'green', 'pink']
        plt.pie(dic_wea.values(), explode=explode, labels=dic_wea.keys(), autopct='%1.1f%%', colors=color)
        plt.title("未来15天气候分布图")
        canvas.draw()
        




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
    


        
   
                
                
    #Selective image rendering
    def draw_image_select(self):
        if photo_select == photo_select_list[0]:
            Drawer().tem_curve_24()
        elif photo_select == photo_select_list[1]:
            Drawer().hum_curve_24()
        elif photo_select == photo_select_list[2]:
            if search_key in ("澳门", "香港", "台北"):
                tk.messagebox.showwarning("提示", "港澳台空气质量无法获取")
            else:
                Drawer().air_curve_24()
        
        elif photo_select == photo_select_list[3]:
            Drawer().wind_radar_24()
        elif photo_select == photo_select_list[4]:
            Drawer().tem_curve_15()
        elif photo_select == photo_select_list[5]:
            Drawer(). wind_radar_15()
        elif photo_select == photo_select_list[6]:
            Drawer().weather_pie()
        
    #The information is updated automatically every 30 minutes
    def infoGet(self):
        global info_1day,info_15day
        info_1day, info_7day, info_15day = HtmlParser.get_city_all_weather_info(search_key)
        screen.after(30 * 60 *1000, self.infoGet)
        self.draw_weather_list()
        self.draw_image_select()
        
        
                
        
                

        
        
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











