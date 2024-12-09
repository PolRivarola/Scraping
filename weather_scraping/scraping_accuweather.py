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

# https://sites.google.com/chromium.org/driver/downloads?authuser=

def get_data_accu():
        
    service = Service(ChromeDriverManager().install())
    driver = Chrome(service=service)
    driver.get("https://www.accuweather.com/")

    user_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.NAME, 'query'))
    )
    user_input.send_keys("Storrs, CT")
    user_input.send_keys(Keys.ENTER)

    monthly_q = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//*[@data-qa='monthly']"))
    )
    monthly_q.send_keys(Keys.ENTER)

    panels = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//*[normalize-space(@class) = 'monthly-daypanel']"))
    )[:9]

    month_year = WebDriverWait(driver, 10).until(
        EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".map-dropdown h2"))
    )

    month = month_year[0].text
    year = month_year[1].text

    highs = []
    lows = []
    days = []

    for index, panel in enumerate(panels, start=1):
        try:
            high_temp = panel.find_element(By.CSS_SELECTOR, ".temp .high").text
            day = panel.find_element(By.CSS_SELECTOR, ".date").text
            low_temp = panel.find_element(By.CSS_SELECTOR, ".temp .low").text

            days.append(int(day))
            highs.append(high_temp)
            lows.append(low_temp)
            
        except Exception as e:
            print(f"Error extracting data from panel {index}: {e}")
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

    plt.plot(stats['days'], highs, marker='o', linestyle='-', label='High Temp (°C)', color='red')

    plt.plot(stats['days'], lows, marker='o', linestyle='-', label='Low Temp (°C)', color='blue')

    plt.xlabel(f'Days of {date["month"]}, {date["year"]}')
    plt.ylabel('Temperature (°C)')
    plt.title('Temperature Evolution')

    plt.xticks(stats['days'], rotation=45)

    plt.ylim(min(lows) - 1, max(highs) + 1)

    plt.tight_layout()

    plt.legend()

    plt.show()

