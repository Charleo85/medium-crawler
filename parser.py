from lxml import html
from lxml import etree
import requests, re, json, random, sys, os
from insert2DB import *

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


def parse_fullcomment(href):
    try:
        page = requests.get(href, allow_redirects=True, timeout=1)
    except:
        return
    tree = html.fromstring(page.content.decode('utf-8'))

    body = tree.xpath('//div[@class="section-inner sectionLayout--insetColumn"]/*')
    content = ''
    for para in body:
        sentence = para.text_content()
        content += sentence + ' '
    return content

def parse_comment(page, uid, url, articleID=None):
    try:
        resp = requests.get(
            url="https://medium.com/_/api/posts/"+uid+"/responsesStream",
            allow_redirects=True, timeout=1
        )
    except:
        print("Cannot make comment requests" + uid, file=sys.stderr)
        return
    # print(uid)
    resp_data = json.loads(resp.content.decode('utf-8')[16:])

    if (resp_data['success']):
        try:
            comm_data=resp_data['payload']['references']['Post']
            user_data=resp_data['payload']['references']['User']
        except:
            print("comment key error with url: "+url, file=sys.stderr)
            return None

        count = 0
        commment_dict = {}
        comment_map = {}
        # parse all comments
        for key, value in comm_data.items():
            count += 1

            comment_id = ''
            creator_id = ''
            comment = ''
            media_id = ''
            try:
                comment_full = value['previewContent']['isFullContent']
                comment_paras = value['previewContent']['bodyModel']['paragraphs']
                comment_id = value['id']
                creator_id = value['creatorId']
                media_id = value['inResponseToMediaResourceId']
                timestamp = convert_unixtime(value['latestPublishedAt'])
            except:
                print("id key error with url: "+url, file=sys.stderr)
                count-=1
                continue

            if comment_id == uid:
                count-=1
                continue

            try:
                username = user_data[creator_id]['username']
                saveAuthor({
                    'name': user_data[creator_id]['name'],
                    'mediumID': creator_id,
                    'username': username,
                    'bio': user_data[creator_id]['bio']
                })
            except:
                return None

            if comment_full:
                for comm_para in comment_paras:
                    comment+=comm_para['text']
            else:
                unique_slug = value['uniqueSlug']
                comment = parse_fullcomment('https://medium.com/@'+username+'/'+unique_slug)

            if media_id != '': #assume one media_id only to one sentences
                commment_dict[media_id] = comment_id

            comment_map[comment_id] = {
                    'content': comment,
                    'authorMediumID': creator_id,
                    'time': timestamp,
                    'corrStnID': '',
                    'articleMediumID':uid
            }

        # parse quote
        # value['inResponseToMediaResourceId'] matches value['MediaResource'][key]
        # "mediumQuote" not none
        quote_count=0
        quote_data=None
        media_data=None
        try:
            media_data=resp_data['payload']['references']['MediaResource']
            quote_data=resp_data['payload']['references']['Quote']
        except KeyError:
            # print("no quote: "+url, file=sys.stderr)
            pass

        if media_data and quote_data:
            for mediaResourceId, media in media_data.items():
                if 'mediumQuote' in media:
                    quote_count += 1
                    media_id = str(mediaResourceId)
                    comment_id = commment_dict.get(media_id)

                    quote_id = media['mediumQuote']['quoteId']
                    quote = quote_data[quote_id]
                    creator_id = ''
                    comment = ''
                    sentence_id = ''
                    try:
                        comment_paras = quote['paragraphs']
                        sentence_id = quote['paragraphs'][0]['name']
                        creator_id = quote['userId']
                    except:
                        print("id key error with url: "+url, file=sys.stderr)

                    for comm_para in comment_paras:
                        comment+=comm_para['text']

                    comment_map[comment_id]['corrStnID'] = sentence_id

        for _, commentObj in comment_map.items():
            saveComment(commentObj)

        return count
    else:
        print("bad request with url: "+url, file=sys.stderr)


def parse_article(page, url, uid, articleID=None):
    tree = html.fromstring(page.content.decode('utf-8'))

    try:
        article_name = tree.xpath('//h1/text()')[0]
    except:
        try:
            article_name = tree.xpath('//h1/*/text()')[0]
        except:
            try:
                article_name = tree.xpath('//p[@class="graf graf--p graf--leading"]/*/text()')[0]
                # print(article_name)
            except:
                print("bad format cannot parse the title: "+url, file=sys.stderr)
                article_name = ""

    try:
        authorNode = tree.xpath('//*[starts-with(@class,"link link link--darken link--darker")]')[0]
        authorName = authorNode.xpath('./text()')[0]
        authorMediumID = authorNode.xpath('./@data-user-id')[0]
        username = matchUsername(authorNode.xpath('./@href')[0])
        # print(username)
        bioNode = tree.xpath('//*[starts-with(@class,"postMetaInline u-noWrapWithEllipsis")]/text()')
        if bioNode:
            bio = bioNode[0]
        else:
            bio = ''
        authorID = saveAuthor({
            'name': authorName,
            'mediumID': authorMediumID,
            'username': username,
            'bio': bio
        })
    except:
        print("bad format cannot parse the author: "+url, file=sys.stderr)
        return False


    try:
        tags = tree.xpath('//ul[@class="tags tags--postTags tags--borderless"]')[0]
        timestamp = convert_utctime(tree.xpath('//time/@datetime')[0])
        numberLikes = convert_count(tree.xpath('//button[@data-action="show-recommends"]/text()')[0])
    except:
        print("bad format cannot parse the article: "+url, file=sys.stderr)
        return False

    tags_arr = []
    for tag in tags.xpath('./*/a/text()'):
        tags_arr.append(tag)

    # try:
    #     highlights = tree.xpath('//span[starts-with(@class,"markup--quote")]/text()')
    #     print(highlights)
    #     for high in highlights:
    #         art['highlights'].append(high)
    # except:
    #     pass

    saveArticle({
        'mediumID': uid,
        'authorMediumID': authorMediumID,
        'content' : '', # to remove
        'title': article_name,
        'time': timestamp,
        'tag': tags_arr,
        'numberLikes': numberLikes
    }, articleID, authorID)

    section = tree.xpath('//section/div[@class="section-content"]')
    for sec in section:
        body = sec.xpath('./div[starts-with(@class,"section-inner")]/*')
        parse_para(body, uid, articleID)

    return True;


def parse_para(body, uid, articleID):
    for para in body:
        sentence = para.text_content()
        try:
            key = para.xpath('@id')[0]
        except:
            sub_body = para.xpath('./*')
            parse_para(sub_body, uid, articleID)
            continue
        if sentence == "" or not key: continue
        # art['sentences'].append({key : sentence})
        # art['content'] += sentence + ' '

        saveSentence({
            'content': sentence,
            'id': key,
            'articleMediumID': uid
        }, articleID)


def parse_uid(href):
    n = len(href)
    for i in range(n):
        if (href[n-1-i] == '-'):
            return href[n-i:n]

def parse(href, id=None, articleID=None):
    if not id:
        uid = parse_uid(href)
    else:
        uid = id
    try:
        page = requests.get(href, allow_redirects=True, timeout=1)
    except:
        return
    # if not first:
    #     # try:
    #     os.system('rm data/*/'+str(pk//1000)+'/'+str(pk)+'_*')
    #     os.system('rm data/article/'+str(pk//1000)+'/'+str(pk)+'.json')
    #     print("again")
    #     # except:
    #     #     print("fail to rm", file=sys.stderr)
    #     #     return

    if parse_article(page, href, uid, articleID):
        parse_comment(page, uid, href, articleID)
    # parse_image(page, href, count, pk)


if __name__ == '__main__':
    if len(sys.argv) == 3:
        parse(sys.argv[1], int(sys.argv[2]))
    else:
        # parse("https://medium.com/tag/artificial-intelligence", 0)
        # parse("https://medium.freecodecamp.com/big-picture-machine-learning-classifying-text-with-neural-networks-and-tensorflow-d94036ac2274", 0)
        # parse("https://backchannel.com/i-work-i-swear-a649e0eb697d", 0) #815
        # sys.stdout = open('cache/logs/'+logtime+'/std.log', 'w')

        # sys.stderr = open('output.txt', 'w')
        initdb()
        parse("https://healthcareinamerica.us/storing-medical-records-on-the-ethereum-blockchain-e088f19c9fca")
