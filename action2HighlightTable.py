# -*- coding: utf-8 -*-
import psycopg2,sys

from config import config

def createHighlightTable():
	command = ("""
		CREATE TABLE highlight (
			highlightID SERIAL PRIMARY KEY,
			content text,
			numLikes int,
			corrArticleID int,
			corrStnMediumIDs varchar(300)
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

def insertHighlight(content, numlikes, corrArticleID, corrStnMediumIDs):
	command = ("""
		INSERT INTO highlight (
			content,
			numLikes,
			corrArticleID,
			corrStnMediumIDs
		)
		VALUES(
		%s, %s, %s, %s)

		RETURNING highlightID;
		""")

	conn = None
	try:
		params = config()

		conn = psycopg2.connect(**params)

		cur = conn.cursor()
		# print("before inserting into article table....")

		# for command in commands:
		cur.execute(command, (content, numlikes, corrArticleID, corrStnMediumIDs,  ))
		# print("after inserting into article table....")

		highlightID = cur.fetchone()[0]

		cur.close()

		conn.commit()

		return highlightID

	except(Exception, psycopg2.DatabaseError) as error:
		print(error, file=sys.stderr)
	finally:
		if conn is not None:
			conn.close()

def existHighlight(corrArticleID, content):

	command = ("""
		SELECT
			highlightID
		FROM highlight
		WHERE corrArticleID = %s
		AND content = %s
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
		cur.execute(command, (corrArticleID, content,))
		# print("after querying sentence table....")

		highlightID = cur.fetchone()
		if highlightID is None:
			# print("no stn fetched: " + mediumID + ' '+ str(articleID) )
			return -1
		cur.close()

		conn.commit()

		return highlightID[0]

	except(Exception, psycopg2.DatabaseError) as error:
		print(error, file=sys.stderr)
	finally:
		if conn is not None:
			conn.close()
