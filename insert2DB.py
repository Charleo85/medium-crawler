import psycopg2

from config import config
from action2AuthorTable import *

from action2ArticleTable import *
from action2StnTable import *
from action2CommentTable import *

###insert author if not exist into the author table
authorName = 
authorMediumID = 

authorExistFlag = existAuthor(authorName)
authorID = -1

if authorExistFlag:
	print("exist author\t", authorName)
	authorID = queryAuthorIDbyAuthorName(authorName)
else:
	authorID = insertAuthor(authorName, authorMediumID)


####insert article into article table
articleName = 
articleTitle = 
articleContent = 
authorName = 
tag = 

### the format of time is "1999-01-08 04:05:06" 
articleTime = 
numberLikes =

authorID = queryAuthorIDbyAuthorName(authorName)

articleID = insertArticle(articleName, articleTitle, articleContent, authorID, tag, articleTime, numberLikes)


###insert sentence into stn table
stnName = 
articleName = 
stnContent = 

articleID = queryArticleIDbyArticleName(articleName)

stnID = insertSTN(stnName, articleID, stnContent)

###insert comment into comment table

commentName = 
commentContent = 
authorName = 
commentTime = 
numLikes = 
corrStnName = 
articleName = 

authorID = queryAuthorIDbyAuthorName(authorName)
corrStnID = queryStnIDbyStnName(corrStnName)
articleID = queryArticleIDbyArticleName(articleName)

insertComment(commentName, commentContent, authorID, commentTime, numLikes, corrStnID, articleID)
