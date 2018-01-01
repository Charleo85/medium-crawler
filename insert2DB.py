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
	# createHighlightTable()

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
	highlight = article['highlight']
	tag = article['tag']
	numberLikes = article['numberLikes']
	articleTime = article['time']

	if authorID is None:
		authorID = queryAuthorIDbyMediumID(authorMediumID)

	if articleID:
		updateArticle(articleMediumID, articleTitle, highlight, authorID, tag, articleTime, numberLikes, articleID)
	else:
		articleID = insertArticle(articleMediumID, articleTitle, highlight, authorID, tag, articleTime, numberLikes)


def saveSratchArticle(articleMediumID):
	articleID = insertArticle(articleMediumID)
	return articleID

###insert sentence into stn table
def saveSentence(sentence, articleID=None):
	stnMediumID = sentence['id']
	stnContent = sentence['content']
	articleMediumID = sentence['articleMediumID']
	if articleID is None:
		articleID = queryArticleIDbyMediumID(articleMediumID)
	stnID = insertSTN(stnMediumID, articleID, stnContent)

###insert comment into comment table
def saveComment(comment):
	commentMediumID = comment['mediumID']
	commentContent = comment['content']
	authorMediumID = comment['authorMediumID']
	commentTime = comment['time']
	numberLikes = comment['numberLikes']
	corrStnMediumID = comment['corrStnID']
	articleMediumID = comment['articleMediumID']

	authorID = queryAuthorIDbyMediumID(authorMediumID)
	articleID = queryArticleIDbyMediumID(articleMediumID)
	corrStnID = -1
	if corrStnMediumID != '':
		corrStnID = queryStnIDbyMediumID(corrStnMediumID, articleID)

	insertComment(commentMediumID, commentContent, authorID, commentTime, numberLikes, corrStnID, articleID)
