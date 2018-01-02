from insert2DB import *
from utils import *

def parse_comment_tags(tag_dict_arr):
    tags_arr = []
    if tag_dict_arr:
        for tag_dict in tag_dict_arr:
            tags_arr.append(tag_dict['name'])
    return tags_arr

def parse_comment(uid, session):
    href = "https://medium.com/_/api/posts/"+uid+"/responsesStream"
    resp_data = load_json(session, href)
    if resp_data is None: return

    references = resp_data['payload']['references']
    paging = resp_data['payload']['paging']
    parse_stream(uid, session, href, references)

    while 'next' in paging:
        resp_data = load_json(session, href, params=paging['next'])
        if resp_data is None: break
        references = resp_data['payload']['references']
        paging = resp_data['payload']['paging']
        parse_stream(uid, session, href, references)

def parse_stream(uid, session, href, references):
    if 'Post' in references and 'User' in references:
        comm_data = references['Post']
        user_data = references['User']
    else: return

    commment_dict = {}
    comment_map = {}
    # parse all comments
    for self_article_mediumID, value in comm_data.items():
        if exist_article(self_article_mediumID): continue
        try:
            comment_full = value['previewContent']['isFullContent']
            comment_paras = value['previewContent']['bodyModel']['paragraphs']
            creator_id = value['creatorId']
            numLikes = value['virtuals']['totalClapCount']
            num_responses = value['virtuals']['responsesCreatedCount']
            recommends = value['virtuals']['recommends']
            tag_arr = parse_comment_tags(value['virtuals']['tags'])
            comment_title = value['title']
            media_id = value['inResponseToMediaResourceId']
            corr_article_mediumID = value['inResponseToPostId']
            timestamp = convert_unixtime(value['latestPublishedAt'])
        except KeyError:
            print("id key error with url: "+href, file=sys.stderr)
            continue

        try:
            username = user_data[creator_id]['username']
            authorID = saveAuthor({
                'name': user_data[creator_id]['name'],
                'mediumID': creator_id,
                'username': username,
                'bio': user_data[creator_id]['bio']
            })
        except KeyError:
            print("comment author key error with url: "+href, file=sys.stderr)

        self_articleID = saveArticle({
            'mediumID': self_article_mediumID,
            'authorMediumID': creator_id,
            'recommends' : recommends,
            'title': comment_title,
            'time': timestamp,
            'tags': tag_arr,
            'numLikes': numLikes
        }, authorID=authorID)

        if comment_full:
            for comm_para in comment_paras:
                saveSentence({
                    'content': comm_para['text'],
                    'id': comm_para['name'],
                    'articleID': self_articleID
                })
        else:
            unique_slug = value['uniqueSlug']
            comment_href = 'https://medium.com/@'+username+'/'+unique_slug
            parse_sentence(self_article_mediumID, self_articleID, comment_href, session)

        parse_highlight(self_article_mediumID, self_articleID, session)

        if num_responses > 0: parse_comment(self_article_mediumID, session)

        if media_id != '': commment_dict[media_id] = self_article_mediumID

        comment_map[self_article_mediumID] = {
                'selfArticleID': self_articleID,
                'corrArticleMediumID':corr_article_mediumID,
                'corrHighlightID':-1
        }

    # parse quote
    if 'MediaResource' in references and 'Quote' in references:
        media_data=references['MediaResource']
        quote_data=references['Quote']
        for mediaResourceId, media in media_data.items():
            if 'mediumQuote' in media:
                media_id = str(mediaResourceId)
                self_article_mediumID = commment_dict.get(media_id)
                if self_article_mediumID is None: continue
                    # print(mediaResourceId)

                quote = quote_data[media['mediumQuote']['quoteId']]

                try:
                    start = quote['startOffset']
                    end = quote['endOffset']
                except KeyError:
                    print("quote key error with url: "+href, file=sys.stderr)
                    contine

                content = ''
                corrStnMediumIDs = []
                for para in quote['paragraphs']:
                    content += para['text']
                    corrStnMediumIDs.append(para['name'])

                content = content[start:end]
                corr_article_mediumID = quote['postId']

                highlightID = exist_highlight(corr_article_mediumID, content)
                if highlightID == -1:
                    highlightID = saveHighlight({
                        'content': content,
                        'corrStnMediumIDs': corrStnMediumIDs,
                        'numLikes': -1,
                        'articleMediumID': corr_article_mediumID
                    })

                comment_map[self_article_mediumID]['corrHighlightID'] = highlightID

    for _, commentObj in comment_map.items(): saveComment(commentObj)

def parse_highlight(uid, articleID, session):
    href = 'https://medium.com/p/'+uid+'/quotes'
    resp_data = load_json(session, href)
    if resp_data is None: return

    for highlight in resp_data['payload']['value']:
        try:
            start = highlight['startOffset']
            end = highlight['endOffset']
            numLikes = highlight['count']
        except KeyError:
            print("highlight key error with url: "+href, file=sys.stderr)
            contine

        content = ''
        corrStnMediumIDs = []
        for para in highlight['paragraphs']:
            content += para['text']
            corrStnMediumIDs.append(para['name'])

        content = content[start:end]
        saveHighlight({
            'content': content,
            'corrStnMediumIDs': corrStnMediumIDs,
            'numLikes': numLikes,
            'articleMediumID': uid
        }, articleID)

def parse_sentence(uid, articleID, href, session):
    tree = load_html(session, href)
    if tree is None: return

    section = tree.xpath('//section/div[@class="section-content"]')
    for sec in section:
        body = sec.xpath('./div[contains(@class,"section-inner")]/*')
        parse_para(body, uid, articleID)

def parse_para(body, uid, articleID):
    for para in body:
        sentence = para.text_content()
        try: key = para.xpath('@id')[0]
        except:
            sub_body = para.xpath('./*')
            parse_para(sub_body, uid, articleID)
            continue
        if sentence == "" or not key: continue

        saveSentence({
            'content': sentence,
            'id': key,
            'articleID': articleID
        })


def parse(href, session, uid=None, articleID=None, tree=None):
    if not uid:
        uid = parse_uid(href)

    parse_comment(uid, session)


if __name__ == '__main__':
    if len(sys.argv) == 3:
        parse(sys.argv[1], int(sys.argv[2]))
    else:
        # parse("https://medium.com/tag/artificial-intelligence", 0)
        # parse("https://medium.freecodecamp.com/big-picture-machine-learning-classifying-text-with-neural-networks-and-tensorflow-d94036ac2274", 0)
        # parse("https://backchannel.com/i-work-i-swear-a649e0eb697d", 0) #815
        # parse("https://medium.com/@OrganicsByLee/sprouted-grains-and-the-harvesting-process-8fa878bea2ee")
        sys.stdout = open('logs/std.log', 'w')
        sys.stderr = open('logs/err.log', 'w')

        initdb()
        session = load_obj('login.obj')
        # session = login()
        # parse('https://timeline.com/it-was-sex-all-the-time-at-this-1800s-commune-with-anyone-you-wanted-and-none-of-the-guilt-c7ea4734e9ca', session)
        parse('https://medium.com/@beyondtherobot/my-real-life-superpower-c2a9b309cf7', session)
