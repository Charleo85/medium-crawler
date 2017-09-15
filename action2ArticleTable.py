# -*- coding: utf-8 -*-
import psycopg2

from config import config

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
		print("creating article table....")

		# for command in commands:
		cur.execute(command)
		print("after creating article table....")

		cur.close()

		conn.commit()

	except(Exception, psycopg2.DatabaseError) as error:
		print(error)
	finally:
		if conn is not None:
			conn.close()

def insertArticle(articleMediumID, articleTitle, articleContent, authorID, tag, articleTime, numberLikes):
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
		print("before inserting into article table....")

		# for command in commands:
		cur.execute(command, (articleMediumID, articleTitle, articleContent, authorID, tag, articleTime, numberLikes, ))
		print("after inserting into article table....")

		articleID = cur.fetchone()[0]

		cur.close()

		conn.commit()

		return articleID

	except(Exception, psycopg2.DatabaseError) as error:
		print(error)
	finally:
		if conn is not None:
			conn.close()

def queryArticleIDbyMediumID(mediumID):
	command = ("""
		SELECT
			articleID
		FROM article
		WHERE articleMediumID = %s
		)
		VALUES(
		%s )
		""")

	conn = None
	try:
		params = config()

		conn = psycopg2.connect(**params)

		cur = conn.cursor()
		print("querying article table....")

		# for command in commands:
		cur.execute(command, (mediumID,))
		print("after querying article table....")

		articleID = cur.fetchone()[0]

		cur.close()

		conn.commit()

		return articleID

	except(Exception, psycopg2.DatabaseError) as error:
		print(error)
	finally:
		if conn is not None:
			conn.close()
