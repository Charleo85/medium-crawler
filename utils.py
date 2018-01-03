import requests, re, json, random, sys, os
import datetime, sys, time
import pickle, queue
from lxml import html
from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def write_html(data, filename='sample.html'):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(data.content.decode('utf-8'))

def write_json(data, filename='sample.json'):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(json.dumps(data))

def write_obj(data, filename='sample.obj'):
    with open(filename, 'wb') as f:
        pickle.dump(data, f)

def load_obj(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)

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
def match_username(url):
    m = re.match(pattern, url)
    return m.group(1)

def parse_uid(href):
    n = len(href)
    for i in range(n):
        if (href[n-1-i] == '-'):
            return href[n-i:n]

def load_page(session, href, timeout=15, allow_redirects=True, params=None, headers=None, max_retry=3):
    try: page = session.get(href, allow_redirects=allow_redirects, timeout=timeout, params=params, headers=headers)
    except Exception as e:
        logger("error in loading page: "+str(e)+href, file=sys.stderr)
        return None
    if page.status_code != 200:
        return page
    else:
        logger("getting status code: " + page.status_code+ "with url: "+href, file=sys.stderr)
        time.sleep(30)
        return load_page(session, href, timeout=timeout, allow_redirects=allow_redirects, params=params, headers=headers,
                        max_retry=max_retry-1)


def load_html(session, href, params=None, headers=None):
    page = load_page(session, href, params=params, headers=headers)
    if page is None: return None
    try:
        tree = html.fromstring(page.content.decode('utf-8'))
    except Exception as e:
        print("error in loading html tree: "+str(e)+href, file=sys.stderr)
        return None
    return tree

def load_json(session, href, params=None, headers=None):
    resp = load_page(session, href, params=params, headers=headers)
    if resp is None: return None
    try:
        resp_data = json.loads(resp.content.decode('utf-8')[16:])
    except Exception as e:
        print("error in loading json: "+str(e)+href, file=sys.stderr)
        return None

    if 'success' in resp_data: return resp_data.get('payload', None)

    print("json request not successful with url: "+href, file=sys.stderr)
    return None

def config_logger():
    logtime = datetime.datetime.fromtimestamp(int(time.time())).strftime('%Y-%m-%d-%H-%M-%S')
    print('started parser logger at ' + logtime)
    os.system('mkdir -p logs/'+logtime+'/')
    sys.stdout = open('logs/'+logtime+'/std.log', 'w')
    sys.stderr = open('logs/'+logtime+'/error.log', 'w')

def flush_logger():
    sys.stdout.flush()
    sys.stderr.flush()

def logger(message, file=sys.stdout):
    print(message, file=file)
    flush_logger()


def login():
    login_filepath = './objects/login.obj'
    if os.path.exists(login_filepath): return load_obj(login_filepath)

    mail_address = "one2infinity1900@gmail.com"
    password = "afishUVA@1900G"
    driver = webdriver.Chrome('./chromedriver')
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
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@data-action='google-auth']")))
    element.click()
    WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, "//button[@title='Notifications']")))

    headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36"}
    s = requests.session()
    s.headers.update(headers)
    for cookie in driver.get_cookies():
        c = {cookie['name']: cookie['value']}
        s.cookies.update(c)
    driver.close()
    write_obj(s, 'login.obj')
    return s
