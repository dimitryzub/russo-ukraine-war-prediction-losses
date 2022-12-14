import requests, time, json, lxml, re
from bs4 import BeautifulSoup
from random import randint
import pandas as pd

month = 2

russo_loses_data = []

for i in range(0, 9):
    html = requests.get(f'https://index.minfin.com.ua/en/russian-invading/casualties/month.php?month=2022-{month}')
    soup = BeautifulSoup(html.text, 'lxml')

    for results in soup.select('.gold'):
        date = re.search(r'(\d{2}.\d{2}.\d{4})', results.text).group()
        
        try:
            tanks = int(re.search(r'Tanks.*?(\d+)', results.text).group(1))
        except: tanks = None
        
        try:
            armored_vehicle = int(re.search(r'Armored fighting vehicle.*?(\d+)', results.text).group(1))
        except: armored_vehicle = None

        try:
            planes = int(re.search(r'Planes.*?(\d+)', results.text).group(1))
        except: planes = None

        try:
            helicopters = int(re.search(r'Helicopters.*?(\d+)', results.text).group(1))
        except: helicopters = None

        try:
            cannons = int(re.search(r'Cannons.*?(\d+)', results.text).group(1))
        except: cannons = None

        try:
            mlrs_buk = int(re.search(r'BUK missile system.*?(\d+)', results.text).group(1))
        except: mlrs_buk = None
        
        try:
            mlrs_grad = int(re.search(r'MLRS Grad.*?(\d+)', results.text).group(1))
        except: mlrs_grad = None
        
        try:
            mlrs = int(re.search(r'\bMLRS\b.*?(\d+)', results.text).group(1))
        except: mlrs = None

        try:
            anti_air = int(re.search(r'Anti-aircraft warfare.*?(\d+).*?(\d+)', results.text).group(1))
        except: anti_air = None
        
        try:
            uav = int(re.search(r'UAV.*?(\d+)', results.text).group(1))
        except: uav = None
        
        try:
            cruise_missiles = int(re.search(r'Cruise missiles.*?(\d+)', results.text).group(1))
        except: cruise_missiles = None

        try:
            ships = int(re.search(r'Ships \(boats\).*?(\d+)', results.text).group(1))
        except: ships = None
        
        try:
            cars_cisterns = int(re.search(r'Special equipment.*?(\d+)', results.text).group(1))
        except: cars_cisterns = None
        
        try:
            special_equpment = int(re.search(r'Special equipment.*?(\d+)', results.text).group(1))
        except: special_equpment = None

        try:
            personnel = int(re.search(r'Military personnel.*?(\d+)', results.text).group(1))
        except: personnel = None

        
        russo_loses_data.append({
            'date': date,
            'tanks': tanks,
            'armored_vehicle': armored_vehicle,
            'planes': planes,
            'helicopters': helicopters,
            'cannons': cannons,
            'mlrs_buk': mlrs_buk,   # could be combined with mlrs category as it's similar thing
            'mlrs_grad': mlrs_grad, # could be combined with mlrs category as it's similar thing
            'mlrs': mlrs,           # later they combined buk,grad to single mlrs category
            'anti_air': anti_air,
            'uav': uav,
            'cruise_missiles': cruise_missiles,
            'ships': ships,
            'cars_cisterns': cars_cisterns,
            'special_equpment': special_equpment,
            'personnel': personnel
        })

    time.sleep(randint(5, 10))
    print(f'exctracting month: {month}')
    month += 1

print(json.dumps(russo_loses_data, indent=2, ensure_ascii=False))
    
pd.DataFrame(data=russo_loses_data).to_csv('russo-ukraine-war-casualties.csv', index=False, encoding='utf-8')
pd.DataFrame(data=russo_loses_data).to_json('russo-ukraine-war-casualties.json', orient='records')
