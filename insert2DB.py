import psycopg2
from db.config import config
from db.action2AuthorTable import *
from db.action2ArticleTable import *
from db.action2StnTable import *
from db.action2CommentTable import *
from db.action2HighlightTable import *
from db.action2TopicTable import *
from db.action2ParagraphTable import *

from utils import *

def initdb():
	createAuthorTable()
	createSTNTable()
	createParagraphTable()
	createCommentTable()
	createArticleTable()
	createHighlightTable()
	createTopicTable()

###insert author if not exist into the author table
def save_author(author):
	authorName = author['name']
	authorMediumID = author['mediumID']
	username = author['username']
	bio = author['bio']

	# authorExistFlag = existAuthor(authorMediumID)
	authorID = queryAuthorIDbyMediumID(authorMediumID)
	# print("exist author\t", authorName)

	if authorID == -1: authorID = insertAuthor(authorName, authorMediumID, username, bio)

	return authorID

###insert author if not exist into the author table
def save_topic(topic):
	name = topic['name']
	mediumID = topic['mediumID']
	description = topic['description']

	topicID = insertTopic(name, mediumID, description)
	return topicID

def exist_topic(mediumID):
	return queryTopicIDbyMediumID(mediumID) != -1

def fetch_all_topic_mediumID():
	mediumIDs = [result[0] for result in queryAllTopicMediumID()]
	return mediumIDs

####insert article into article table
def save_article(article, articleID=None, authorID=None):
	authorMediumID = article['authorMediumID']
	articleMediumID = article['mediumID']
	articleTitle = article['title']
	recommends = article['recommends']
	tags = article['tags']
	numLikes = article['numLikes']
	articleTime = article['time']

	if authorID is None: authorID = queryAuthorIDbyMediumID(authorMediumID)

	# if articleID:
	# 	updateArticle(articleMediumID, articleTitle, recommends, tags, articleTime, numLikes, articleID, authorID)
	# else:
	# 	articleID = queryArticleIDbyMediumID(articleMediumID)
	# 	if articleID != -1:
	# 		updateArticle(articleMediumID, articleTitle, recommends, tags, articleTime, numLikes, articleID, authorID)
	# 	else:
	# 		articleID = insertArticle(articleMediumID, articleTitle, recommends, authorID, tags, articleTime, numLikes)
	articleID = insertArticle(articleMediumID, articleTitle, recommends, authorID, tags, articleTime, numLikes)

	return articleID

def exist_article(articleMediumID):
	return existArticle(articleMediumID)

def saveSratchArticle(articleMediumID):
	if existArticle(articleMediumID): return -1
	articleID = insertArticle(articleMediumID)
	return articleID

###insert sentence into stn table
def save_sentence(sentence):
	stnMediumID = sentence['id']
	stnContent = sentence['content']
	articleID = sentence['articleID']
	stnID = insertSTN(stnMediumID, articleID, stnContent)

###insert comment into comment table
def save_comment(comment):
	selfArticleID = comment['selfArticleID']
	corrHighlightID = comment['corrHighlightID']
	corrArticleMediumID = comment['corrArticleMediumID']
	corrArticleID = queryArticleIDbyMediumID(corrArticleMediumID)

	insertComment(selfArticleID, corrHighlightID, corrArticleID)

###insert highlight into highlight table
def save_highlight(highlight, corrArticleID=None):
	content = highlight['content']
	numLikes = highlight['numLikes']
	corrStnMediumIDs = highlight['corrStnMediumIDs']

	if corrArticleID is None:
		articleMediumID = highlight['articleMediumID']
		corrArticleID = queryArticleIDbyMediumID(articleMediumID)

	highlightID = insertHighlight(content, numLikes, corrArticleID, corrStnMediumIDs)
	return highlightID

def exist_highlight(articleMediumID, content):
	corrArticleID = queryArticleIDbyMediumID(articleMediumID)
	return existHighlight(corrArticleID, content)

def migrate_highlight():
	for highlightID, highlightContent, articleID, corrStnMediumIDs in queryAllHighlights():
		mediumID = corrStnMediumIDs[1:-1]

		paragraphID, paragraphContent = queryParagraphIDbyMediumID(mediumID, articleID)
		if paragraphID is None and paragraphContent is None:
			print("cannot find paragraph")
			continue
		# match = re.finditer(highlightContent, paragraphContent)
		# match_value = next(match, None)
		startOffset, endOffset = -1,-1
		startOffset = paragraphContent.find(highlightContent)
		endOffset = startOffset + len(highlightContent)
		# if match_value:
		# 	startOffset, endOffset = match_value.span()
		# else:
		# 	print(highlightContent, paragraphContent)
		# print(highlightID, paragraphID, startOffset, endOffset)
		updateHighlight(highlightID, paragraphID, startOffset, endOffset)

if __name__ == '__main__':
	migrate_highlight()
