# -*- coding: utf-8 -*-
import psycopg2,sys

from db.config import config
DEFAULT_TIME = "1900-01-01 00:00:00"

def createArticleTable():
	command = ("""
		CREATE TABLE article (
			articleID SERIAL PRIMARY KEY,
			mediumID varchar(20),
			title text,
			recommends int,
			tags varchar(300),
			postTime timestamp,
			numLikes int,
			corrAuthorID int
		)
		""")

	conn = None
	try:
		params = config()

		conn = psycopg2.connect(**params)

		cur = conn.cursor()
		# print("creating article table....")

		# for command in commands:
		cur.execute(command)
		# print("after creating article table....")

		cur.close()

		conn.commit()

	except(Exception, psycopg2.DatabaseError) as error:
		print(error, file=sys.stderr)
	finally:
		if conn is not None:
			conn.close()

def insertArticle(articleMediumID, articleTitle="", recommends=-1, authorID=-1, tags=[], articleTime=DEFAULT_TIME, numLikes=-1):
	command = ("""
		INSERT INTO article (
			mediumID,
			title,
			recommends,
			tags,
			postTime,
			numLikes,
			corrAuthorID
		)
		VALUES(
		%s, %s, %s, %s, %s, %s, %s)

		RETURNING articleID;
		""")

	conn = None
	try:
		params = config()

		conn = psycopg2.connect(**params)

		cur = conn.cursor()
		# print("before inserting into article table....")
		# print("inserting into article:", file=sys.stderr)
		# print(articleMediumID, articleTitle, articleContent, authorID, tags, articleTime, numLikes, sep=", ", file=sys.stderr)
		# for command in commands:
		cur.execute(command, (articleMediumID, articleTitle, recommends, tags, articleTime, numLikes, authorID, ))
		# print("after inserting into article table....")

		articleID = cur.fetchone()[0]

		cur.close()

		conn.commit()

		return articleID

	except(Exception, psycopg2.DatabaseError) as error:
		print(error, file=sys.stderr)
	finally:
		if conn is not None:
			conn.close()

def updateArticle(articleMediumID, articleTitle, recommends, tags, articleTime, numLikes, articleID, authorID):
	command = ("""
		UPDATE article
		SET
			mediumID = %s,
			title = %s,
			recommends = %s,
			tags = %s,
			postTime = %s,
			numLikes = %s,
			corrAuthorID = %s
		WHERE articleID = %s
		""")

	conn = None
	try:
		params = config()

		conn = psycopg2.connect(**params)

		cur = conn.cursor()
		# print("before inserting into article table....")
		# print("inserting into article:", file=sys.stderr)
		# print(articleMediumID, articleTitle, articleContent, authorID, tags, articleTime, numLikes, sep=", ", file=sys.stderr)
		# for command in commands:
		cur.execute(command, (articleMediumID, articleTitle, recommends, tags, articleTime, numLikes, authorID, articleID, ))
		# print("after inserting into article table....")

		cur.close()

		conn.commit()

	except(Exception, psycopg2.DatabaseError) as error:
		print(error, file=sys.stderr)
	finally:
		if conn is not None:
			conn.close()

def queryArticleIDbyMediumID(mediumID):
	command = ("""
		SELECT
			articleID
		FROM article
		WHERE mediumID = %s
		""")

	conn = None
	try:
		params = config()

		conn = psycopg2.connect(**params)

		cur = conn.cursor()
		# print("querying article table....")

		# for command in commands:
		cur.execute(command, (mediumID,))
		# print("after querying article table....")

		articleID = cur.fetchone()

		if articleID is None:
			# print("no article fetched: " + mediumID)
			return -1;

		cur.close()

		conn.commit()

		return articleID[0]

	except(Exception, psycopg2.DatabaseError) as error:
		print(error, file=sys.stderr)
	finally:
		if conn is not None:
			conn.close()

def existArticle(mediumID):
	command = ("""
		select exists(select 1 from article where mediumID=%s)""")

	conn = None
	try:
		params = config()

		conn = psycopg2.connect(**params)

		cur = conn.cursor()
		# print("exist author in the article table....")

		# for command in commands:
		cur.execute(command, (mediumID, ))
		# print("after existing article in the table....")

		existFlag = cur.fetchone()[0]

		cur.close()

		conn.commit()

		return existFlag

	except(Exception, psycopg2.DatabaseError) as error:
		print(error, file=sys.stderr)
	finally:
		if conn is not None:
			conn.close()
