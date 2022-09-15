from time import sleep
import requests
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

class Bot:
    def __init__(self, noheadless=0):
        chrome_options = Options()
        if noheadless == 0:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument('log-level=3')
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36 Edg/89.0.774.75")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get("https://my.keepsolid.com/")

    def login(self, email, password):
        self.driver.find_element(By.CSS_SELECTOR, "input#input-25").send_keys(email)
        self.driver.find_element(By.CSS_SELECTOR, "input#input-26").send_keys(password)
        self.driver.find_element(By.CSS_SELECTOR, ".secondary > .x-button--wrap").click()
        global PHPSESSID_COOKIE
        PHPSESSID_COOKIE = self.driver.get_cookie("PHPSESSID")
        while not PHPSESSID_COOKIE:
            PHPSESSID_COOKIE = self.driver.get_cookie("PHPSESSID")
            sleep(0.5)
        self.driver.close()
        return PHPSESSID_COOKIE['value']

def check_sessid_valid(token):
    res = requests.get('https://my.keepsolid.com/api/account/config/devices/', cookies={'PHPSESSID': token})
    if res.status_code == 200:
        return True
    else:
        return False

def generate_wg(token, uuid, country):
    res = requests.get('https://my.keepsolid.com/api/account/config/?deviceId=' + uuid + '&region=' + country + '&protocol=wireguard&platform=win', cookies={'PHPSESSID': token})
    jsonres = json.loads(res.text)
    wg = jsonres['download_data']
    print(wg)
    return wg

def find_uuid(token, devicename):
    res = requests.get('https://my.keepsolid.com/api/account/config/devices/', cookies={'PHPSESSID': token})
    devicelist = json.loads(res.text)
    uuid = ""
    for d in devicelist:
        if d['name'] == devicename:
            uuid = d['uuid']
            break
    if uuid == "":
        print("specified device not found, choosing first")
        uuid = devicelist[0]['uuid']
    return uuid

def fetchwg(email, password, countrycode, devicename, sessionid, noheadless=0):
    sessid = ""
    if check_sessid_valid(sessionid) == False:
        print("Given session id invalid, logging in and generating new")
        ks = Bot(noheadless)
        sessid = ks.login(email, password)
    else:
        print("Given session id valid, no need to log in")
        sessid = sessionid
    
    device_uuid = find_uuid(sessid, devicename)
    print("If device name found, uuid for \"" + devicename + "\": " + device_uuid)
    wg = generate_wg(sessid, device_uuid, countrycode)

    return {"wg": wg, "sessid": sessid}     # Return wg and sessid in dict
