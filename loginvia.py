from concurrent.futures import ThreadPoolExecutor
import requests
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
import time
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import pyotp

def login_via(subList,stt):
    try:
        if stt <= 8:
            stt = stt
        else:
            stt = stt%8
        if stt >= 4 :
            b = 500
        else:
            b = 0
        if stt <=3 :
            a = stt*500
        else:
            a = (stt%4)*500
        NewlistVia = []
        with open('scanfb.txt', 'r') as f:
            reader = csv.reader(f, delimiter= '|', lineterminator = '\n')
            for i in reader:
                NewlistVia.append(i)
        options = ChromeOptions()
        options.add_argument('--disable-notifications')
        options.add_argument('--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1')
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

        driver.set_window_rect(a,b,400,500)
        Taikhoan = subList[0]
        Matkhau = subList[1]
        FA = subList[2]
        totp = pyotp.TOTP(str(FA).replace(' ','')).now()
        driver.get('https://m.facebook.com/login')
        try:
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div[6]/div[1]/div/div[2]/div[4]/button[2]")))
            driver.find_element((By.XPATH, "/html/body/div[1]/div/div[6]/div[1]/div/div[2]/div[4]/button[2]")).click()
        except:pass
        wait = WebDriverWait(driver,2)  # Add this line
        men_menu = wait.until(EC.visibility_of_element_located((By.ID, "m_login_email")))
        driver.find_element(By.ID, 'm_login_email').send_keys(Taikhoan)

        wait.until(EC.presence_of_element_located((By.ID, "m_login_password")))
        driver.find_element(By.ID, 'm_login_password').send_keys(Matkhau)
        driver.find_element(By.NAME, 'login').click()
        men_menu = wait.until(EC.visibility_of_element_located((By.ID, "approvals_code")))
        driver.find_element(By.ID, 'approvals_code').send_keys(totp)
        driver.find_element(By.ID, 'checkpointSubmitButton-actual-button').click()
        driver.find_element(By.ID, 'checkpointSubmitButton-actual-button').click()
                
        try:
            driver.find_element(By.ID, 'checkpointSubmitButton-actual-button').click()
            driver.find_element(By.ID, 'checkpointSubmitButton-actual-button').click()
            driver.find_element(By.ID, 'checkpointSubmitButton-actual-button').click()
        except NoSuchElementException:
            pass
        # After successful login
        cookies = driver.get_cookies()
        with open('cookie.txt', 'w') as file:
            for cookie in cookies:
                file.write(f"{cookie['name']}={cookie['value']}; ")
        time.sleep(5)
        driver.close()
        try:
            time.sleep(5)
            driver.find_element_by_xpath('/html/body/div[1]/div/div[3]/from/div/article/div[1]/table/tbody/tr/td/button').click()
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div[3]/from/div/article/div[2]/table/tbody/tr/td[2]/button")))
            driver.find_element_by_xpath('/html/body/div[1]/div/div[3]/from/div/article/div[2]/table/tbody/tr/td[2]/button').click()
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div[3]/from/div/article/div[1]/table/tbody/tr/td/button")))
        except:
            pass
        WebDriverWait(driver, 25).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div[2]/div/div[1]/div[2]/div/a")))
        driver.get('https://m.facebook.com/login')
    except Exception as e:
        print(e)
        
list_via = []
with open('scanfb.txt', 'r') as f:
    reader = csv.reader(f, delimiter= '|', lineterminator ='\n')
    for i in reader:
        list_via.append(i)
Newlist_via = [ele for ele in list_via if ele != []]
soluong = 1
List_stt = []
for stt in range(len(Newlist_via)):
    List_stt.append(stt)
with ThreadPoolExecutor(max_workers=soluong) as executor:
    executor.map(login_via, Newlist_via,List_stt)
    executor.shutdown(wait=True)