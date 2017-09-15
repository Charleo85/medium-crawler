import sys, os, time, requests, queue, re
import pickle
from lxml import html
from parser import parse
from action2ArticleTable import queryArticleIDbyMediumID

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

if __name__ == '__main__':

    q = queue.Queue() #uid queue to analyze
    t = [] #topic list to crawl

    logtime = str(time.time())
    # os.system('mkdir cache/logs/'+logtime+'/')
    # sys.stdout = open('cache/logs/'+logtime+'/std.log', 'w')
    # sys.stderr = open('cache/logs/'+logtime+'/error.log', 'w')

    while True: #sleep for a while and load updates
        t.append('https://medium.com')
        t.append('https://medium.com/topic/popular')
        t.append('https://medium.com/topic/editors-picks')
        t.append('https://medium.com/topic/world')
        t.append('https://medium.com/topic/future')
        # getArticles()

        while len(t) > 0:
            analyze(t.pop())

            while not q.empty():
                time.sleep(10)
                uid = q.get()

                queryArticleIDbyMediumID(uid)
                d[uid]["timestamp"] = time.time() #give a timestamp that crawled
                url = d[uid]["url"]
                if d[uid]["pk"] == -1:  # first time crawl
                    d[uid]["pk"] = pk
                    analyze(url)
                    parse(url,pk,uid)
                else: # crawl again
                    analyze(url)
                    stored_pk = d[uid]["pk"]
                    parse(url,stored_pk,uid, False)

                # sys.stdout.flush()
                # sys.stderr.flush()

        print("falling sleep...", file=sys.stderr)
        sleep(60*10) # wait ten minutes to restart
