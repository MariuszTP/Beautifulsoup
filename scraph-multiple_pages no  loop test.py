from bs4 import BeautifulSoup
import requests
import csv
import re
import pandas as pd
import numpy as np
import os
import matplotlib
import matplotlib.pyplot as plt


page = 1
while page != 35:
    url = f"https://www.otodom.pl/pl/oferty/sprzedaz/dom/wiele-lokalizacji?distanceRadius=10&page={page}&limit=72&market=ALL&locations=%5Bcities_6-77%2Ccities_6-1%5D&viewType=listing "
    html_text = requests.get( url ).text
    soup = BeautifulSoup(html_text, 'lxml') 
    houses = soup.find_all('article', class_ = 'css-1th7s4x es62z2j16')

    for house in houses:
        prices = house.find_all('span', class_ = 'css-rmqm02 eclomwz0')[0]
        prices_meter = house.find_all('span', class_ = 'css-rmqm02 eclomwz0')[1]
        areas = house.find_all('span', class_ = 'css-rmqm02 eclomwz0')[-1]
        location = house.find_all('p', class_ = 'css-80g06k es62z2j10')
        #print(location)

        for price in prices:
            p = price.text
            p = re.findall("([\d,.]+)", p)
            p = ",".join(p)
            #print(p)

        for price_meter in prices_meter:
            m = price_meter.text
            m = re.findall("([\d,.]+)", m)
            m = ",".join(m)

        for area in areas:
            a = area.text 
            a = re.findall("([\d,.]+)", a)
            a = ",".join(a)

        for l in location:
            house_loc = l.find_all('span', class_='css-17o293g es62z2j9')
            for loc in house_loc:
                lo = loc.text

            df = pd.DataFrame({ 'price': [p], 'price_meter': [m], 'area': [a], 'house_loc': [lo]} )
            df = df.replace(',','', regex=True)
            df.to_csv("otodom advertisements all from poznan2.csv", mode='a', index=False, header=False, sep = '\t')

    page = page + 1

