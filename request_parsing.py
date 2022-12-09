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


def find_number_of_pages(booking_city,driver,headers):
    
    city_main_page = f'https://www.booking.com/searchresults.html?label=gen173rf-1FCAEoggI46AdIM1gDaLYBiAEBmAEeuAEHyAEM2AEB6AEB-AELiAIBogINcHJvamVjdHByby5pb6gCA7gCuPGqnAbAAgHSAiRjYmY0NzU1MC0xNjgwLTRkMDQtYWUyMy1kMjFmZDlhMWE1ODjYAgbgAgE&sid=5b1a9de8b4303a134dc2264b96999451&aid=304142&tmpl=searchresults&checkin_month=1&checkin_monthday=20&checkin_year=2023&checkout_month=1&checkout_monthday=21&checkout_year=2023&class_interval=1&dtdisc=0&from_sf=1&group_adults=1&group_children=0&inac=0&index_postcard=0&label_click=undef&lang=en-us&no_rooms=1&postcard=0&room1=A&sb_price_type=total&search_pageview_id=5071a3a05ad60076&shw_aparth=1&slp_r_match=0&soz=1&src_elem=sb&srpvid=058ea20c74130085&ss={booking_city}&ss_all=0&ssb=empty&sshis=0&lang_click=other&cdl=pl&lang_changed=1&offset=0&order=popularity'
    driver.get(city_main_page)
    time.sleep(2)
    req = requests.get(city_main_page,headers = headers)
    src = req.text #kod strony internetowej w formacie html
    soup = BeautifulSoup(src,'lxml')

    #pages
    try:
        title_booking = soup.find(class_ = 'd3a14d00da')
        array_number = str(title_booking.text).split()
        if ',' in array_number[1]:
            array_number[1] = array_number[1].replace(',','')

        all_hotels = int(array_number[1])
        print(all_hotels)
        return all_hotels
    except:
        return 25 # tylko pierwsza strone bierzemy

def page_search(list_of_cities, driver,headers):

    for city in list_of_cities:
        number_of_pages = find_number_of_pages(city,driver,headers)
        number = (number_of_pages//50)*25
        if number >= 1000: # можно максимально запарсить только 1000 готелей с 1 города
            number = 1000

        print(f'{city} - {number} hotels \n')

        for page in range(0,number,25):
                        
            city_url = f'https://www.booking.com/searchresults.html?label=gen173rf-1FCAEoggI46AdIM1gDaLYBiAEBmAEeuAEHyAEM2AEB6AEB-AELiAIBogINcHJvamVjdHByby5pb6gCA7gCuPGqnAbAAgHSAiRjYmY0NzU1MC0xNjgwLTRkMDQtYWUyMy1kMjFmZDlhMWE1ODjYAgbgAgE&sid=5b1a9de8b4303a134dc2264b96999451&aid=304142&tmpl=searchresults&checkin_month=1&checkin_monthday=20&checkin_year=2023&checkout_month=1&checkout_monthday=21&checkout_year=2023&class_interval=1&dtdisc=0&from_sf=1&group_adults=1&group_children=0&inac=0&index_postcard=0&label_click=undef&lang=en-us&no_rooms=1&postcard=0&room1=A&sb_price_type=total&search_pageview_id=5071a3a05ad60076&shw_aparth=1&slp_r_match=0&soz=1&src_elem=sb&srpvid=058ea20c74130085&ss={city}&ss_all=0&ssb=empty&sshis=0&lang_click=other&cdl=pl&lang_changed=1&offset={page}&order=popularity'
            driver.get(city_url)
            
            req = requests.get(city_url,headers = headers)
            src = req.text #kod strony internetowej w formacie html
            soup = BeautifulSoup(src,'lxml')

            data_hotels = {}
            time.sleep(5)
            
            #Можно поробовать записать цену з скидкой и цену без скидки
            if page == 0:
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
                hotels_guest_reviews = []


            div = soup.find_all(class_ = 'da89aeb942')
            for d in div:
                
                # try to fix error with ad
                try:
                    ad = d.find(class_ = 'e2f34d59b1')
                    if 'Ad' in ad:
                        print(F'Found {page} pages with ad')
                        city_url = f'https://www.booking.com/searchresults.html?label=gen173rf-1FCAEoggI46AdIM1gDaLYBiAEBmAEeuAEHyAEM2AEB6AEB-AELiAIBogINcHJvamVjdHByby5pb6gCA7gCuPGqnAbAAgHSAiRjYmY0NzU1MC0xNjgwLTRkMDQtYWUyMy1kMjFmZDlhMWE1ODjYAgbgAgE&sid=5b1a9de8b4303a134dc2264b96999451&aid=304142&tmpl=searchresults&checkin_month=1&checkin_monthday=20&checkin_year=2023&checkout_month=1&checkout_monthday=21&checkout_year=2023&class_interval=1&dtdisc=0&from_sf=1&group_adults=1&group_children=0&inac=0&index_postcard=0&label_click=undef&lang=en-us&no_rooms=1&postcard=0&room1=A&sb_price_type=total&search_pageview_id=5071a3a05ad60076&shw_aparth=1&slp_r_match=0&soz=1&src_elem=sb&srpvid=058ea20c74130085&ss={city}&ss_all=0&ssb=empty&sshis=0&lang_click=other&cdl=pl&lang_changed=1&offset={page+25}&order=popularity'
                        driver.get(city_url)
            
                        req = requests.get(city_url,headers = headers)
                        src = req.text #kod strony internetowej w formacie html
                        soup = BeautifulSoup(src,'lxml')

                        time.sleep(3)
                        break
                except:
                    pass

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

                #for attempt in range(attempts):
                try:
                    prices = d.find_all(class_='e6e585da68')
                    for price in prices:
                        if price.text != 'Opens in new window':
                            hotels_prices.append(price.text)

                except:
                    prices = ''
                    hotels_prices.append(prices)

                    # if len(hotels_prices) % 5 == 0:
                    #         break
                    # else:
                    #     time.sleep(3)
                    #     driver.refresh()

                distances = d.find_all(class_ = 'cb5ebe3ffb')
                for distance in distances:
                    try:
                        if 'center' in distance.text:
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
                    hotels_breakfasts.append(breakfasts.text)
                except:
                    breakfast = ''
                    hotels_breakfasts.append(breakfast)

                try:
                    guests_reviews = d.find(class_ = 'f9afbb0024')
                    hotels_guest_reviews.append(guests_reviews.text)
                except:
                    guests_reviews = ''
                    hotels_guest_reviews.append(guests_reviews)
                
             
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
            'Breakfast' : hotels_breakfasts,
            'Guests reviews:' : hotels_guest_reviews
            }

        try:
            save_json(data_hotels, city)
        except:
            pass
            #print(f'With {city} and {page} pages something was wrong...\n start caclucale for begin until error',)            
            


def driver_close(driver):
    driver.close()
    driver.quit()

def save_csv(json_file, city):
    df = pd.read_json(json_file)
    df.to_csv(f'data_csv/{city}.csv')

def save_json(dict1, city):
    file_name = f"data_json/{city}_booking.json"
    with open(file_name, "w") as file:
        json.dump(dict1, file, indent=4, ensure_ascii=False)

    save_csv(file_name,city=city)


def read_txt():
    with open('cities.txt') as file: #'booking_cities.txt'
        lines = file.readlines()
    
    list_cities = [x[:-1] for x in lines]
    
    return list_cities

if __name__ == "__main__":
    
    headers = {
                "accept": "*/*",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
            }
    
    print('Read txt file with cities names...') 
    cities = read_txt()

    chrome_options = Options()
    chrome_options.add_argument("--window-size=1920,1080")
    #chrome_options.headless = True

    #driver
    wd = webdriver.Chrome(executable_path='/Users/denyszvarych/Desktop/booking_project/chromedriver', options=chrome_options)
        
    page_search(cities,wd, headers)
    driver_close(wd)