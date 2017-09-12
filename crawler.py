import sys, os, time, requests, queue, re
import pickle
from lxml import html
from parser import parse


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

def analyze(url):
    global q
    global s
    global t
    try:
        page = requests.get(url, allow_redirects=True, timeout=1)
    except:
        return
    tree = html.fromstring(page.content.decode('utf-8'))

    all_links = tree.xpath('//a/@href')
    regex = re.compile(r'https:\/\/[\s\S]+-[\w]{12}\?source=[\s\S]+')
    re_tag = re.compile(r'https:\/\/[\w|.]+\/(tag|topic|tagged)\/[\s\S]+')

    for href in all_links:
        if re_tag.search(href):
            t.append(href)
            continue
        if regex.search(href):
            link, uid = concat(href)
            if not link or not uid: continue
            if uid in d:
                pack = d[uid]
                if pack["timestamp"] == 0: continue #must be on queue still
                elif (time.time()-d[uid]["timestamp"])>172800: # if crawled more than two day ago we can crawl again
                    pack["timestamp"] = 0 #put on queue
                    d[uid] = pack
                    q.put(uid)
                continue
            else:
                pack = {}
                pack["url"] = link
                pack["timestamp"] = 0 #must be on queue still
                pack["pk"] = -1 #pk not assigned yet
                d[uid] = pack
                q.put(uid)
        else:
            continue

# def getArticles():
#     global q
#     global s
#     global t
#     try:
#         resp = requests.get(
#             url="https://medium.com/_/api/topics/9d34e48ecf94/stream",
#             params={
#                 "limit": "1000",
#             },timeout=60
#         )
#     except requests.exceptions.RequestException:
#         print('topic stream Request failed')
#
#     resp_data = json.loads(resp.content.decode('utf-8')[16:])
#
#     if (resp_data['success']):
#         try:
#             article_data=resp_data['payload']['references']['Post']
#         except:
#             print("comment key error with url: "+url, file=sys.stderr)
#             return None
#
#         for key, value in article_data.items():
#             if key in d:
#                 continue
#             try:
#                 url = value['uniqueSlug']
#             except:
#                 print("id key error with url: "+url, file=sys.stderr)
#                 continue
#             try:
#                 domain = value['domain']
#             except:
#                 domain = "medium.com"




def loadvaribles():
    try:
        f1 = open('cache/variable/queue.pckl', 'rb')
        f2 = open('cache/variable/dict.pckl', 'rb')
        f3 = open('cache/variable/pk.pckl', 'rb')
    except FileNotFoundError:
        print("variable file not found", file=sys.stderr)
        ans = input("Are your sure you want to initalize everything?(y/n)")
        if ans != 'y':
            sys.exit()

        return None, None, None
    q = pickle.load(f1)
    f1.close()
    d = pickle.load(f2)
    f2.close()
    pk = pickle.load(f3)
    f3.close()
    return q, d, pk


def savevariable(q, d, pk):
    f = open('cache/variable/queue.pckl', 'wb')
    pickle.dump(q, f)
    f.close()
    f = open('cache/variable/dict.pckl', 'wb')
    pickle.dump(d, f)
    f.close()
    f = open('cache/variable/pk.pckl', 'wb')
    pickle.dump(pk, f)
    f.close()

def savepk(pk):
    f = open('cache/variable/pk.pckl', 'wb')
    pickle.dump(pk, f)
    f.close()


def checkpk(pk):
    os.system("echo 'checking PK......' ")
    os.system("ls cache/html/"+str(pk//1000)+"/ | grep '"+str(pk)+"_*.html' ")


def create_directory(n):
    os.system('mkdir cache/html/'+n+'/')
    os.system('mkdir cache/json/'+n+'/')
    os.system('mkdir data/article/'+n+'/')
    os.system('mkdir data/comment/'+n+'/')
    os.system('mkdir data/truth/'+n+'/')


if __name__ == '__main__':

    create_directory(str(0))

    l, d, pk = loadvaribles()
    q = queue.Queue()
    if not d:
        print("variable caches not found", file=sys.stderr)
        d = {} #dictionary of uid and url
        pk = 1
    else:
        print(pk)
        checkpk(pk)
        for item in l:
            q.put(item)

    t = [] #topic list to crawl

    logtime = str(time.time())
    os.system('mkdir cache/logs/'+logtime+'/')
    sys.stdout = open('cache/logs/'+logtime+'/std.log', 'w')
    sys.stderr = open('cache/logs/'+logtime+'/error.log', 'w')

    while True: #sleep for a while and load updates
        t.append('https://medium.com')
        t.append('https://medium.com/topic/popular')
        t.append('https://medium.com/topic/editors-picks')
        t.append('https://medium.com/topic/world')
        t.append('https://medium.com/topic/future')
        # getArticles()

        while len(t) > 0:
            savepk(pk)
            analyze(t.pop())

            while not q.empty():
                savepk(pk)
                time.sleep(10)
                uid = q.get()
                d[uid]["timestamp"] = time.time() #give a timestamp that crawled
                url = d[uid]["url"]
                if d[uid]["pk"] == -1:  # first time crawl
                    d[uid]["pk"] = pk
                    analyze(url)
                    parse(url,pk,uid)
                    pk += 1
                else: # crawl again
                    analyze(url)
                    stored_pk = d[uid]["pk"]
                    parse(url,stored_pk,uid, False)

                sys.stdout.flush()
                sys.stderr.flush()
                if pk%1000 == 0:
                    create_directory(str(pk//1000))

                savevariable(list(q.queue), d, pk)

        print("falling sleep...", file=sys.stderr)
        sleep(60*10) # wait ten minutes to restart
