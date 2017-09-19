import psycopg2
import datetime, sys, time
from config import config
from action2AuthorTable import *
from action2ArticleTable import *
from action2StnTable import *
from action2CommentTable import *


def initdb():
	createAuthorTable()
	createSTNTable()
	createCommentTable()
	createArticleTable()

###insert author if not exist into the author table
def saveAuthor(author):
	authorName = author['name']
	authorMediumID = author['mediumID']
	username = author['username']
	bio = author['bio']

	authorExistFlag = existAuthor(authorMediumID)

	if not authorExistFlag:
		authorID = insertAuthor(authorName, authorMediumID, username, bio)


	# # print("exist author\t", authorName)
	# authorID = queryAuthorIDbyMediumID(authorMediumID)

####insert article into article table
def saveArticle(article, articleID=None, authorID=None):
	authorMediumID = article['authorMediumID']
	# authorName = article['author']

	articleMediumID = article['mediumID']
	articleTitle = article['title']
	articleContent = article['content']
	tag = article['tag']
	numberLikes = article['numberLikes']
	articleTime = article['time']

	if authorID is None:
		authorID = queryAuthorIDbyMediumID(authorMediumID)

	if articleID:
		updateArticle(articleMediumID, articleTitle, articleContent, authorID, tag, articleTime, numberLikes, articleID)
	else:
		articleID = insertArticle(articleMediumID, articleTitle, articleContent, authorID, tag, articleTime, numberLikes)


def saveSratchArticle(articleMediumID):
	articleID = insertArticle(articleMediumID)
	return articleID

###insert sentence into stn table
def saveSentence(sentence, articleID=None):
	stnName = sentence['id']
	stnContent = sentence['content']
	articleMediumID = sentence['articleMediumID']
	if articleID is None:
		articleID = queryArticleIDbyMediumID(articleMediumID)
	stnID = insertSTN(stnName, articleID, stnContent)

###insert comment into comment table
def saveComment(comment):
	commentName = ''
	commentContent = comment['content']
	authorMediumID = comment['authorMediumID']
	commentTime = comment['time']
	numberLikes = -1
	corrStnID = comment['corrStnID']
	articleMediumID = comment['articleMediumID']

	authorID = queryAuthorIDbyMediumID(authorMediumID)
	articleID = queryArticleIDbyMediumID(articleMediumID)

	insertComment(commentName, commentContent, authorID, commentTime, numberLikes, corrStnID, articleID)
