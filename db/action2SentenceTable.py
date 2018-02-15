# -*- coding: utf-8 -*-
import psycopg2,sys

from db.config import config

def createSentenceTable():
	command = ("""
		CREATE TABLE sentence (
			sentenceID SERIAL PRIMARY KEY,
			paragraphID int,
			content text,
			corrArticleID int
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

def insertSentence(paragraphID, articleID, stnContent):
	command = ("""
		INSERT INTO sentence (
			paragraphID,
			content,
			corrArticleID
		)
		VALUES(
		%s, %s, %s)

		RETURNING sentenceID;
		""")

	conn = None
	try:
		params = config()

		conn = psycopg2.connect(**params)

		cur = conn.cursor()
		# print("before inserting into stn table....")

		# for command in commands:
		cur.execute(command, (paragraphID, stnContent, articleID, ))

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

def querySentenceIDbyMediumID(mediumID, articleID):

	command = ("""
		SELECT
			sentenceID
		FROM sentence
		WHERE mediumID = %s
		AND corrArticleID = %s
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
		cur.execute(command, (mediumID, articleID,))
		# print("after querying sentence table....")

		stnID = cur.fetchone()
		if stnID is None:
			print("no stn fetched: " + mediumID + ' '+ str(articleID) )
			return -1
		cur.close()

		conn.commit()

		return stnID[0]

	except(Exception, psycopg2.DatabaseError) as error:
		print(error, file=sys.stderr)
	finally:
		if conn is not None:
			conn.close()
