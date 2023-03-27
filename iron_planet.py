import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import sqlite3

# set environmental path first
path = "chromedriver"
driver = webdriver.Chrome(path)
# sqlite3 db
con = sqlite3.connect('iron_planet.db')
cur = con.cursor()
cur.execute("CREATE TABLE ended_bid (id INTEGER PRIMARY KEY, name TEXT, winningbid TEXT, metersread TEXT)")

def index():
    '''Index page of all machines.'''
    # all find element methods priority https://stackoverflow.com/questions/38716233/in-selenium-webdriver-which-is-better-in-terms-of-performance-linktext-or-css
    page = "https://www.ironplanet.com/Caterpillar-Crawler+Tractor?m=Cat&mode=1&sm=1&mf=1"
    # hard coded ... there are 69 pages in total, last page contains irrelevant stuff
    for i in range(68):
        driver.get(page)
        page = driver.find_element(By.XPATH, "//a[@class='sj sr_pagination s_top']").get_attribute('href')
        print(driver.title)
        elements = driver.find_elements(By.CSS_SELECTOR, 'a[itemprop="url"]')
        hrefs = []
        results = []
        for e in elements:
            href = e.get_attribute("href")
            hrefs.append(href)
        for i in range(len(hrefs)):
            print(i)
            href = hrefs[i]
            driver.get(href)
            name = driver.find_element(By.CSS_SELECTOR,'h1.itemdesc[itemprop=name]').get_attribute('textContent')
            winning_bid = driver.find_element(By.CSS_SELECTOR,"span.IP_Price").text
            data = driver.find_elements(By.CSS_SELECTOR,"span.itemPropValue")
            meters_read = "NONE"
            for d in data:
                if d.text.endswith("Hours"):
                    meters_read = d.text
            results.append((name, winning_bid, meters_read))
            print("name: ", name)
            print("winning_bid: ", winning_bid)
            print("meters_read: ", meters_read)
            cur.execute("INSERT INTO ended_bid (name, winningbid, metersread) VALUES (?, ?, ?)", (name, winning_bid, meters_read))
            con.commit()
    return results
        

def login():
    '''Need to login before viewing the machine details.'''
    driver.get("https://www.ironplanet.com/jsp/acct/login-form.jsp?kwtag=navbar")
    driver.find_element(By.NAME, "!login").send_keys("yunkai@umich.edu")
    driver.find_element(By.NAME, "!password").send_keys("1234")
    driver.find_element(By.NAME, "submit2").click()
    print("Logged in")

login()
results = index()
cur.close()