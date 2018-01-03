from parser import parse, parse_topicStream
from insert2DB import *
from utils import *
from selenium import webdriver

def parse_topic_dict(topic_dict, topic_mediumID = None):
    global t
    if topic_mediumID is None: topic_mediumID = topic_dict['topicId']
    if exist_topic(topic_mediumID): return
    t.put(topic_mediumID)
    try: name = topic_dict['name']
    except KeyError: print("topic key error with url: "+href, file=sys.stderr)
    description = topic_dict.get('description', '')
    save_topic({
        'name':name,
        'description':description,
        'mediumID': topic_mediumID
    })
    for topics_dict in topic_dict.get('relatedTopics', []):
        parse_topic_dict(topics_dict)


def parse_topic(href, session):
    resp_data = load_json(session, href, headers={"accept": "application/json"})
    if resp_data is None: return

    references = resp_data['references']
    parse_topicStream(references, session)

    topics = references.get('Topic', None)
    if topics is None: topics = resp_data.get('topic', {})
    for topic_mediumID, value in topics.items():
        parse_topic_dict(value, topic_mediumID)

    paging = resp_data.get('paging', {})
    while 'next' in paging and 'path' in paging:
        href='https://medium.com'+paging['path']
        resp_data = load_json(session, href, params=paging['next'])
        if resp_data is None: break
        references = resp_data['references']
        paging = resp_data['paging']
        parse_topicStream(references, session)

if __name__ == '__main__':
    initdb()
    session = login()
    config_logger()

    t = queue.Queue() #topic list to crawl
    parse_topic('https://medium.com/topics', session)

    while not t.empty():
        topic_id = t.get()
        href = 'https://medium.com/_/api/topics/'+topic_id+'/stream'
        parse_topic(href, session)

    while True:
        print('start to revisit all topics...')
        topic_ids = fetch_all_topic_mediumID()
        for topic_id in topic_ids:
            href = 'https://medium.com/_/api/topics/'+topic_id+'/stream'
            parse_topic(href, session)
        print('finished one loop, taking a rest...')
        time.sleep(5*60)
