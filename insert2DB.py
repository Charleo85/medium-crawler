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
	authorMediumID = 'mediumID'#author['mediumID']

	authorExistFlag = existAuthor(authorMediumID)

	if authorExistFlag:
		print("exist author\t", authorName)
		authorID = queryAuthorIDbyMediumID(authorMediumID)
	else:
		authorID = insertAuthor(authorName, authorMediumID)


####insert article into article table
def saveArticle(article):
	authorMediumID = article['authorMediumID']
	# authorName = article['author']

	articleMediumID = article['mediumID']
	articleTitle = article['title']
	articleContent = article['content']
	tag = article['tag']
	numberLikes = article['numberLikes']
	### the format of time is "1999-01-08 04:05:06"
	unixtime = time.mktime(time.strptime(article['time'], '%Y-%m-%dT%H:%M:%S.%fZ'))
	articleTime = datetime.datetime.fromtimestamp(int(unixtime)).strftime('%Y-%m-%d %H:%M:%S')
	#author name not unique??? query by mediumid
	authorID = queryAuthorIDbyMediumID(authorMediumID)

	articleID = insertArticle(articleMediumID, articleTitle, articleContent, authorID, tag, articleTime, numberLikes)


###insert sentence into stn table
def saveSentence(sentence):
	stnName = sentence['id']
	stnContent = sentence['content']
	articleMediumID = sentence['articleMediumID']
	articleID = queryArticleIDbyMediumID(articleMediumID)
	stnID = insertSTN(stnName, articleID, stnContent)

###insert comment into comment table
def saveComment(comment):
	commentName = ''
	commentContent = comment['content']
	authorMediumID = comment['authorMediumID']
	commentTime = datetime.datetime.fromtimestamp(int(comment['time'])/1000).strftime('%Y-%m-%d %H:%M:%S')
	numLikes = -1
	corrStnID = comment['corrStnID']
	articleMediumID = comment['articleMediumID']

	authorID = queryAuthorIDbyMediumID(authorMediumID)
	# corrStnID = queryStnIDbyStnName(corrStnName)
	articleID = queryArticleIDbyMediumID(articleMediumID)

	insertComment(commentName, commentContent, authorID, commentTime, numLikes, corrStnID, articleID)
