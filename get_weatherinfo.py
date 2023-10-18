# -*- coding: utf-8 -*-
"""
Created on Tue Oct 10 16:58:21 2023

@author: 12133
"""

import requests
from bs4 import BeautifulSoup
import json
import csv
import re


Weather_base_url = "http://www.weather.com.cn/"
CityID_base_url = "https://j.i8tq.com/weather2020/search/city.js"
Weather_url_end =".shtml"

Test_str = "北京"

headers = {
            'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)\
                Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.60'
           }
  

                    
class Get_city_info(object):
    
    #Cannot access the website directly by using the city's name
    #Access is required by obtaining city's ID
    def Get_cityID(self, url = CityID_base_url): #Get the city's ID
        response = requests.get(url)
        city_data_str = response.text
        city_data_lines = city_data_str.split("\n")
        city_data= city_data_lines[1:-1]
        city_data_text = "\n".join(city_data)
        city_dict = eval(city_data_text)
        with open(r"./cityname.txt",'w',encoding='utf-8') as f:
            f.write(response.text)
        return city_dict
    
    def find_value(self, city_data, search_key):
        for key ,value in city_data.items():
            if isinstance(value, dict):
                result = self.find_value(value, search_key)
                if result is not None:
                    return result
                elif key == search_key:
                    return value
            
        return None    
    
    def Get_city_url(self, city_ID, day):
        if day == 1:
            City_url_1d = Weather_base_url +"weather1d/" + city_ID + Weather_url_end
            return City_url_1d
        elif day == 7:
            City_url_7d = Weather_base_url + "weather/" + city_ID + Weather_url_end
            return City_url_7d
        elif day == 15:
            City_url_15d = Weather_base_url +"weather15d/" + city_ID + Weather_url_end
            return City_url_15d
        else :
            return None
        
            
            
                

class HtmlCrawler(object):
    
    def Crawl_html(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        with open(r"./city_html_info.txt", 'w', encoding= 'utf-8') as f:
            f.write(soup.prettify(formatter="html"))
        return soup

 
class HtmlParser(object):
    
    def Parse_html_1d(self, html):
        html_body = html.body
        div_class_leftdiv = html_body.find_all('div', {'class': 'left-div'})
        text = div_class_leftdiv[1].find('script').string
        text = text[text.index('=') + 1:-2]
        hjson = json.loads(text)
        day = hjson["od"]["od2"]
        weather_1d = []
        count = 0
        for d in day:
            temp = []
            if count <= 24:
                temp.append(d['od21'])#time
                temp.append(d['od22'])#temperature
                temp.append(d['od24'])#wind direction
                temp.append(d['od25'])#wind scale
                temp.append(d['od26'])#precipitation
                temp.append(d['od27'])#relative humidity
                temp.append(d['od28'])#air quality
                weather_1d.append(temp)
            count = count + 1
        #print(weather_1d) 
        return weather_1d
    
    def Parse_html_7d(self, html):
        html_body = html.body
        div_class_c7d = html_body.find('div', {'class':"c7d" ,'id' : "7d"})
        ul = div_class_c7d.find('ul')
        li = ul.find_all('li')
        weather_7d = []
        count = 0
        for day in li:
            temp = []
            if count < 7:
                date = day.find('h1').string #date
                temp.append(date)
                
                inf = day.find_all('p')
                weather = inf[0].string #weather 
                temp.append(weather) 
                
                tep_low = inf[1].find('i').string #minimum temperature
                temp.append(tep_low[:-1]) 
                if inf[1].find('span') is not None:
                    tep_high = inf[1].find('span').string
                    temp.append(tep_high)#maximum temperature
                else:
                    tep_high = None
                    temp.append(tep_high)
                
                
                wind = inf[2].find_all('span') #wind direction
                i = 0
                for j in wind:
                    wind_dir = j["title"]
                    temp.append(wind_dir)
                    i = i + 1
                if i == 1:
                    temp.append(wind_dir)

                wind_scale = inf[2].find('i').string #wind scale
                index1 = wind_scale.index('级')
                temp.append(wind_scale[index1 - 1 : index1])
                
                weather_7d.append(temp)
            count = count + 1
        #print(weather_7d)
        return weather_7d
    
    def Parse_html_15d(self, html):
        html_body = html.body
        div_class_c15d = html_body.find('div', {'class':"c15d" ,'id' : "15d"})
        ul = div_class_c15d.find('ul')
        li = ul.find_all('li')
        weather_15d = []
        count = 0
        for day in li:
            temp = []
            if count < 8:
                date_str = day.find('span', {'class':'time'}).string#date
                date=date_str[date_str.index('（') +1:date_str.index('）')] + '（'  + \
                     date_str[:date_str.index('（')] + '）'
                temp.append(date)
                
               
                weather = day.find('span', {'class': 'wea'}).string  #weather 
                temp.append(weather) 
                
                tep = day.find('span', {'class': 'tem'})
                tep_str = tep.text
                index = tep_str.index('/') 
                tep_low =tep_str[index + 1:-1]  #minimum temperature
                temp.append(tep_low)
                tep_high = tep_str[:index-1]
                temp.append(tep_high)
                
                wind_dir = day.find('span', {'class' : 'wind'}).string #wind direction
                if '转' in wind_dir:
                    temp.append(wind_dir[:wind_dir.index('转')])
                    temp.append(wind_dir[wind_dir.index('转')+1 :])
                else:
                    temp.append(wind_dir)
                    temp.append(wind_dir)
                    

                wind_scale = day.find('span', {'class' : 'wind1'}).string  #wind scale
                index1 = wind_scale.index('级')
                temp.append(wind_scale[index1-1 : index1])
                
                weather_15d.append(temp)
            count = count + 1
        #print(weather_15d)
        return weather_15d
    
    def get_city_all_weather_info(self, search_key):
        try:
            city_data = Get_city_info.Get_cityID(CityID_base_url)
            result = Get_city_info().find_value(city_data, search_key)
            if result is None:
                return None
            city_ID = result['AREAID']
        
            city_url_1d= Get_city_info().Get_city_url(city_ID, 1)
            City_html_1d = HtmlCrawler().Crawl_html(city_url_1d)
            data_1d = HtmlParser().Parse_html_1d(City_html_1d) 
        
            city_url_7d= Get_city_info().Get_city_url(city_ID, 7)
            City_html_7d = HtmlCrawler().Crawl_html(city_url_7d)
            data_7d = HtmlParser().Parse_html_7d(City_html_7d) 
        
            city_url_15d= Get_city_info().Get_city_url(city_ID, 15)
            City_html_15d = HtmlCrawler().Crawl_html(city_url_15d)
            data_15d = HtmlParser().Parse_html_15d(City_html_15d)
        
            return data_1d, data_7d + data_15d
        except KeyError:
            return None
    
    
    
class Write_to_csv(object):
    
    
    def write_info_to_csv(self, filename, data, day=15):
            with open(filename, 'w', errors = 'ignore', newline = '') as f:
                if(day == 1):
                    header = ['小时', '温度', '风向', '风级', '降水量', '相对湿度', '空气质量']
                elif(day == 7):
                    header = ['日期', '天气', '最低气温', '最高气温', '风向1', '风向2','风级']
                elif(day == 15):
                    header = ['日期', '天气', '最低气温', '最高气温', '风向1', '风向2','风级']
                else:
                    print("error:Failed to write the csv file")
                
                f_csv = csv.writer(f)
                f_csv.writerow(header)
                f_csv.writerows(data)
                
    def write_all_info_to_csvs(self, search_key):
        data = HtmlParser().get_city_all_weather_info(search_key)
        if data is None:
            return
        data_1d, data_15d = data
        Write_to_csv().write_info_to_csv(r'./1d_info.csv', data_1d, day=1)
        Write_to_csv().write_info_to_csv(r'./15d_info.csv', data_15d,day=15)
        
            
                
                
                
                
                
                
            
















