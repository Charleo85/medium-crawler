from parser import parse
from insert2DB import *
from utils import *
from selenium import webdriver

def concat(href):
    n = len(href)
    for i in range(n):
        if (href[n-1-i] == '?'):
            href = href[0:n-i-1]
            m = len(href)
            for j in range(m):
                if (href[m-1-j] == '-'):
                    return href, href[m-j: m]
    return None, None

re_article = re.compile(r'https:\/\/[\s\S]+-[\w]{12}\?source=[\s\S]+')
re_tag = re.compile(r'https:\/\/[\w|.]+\/(tag|topic|tagged)\/[\s\S]+')

def analyze(url, session):
    global q
    global t

    s = set()
    tree = load_html(session, url)
    if tree is None: return

    all_links = tree.xpath('//a/@href')

    for href in all_links:
        if re_tag.search(href): #find topic links
            t.add(href)
            continue
        elif re_article.search(href): #find article links
            link, uid = concat(href)
            if not link or not uid or uid in s: continue
            s.add(uid)
            if exist_article(uid): continue #already crawled article
            else: q.put((uid, link))

    return tree

if __name__ == '__main__':
    login_filepath = './objects/login.obj'
    topic_filepath = './objects/topic.obj'
    initdb()
    if os.path.exists(login_filepath): session = load_obj(login_filepath)
    else: session = login()

    q = queue.Queue() #uid queue to analyze
    t = set() #topic list to crawl

    logtime = datetime.datetime.fromtimestamp(int(time.time())).strftime('%Y-%m-%d-%H-%M-%S')
    print('login and started parser at ' + logtime)
    os.system('mkdir -p logs/'+logtime+'/')
    sys.stdout = open('logs/'+logtime+'/std.log', 'w')
    sys.stderr = open('logs/'+logtime+'/error.log', 'w')

    if os.path.exists(topic_filepath):
        t = load_obj(topic_filepath)
    else:
        t.add('https://medium.com')
        t.add('https://medium.com/topics')
    while True: #sleep for a while and load updates
        for topic in list(t):
            analyze(topic, session)
            while not q.empty():
                time.sleep(10)
                uid, url = q.get()
                print(url, uid)
                # parse(url, session, uid)

                sys.stdout.flush()
                sys.stderr.flush()

        write_obj(t, topic_filepath)
        print("taking a rest...", file=sys.stderr)
        time.sleep(60*3) # wait ten minutes to restart
