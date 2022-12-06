from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import requests
from bs4 import BeautifulSoup
import json
import numpy as np
import pandas as pd

#headless
#options.headless = True

chrome_options = Options()
#chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920,1080")

#driver
driver = webdriver.Chrome(executable_path='/Users/denyszvarych/Desktop/booking_project/chromedriver',options=chrome_options)
        
def driver_close():

    driver.close()
    driver.quit()

headers = {
            "accept": "*/*",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
        }
    

def search_city(list_of_cities):

    main_page = "https://www.booking.com/index.en.html"
    driver.get(main_page)
    
    search = driver.find_element(By.NAME, 'ss')
    search.send_keys(list_of_cities[0])
    search.send_keys(Keys.ENTER)


def page_search(list_of_cities):
    pages = [25, 50, 100, 125]
    attempts = 3

    for city in list_of_cities:
        for page in range(0,25,25):
            
            city_url = f'https://www.booking.com/searchresults.html?label=gen173rf-1FCAEoggI46AdIM1gDaLYBiAEBmAEeuAEHyAEM2AEB6AEB-AELiAIBogINcHJvamVjdHByby5pb6gCA7gCuPGqnAbAAgHSAiRjYmY0NzU1MC0xNjgwLTRkMDQtYWUyMy1kMjFmZDlhMWE1ODjYAgbgAgE&sid=5b1a9de8b4303a134dc2264b96999451&aid=304142&tmpl=searchresults&checkin_month=1&checkin_monthday=20&checkin_year=2023&checkout_month=1&checkout_monthday=21&checkout_year=2023&class_interval=1&dtdisc=0&from_sf=1&group_adults=1&group_children=0&inac=0&index_postcard=0&label_click=undef&lang=en-us&no_rooms=1&postcard=0&room1=A&sb_price_type=total&search_pageview_id=5071a3a05ad60076&shw_aparth=1&slp_r_match=0&soz=1&src_elem=sb&srpvid=058ea20c74130085&ss={list_of_cities[0]}&ss_all=0&ssb=empty&sshis=0&lang_click=other&cdl=pl&lang_changed=1&offset={page}&order=popularity'
            driver.get(city_url)
            

            req = requests.get(city_url,headers = headers)
            src = req.text #kod strony internetowej w formacie html
            soup = BeautifulSoup(src,'lxml')

            data_hotels = {}
            time.sleep(3)

            

            #Можно поробовать записать цену з скидкой и цену без скидки
            if city == list_of_cities[0] and page == 0:
                hotels_names = [] #
                hotels_prices = []
                hotels_reviews = [] #
                hotels_city_reqion = [] #
                hotels_performances = [] #
                hotels_marks = [] #
                hotels_distances = [] #
                hotels_discriptions = [] #
                hotels_stars = []
                hotels_breakfasts = []


            div = soup.find_all(class_ = 'da89aeb942')
            for d in div:
                names = d.find(class_ = 'a23c043802').text
                hotels_names.append(names)
                # не нужно в try expect потому что имя всегда есть на странице

                try:
                    marks = d.find(class_ = 'd10a6220b4')
                    hotels_marks.append(marks.text)
                except:
                    marks = ''
                    hotels_marks.append(marks)

                try:
                    reviews = d.find(class_ = 'db63693c62')
                    hotels_reviews.append(reviews.text)
                except:
                    reviews = ''
                    hotels_reviews.append(reviews)

                try:
                    performances = d.find(class_ = 'e46e88563a')
                    hotels_performances.append(performances.text)
                except:
                    performances = ''
                    hotels_performances.append(performances)

                try:
                    city_reqion = d.find(class_ = 'b4273d69aa')
                    hotels_city_reqion.append(city_reqion.text)
                except:
                    city_reqion = ''
                    hotels_city_reqion.append(city_reqion)

                try:
                    prices = d.find_all(class_='e6e585da68')
                    for price in prices:
                        if price.text != 'Opens in new window':
                            hotels_prices.append(price.text)
                except:
                    prices = ''
                    hotels_prices.append(prices)

                distances = d.find_all(class_ = 'cb5ebe3ffb')
                for distance in distances:
                    try:
                        if  'center' in distance.text:
                            hotels_distances.append(distance.text)
                    except:
                        pass
                
                try:
                    discriptions = d.find(class_ = 'df597226dd')
                    hotels_discriptions.append(discriptions.text)
                except:
                    discriptions = ''
                    hotels_discriptions.append(discriptions)

                
                try:
                    div_stars = d.find_all(class_ = 'fe621d6382')
                    stars = (len(div_stars))
                    hotels_stars.append(stars)
                except:
                    stars = ''
                    hotels_stars.append(stars)

                try:
                    breakfasts = d.find(class_ = 'a53696345b')
                    #print(f'---{breakfasts.text}\n')
                    hotels_breakfasts.append(breakfasts.text)
                except:
                    breakfast = ''
                    hotels_breakfasts.append(breakfast)
                    
                    
                    
                # hotels_links



        data_hotels = {
        'Hotel name' : hotels_names,
        'Marks' : hotels_marks,
        'Region City' : hotels_city_reqion,
        'Performances' : hotels_performances,
        'Reviews' : hotels_reviews,
        'Price' : hotels_prices,
        'Distances' : hotels_distances,
        'Discriptions': hotels_discriptions,
        'Stars': hotels_stars,
        'Breakfast' : hotels_breakfasts
        }

        save_json(data_hotels)

def save_json(dict1):
     with open("data_booking.json", "w") as file:
        json.dump(dict1, file, indent=4, ensure_ascii=False)

    
list_cities = ['krakow']

page_search(list_cities)
driver_close()

df = pd.read_json("data_booking.json")
df.to_csv('hotels_test.csv')
