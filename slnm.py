import time

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import selenium
from selenium.webdriver.common.by import By
driver = webdriver.Chrome()

SCROLL_PAUSE_TIME = 2




driver.get('https://www.reddit.com/search/?q=bitcoin&sort=new')

# driver.implicitly_wait(100)


i = 1
while True:
    try:
        my_element = driver.find_element(By.XPATH, f"/html/body/shreddit-app/dsa-transparency-modal-provider/search-dynamic-id-cache-controller/div/div/div[1]/div[2]/main/div/reddit-feed/faceplate-tracker[{i}]/post-consume-tracker/div/faceplate-tracker/h2/a")
    except selenium.common.exceptions.NoSuchElementException as e:
        break
    i+=1
    print(my_element.text)
    
# driver.implicitly_wait(1)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
# Wait to load page
time.sleep(SCROLL_PAUSE_TIME)


    
while True:
    try:
        my_element = driver.find_element(By.XPATH, f"/html/body/shreddit-app/dsa-transparency-modal-provider/search-dynamic-id-cache-controller/div/div/div[1]/div[2]/main/div/reddit-feed/faceplate-tracker[{i}]/post-consume-tracker/div/faceplate-tracker/h2/a")
    except selenium.common.exceptions.NoSuchElementException as e:
        break
    i+=1
    print(my_element.text)

# driver.implicitly_wait(1)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
# Wait to load page
time.sleep(SCROLL_PAUSE_TIME)


    
while True:
    try:
        my_element = driver.find_element(By.XPATH, f"/html/body/shreddit-app/dsa-transparency-modal-provider/search-dynamic-id-cache-controller/div/div/div[1]/div[2]/main/div/reddit-feed/faceplate-tracker[{i}]/post-consume-tracker/div/faceplate-tracker/h2/a")
    except selenium.common.exceptions.NoSuchElementException as e:
        break
    i+=1
    print(my_element.text)
    
    
    
# driver.implicitly_wait(1)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
# Wait to load page
time.sleep(SCROLL_PAUSE_TIME)


    
while True:
    try:
        my_element = driver.find_element(By.XPATH, f"/html/body/shreddit-app/dsa-transparency-modal-provider/search-dynamic-id-cache-controller/div/div/div[1]/div[2]/main/div/reddit-feed/faceplate-tracker[{i}]/post-consume-tracker/div/faceplate-tracker/h2/a")
    except selenium.common.exceptions.NoSuchElementException as e:
        break
    i+=1
    print(my_element.text)
    


driver.quit()
