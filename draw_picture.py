# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 10:08:59 2023

@author: 12133
"""
import matplotlib.pyplot as plt
import numpy as np

class Drawer(object):
    
    #24 hours temperature curves 
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
    
    #24 hours air quality graph
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
              
    #24 hours wind curve
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

    #24 hours relative humidity 
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
    
    #Temperature curves    
    def tem_curve(self, info_15day_1,day):
        tem_low = []
        tem_high = []
        data = info_15day_1         
        #Save data
        for i in range(day):
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
        low_sum = day
        high_sum = day
        for i in range(day):
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
        x = range(1, day+1)
        plt.clf()
        plt.plot(x, tem_high, color='red', label='高温')
        plt.scatter(x, tem_high, color='red')
        plt.plot(x, tem_low, color='blue', label='低温')
        plt.scatter(x, tem_low, color='blue')
        plt.plot([1,day+1],[tem_high_ave, tem_high_ave], c='black', linestyle = '--')
        plt.plot([1,day+1],[tem_low_ave, tem_low_ave], c='black', linestyle = '--')
        plt.legend() 
        plt.text(tem_max_date + 0.15, tem_max +0.15, str(tem_max), ha='center', va='top', fontsize=10.5)
        plt.text(tem_min_date + 0.15, tem_min +0.15, str(tem_min), ha='center', va='top', fontsize=10.5)
        plt.text(1, round(tem_high_ave, 2), str(round(tem_high_ave, 2)), ha='center', va='top', fontsize=10.5)
        plt.text(1, round(tem_low_ave, 2), str(round(tem_low_ave, 2)), ha='center', va='top', fontsize=10.5)
        plt.xticks(x)
        plt.title('未来{}天高温低温变化曲线图'.format(day))
           
    #Change of the wind direction
    def change_wind(self, wind, day):
        for i in range(0, day):
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
            else:
                pass  
        return wind

    #Wind radar chart
    def wind_radar(self,info_15day_1, day):
        wind1 = []
        wind2 = []
        wind_speed = []
        for i in range(day):
            wind1.append(info_15day_1[i][4])
            wind2.append(info_15day_1[i][5])
            wind_speed.append(int(info_15day_1[i][6]))
        wind1 = self.change_wind(wind1, day)
        wind2 = self.change_wind(wind2, day)
        degs = np.arange(45, 361, 45)
        temp = []
        for deg in degs:
            speed = []
            for i in range(0,day):
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
        if max(temp) == 0:
            pass
        else:
            colors = [(1- x /max(temp), 1- x /max(temp), 0.6) for x in radii]
            plt.bar(theta, radii, width=(2 * np.pi / N), bottom=0.0, color=colors)
            plt.title("未来{}天风向雷达图".format(day), x=1, y=1, fontsize=10)

    #Weather pie chart
    def weather_pie(self, info_15day_1, day):
        weather = []
        for i in range(day):
            weather.append(info_15day_1[i][1])
        dic_wea = {}
        for i in range(0, day):
            if weather[i] in dic_wea.keys():
                dic_wea[weather[i]] += 1
            else:
                dic_wea[weather[i]] = 1
        plt.clf()
        if len(dic_wea) > 0:
            explode = [0.01] * len(dic_wea.keys())
            color = ['lightskyblue', 'silver', 'yellow', 'salmon', 'grey', 'lime', 'gold', 'red', 'green', 'pink']
            plt.pie(dic_wea.values(), explode=explode, labels=dic_wea.keys(), autopct='%1.1f%%', colors=color)
            plt.title("未来{}天气候分布图".format(day))
        else:
            plt.title("暂无数据可用")
