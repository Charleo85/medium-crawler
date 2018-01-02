import psycopg2
from config import config
from action2AuthorTable import *
from action2ArticleTable import *
from action2StnTable import *
from action2CommentTable import *
from action2HighlightTable import *

def initdb():
	createAuthorTable()
	createSTNTable()
	createCommentTable()
	createArticleTable()
	createHighlightTable()

###insert author if not exist into the author table
def saveAuthor(author):
	authorName = author['name']
	authorMediumID = author['mediumID']
	username = author['username']
	bio = author['bio']

	# authorExistFlag = existAuthor(authorMediumID)
	authorID = queryAuthorIDbyMediumID(authorMediumID)
	# print("exist author\t", authorName)

	if authorID == -1: authorID = insertAuthor(authorName, authorMediumID, username, bio)

	return authorID


####insert article into article table
def saveArticle(article, articleID=None, authorID=None):
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

def savedArticle(articleMediumID):
	return existArticle(articleMediumID)

def saveSratchArticle(articleMediumID):
	if existArticle(articleMediumID): return -1
	articleID = insertArticle(articleMediumID)
	return articleID

###insert sentence into stn table
def saveSentence(sentence):
	stnMediumID = sentence['id']
	stnContent = sentence['content']
	articleID = sentence['articleID']
	stnID = insertSTN(stnMediumID, articleID, stnContent)

###insert comment into comment table
def saveComment(comment):
	selfArticleID = comment['selfArticleID']
	corrHighlightID = comment['corrHighlightID']
	corrArticleMediumID = comment['corrArticleMediumID']
	corrArticleID = queryArticleIDbyMediumID(corrArticleMediumID)

	insertComment(selfArticleID, corrHighlightID, corrArticleID)

###insert highlight into highlight table
def saveHighlight(highlight, corrArticleID=None):
	content = highlight['content']
	numLikes = highlight['numLikes']
	corrStnMediumIDs = highlight['corrStnMediumIDs']

	if corrArticleID is None:
		articleMediumID = highlight['articleMediumID']
		corrArticleID = queryArticleIDbyMediumID(articleMediumID)

	highlightID = insertHighlight(content, numLikes, corrArticleID, corrStnMediumIDs)
	return highlightID

def existHighlight(articleMediumID):
	return existHighlight(articleMediumID)
