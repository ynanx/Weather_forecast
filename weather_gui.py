# -*- coding: utf-8 -*-
"""
Created on Fri Oct 13 22:11:28 2023

@author: 12133
"""

import datetime
import pyttsx3
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
import numpy as np
from get_weatherinfo import HtmlParser, Write_to_csv


global picture, time_select, photo_select, info_select,\
       weather_1day,weather_list,frame
time_select = ("24h","7天","8-15天")
info_select = "24h"
photo_select = "过去24小时温度变化曲线图"
photo_select_list = ("过去24小时温度变化曲线图", "过去24小时相对湿度变化曲线图", 
                     "过去24小时空气质量柱状图", "过去24小时风向雷达图", 
                     "未来7天高温低温变换曲线图",
                     "未来15天高温低温变换曲线图", "未来8-15天风向雷达图",
                     "未来15天气候分布饼状图")
html_parser = HtmlParser()

class App(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
        self.after(3000, self.hide_image)

    def create_widgets(self):
        self.image_path = './Image.jpg'
        self.photo = Image.open(self.image_path)
        self.photo = self.photo.resize((1000, 600))
        self.img_jpg = ImageTk.PhotoImage(self.photo)

        # 创建标签
        self.h1 = tk.Label(self.master)
        self.h1.pack()

        self.after(0, self.set_image)

    def set_image(self):
        self.img_jpg = ImageTk.PhotoImage(self.photo)
        self.h1.config(image=self.img_jpg, width=1000, height=600)
        self.h1.image = self.img_jpg

    def hide_image(self):
        self.h1.pack_forget()


class Outputer(object):
    def __init__(self):     
        self.search_key = None
        self.info_1day = None
        self.info_15day = None
        self.time_list = None
        self.photo_list =None
        self.weather_1day = None
        self.weather_list = None
        self.frame = None
        self.info_select = '24h'
        self.screen = tk.Tk()
        
        self.picture = plt.figure(figsize=(4.5, 3), dpi=100)
        plt.subplot(1, 1, 1)
        self.canvas = None
        
        self.entry = None

        #Setup window interface
        self.screen.iconbitmap(r"./logo.ico")
        self.screen.title("天气预报系统")
        self.screen.geometry('1000x600')

        if 'combostyle' not in ttk.Style().theme_names():
                    combostyle = tk.ttk.Style()
                    combostyle.theme_create('combostyle', parent='alt', settings={
                                            'TCombobox':{'configure':{
                                                         'selectbackground': 'white',
                                                         'background':'green',
                                                         'selectforeground':'black',
                                                         'selectborderwidth': 0}}})
                    combostyle.theme_use('combostyle') 
        else:
            combostyle = tk.ttk.Style()
            combostyle.theme_use('combostyle')            


        #Set the Chinese display in matplotlib
        plt.rcParams['font.sans-serif'] = 'SimHei'
        plt.rcParams['axes.unicode_minus'] = False



        self.app=App(master=self.screen)
        self.screen.geometry("1000x600+0+0")
        self.screen_model()
        self.screen.mainloop()

    #Temperature curves were drawn for 8-15 days   
    def tem_curve_7(self, info_7day_1):
        tem_low = []
        tem_high = []
        data = info_7day_1 
        
        #Save data
        for i in range(7):
            if data[i][2] != None:
                tem_low.append(int(float(data[i][2])))
            else:
                tem_low.append(data[i][2])
            if data[i][3] != None:
                tem_high.append(int(float(data[i][3])))
            else:
                tem_high.append(data[i][3])
                
        tem_high_sum = 0
        tem_low_sum = 0
        low_sum = 7
        high_sum = 7
        for i in range(7):
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
        #global picture_a
        x = range(1, 8)
        plt.clf()
        plt.plot(x, tem_high, color='red', label='高温')
        plt.scatter(x, tem_high, color='red')
        plt.plot(x, tem_low, color='blue', label='低温')
        plt.scatter(x, tem_low, color='blue')
        plt.plot([1,8],[tem_high_ave, tem_high_ave], c='black', linestyle = '--')
        plt.plot([1,8],[tem_low_ave, tem_low_ave], c='black', linestyle = '--')
        plt.legend() 
        plt.text(tem_max_date + 0.15, tem_max +0.15, str(tem_max), ha='center', va='top', fontsize=10.5)
        plt.text(tem_min_date + 0.15, tem_min +0.15, str(tem_min), ha='center', va='top', fontsize=10.5)
        plt.text(1, round(tem_high_ave, 2), str(round(tem_high_ave, 2)), ha='center', va='top', fontsize=10.5)
        plt.text(1, round(tem_low_ave, 2), str(round(tem_low_ave, 2)), ha='center', va='top', fontsize=10.5)
        plt.xticks(x)
        plt.title('未来7天高温低温变化曲线图')
        self.canvas.draw()
        
        
    def tem_curve_15(self, info_15day_1,info_7day_1):
        tem_low = []
        tem_high = []
        data = info_7day_1 + info_15day_1
        
        #Save data
        for i in range(15):
            if data[i][2] != None:
                tem_low.append(int(float(data[i][2])))
            else:
                tem_low.append(data[i][2])
            if data[i][3] != None:
                tem_high.append(int(float(data[i][3])))
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
        #global picture_a
        x = range(1, 16)
        plt.clf()
        plt.plot(x, tem_high, color='red', label='高温')
        plt.scatter(x, tem_high, color='red')
        plt.plot(x, tem_low, color='blue', label='低温')
        plt.scatter(x, tem_low, color='blue')
        plt.plot([1,16],[tem_high_ave, tem_high_ave], c='black', linestyle = '--')
        plt.plot([1,16],[tem_low_ave, tem_low_ave], c='black', linestyle = '--')
        plt.legend() 
        plt.text(tem_max_date + 0.15, tem_max +0.15, str(tem_max), ha='center', va='top', fontsize=10.5)
        plt.text(tem_min_date + 0.15, tem_min +0.15, str(tem_min), ha='center', va='top', fontsize=10.5)
        plt.text(1, round(tem_high_ave, 2), str(round(tem_high_ave, 2)), ha='center', va='top', fontsize=10.5)
        plt.text(1, round(tem_low_ave, 2), str(round(tem_low_ave, 2)), ha='center', va='top', fontsize=10.5)
        plt.xticks(x)
        plt.title('未来15天高温低温变化曲线图')
        self.canvas.draw()
    
    #Temperature curves are drawn for 24 hours
    def tem_curve_24(self,info_1day_1):
        hour = []
        tem = []
        data = info_1day_1
        
        for i in range(25):
            hour.append(int(float(data[i][0])))
            if data[i][1] != None:
                tem.append(int(float(data[i][1])))
            else:
                tem.append(data[i][1])
        print(hour)
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
        x= range(1, 26)
        plt.plot(x, tem, color='red', label='温度')
        plt.scatter(x, tem, color='red')
        plt.plot([0, 25],[tem_ave, tem_ave], c='blue', linestyle = '--', label = '平均温度')
        plt.text(tem_max_hour + 0.15, tem_max +0.15, str(tem_max), ha='center', va='top', fontsize=10.5)
        plt.text(tem_min_hour + 0.15, tem_min +0.15, str(tem_min), ha='center', va='top', fontsize=10.5)
        plt.text(1, tem_ave, str(round(tem_ave, 2)), ha='center', va='top', fontsize=10.5)
        plt.xticks(range(1, 26), hour)
        plt.legend()
        plt.title("过去24小时温度变化曲线图")
        self.canvas.draw()
    
    #Plot a 24-hour air quality graph
    def air_curve_24(self,info_1day_1):
        #global info_1day
        hour = []
        air = []
        data = info_1day_1
        
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
        global picture_a, picture
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
        plt.text(1, round(air_ave, 2), str(round(air_ave, 2)), ha='center', va='top', fontsize=10.5)
        plt.xticks(x, hour)
        plt.title("过去24小时空气质量柱状图")
        self.canvas.draw()
              
    #Plot a 24-hour wind curve
    def wind_radar_24(self,info_1day_1):
        wind = []
        wind_speed = []
        for i in range(25):
            wind.append(info_1day_1[i][2])
            wind_speed.append(int(info_1day_1[i][3]))
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
            theta = np.arange(0. + np.pi / 8, 2 * np.pi + np.pi /8, 2 * np.pi /8)
            radii = np.array(temp)
            
        plt.clf()
        plt.axes(polar=True)
        
        colors = [(1- x /max(temp), 1- x /max(temp), 0.6) for x in radii]
        plt.bar(theta, radii, width=(2 * np.pi / N), bottom=0.0, color=colors)
        plt.title("过去24小时风向雷达图", x=1, y=1, fontsize=10)
        self.canvas.draw()

    #Plot the relative humidity over 24 hours
    def hum_curve_24(self,info_1day_1):
        hour = []
        hum = []
        data = info_1day_1
        
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
        plt.text(1, round(hum_ave, 2), str(round(hum_ave, 2)), ha='center', va='top', fontsize=10.5)
        plt.xticks(x, hour)
        plt.title("过去24小时相对湿度变化曲线图")
        self.canvas.draw()
   
    #Change of the wind direction
    def change_wind(self,wind):
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
    def wind_radar_15(self,info_15day_1):
        wind1 = []
        wind2 = []
        wind_speed = []
        for i in range(15):
            wind1.append(info_15day_1[i][4])
            wind2.append(info_15day_1[i][5])
            wind_speed.append(int(info_15day_1[i][6]))
        wind1 = self.change_wind(wind1)
        wind2 = self.change_wind(wind2)
        degs = np.arange(45, 361, 45)
        temp = []
        for deg in degs:
            speed = []
            for i in range(0,8):
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
        plt.title("未来8-15天风向雷达图", x=1, y=1, fontsize=10)
        self.canvas.draw()
        
    #15-day weather pie chart
    def weather_pie(self, info_15day_1):
        weather = []
        for i in range(8):
            weather.append(info_15day_1[i][1])
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
        plt.title("未来8-15天气候分布图")
        self.canvas.draw()
   # def __init__(self):
    #    self.frame = tk.Frame(self.screen, width=400, height=350)
     #   self.weather_list = tk.Canvas(self.frame, bd=0, bg='white', width=400, height=350, scrollregion=(0, 0, 850, 1500))
      #  self.weather_1day = tk.Canvas(self.screen, bd=2, bg='white', width=300, height=200)

    #Image display interface and image toolbar
    def draw_map(self):
        draw = tk.Canvas(self.screen, bd=0, bg='blue', width=450, height=300)
        draw.place(x=520, y=288)
        tool = tk.Canvas(self.screen, bd=0, bg='blue', width=200, height=30)
        tool.place(x=610, y=238)
        self.canvas = FigureCanvasTkAgg(self.picture, master=draw)
        self.canvas.draw()
        toolbar = NavigationToolbar2Tk(self.canvas, tool)
        toolbar.update()
        
        self.canvas.get_tk_widget().place(x=2, y=2)

    #Generate menus, buttons, selections
    
    #Weather list display(table)        
    def draw_weather_list(self,search_key_1, info_1day_1, info_7day_1,info_15day_1, info_select_1):
        self.weather_list.delete(tk.ALL)
        self.weather_1day.delete(tk.ALL)
        self.weather_1day.create_text(40, 20, text=search_key_1 + ':', font=('宋体', 16), fill='red')
        self.weather_1day.create_text(150, 20, text=info_15day_1[0][0] + info_1day_1[0][0] + '时' , font=('宋体', 14), fill='red')
        self.weather_1day.create_text(150, 48, text=info_15day_1[0][1], font=('宋体', 14), fill='red')
        if info_15day_1[0][3] !=None:
            self.weather_1day.create_text(150, 76, text=info_15day_1[0][3] + '/' + info_15day_1[0][2] + '——' + info_1day_1[0][1] + '℃',
                                     font=('宋体', 14), fill='red')
        else:
            self.weather_1day.create_text(150, 76, text=' ' + '/' + info_15day_1[0][2] + '——' + info_1day_1[0][1] + '℃',
                                     font=('宋体', 14), fill='red')
        self.weather_1day.create_text(150, 104, text=info_1day_1[0][2] + '——' + info_1day_1[0][3] + '级', font=('宋体', 14), fill='red')
        self.weather_1day.create_text(150, 132, text='降水' + '——' + info_1day_1[0][4], font=('宋体', 14), fill='red')
        self.weather_1day.create_text(150, 160, text='相对湿度' + '——' + info_1day_1[0][5], font=('宋体', 14), fill='red')
        self.weather_1day.create_text(150, 188, text='空气质量' + '——' + info_1day_1[0][6], font=('宋体', 14), fill='red')
         
        if info_select_1 == '24h':
            self.weather_list.create_text(50, 20, text='时间/h', font=('宋体', 15))
            self.weather_list.create_text(150, 20, text='温度', font=('宋体', 15))
            self.weather_list.create_text(250, 20, text='风向', font=('宋体', 15))
            self.weather_list.create_text(350, 20, text='风速', font=('宋体', 15))
            self.weather_list.create_text(450, 20, text='降水', font=('宋体', 15))
            self.weather_list.create_text(550, 20, text='湿度', font=('宋体', 15))
            self.weather_list.create_text(650, 20, text='空气质量', font=('宋体', 15))
            for i in range(25):
                self.weather_list.create_text(50,70 + i * 50, text=str(info_1day_1[i][0]),font=('宋体',15))
                self.weather_list.create_text(150,70 + i * 50, text=str(info_1day_1[i][1]),font=('宋体',15))
                self.weather_list.create_text(250,70 + i * 50, text=str(info_1day_1[i][2]),font=('宋体',15))
                self.weather_list.create_text(350,70 + i * 50, text=str(info_1day_1[i][3]),font=('宋体',15))
                self.weather_list.create_text(450,70 + i * 50, text=str(info_1day_1[i][4]),font=('宋体',15))
                self.weather_list.create_text(550,70 + i * 50, text=str(info_1day_1[i][5]),font=('宋体',15))
                self.weather_list.create_text(650,70 + i * 50, text=str(info_1day_1[i][6]),font=('宋体',15))
        elif info_select_1 == "7天":
            self.weather_list.create_text(80, 20, text='时间/Day', font=('宋体', 15))
            self.weather_list.create_text(200, 20, text='天气', font=('宋体', 15))
            self.weather_list.create_text(320, 20, text='最低温度', font=('宋体', 15))
            self.weather_list.create_text(440, 20, text='最高温度', font=('宋体', 15))
            self.weather_list.create_text(560, 20, text='风向1', font=('宋体', 15))
            self.weather_list.create_text(680, 20, text='风向2', font=('宋体', 15))
            self.weather_list.create_text(800, 20, text='风级', font=('宋体', 15))
            for i in range(7):
                self.weather_list.create_text(80,70 + i * 50, text=str(info_7day_1[i][0]),font=('宋体',15))
                self.weather_list.create_text(200,70 + i * 50, text=str(info_7day_1[i][1]),font=('宋体',15))
                self.weather_list.create_text(320,70 + i * 50, text=str(info_7day_1[i][2]),font=('宋体',15))
                self.weather_list.create_text(440,70 + i * 50, text=str(info_7day_1[i][3]),font=('宋体',15))
                self.weather_list.create_text(560,70 + i * 50, text=str(info_7day_1[i][4]),font=('宋体',15))
                self.weather_list.create_text(680,70 + i * 50, text=str(info_7day_1[i][5]),font=('宋体',15))
                self.weather_list.create_text(800,70 + i * 50, text=str(info_7day_1[i][6]),font=('宋体',15))        
        elif info_select_1 == "8-15天":
            self.weather_list.create_text(80, 20, text='时间/Day', font=('宋体', 15))
            self.weather_list.create_text(200, 20, text='天气', font=('宋体', 15))
            self.weather_list.create_text(320, 20, text='最低温度', font=('宋体', 15))
            self.weather_list.create_text(440, 20, text='最高温度', font=('宋体', 15))
            self.weather_list.create_text(560, 20, text='风向', font=('宋体', 15))
            self.weather_list.create_text(750, 20, text='风级', font=('宋体', 15))
            for i in range(8):
                self.weather_list.create_text(80,70 + i * 50, text=str(info_15day_1[i][0]),font=('宋体',15))
                self.weather_list.create_text(200,70 + i * 50, text=str(info_15day_1[i][1]),font=('宋体',15))
                self.weather_list.create_text(320,70 + i * 50, text=str(info_15day_1[i][2]),font=('宋体',15))
                self.weather_list.create_text(440,70 + i * 50, text=str(info_15day_1[i][3]),font=('宋体',15))
                self.weather_list.create_text(560,70 + i * 50, text=str(info_15day_1[i][4]),font=('宋体',15))
                self.weather_list.create_text(750,70 + i * 50, text=str(info_15day_1[i][5]),font=('宋体',15))
    

    def get_weather_info(self):
        global search_key
        search_key = self.entry.get()
        info_select = self.time_list.get()
        photo_select = self.photo_list.get()
        try:
            global info_1day,info_7day, info_15day
            info_1day,info_7day, info_15day =html_parser.get_city_all_weather_info(search_key)
            print(search_key,info_1day,info_7day,info_15day,info_select,photo_select)
            self.draw_weather_list(search_key,info_1day,info_7day,info_15day,info_select)
            self.draw_image_select(photo_select,search_key, info_1day, info_7day,info_15day)
        except Exception as e:
                error_message = "无法获取天气数据：" + str(e)
                messagebox.showerror("错误", error_message)
                print(error_message)
                return
            

        
    def draw_menu(self):
        #City search
        city_select= tk.Label(self.screen, text="搜索城市", font=("楷体", 15), width=8, height=1)
        city_select.place(x=50, y=50)
       
        self.entry = tk.Entry(self.screen, font=("楷体", 15))
        self.entry.place(x=150, y=50)
        button = tk.Button(self.screen, text="确定", font=("楷体", 10), command=self.get_weather_info)
        button.place(x=220, y=50)    
        
        #time selection
        timed_h = tk.Label(self.screen, text="时间选择", font=("楷体", 15), width=8, height=1)
        timed_h.place(x=260, y=50)

        self.time_list = ttk.Combobox(self.screen, font={"font": "楷体", "size": 15}, width=9, state="readonly", values=time_select)
        self.time_list.set("24h")
        self.time_list.place(x=350, y=50)
           
        #Image selection
        photo_label = tk.Label(self.screen, text="图像选择", font=("楷体", 15), width=8, height=1)
        photo_label.place(x=50, y=120)


        self.photo_list = ttk.Combobox(self.screen, font={"font": "楷体", "size": 15}, width=9, state="readonly", values=photo_select_list)
        self.photo_list.set(photo_select_list[0])  
        self.photo_list.place(x=150, y=120)

           
        #Button selection
        #switch
        ok_label = tk.Label(self.screen, text="数据更新", font=("楷体", 15), width=8, height=1)
        ok_label.place(x=260, y=120)
        ok = tk.Button(self.screen, text= "确认更新", command=self.get_weather_info, font=("楷体", 15), width=10, height=1)
        ok.place(x=347, y=115)
        #function
        menu = tk.Label(self.screen, text="功能按钮", font=("楷体", 15), width=8, height=1)
        menu.place(x=50,y=190)
        say = tk.Button(self.screen, text= "语音播报", command=self.say_voice, font=("楷体", 15), width=10, height=1)
        say.place(x=150, y=185)
        save = tk.Button(self.screen, text= "数据保存", command=self.save_message, font=("楷体", 15), width=10, height=1)
        save.place(x=347, y=185)
        


    #Weather list display(text)
    def draw_weather_text(self):
        print(self.info_1day)
        self.weather_1day = tk.Canvas(self.screen, bd=2, bg='white', width=300, height=200)
        self.weather_1day.place(x=580, y=20)
        self.frame = tk.Frame(self.screen, width=400, height=350)
        self.frame.place(x=60, y=225)
        self.weather_list = tk.Canvas(self.frame, bd=0, bg='white', width=400, height=350, scrollregion=(0, 0, 850, 1500))
        hbar = tk.Scrollbar(self.frame, orient=tk.HORIZONTAL)
        hbar.pack(side=tk.BOTTOM, fill=tk.X)
        hbar.config(command=self.weather_list.xview)
        vbar = tk.Scrollbar(self.frame, orient=tk.VERTICAL)
        vbar.pack(side=tk.RIGHT, fill=tk.Y)
        vbar.config(command=self.weather_list.yview)
        self.weather_list.config(width=400, height=350)
        self.weather_list.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
        self.weather_list.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        
        
   


      
            #Selective image rendering
    def draw_image_select(self,photo_select_1,search_key_1, info_1day_1, info_7day_1,info_15day_1):
        global photo_select_list
        if photo_select_1 == photo_select_list[0]:
            self.tem_curve_24(info_1day_1)
        elif photo_select_1 == photo_select_list[1]:
            self.hum_curve_24(info_1day_1)
        elif photo_select_1 == photo_select_list[2]:
            if search_key_1 in ("澳门", "香港", "台北"):
                tk.messagebox.showwarning("提示", "港澳台空气质量无法获取")
            else:
                self.air_curve_24(info_1day_1)
                
        elif photo_select_1 == photo_select_list[3]:
            self.wind_radar_24(info_1day_1)
        elif photo_select_1 == photo_select_list[4]:
            self.tem_curve_7(info_7day_1)
        elif photo_select_1 == photo_select_list[5]:
            self.tem_curve_15(info_15day_1,info_7day_1)
        elif photo_select_1 == photo_select_list[6]:
            self. wind_radar_15(info_15day_1)
        elif photo_select_1 == photo_select_list[7]:
            self.weather_pie(info_15day_1)

     #save data

    def save_message(self): 
        now_time = datetime.datetime.now().strftime('%T')
        now_time = now_time.replace(':', '-')
        now_date = datetime.datetime.now().strftime('%F')
        w = Write_to_csv()
        if info_select == '24h':
            file_name = search_key +"24小时的天气数据-" + now_date + '-' + now_time + ".csv"
            w.write_info_to_csv(file_name, info_1day, day=1)
            tk.messagebox.showinfo("提示", "24小时数据保存完成")
        else:
            file_name = search_key +"15天的天气数据-" + now_date + '-' + now_time + ".csv"
            w.write_info_to_csv(file_name, info_15day, day=15)
            tk.messagebox.showinfo("提示", "15天数据保存完成")
   

    #The information is updated automatically every 30 minutes
    def infoGet(self):
        info_1day, info_7day, info_15day = html_parser.get_city_all_weather_info(search_key)
        self.screen.after(30 * 60 *1000, self.infoGet)
        self.draw_weather_list()
        self.draw_image_select()
        
        
    def say_text(self):
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
        
    #Refresh the interface and draw the elements in the interface
    def screen_model(self):
        global canvas,weather_1day,weather_list
        self.screen.after(3000, self.draw_map)
        self.screen.after(3000, self.draw_menu)
        self.screen.after(3000, self.draw_weather_text)
        #screen.after(3000, self.draw_weather_list())
        #screen.after(3000, self.draw_image_select(canvas))






#Drop down property Settings

#Capture data during the animation display and draw interface elements

#The information is updated automatically every 30 minutes
#screen.after(30 * 60 * 1000, outputer.infoGet())





Outputer()


'''canvas_widget = FigureCanvasTkAgg(self.picture, master=self.canvas)
canvas_widget.draw()
canvas_widget.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)'''

