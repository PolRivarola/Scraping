from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



import time
# Web driver 
service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)

# Open site
driver.get("https://google.com")

# Wait for element
WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.CLASS_NAME, "gLFyf"))
)

input_ele = driver.find_element(By.CLASS_NAME, "gLFyf")
input_ele.clear()
input_ele.send_keys("Pol Rivarola" + Keys.ENTER)


WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "Pol Rivarola"))
)
# Find first link containing Pol Rivarola
link = driver.find_element(By.PARTIAL_LINK_TEXT, "Pol Rivarola")

# Find array of links containing Pol Rivarola
# link = driver.find_elements(By.PARTIAL_LINK_TEXT, "Pol Rivarola")


link.click()

time.sleep(4)


driver.quit()