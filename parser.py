from lxml import html
from lxml import etree
from insert2DB import *
from utils import *
from selenium import webdriver

def parse_fullcomment(href):
    try:
        page = requests.get(href, allow_redirects=True, timeout=1)
        tree = html.fromstring(page.content.decode('utf-8'))
    except Exception as e:
        print("error in loading comment page: "+str(e)+href, file=sys.stderr)
        return

    content = ''

    section = tree.xpath('//section/div[@class="section-content"]')
    for sec in section:
        body = sec.xpath('./div[contains(@class,"section-inner")]/*')
        # parse_para(body, uid, articleID)

    return content

def parse_comment(uid, url, articleID=None):
    try:
        resp = requests.get(
            url="https://medium.com/_/api/posts/"+uid+"/responsesStream",
            allow_redirects=True, timeout=10
        )
    except Exception as e:
        print("error in making comment requests: "+str(e) + uid, file=sys.stderr)
        return
    # print(uid)
    resp_data = json.loads(resp.content.decode('utf-8')[16:])

    if (resp_data['success']):
        try:
            comm_data=resp_data['payload']['references']['Post']
            user_data=resp_data['payload']['references']['User']
        except KeyError:
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
            content = ''
            media_id = ''
            try:
                comment_full = value['previewContent']['isFullContent']
                comment_paras = value['previewContent']['bodyModel']['paragraphs']
                comment_id = value['id']
                creator_id = value['creatorId']
                numberLikes = value['virtuals']['totalClapCount']
                media_id = value['inResponseToMediaResourceId']
                timestamp = convert_unixtime(value['latestPublishedAt'])
            except KeyError:
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
            except KeyError:
                print("comment user key error with url: "+url, file=sys.stderr)


            if comment_full:
                for comm_para in comment_paras:
                    content+=comm_para['text']
            else:
                unique_slug = value['uniqueSlug']
                content = parse_fullcomment('https://medium.com/@'+username+'/'+unique_slug)

            if media_id != '': #assume one media_id only to one sentences
                commment_dict[media_id] = comment_id

            comment_map[comment_id] = {
                    'mediumID': comment_id,
                    'content': content,
                    'authorMediumID': creator_id,
                    'time': timestamp,
                    'corrStnID': '',
                    'numberLikes':numberLikes,
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
                    except Exception as e:
                        print("id key error with url: "+url, file=sys.stderr)

                    for comm_para in comment_paras:
                        comment+=comm_para['text']

                    comment_map[comment_id]['corrStnID'] = sentence_id

        for _, commentObj in comment_map.items():
            saveComment(commentObj)
        return count
    else:
        print("bad request with url: "+url, file=sys.stderr)


def parse_article(tree, url, uid, articleID=None):

    try:
        article_name = tree.xpath('//h1/text()')[0]
    except Exception as e:
        try:
            article_name = tree.xpath('//h1/*/text()')[0]
        except Exception as e:
            try:
                article_name = tree.xpath('//p[@class="graf graf--p graf--leading"]/*/text()')[0]
                # print(article_name)
            except Exception as e:
                print("bad format cannot parse the title: "+url, file=sys.stderr)
                article_name = ""

    try:
        authorNode = tree.xpath('//*[contains(@class,"link link--darken link--darker")]')[0]
        authorName = authorNode.xpath('./text()')[0]
        authorMediumID = authorNode.xpath('./@data-user-id')[0]
        username = matchUsername(authorNode.xpath('./@href')[0])
        # print(username)
        bioNode = tree.xpath('//*[contains(@class,"postMetaInline u-noWrapWithEllipsis")]/text()')
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
    except Exception as e:
        print("bad format in parsing author: "+str(e)+url, file=sys.stderr)
        return False


    try:
        tags = tree.xpath('//ul[@class="tags tags--postTags tags--borderless"]')[0]
        timestamp = convert_utctime(tree.xpath('//time/@datetime')[0])
        likeNode = tree.xpath('//button[@data-action="show-recommends"]/text()')
        if len(likeNode) == 0 :
            numberLikes = 0
        else:
            numberLikes = convert_count(likeNode[0])
    except Exception as e:
        print("bad format in parsing timestamp, tag or like: "+str(e)+url, file=sys.stderr)
        return False

    tags_arr = []
    for tag in tags.xpath('./*/a/text()'):
        tags_arr.append(tag)

    highlight = ''
    try:
        highlights = tree.xpath('//span[starts-with(@class,"markup--quote")]/text()')
        if len(highlights) > 0:
            highlight = highlights[0]
            if len(highlights) > 1:
                print("multiple hightlights exists"+url, file=sys.stderr)
    except Exception as e:
        print("bad format in parsing hightlight: "+str(e)+url, file=sys.stderr)

    saveArticle({
        'mediumID': uid,
        'authorMediumID': authorMediumID,
        'highlight' : '',
        'title': article_name,
        'time': timestamp,
        'tag': tags_arr,
        'numberLikes': numberLikes
    }, articleID, authorID)

    section = tree.xpath('//section/div[@class="section-content"]')
    for sec in section:
        body = sec.xpath('./div[contains(@class,"section-inner")]/*')
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

        saveSentence({
            'content': sentence,
            'id': key,
            'articleMediumID': uid
        }, articleID)


def parse(href, driver, id=None, articleID=None, tree=None):
    if not id:
        uid = parse_uid(href)
    else:
        uid = id
    # print(uid)
    if tree is None:
        try:
            driver.get(href)
            page = driver.page_source
            tree = html.fromstring(page)
        except Exception as e:
            print("error in loading article page: "+str(e)+href, file=sys.stderr)
            return

    if parse_article(tree, href, uid, articleID):
        parse_comment(uid, href, articleID)

    # parse_image(page, href, count, pk)


if __name__ == '__main__':
    if len(sys.argv) == 3:
        parse(sys.argv[1], int(sys.argv[2]))
    else:
        # parse("https://medium.com/tag/artificial-intelligence", 0)
        # parse("https://medium.freecodecamp.com/big-picture-machine-learning-classifying-text-with-neural-networks-and-tensorflow-d94036ac2274", 0)
        # parse("https://backchannel.com/i-work-i-swear-a649e0eb697d", 0) #815
        # sys.stdout = open('cache/logs/'+logtime+'/std.log', 'w')
        #
        # sys.stderr = open('output.txt', 'w')
        initdb()
        # parse("https://medium.com/@OrganicsByLee/sprouted-grains-and-the-harvesting-process-8fa878bea2ee")
        driver = webdriver.Chrome('./chromedriver')
        driver = login(driver)
        parse('https://medium.com/@beyondtherobot/my-real-life-superpower-c2a9b309cf7', driver)
