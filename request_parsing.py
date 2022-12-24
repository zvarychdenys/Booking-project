# import libraries
import json
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def total_number_of_hotels(booking_city,driver,headers):
    
    '''Function gets the name of the city and loads the 
    main page booking.com with this city using webdriver
    and return the total number of hotels in this city'''

    time_pages = 2
    
    city_main_page = f'https://www.booking.com/searchresults.html?label=gen173rf-1FCAEoggI46AdIM1gDaLYBiAEBmAEeuAEHyAEM2AEB6AEB-AELiAIBogINcHJvamVjdHByby5pb6gCA7gCuPGqnAbAAgHSAiRjYmY0NzU1MC0xNjgwLTRkMDQtYWUyMy1kMjFmZDlhMWE1ODjYAgbgAgE&sid=5b1a9de8b4303a134dc2264b96999451&aid=304142&tmpl=searchresults&checkin_month=1&checkin_monthday=20&checkin_year=2023&checkout_month=1&checkout_monthday=21&checkout_year=2023&class_interval=1&dtdisc=0&from_sf=1&group_adults=1&group_children=0&inac=0&index_postcard=0&label_click=undef&lang=en-us&no_rooms=1&postcard=0&room1=A&sb_price_type=total&search_pageview_id=5071a3a05ad60076&shw_aparth=1&slp_r_match=0&soz=1&src_elem=sb&srpvid=058ea20c74130085&ss={booking_city}&ss_all=0&ssb=empty&sshis=0&lang_click=other&cdl=pl&lang_changed=1&offset=0&order=popularity'
    driver.get(city_main_page)
    
    time.sleep(time_pages) # waiting 2 seconds for the page to load

    req = requests.get(city_main_page,headers = headers)
    src = req.text 
    soup = BeautifulSoup(src,'lxml')

    # find the element with the total number of hotels on this page
    try:
        title_booking = soup.find(class_ = 'd3a14d00da')
        array_number = str(title_booking.text).split()
        if ',' in array_number[1]:
            array_number[1] = array_number[1].replace(',','')

        all_hotels = int(array_number[1])
        print(f'Total number of hotels in {booking_city} - {all_hotels}')
        return all_hotels
    except:
        return 25


def parsing_hotels(list_of_cities, driver,headers):

    for city in list_of_cities:

        # calculate how many pages should by parsed by dividing total number of hotels by 25 (25 hotels per 1 page)
        total_number = total_number_of_hotels(city,driver,headers)
        number_of_hotels = (total_number//50)*25  # 50 - means that I took only half of total hotels in this city 

        # it is possible to maximally parse only 1000 hotels from 1 city
        if number_of_hotels >= 1000: 
            number_of_hotels = 1000

        print(f'{number_of_hotels} hotels will be parsed in {city}\n')

        for page in range(0,number_of_hotels,25):

            time_page = 5 # set the waiting time on page

            city_url = f'https://www.booking.com/searchresults.html?label=gen173rf-1FCAEoggI46AdIM1gDaLYBiAEBmAEeuAEHyAEM2AEB6AEB-AELiAIBogINcHJvamVjdHByby5pb6gCA7gCuPGqnAbAAgHSAiRjYmY0NzU1MC0xNjgwLTRkMDQtYWUyMy1kMjFmZDlhMWE1ODjYAgbgAgE&sid=5b1a9de8b4303a134dc2264b96999451&aid=304142&tmpl=searchresults&checkin_month=1&checkin_monthday=20&checkin_year=2023&checkout_month=1&checkout_monthday=21&checkout_year=2023&class_interval=1&dtdisc=0&from_sf=1&group_adults=1&group_children=0&inac=0&index_postcard=0&label_click=undef&lang=en-us&no_rooms=1&postcard=0&room1=A&sb_price_type=total&search_pageview_id=5071a3a05ad60076&shw_aparth=1&slp_r_match=0&soz=1&src_elem=sb&srpvid=058ea20c74130085&ss={city}&ss_all=0&ssb=empty&sshis=0&lang_click=other&cdl=pl&lang_changed=1&offset={page}&order=popularity'
            driver.get(city_url)
            
            req = requests.get(city_url,headers = headers)  
            src = req.text 
            soup = BeautifulSoup(src,'lxml')

            time.sleep(time_page)
            
            # creating lists for each city on the first page
            if page == 0:
                hotels_names = [] 
                hotels_prices = []
                hotels_reviews = [] 
                hotels_city_reqion = [] 
                hotels_performances = [] 
                hotels_marks = [] 
                hotels_distances = [] 
                hotels_discriptions = [] 
                hotels_stars = []
                hotels_breakfasts = []
                hotels_guest_reviews = []

            # trying to find ad in pages, if the ad is on the page, then we skip page
            div = soup.find_all(class_ = 'da89aeb942')
            for d in div:
                try:
                    ad = d.find(class_ = 'e2f34d59b1')
                    if 'Ad' in ad:

                        print(f'Ad was found on the {page} page..')
                        
                        city_url = f'https://www.booking.com/searchresults.html?label=gen173rf-1FCAEoggI46AdIM1gDaLYBiAEBmAEeuAEHyAEM2AEB6AEB-AELiAIBogINcHJvamVjdHByby5pb6gCA7gCuPGqnAbAAgHSAiRjYmY0NzU1MC0xNjgwLTRkMDQtYWUyMy1kMjFmZDlhMWE1ODjYAgbgAgE&sid=5b1a9de8b4303a134dc2264b96999451&aid=304142&tmpl=searchresults&checkin_month=1&checkin_monthday=20&checkin_year=2023&checkout_month=1&checkout_monthday=21&checkout_year=2023&class_interval=1&dtdisc=0&from_sf=1&group_adults=1&group_children=0&inac=0&index_postcard=0&label_click=undef&lang=en-us&no_rooms=1&postcard=0&room1=A&sb_price_type=total&search_pageview_id=5071a3a05ad60076&shw_aparth=1&slp_r_match=0&soz=1&src_elem=sb&srpvid=058ea20c74130085&ss={city}&ss_all=0&ssb=empty&sshis=0&lang_click=other&cdl=pl&lang_changed=1&offset={page+25}&order=popularity'
                        driver.get(city_url)
            
                        req = requests.get(city_url,headers = headers)
                        src = req.text 
                        soup = BeautifulSoup(src,'lxml')

                        time.sleep(time_page)
                        break
                except:
                    pass


                # find the name of the hotel and add this name to the hotels_names list
                names = d.find(class_ = 'a23c043802').text
                hotels_names.append(names) 
    
                #  find the hotel rating and add this rating to the hotels_marks list
                try:
                    marks = d.find(class_ = 'd10a6220b4')
                    hotels_marks.append(marks.text)
                except:
                    marks = ''
                    hotels_marks.append(marks)
            
                #  find the number of hotel reviews and add this number to the hotels_reviews list
                try:
                    reviews = d.find(class_ = 'db63693c62')
                    hotels_reviews.append(reviews.text)
                except:
                    reviews = ''
                    hotels_reviews.append(reviews)

                #  find the performances and add to the hotels_performances list
                try:
                    performances = d.find(class_ = 'e46e88563a')
                    hotels_performances.append(performances.text)
                except:
                    performances = ''
                    hotels_performances.append(performances)

                # find the city and region and add to the hotels_city_reqion list
                try:
                    city_reqion = d.find(class_ = 'b4273d69aa')
                    hotels_city_reqion.append(city_reqion.text)
                except:
                    city_reqion = ''
                    hotels_city_reqion.append(city_reqion)

                # find price of hotels and add to hotels_prices list
                try:
                    prices = d.find_all(class_='e6e585da68')
                    for price in prices:
                        if price.text != 'Opens in new window':
                            if 'This property spends' not in  price.text:
                                hotels_prices.append(price.text)
                except:
                    prices = ''
                    hotels_prices.append(prices)

                # find the distances of hotel from center 
                distances = d.find_all(class_ = 'cb5ebe3ffb')
                for distance in distances:
                    try:
                        if 'center' in distance.text:
                            hotels_distances.append(distance.text)
                    except:
                        pass
                
                # find discriptions of hotels and add to hotels_discriptions list
                try:
                    discriptions = d.find(class_ = 'df597226dd')
                    hotels_discriptions.append(discriptions.text)
                except:
                    discriptions = ''
                    hotels_discriptions.append(discriptions)

                # find number of stars and add to hotels_stars list
                try:
                    div_stars = d.find_all(class_ = 'fe621d6382')
                    stars = (len(div_stars))
                    hotels_stars.append(stars)
                except:
                    stars = ''
                    hotels_stars.append(stars)
                
                # try find type of meal in this hotel
                try:
                    breakfasts = d.find(class_ = 'a53696345b')
                    hotels_breakfasts.append(breakfasts.text)
                except:
                    breakfast = ''
                    hotels_breakfasts.append(breakfast)

                # try to find the highest reviews by guests
                try:
                    guests_reviews = d.find(class_ = 'f9afbb0024')
                    hotels_guest_reviews.append(guests_reviews.text)
                except:
                    guests_reviews = ''
                    hotels_guest_reviews.append(guests_reviews)
                
            # create dictionary with all inforamation about hotels
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

       # save dictionary to json file
        try:
            save_json(data_hotels, city)
        except:
            pass
            print(f'With {city} and {page} page something was wrong...')            
            

def driver_close(driver):
    driver.close()
    driver.quit()


def save_csv(json_file, city):
    try:
        df = pd.read_json(json_file)
        df.to_csv(f'data_csv/{city}.csv')
        
        print(f'{city}.csv file was created')
    except:
        print('Something went wrong')
    

def save_json(dict1, city):
    file_name = f"data_json/{city}_booking.json"
    with open(file_name, "w") as file:
        json.dump(dict1, file, indent=4, ensure_ascii=False)

    save_csv(file_name,city=city)


def read_txt():
    with open('european cities.txt') as file:
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

    #create webdriver for navigating to web pages in Coogle Chrome browser
    wd = webdriver.Chrome(executable_path='/Users/denyszvarych/Desktop/booking_project/chromedriver', options=chrome_options)
        
    parsing_hotels(cities,wd, headers)
    driver_close(wd)