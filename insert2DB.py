import psycopg2

from config import config
from action2AuthorTable import *

from action2ArticleTable import *
from action2StnTable import *
from action2CommentTable import *

###insert author if not exist into the author table
def saveAuthor(author):
	authorName = author['name']
	authorMediumID = author['mediumID']

	authorExistFlag = existAuthor(authorName)
	authorID = -1

	if authorExistFlag:
		print("exist author\t", authorName)
		# what's the need for queryAuthorIDbyAuthorName
		authorID = queryAuthorIDbyAuthorName(authorName)
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
	articleTime = article['time']

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
	commentTime = comment['time']
	numLikes = -1
	corrStnName = comment['corrStnName']
	articleMediumID = comment['articleMediumID']

	authorID = queryAuthorIDbyMediumID(authorMediumID)
	corrStnID = queryStnIDbyStnName(corrStnName)
	articleID = queryArticleIDbyMediumID(articleMediumID)

	insertComment(commentName, commentContent, authorID, commentTime, numLikes, corrStnID, articleID)
