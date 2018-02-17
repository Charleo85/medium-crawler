# -*- coding: utf-8 -*-
import psycopg2,sys

from db.config import config

def createParagraphTable():
	command = ("""
		CREATE TABLE paragraph (
			paragraphID SERIAL PRIMARY KEY,
			mediumID varchar(20),
			content text,
			corrArticleID int,
			prevParagraphID int
		)
		""")

	conn = None
	try:
		params = config()

		conn = psycopg2.connect(**params)

		cur = conn.cursor()
		# print("creating sentence table....")

		# for command in commands:
		cur.execute(command)
		# print("after creating sentence table....")

		cur.close()

		conn.commit()

	except(Exception, psycopg2.DatabaseError) as error:
		print(error, file=sys.stderr)
	finally:
		if conn is not None:
			conn.close()

def insertParagraph(mediumID, articleID, content, prevParagraphID):
	command = ("""
		INSERT INTO paragraph (
			mediumID,
			content,
			corrArticleID,
			prevParagraphID
		)
		VALUES(
		%s, %s, %s, %s)

		RETURNING paragraphID;
		""")

	conn = None
	try:
		params = config()

		conn = psycopg2.connect(**params)

		cur = conn.cursor()
		# print("before inserting into stn table....")

		# for command in commands:
		cur.execute(command, (mediumID, content, articleID, prevParagraphID, ))

		stnID = cur.fetchone()[0]
		# print("after inserting into stn table....")

		cur.close()

		conn.commit()

		return stnID

	except(Exception, psycopg2.DatabaseError) as error:
		print(error, file=sys.stderr)
	finally:
		if conn is not None:
			conn.close()

def existParagraphID(mediumID, articleID, content):
	command = ("""
		SELECT
			paragraphID
		FROM paragraph
		WHERE mediumID = %s
		AND (corrArticleID = %s
		OR content = %s
		)
		""")

	conn = None
	try:
		params = config()

		conn = psycopg2.connect(**params)

		cur = conn.cursor()
		# print("querying sentence table....")
		# print("inserting into sentence:", file=sys.stderr)
		# print(commentName, commentContent, authorID, commentTime, numLikes, corrStnID, articleID, sep=", ", file=sys.stderr)
		# for command in commands:
		cur.execute(command, (mediumID, articleID, content,))
		# print("after querying sentence table....")

		stnID = cur.fetchone()
		if stnID is None:
			print("no paragraph fetched: " + mediumID + ' '+ str(articleID), file=sys.stderr)
			return -1
		cur.close()

		conn.commit()

		return stnID[0]

	except(Exception, psycopg2.DatabaseError) as error:
		print(error, file=sys.stderr)
	finally:
		if conn is not None:
			conn.close()
