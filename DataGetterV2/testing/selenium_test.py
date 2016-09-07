import time
from selenium import webdriver

driver = webdriver.Chrome("C:\Program Files (x86)\Google\Chrome\Application\chrome.exe")
driver.get("http://www.neco.cz")
time.sleep(5)
driver.quit()
