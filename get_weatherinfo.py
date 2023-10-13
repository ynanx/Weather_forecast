# -*- coding: utf-8 -*-
"""
Created on Tue Oct 10 16:58:21 2023

@author: 12133
"""

import requests
from bs4 import BeautifulSoup
import json



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
        print(weather_1d) 
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
                temp.append(tep_low) 
                tep_high = inf[1].find('span').string #maximum temperature
                temp.append(tep_high)
                
                wind = inf[2].find_all('span') #wind direction
                i = 0
                for j in wind:
                    wind_dir = j["title"]
                    temp.append(wind_dir)
                    i = i + 1

                wind_scale = inf[2].find('i').string #wind scale
                index1 = wind_scale.index('级')
                temp.append(wind_scale[index1 - 1 : index1 + 1])
                
                weather_7d.append(temp)
            count = count + 1
        print(weather_7d)
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
                date = day.find('span', {'class':'time'}).string  #date
                temp.append(date)
                
               
                weather = day.find('span', {'class': 'wea'}).string  #weather 
                temp.append(weather) 
                
                tep = day.find('span', {'class': 'tem'})
                tep_str = tep.text
                tep_high = tep.find('em').string #maximum temperature
                temp.append(tep_high)
                print(tep_high)
                
                print(tep_str)
                tep_low =tep_str[-3:]  #minimum temperature
                temp.append(tep_low)


               
                
                wind_dir = day.find('span', {'class' : 'wind'}).string #wind direction
                temp.append(wind_dir)

                wind_scale = day.find('span', {'class' : 'wind1'}).string  #wind scale
                index1 = wind_scale.index('级')
                temp.append(wind_scale[index1 - 1 : index1 + 5])
                
                weather_15d.append(temp)
            count = count + 1
        print(weather_15d)
        return weather_15d
        
        
            
                
                
                
                
                
                
                
                
                


      
city_data = Get_city_info.Get_cityID(CityID_base_url)

#print(city_data)
print(type(city_data))

#new_dict = {city:info[city][city][city]['AREAID'] for city, info in city_data.items()}

#print(new_dict)


search_key = '晋江'
city_ID = Get_city_info().find_value(city_data, search_key)['AREAID']


if city_ID is not None:
    
    print(f"The value of {search_key} is {city_ID}")
else:
    print(f"Cannot find the value of {search_key}")
#city_url_1d= Get_city_info().Get_city_url(city_ID, 1)
#City_html_1d = HtmlCrawler().Crawl_html(city_url_1d)

#city_url_7d= Get_city_info().Get_city_url(city_ID, 7)
#City_html_7d = HtmlCrawler().Crawl_html(city_url_7d)


#city_url_15d= Get_city_info().Get_city_url(city_ID, 15)
#City_html_15d = HtmlCrawler().Crawl_html(city_url_15d)


#HtmlParser().Parse_html_15d(City_html_7d)
