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
    # paging = resp_data['payload']['paging']
    # while 'next' in paging:
    #     paging_params = href+paging['next']
    #     resp_paging_data = load_json(session, href, params=paging_params)
    #     references
    #     paging = resp_paging_data['payload']['paging']
    if 'Post' in references and 'User' in references:
        comm_data = references['Post']
        user_data = references['User']
    else: return

    commment_dict = {}
    comment_map = {}
    # parse all comments
    for key, value in comm_data.items():
        try:
            comment_full = value['previewContent']['isFullContent']
            comment_paras = value['previewContent']['bodyModel']['paragraphs']
            self_article_mediumID = value['id']
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

        if savedArticle(self_article_mediumID): continue

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

        if num_responses > 0: parse_comment(self_article_mediumID, session)

        parse_highlight(self_article_mediumID, self_articleID, session)

        if media_id != '': #assume one media_id only to one sentences
            commment_dict[media_id] = self_article_mediumID

        comment_map[self_article_mediumID] = {
                'selfArticleID': self_articleID,
                'corrArticleMediumID':corr_article_mediumID,
                'corrHighlightID':-1
        }

    # parse quote
    # value['inResponseToMediaResourceId'] matches value['MediaResource'][key]
    # "mediumQuote" not none
    quote_count=0
    if 'MediaResource' in references and 'Quote' in references:
        media_data=references['MediaResource']
        quote_data=references['Quote']
        for mediaResourceId, media in media_data.items():
            if 'mediumQuote' in media:
                quote_count += 1
                self_article_mediumID = commment_dict.get(str(mediaResourceId))
                if self_article_mediumID is None:
                    print(self_article_mediumID)
                    continue

                quote = quote_data[media['mediumQuote']['quoteId']]

                content = ''
                corrStnMediumIDs = []
                for para in quote['paragraphs']:
                    content += para['text']
                    corrStnMediumIDs.append(para['name'])

                content = content[quote['startOffset']:quote['endOffset']]
                corr_article_mediumID = quote['postId']

                highlightID = saveHighlight({
                    'content': content,
                    'corrStnMediumIDs': corrStnMediumIDs,
                    'numLikes': -1,
                    'articleMediumID': corr_article_mediumID
                })

                # comment_map[self_article_mediumID]['corrArticleMediumID'] = corr_article_mediumID
                comment_map[self_article_mediumID]['corrHighlightID'] = highlightID

    for _, commentObj in comment_map.items(): saveComment(commentObj)


# def parse_article(tree, url, uid, articleID=None, session=None):
#
#     try:
#         article_name = tree.xpath('//h1/text()')[0]
#     except Exception as e:
#         try:
#             article_name = tree.xpath('//h1/*/text()')[0]
#         except Exception as e:
#             try:
#                 article_name = tree.xpath('//p[@class="graf graf--p graf--leading"]/*/text()')[0]
#             except Exception as e:
#                 print("bad format cannot parse the title: "+url, file=sys.stderr)
#                 article_name = ""
#
#     try:
#         authorNode = tree.xpath('//*[contains(@class,"link link--darken link--darker")]')[0]
#         authorName = authorNode.xpath('./text()')[0]
#         authorMediumID = authorNode.xpath('./@data-user-id')[0]
#         username = match_username(authorNode.xpath('./@href')[0])
#         bioNode = tree.xpath('//*[contains(@class,"postMetaInline u-noWrapWithEllipsis")]/text()')
#         if bioNode: bio = bioNode[0]
#         else: bio = ''
#         authorID = saveAuthor({
#             'name': authorName,
#             'mediumID': authorMediumID,
#             'username': username,
#             'bio': bio
#         })
#     except Exception as e:
#         print("bad format in parsing author: "+str(e)+url, file=sys.stderr)
#         return False
#
#     try:
#         tags = tree.xpath('//ul[@class="tags tags--postTags tags--borderless"]')[0]
#         timestamp = convert_utctime(tree.xpath('//time/@datetime')[0])
#         likeNode = tree.xpath('//button[@data-action="show-recommends"]/text()')
#         if len(likeNode) == 0: numLikes = 0
#         else: numLikes = convert_count(likeNode[0])
#     except Exception as e:
#         print("bad format in parsing timestamp, tag or like: "+str(e)+url, file=sys.stderr)
#         return False
#
#     tags_arr = []
#     for tag in tags.xpath('./*/a/text()'): tags_arr.append(tag)
#
#     articleID = saveArticle({
#         'mediumID': uid,
#         'authorMediumID': authorMediumID,
#         'recommends' : -1,
#         'title': article_name,
#         'time': timestamp,
#         'tags': tags_arr,
#         'numLikes': numLikes
#     }, articleID, authorID)
#
#     parse_sentence(uid, articleID, url, session, tree=tree)
#     parse_highlight(uid, articleID, session)
#     return True;

def parse_highlight(uid, articleID, session):
    href = 'https://medium.com/p/'+uid+'/quotes'
    resp_data = load_json(session, href)
    if resp_data is None: return

    for highlight in resp_data['payload']['value']:
        content = ''
        corrStnMediumIDs = []
        for para in highlight['paragraphs']:
            content += para['text']
            corrStnMediumIDs.append(para['name'])

        content = content[highlight['startOffset']:highlight['endOffset']]
        print(corrStnMediumIDs, highlight['count'], uid, articleID)
        saveHighlight({
            'content': content,
            'corrStnMediumIDs': corrStnMediumIDs,
            'numLikes': highlight['count'],
            'articleMediumID': uid
        }, articleID)

def parse_sentence(uid, articleID, href, session, tree=None):
    if tree is None:
        tree = load_html(session, href)
        if tree is None: return

    section = tree.xpath('//section/div[@class="section-content"]')
    for sec in section:
        body = sec.xpath('./div[contains(@class,"section-inner")]/*')
        parse_para(body, uid, articleID)

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
            'articleID': articleID
        })


def parse(href, session, uid=None, articleID=None, tree=None):
    if not uid:
        uid = parse_uid(href)

    # print(uid)
    if tree is None:
        tree = load_html(session, href)
        if tree is None: return

    # if parse_article(tree, href, uid, articleID=articleID, session=session):
    parse_comment(uid, session)

    # parse_image(page, href, count, pk)


if __name__ == '__main__':
    if len(sys.argv) == 3:
        parse(sys.argv[1], int(sys.argv[2]))
    else:
        # parse("https://medium.com/tag/artificial-intelligence", 0)
        # parse("https://medium.freecodecamp.com/big-picture-machine-learning-classifying-text-with-neural-networks-and-tensorflow-d94036ac2274", 0)
        # parse("https://backchannel.com/i-work-i-swear-a649e0eb697d", 0) #815
        # parse("https://medium.com/@OrganicsByLee/sprouted-grains-and-the-harvesting-process-8fa878bea2ee")
        # sys.stdout = open('logs/std.log', 'w')
        # sys.stderr = open('logs/err.log', 'w')

        initdb()
        session = load_obj('login.obj')
        # session = login()
        # parse('https://timeline.com/it-was-sex-all-the-time-at-this-1800s-commune-with-anyone-you-wanted-and-none-of-the-guilt-c7ea4734e9ca', session)
        parse('https://medium.com/@beyondtherobot/my-real-life-superpower-c2a9b309cf7', session)
