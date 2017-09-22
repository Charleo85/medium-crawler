import sys, os, time, requests, queue, re
import pickle
from lxml import html
from parser import parse
from action2ArticleTable import existArticle
from insert2DB import *

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

regex = re.compile(r'https:\/\/[\s\S]+-[\w]{12}\?source=[\s\S]+')
re_tag = re.compile(r'https:\/\/[\w|.]+\/(tag|topic|tagged)\/[\s\S]+')

def analyze(url, tree=None):
    global q
    global t

    if tree is None:
        try:
            page = requests.get(url, allow_redirects=True, timeout=1)
        except:
            return
        tree = html.fromstring(page.content.decode('utf-8'))

    all_links = tree.xpath('//a/@href')

    for href in all_links:
        if re_tag.search(href):
            t.put(href)
            print(href, file=sys.stdout)
            continue
        if regex.search(href):
            link, uid = concat(href)
            if not link or not uid: continue
            if existArticle(uid):
                continue
            else:
                articleID = saveSratchArticle(uid);
                q.put((uid, link, articleID))
            # if uid in d:
            #     pack = d[uid]
            #     if pack["timestamp"] == 0: continue #must be on queue still
            #     elif (time.time()-d[uid]["timestamp"])>172800: # if crawled more than two day ago we can crawl again
            #         pack["timestamp"] = 0 #put on queue
            #         d[uid] = pack
            #         q.put(uid)
            #     continue
            # else:
            #     pack = {}
            #     pack["url"] = link
            #     pack["timestamp"] = 0 #must be on queue still
            #     pack["pk"] = -1 #pk not assigned yet
            #     d[uid] = pack
            #     q.put(uid)
        else:
            continue

    return tree

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

if __name__ == '__main__':
    initdb()

    q = queue.Queue() #uid queue to analyze
    t = queue.Queue() #topic list to crawl

    logtime = datetime.datetime.fromtimestamp(int(time.time())).strftime('%Y-%m-%d-%H-%M-%S')
    print(logtime)
    os.system('mkdir -p logs/'+logtime+'/')
    sys.stdout = open('logs/'+logtime+'/std.log', 'w')
    sys.stderr = open('logs/'+logtime+'/error.log', 'w')

    while True: #sleep for a while and load updates
        t.put('https://medium.com')
        t.put('https://medium.com/topics')
        t.put('https://medium.com/topic/popular')
        t.put('https://medium.com/topic/editors-picks')
        t.put('https://medium.com/topic/world')
        t.put('https://medium.com/topic/future')
        t.put('https://medium.com/topic/education')
        t.put('https://medium.com/topic/family')
        #https://medium.com/topics

        while not t.empty():
            analyze(t.get())

            while not q.empty():
                time.sleep(10)
                uid, url, articleID = q.get()
                tree = analyze(url)
                parse(url, uid, articleID, tree)
                # d[uid]["timestamp"] = time.time() #give a timestamp that crawled
                # url = d[uid]["url"]
                # if d[uid]["pk"] == -1:  # first time crawl
                #     d[uid]["pk"] = pk
                #     analyze(url)
                #     parse(url,pk,uid)
                # else: # crawl again
                #     analyze(url)
                #     stored_pk = d[uid]["pk"]
                #     parse(url,stored_pk,uid, False)

                sys.stdout.flush()
                sys.stderr.flush()

        # print("falling sleep...", file=sys.stderr)
        # sleep(60*10) # wait ten minutes to restart
