# -*- coding: utf-8 -*-
import psycopg2,sys

from config import config

def createCommentTable():
	command = ("""
		CREATE TABLE comment (
			commentID SERIAL PRIMARY KEY,
			mediumID varchar(20),
			content text,
			commentTime timestamp,
			numberLikes int,
			corrAuthorID int,
			corrArticleID int,
			corrStnID int
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

def insertComment(mediumID, content, corrAuthorID, commentTime, numberLikes, corrStnID, corrArticleID):
	command = ("""
		INSERT INTO comment (
			mediumID,
			content,
			commentTime,
			numberLikes,
			corrAuthorID,
			corrArticleID,
			corrStnID
		)
		VALUES(
		%s, %s, %s, %s, %s, %s, %s)

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
		cur.execute(command, (mediumID, content, commentTime, numberLikes, corrAuthorID, corrArticleID, corrStnID, ))
		# print("after inserting into comment table....")

		commentID = cur.fetchone()[0]

		cur.close()

		conn.commit()

		return commentID

	except(Exception, psycopg2.DatabaseError) as error:
		print(error, file=sys.stderr)
	finally:
		if conn is not None:
			conn.close()
