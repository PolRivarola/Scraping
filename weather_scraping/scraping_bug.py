import datetime
import time
from selenium.webdriver import Chrome,ChromeOptions
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import matplotlib.pyplot as plt
from selenium.webdriver.chrome.options import Options


# https://sites.google.com/chromium.org/driver/downloads?authuser=

def get_data_bug():
        
    options = Options()
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--ignore-ssl-errors")
    options.add_argument("--start-fullscreen")
    
    
    service = Service(ChromeDriverManager().install(),options=options)
    driver = Chrome(service=service)
    driver.get("https://www.weatherbug.com/weather-forecast/10-day-weather/")

    user_input = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.ID, 'locationInput'))
    )
    user_input.send_keys("Storrs, CT")
    user_input.send_keys(Keys.ENTER)
    
    # largeDayCardListItem
    highs = []
    lows = []
    days = []
    monthDict={1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'May', 6:'Jun', 7:'Jul', 8:'Aug', 9:'Sep', 10:'Oct', 11:'Nov', 12:'Dec'}

    # Find the list items for the day forecast cards
    forecast_items = driver.find_elements(By.CSS_SELECTOR, 'li.largeDayCardListItem__Container-sc-1mrqzix-1')[1:]

    # Loop through each forecast item and extract the max and min temperatures
    get_month = False
    for item in forecast_items:
        try:
            
            date = item.find_element(By.CSS_SELECTOR, '.dateWrap__CardDate-sc-kqdwnh-1').text
            day = int(date.split("/")[1])
            days.append( day)
            if not get_month:
                month = int(date.split("/")[0])
                if day < 25:
                    month +=1
                month = monthDict[month%12]
                year = date.split("/")[2] 
                get_month = True
            max_temp = item.find_element(By.CSS_SELECTOR, '.largeCardBodyItem__Container-sc-qy2n0b-0:first-child .cardSectionText__TemperatureReading-sc-oi8qub-2').text
            highs.append(max_temp)
            
            min_temp = item.find_element(By.CSS_SELECTOR, '.largeCardBodyItem__Container-sc-qy2n0b-0:last-child .cardSectionText__TemperatureReading-sc-oi8qub-2').text
            lows.append(min_temp)
            
        except Exception as e:
            print(f"Error extracting data for an item: {e}")

    driver.quit()
    
    highs = [int(temp.replace('°', '')) for temp in highs]
    lows = [int(temp.replace('°', '')) for temp in lows]
    
    stats = {'highs':highs,'lows':lows,'days':days}
    date =  {'month':month, 'year':year}
    return stats, date
            
            
def graph_site(stats, date):
    highs = [int(temp.replace('°', '')) for temp in stats['highs']]
    lows = [int(temp.replace('°', '')) for temp in stats['lows']]

    plt.figure(figsize=(12, 6))

    plt.plot(stats['days'], highs, marker='o', linestyle='-', label='High Temp (°F)', color='red')

    plt.plot(stats['days'], lows, marker='o', linestyle='-', label='Low Temp (°F)', color='blue')

    plt.xlabel(f'Days of {date["month"]}, {date["year"]}')
    plt.ylabel('Temperature (°F)')
    plt.title('Temperature Evolution')

    plt.xticks(stats['days'], rotation=45)

    plt.ylim(min(lows) - 1, max(highs) + 1)

    plt.tight_layout()

    plt.legend()

    plt.show()

