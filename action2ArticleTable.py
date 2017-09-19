# -*- coding: utf-8 -*-
import psycopg2,sys

from config import config
DEFAULT_TIME = "1900-01-01 00:00:00"

def createArticleTable():
	command = ("""
		CREATE TABLE article (
			articleID SERIAL PRIMARY KEY,
			articleMediumID text,
			articleTitle text,
			articleContent text,
			authorID int,
			tag varchar(300),
			articleTime timestamp,
			numberLikes int
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

def insertArticle(articleMediumID, articleTitle="", articleContent="", authorID=-1, tag="", articleTime=DEFAULT_TIME, numberLikes=-1):
	command = ("""
		INSERT INTO article (
			articleMediumID,
			articleTitle,
			articleContent,
			authorID,
			tag,
			articleTime,
			numberLikes
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
		# print(articleMediumID, articleTitle, articleContent, authorID, tag, articleTime, numberLikes, sep=", ", file=sys.stderr)
		# for command in commands:
		cur.execute(command, (articleMediumID, articleTitle, articleContent, authorID, tag, articleTime, numberLikes, ))
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

def updateArticle(articleMediumID, articleTitle, articleContent, authorID, tag, articleTime, numberLikes, articleID):
	command = ("""
		UPDATE article
		SET
			articleMediumID = %s,
			articleTitle = %s,
			articleContent = %s,
			authorID = %s,
			tag = %s,
			articleTime = %s,
			numberLikes = %s
		WHERE articleID = %s
		""")

	conn = None
	try:
		params = config()

		conn = psycopg2.connect(**params)

		cur = conn.cursor()
		# print("before inserting into article table....")
		# print("inserting into article:", file=sys.stderr)
		# print(articleMediumID, articleTitle, articleContent, authorID, tag, articleTime, numberLikes, sep=", ", file=sys.stderr)
		# for command in commands:
		cur.execute(command, (articleMediumID, articleTitle, articleContent, authorID, tag, articleTime, numberLikes, articleID, ))
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
		WHERE articleMediumID = %s
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

		articleID = cur.fetchone()[0]

		cur.close()

		conn.commit()

		return articleID

	except(Exception, psycopg2.DatabaseError) as error:
		print(error, file=sys.stderr)
	finally:
		if conn is not None:
			conn.close()

def existArticle(mediumID):
	command = ("""
		select exists(select 1 from article where articleMediumID=%s)""")

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
