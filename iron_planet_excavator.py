import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import sqlite3
import time

# set environmental path first
path = "chromedriver"
driver = webdriver.Chrome(path)
# sqlite3 db
con = sqlite3.connect('iron_planet_excavator.db')
cur = con.cursor()
cur.execute("DROP TABLE bids")
cur.execute("CREATE TABLE bids (id INTEGER PRIMARY KEY, name TEXT, winningbid TEXT, metersread TEXT)")

def index():
    '''Index page of all machines.'''
    for i in range(9):
        start = i * 60
        page = "https://www.ironplanet.com/jsp/s/search.ips?pstart="+ str(start) +"&mode=1&&c=3&l2=USA&sm=1&m=Cat&mf=1"
        driver.get(page)
        # print(page)

        time.sleep(4)
        elements = driver.find_elements(By.CSS_SELECTOR, 'a[itemprop="url"]')
        hrefs = []
        for e in elements:
            href = e.get_attribute("href")
            # print(href)
            hrefs.append(href)

        for href in hrefs:
            driver.get(href)
            name = driver.find_element(By.CSS_SELECTOR,'h1.itemdesc[itemprop=name]').get_attribute('textContent')
            winning_bid = driver.find_element(By.CSS_SELECTOR,"span.IP_Price").text
            data = driver.find_elements(By.CSS_SELECTOR,"span.itemPropValue")
            meters_read = "NONE"
            for d in data:
                if d.text.endswith("Hours"):
                    meters_read = d.text
            print("name: ", name)
            print("winning_bid: ", winning_bid)
            print("meters_read: ", meters_read)
            cur.execute("INSERT INTO bids (name, winningbid, metersread) VALUES (?, ?, ?)", (name, winning_bid, meters_read))
            con.commit()
    

def login():
    '''Need to login before viewing the machine details.'''
    driver.get("https://www.ironplanet.com/jsp/acct/login-form.jsp?kwtag=navbar")
    driver.find_element(By.NAME, "!login").send_keys("yunkai@umich.edu")
    driver.find_element(By.NAME, "!password").send_keys("1234")
    driver.find_element(By.NAME, "submit2").click()
    print("Logged in")

login()
index()
cur.close()
driver.close()
