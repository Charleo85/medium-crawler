from insert2DB import *
from utils import *
from nltk.tokenize import sent_tokenize

def parse_comment_tags(tag_dict_arr):
    tags_arr = []
    if tag_dict_arr:
        for tag_dict in tag_dict_arr:
            tags_arr.append(tag_dict['name'])
    return tags_arr

def parse_quotes(quote, href, articleID, aricleMediumID=None):
    try:
        start = quote['startOffset']
        end = quote['endOffset']
        paras = quote['paragraphs']
    except KeyError:
        print("quote key error with url: "+href, file=sys.stderr)
        return None, None, None, None

    if len(paras) > 1 or len(paras) == 0: print("highlight has multiple pargraph with url: "+href, file=sys.stderr)
    para = paras[0]
    paragraph_content = para['text']
    content = paragraph_content[start:end]

    corrStnMediumID = para['name']
    corrParagraphID = exist_paragraph(corrStnMediumID, paragraph_content, articleID, aricleMediumID)
    if corrParagraphID == -1:
        print("no corresponding paragraph is found: "+href, file=sys.stderr)
        corrParagraphID = save_paragraph({
            'content': paragraph_content,
            'id': corrStnMediumID,
            'articleID': articleID,
            'prevParagraphID': -2
        })
        print("saved under paragraphid: %d"%(corrParagraphID), file=sys.stderr)


    return content, corrParagraphID, start, end

def parse_paragraph(uid, articleID, href, session):
    tree = load_html(session, href)
    if tree is None: return

    prevParagraphID = -1
    section = tree.xpath('//section/div[@class="section-content"]')
    for sec in section:
        body = sec.xpath('./div[contains(@class,"section-inner")]/*')
        prevParagraphID = parse_para(body, uid, articleID, prevParagraphID)

def parse_para(body, uid, articleID, prevParagraphID):
    for para in body:
        paragraph = para.text_content()
        try: key = para.xpath('@id')[0]
        except:
            sub_body = para.xpath('./*')
            prevParagraphID = parse_para(sub_body, uid, articleID, prevParagraphID)
            continue

        if paragraph == '' or not key: continue

        paragraphID = save_paragraph({
            'content': paragraph,
            'id': key,
            'articleID': articleID,
            'prevParagraphID': prevParagraphID
        })
        prevParagraphID = paragraphID

        parse_sentence(paragraph, paragraphID, articleID)

    return prevParagraphID

def parse_sentence(paragraph, paragraphID, articleID):
    sentences = sent_tokenize(paragraph)
    prevSentenceID = -1
    for sentence in sentences:
        sentenceID = save_sentence({
            'prevSentenceID':prevSentenceID,
            'content': sentence,
            'paragraphID': paragraphID,
            'articleID': articleID
        })
        prevSentenceID = sentenceID

def parse_highlight(uid, articleID, session):
    href = 'https://medium.com/p/'+uid+'/quotes'
    resp_data = load_json(session, href)
    if resp_data is None: return

    for highlight in resp_data['value']:
        content, corrParagraphID, startOffset, endOffset = parse_quotes(highlight, href, articleID)
        if content is None: continue

        # highlightID = exist_highlight(None, content, articleID)
        # if highlightID != -1: continue
        # if highlight['userId'] != "anon": continue
        # print(highlight)

        save_highlight({
            'content': content,
            'corrParagraphID': corrParagraphID,
            'numLikes': highlight.get('count', -1),
            'articleMediumID': uid,
            'startOffset': startOffset,
            'endOffset': endOffset
        }, articleID)

def parse_responseStream(uid, session, href, references):
    if 'Post' in references and 'User' in references:
        comm_data = references['Post']
        user_data = references['User']
    else: return

    commment_dict = {}
    comment_map = {}
    paragraph_map = {}
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
            authorID = save_author({
                'name': user_data[creator_id]['name'],
                'mediumID': creator_id,
                'username': username,
                'bio': user_data[creator_id]['bio']
            })
        except KeyError: print("comment author key error with url: "+href, file=sys.stderr)

        self_articleID = save_article({
            'mediumID': self_article_mediumID,
            'authorMediumID': creator_id,
            'recommends' : recommends,
            'title': comment_title,
            'time': timestamp,
            'tags': tag_arr,
            'numLikes': numLikes
        }, authorID=authorID)

        if comment_full:
            prevParagraphID = -1
            for comm_para in comment_paras:
                content = comm_para['text']
                paragraph_mediumID = comm_para['name']
                paragraphID = save_paragraph({
                    'content': content,
                    'id': paragraph_mediumID,
                    'articleID': self_articleID,
                    'prevParagraphID': prevParagraphID
                })
                prevParagraphID = paragraphID

                parse_sentence(content, paragraphID, self_articleID)

        else:
            unique_slug = value['uniqueSlug']
            comment_href = 'https://medium.com/@'+username+'/'+unique_slug
            parse_paragraph(self_article_mediumID, self_articleID, comment_href, session)

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
                corr_article_mediumID = quote['postId']

                content, corrParagraphID, startOffset, endOffset = parse_quotes(quote, href, None, corr_article_mediumID)
                if content is None: continue

                highlightID = exist_highlight(corr_article_mediumID, content)
                if highlightID == -1:
                    highlightID = save_highlight({
                        'content': content,
                        'corrParagraphID': corrParagraphID,
                        'numLikes': -1,
                        'articleMediumID': corr_article_mediumID,
                        'startOffset': startOffset,
                        'endOffset': endOffset
                    })

                comment_map[self_article_mediumID]['corrHighlightID'] = highlightID

    for _, comment_obj in comment_map.items(): save_comment(comment_obj)

def parse_comment(uid, session):
    href = "https://medium.com/_/api/posts/"+uid+"/responsesStream"
    resp_data = load_json(session, href)
    if resp_data is None: return

    references = resp_data['references']
    paging = resp_data['paging']
    parse_responseStream(uid, session, href, references)

    while 'next' in paging:
        resp_data = load_json(session, href, params=paging['next'])
        if resp_data is None: break
        references = resp_data['references']
        paging = resp_data['paging']
        parse_responseStream(uid, session, href, references)

def parse_topicStream(references, session):
    for mediumID, value in references.get('Post', {}).items():
        if not exist_article(mediumID):
            parse_comment(mediumID, session)

def parse(href, session, uid=None, articleID=None, tree=None):
    if not uid: uid = parse_uid(href)
    parse_comment(uid, session)


if __name__ == '__main__':
    if len(sys.argv) == 3:
        parse(sys.argv[1], int(sys.argv[2]))
    else:
        # sys.stdout = open('logs/std.log', 'w')
        # sys.stderr = open('logs/err.log', 'w')

        initdb()
        session = load_obj('./objects/login.obj')
        # session = login()
        # parse('https://timeline.com/it-was-sex-all-the-time-at-this-1800s-commune-with-anyone-you-wanted-and-none-of-the-guilt-c7ea4734e9ca', session)
        parse('https://medium.com/message/37-up-and-coming-creative-job-titles-754fd5488688', session)
