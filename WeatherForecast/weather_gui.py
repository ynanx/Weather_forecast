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
from get_weatherinfo import HtmlParser, Write_to_csv
from draw_picture import Drawer

time_select = ("24h","7天","15天")
photo_select_list = ("过去24小时温度变化曲线图", "过去24小时相对湿度变化曲线图", 
                     "过去24小时空气质量柱状图", "过去24小时风向雷达图", 
                     "未来7天高温低温变换曲线图","未来7天风向雷达图",
                     "未来7天气候分布饼状图",
                     "未来15天高温低温变换曲线图", "未来15天风向雷达图",
                     "未来15天气候分布饼状图")
html_parser = HtmlParser()
my_drawr=Drawer() 

#Set the startup image to avoid whiteboards due to loading data
class Start_picture(tk.Frame):
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
        self.time_list = None
        self.photo_list =None
        self.weather_1day = None
        self.weather_list = None
        self.frame = None

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
                                                         'selectbackground': 'green',
                                                         'background':'green',
                                                         'selectforeground':'black',
                                                         'selectborderwidth': 0
                                                             }}})
        else:
            combostyle = tk.ttk.Style()
        combostyle.theme_use('combostyle')  

        #Set the Chinese display in matplotlib
        plt.rcParams['font.sans-serif'] = 'SimHei'
        plt.rcParams['axes.unicode_minus'] = False

        self.app=Start_picture(master=self.screen)
        self.screen.geometry("1000x600+0+0")
        self.screen_model()
        self.screen.after(30 * 60 * 1000, self.infoGet)
        self.screen.mainloop()

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
    
    #Weather list display(text)
    def draw_weather_text(self):
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
        
    #Weather list display(table)        
    def draw_weather_list(self,search_key_1, info_1day_1, info_15day_1, info_select_1):
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
                self.weather_list.create_text(80,70 + i * 50, text=str(info_15day_1[i][0]),font=('宋体',15))
                self.weather_list.create_text(200,70 + i * 50, text=str(info_15day_1[i][1]),font=('宋体',15))
                self.weather_list.create_text(320,70 + i * 50, text=str(info_15day_1[i][2]),font=('宋体',15))
                self.weather_list.create_text(440,70 + i * 50, text=str(info_15day_1[i][3]),font=('宋体',15))
                self.weather_list.create_text(560,70 + i * 50, text=str(info_15day_1[i][4]),font=('宋体',15))
                self.weather_list.create_text(680,70 + i * 50, text=str(info_15day_1[i][5]),font=('宋体',15))
                self.weather_list.create_text(800,70 + i * 50, text=str(info_15day_1[i][6]),font=('宋体',15))        
        elif info_select_1 == "15天":
            self.weather_list.create_text(80, 20, text='时间/Day', font=('宋体', 15))
            self.weather_list.create_text(200, 20, text='天气', font=('宋体', 15))
            self.weather_list.create_text(320, 20, text='最低温度', font=('宋体', 15))
            self.weather_list.create_text(440, 20, text='最高温度', font=('宋体', 15))
            self.weather_list.create_text(560, 20, text='风向1', font=('宋体', 15))
            self.weather_list.create_text(680, 20, text='风向2', font=('宋体', 15))
            self.weather_list.create_text(800, 20, text='风级', font=('宋体', 15))
            for i in range(15):
                self.weather_list.create_text(80,70 + i * 50, text=str(info_15day_1[i][0]),font=('宋体',15))
                self.weather_list.create_text(200,70 + i * 50, text=str(info_15day_1[i][1]),font=('宋体',15))
                self.weather_list.create_text(320,70 + i * 50, text=str(info_15day_1[i][2]),font=('宋体',15))
                self.weather_list.create_text(440,70 + i * 50, text=str(info_15day_1[i][3]),font=('宋体',15))
                self.weather_list.create_text(560,70 + i * 50, text=str(info_15day_1[i][4]),font=('宋体',15))
                self.weather_list.create_text(680,70 + i * 50, text=str(info_15day_1[i][5]),font=('宋体',15))
                self.weather_list.create_text(800,70 + i * 50, text=str(info_15day_1[i][6]),font=('宋体',15))    

    def get_weather_info(self):
        search_key = self.entry.get()
        try:
            info_1day, info_15day =html_parser.get_city_all_weather_info(search_key)
            return search_key, info_1day, info_15day
        except Exception as e:
                error_message = "无法获取天气数据：" + str(e)
                messagebox.showerror("错误", error_message)
                print(error_message)
                return 
    
    def  draw_to_canvas(self):
        search_key_1,info_1day_1,info_15day_1 = self.get_weather_info()
        info_select = self.time_list.get()
        photo_select = self.photo_list.get()
        self.draw_image_select(photo_select,search_key_1, info_1day_1,info_15day_1)
        self.draw_weather_list(search_key_1,info_1day_1,info_15day_1,info_select)
        
    #Generate menus, buttons and selection boxes
    def draw_menu(self):
        #City search
        city_select= tk.Label(self.screen, text="搜索城市", font=("楷体", 15), width=8, height=1)
        city_select.place(x=50, y=50)
       
        self.entry = tk.Entry(self.screen, font=("楷体", 15))
        self.entry.place(x=150, y=50)
        button = tk.Button(self.screen, text="确定", font=("楷体", 10), command=self.draw_to_canvas)
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
        ok_label = tk.Label(self.screen, text="数据更新", font=("楷体", 15), width=8, height=1)
        ok_label.place(x=260, y=120)
        ok = tk.Button(self.screen, text= "确认更新", command=self.draw_to_canvas, font=("楷体", 15), width=10, height=1)
        ok.place(x=347, y=115)
        #function
        menu = tk.Label(self.screen, text="功能按钮", font=("楷体", 15), width=8, height=1)
        menu.place(x=50,y=190)
        say = tk.Button(self.screen, text= "语音播报", command=self.say_voice, font=("楷体", 15), width=10, height=1)
        say.place(x=150, y=185)
        save = tk.Button(self.screen, text= "数据保存", command=self.save_message, font=("楷体", 15), width=10, height=1)
        save.place(x=347, y=185)
        
    #Select image
    def draw_image_select(self,photo_select_1,search_key_1, info_1day_1, info_15day_1):
        global photo_select_list
        if photo_select_1 == photo_select_list[0]:
            my_drawr.tem_curve_24(info_1day_1)
        elif photo_select_1 == photo_select_list[1]:
            my_drawr.hum_curve_24(info_1day_1)
        elif photo_select_1 == photo_select_list[2]:
            if search_key_1 in ("澳门", "香港", "台北"):
                tk.messagebox.showwarning("提示", "港澳台空气质量无法获取")
            else:
                my_drawr.air_curve_24(info_1day_1)       
        elif photo_select_1 == photo_select_list[3]:
            my_drawr.wind_radar_24(info_1day_1)
        elif photo_select_1 == photo_select_list[4]:
            my_drawr.tem_curve( info_15day_1,7)
        elif photo_select_1 == photo_select_list[5]:
            my_drawr.wind_radar(info_15day_1,7)
        elif photo_select_1 == photo_select_list[6]:
            my_drawr.weather_pie(info_15day_1,7)
        elif photo_select_1 == photo_select_list[7]:
            my_drawr.tem_curve(info_15day_1,15)
        elif photo_select_1 == photo_select_list[8]:
            my_drawr.wind_radar(info_15day_1,15)
        elif photo_select_1 == photo_select_list[9]:
            my_drawr.weather_pie(info_15day_1,15)
        self.canvas.draw()

    #save data
    def save_message(self): 
        search_key_1,info_1day_1,info_15day_1 = self.get_weather_info()
        info_select_1 = self.time_list.get()
        now_time = datetime.datetime.now().strftime('%T')
        now_time = now_time.replace(':', '-')
        now_date = datetime.datetime.now().strftime('%F')
        w = Write_to_csv()
        if info_select_1 == '24h':
            file_name = search_key_1 +"24小时的天气数据-" + now_date + '-' + now_time + ".csv"
            w.write_info_to_csv(file_name, info_1day_1, day=1)
            tk.messagebox.showinfo("提示", "24小时数据保存完成")
        elif info_select_1 == '7天':
            file_name = search_key_1 +"7天的天气数据-" + now_date + '-' + now_time + ".csv"
            w.write_info_to_csv(file_name, info_15day_1[0:7], day=7)
            tk.messagebox.showinfo("提示", "7天数据保存完成")
        else:
            file_name = search_key_1 +"15天的天气数据-" + now_date + '-' + now_time + ".csv"
            w.write_info_to_csv(file_name, info_15day_1, day=15)
            tk.messagebox.showinfo("提示", "15天数据保存完成")
   
    #Updated information automatically every 30 minutes
    def infoGet(self):
        search_key_1,info_1day_1,info_15day_1 = self.get_weather_info()
        self.screen.after(30 * 60 *1000, self.infoGet)
        self.draw_to_canvas()
    
    def say_text(self):
        search_key_1,info_1day_1,info_15day_1 = self.get_weather_info()
        text_read = [""] * 6
        text_read[0] = search_key_1 + "市" 
        text_read[1] = str(info_15day_1[0][0]) + str(info_1day_1[0][0]) + "时" +","
        text_read[2] = "天气" + info_15day_1[0][1] + ","
        if info_15day_1[0][3] == None:
            text_read[3] = "最高气温" + "暂无" + "，" + "最低气温" + str(info_15day_1[0][2]) + "度" +"，" + "当前温度" + str(info_1day_1[0][1]) + \
            + "度"  + ","           
        else:
            text_read[3] = "最高气温" + str(info_15day_1[0][3]) + "," + "最低气温" + str(info_15day_1[0][2]) + "度" + "，" + "当前温度" + \
            str(info_1day_1[0][1]) + "度"  + "," 
        
        text_read[4] = info_1day_1[0][2] + str(info_1day_1[0][3]) + "级"
        
        if info_1day_1[0][6] == '':
            text_read[5] = "降水" + str(info_1day_1[0][4]) + "," + "相对湿度" + str(info_1day_1[0][5]) + "," + "空气质量" + "暂无"
        else:
            text_read[5] = "降水" + str(info_1day_1[0][4]) + "," + "相对湿度" + str(info_1day_1[0][5]) + "," + "空气质量" + str(info_1day_1[0][6]) 
        return text_read
                 
    #voice function
    def say_voice(self):
        voice = pyttsx3.init()
        voice.setProperty('rate', 200)
        text_read_1 = self.say_text()
        for i in range(6):
            voice.say(text_read_1[i])
        voice.runAndWait()
        
    #Refresh the interface and draw the elements in the interface
    def screen_model(self):
        global canvas,weather_1day,weather_list
        self.screen.after(3000, self.draw_map)
        self.screen.after(3000, self.draw_menu)
        self.screen.after(3000, self.draw_weather_text)
        



