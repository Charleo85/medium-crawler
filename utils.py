import requests, re, json, random, sys, os
import datetime, sys, time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def write_html(data, filename='sample.html'):
    output = open(filename, 'w', encoding='utf-8')
    output.write(data.content.decode('utf-8'))
    output.close()

def write_json(data, filename='sample.json'):
    output = open(filename, 'w', encoding='utf-8')
    output.write(json.dumps(data))
    output.close()

### the format of time is "1999-01-08 04:05:06"
def convert_unixtime(unixtime):
    return datetime.datetime.fromtimestamp(int(unixtime)/1000).strftime('%Y-%m-%d %H:%M:%S')

def convert_utctime(utctime):
	unixtime = time.mktime(time.strptime(utctime, '%Y-%m-%dT%H:%M:%S.%fZ'))
	return datetime.datetime.fromtimestamp(int(unixtime)).strftime('%Y-%m-%d %H:%M:%S')

def convert_count(text):
    unit = text[-1:]
    if unit == 'K':
        return int(float(text[:-1])*1000)
    elif unit == 'M':
        return int(float(text[:-1])*1000000)
    elif unit == 'B':
        return int(float(text[:-1])*1000000000)
    return int(text)

pattern = re.compile(r'https:\/\/[\s\S]+\/@(.+)\?source=[\s\S]+')
def matchUsername(url):
    m = re.match(pattern, url)
    return m.group(1)

def parse_uid(href):
    n = len(href)
    for i in range(n):
        if (href[n-1-i] == '-'):
            return href[n-i:n]

def login(driver):
    mail_address = "one2infinity1900@gmail.com"
    password = "afishUVA@1900G"
    driver.get('https://www.google.com/accounts/Login')
    driver.find_element_by_id("identifierId").send_keys(mail_address)
    driver.find_element_by_id("identifierNext").click()
    element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//input[@type='password']")))
    element.send_keys(password)
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'passwordNext')))
    element.click()
    driver.get('https://medium.com')
    driver.find_element(By.XPATH, "//a[contains(.,'Sign in')]").click()
    element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//button[@data-action='google-auth']")))
    element.click()
    WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, "//button[@title='Notifications']")))

    return driver
