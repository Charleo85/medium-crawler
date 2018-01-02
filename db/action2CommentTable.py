# -*- coding: utf-8 -*-
import psycopg2,sys

from db.config import config

def createCommentTable():
	command = ("""
		CREATE TABLE comment (
			commentID SERIAL PRIMARY KEY,
			selfArticleID int,
			corrArticleID int,
			corrHighlightID int
		)
		""")

	conn = None
	try:
		params = config()

		conn = psycopg2.connect(**params)

		cur = conn.cursor()
		# print("creating comment table....")

		# for command in commands:
		cur.execute(command)
		# print("after creating comment table....")

		cur.close()

		conn.commit()

	except(Exception, psycopg2.DatabaseError) as error:
		print(error, file=sys.stderr)
	finally:
		if conn is not None:
			conn.close()

def insertComment(selfArticleID, corrHighlightID, corrArticleID):
	command = ("""
		INSERT INTO comment (
			selfArticleID,
			corrArticleID,
			corrHighlightID
		)
		VALUES(
		%s, %s, %s)

		RETURNING commentID;
		""")

	conn = None
	try:
		params = config()

		conn = psycopg2.connect(**params)

		cur = conn.cursor()
		# print("before inserting into comment table....")
		# print("inserting into comment:", file=sys.stderr)
		# print(mediumID, content, corrAuthorID, commentTime, numLikes, corrStnID, corrArticleID, sep=", ", file=sys.stderr)
		# for command in commands:
		cur.execute(command, (selfArticleID, corrArticleID, corrHighlightID, ))

		commentID = cur.fetchone()[0]
		# print("after inserting into comment table....")

		cur.close()

		conn.commit()

		return commentID

	except(Exception, psycopg2.DatabaseError) as error:
		print(error, file=sys.stderr)
	finally:
		if conn is not None:
			conn.close()
