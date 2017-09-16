# -*- coding: utf-8 -*-
import psycopg2,sys

from config import config

def createCommentTable():
	command = ("""
		CREATE TABLE comment (
			commentID SERIAL PRIMARY KEY,
			commentName text,
			commentContent text,
			authorID varchar(300),
			commentTime timestamp,
			numberLikes int,
			corrStnID varchar(300),
			articleID int
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
		print(error)
	finally:
		if conn is not None:
			conn.close()

def insertComment(commentName, commentContent, authorID, commentTime, numLikes, corrStnID, articleID):
	command = ("""
		INSERT INTO comment (
			commentName,
			commentContent,
			authorID,
			commentTime,
			numberLikes,
			corrStnID,
			articleID
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
		# print(commentName, commentContent, authorID, commentTime, numLikes, corrStnID, articleID, sep=", ", file=sys.stderr)
		# for command in commands:
		cur.execute(command, (commentName, commentContent, authorID, commentTime, numLikes, corrStnID, articleID, ))
		# print("after inserting into comment table....")

		commentID = cur.fetchone()[0]

		cur.close()

		conn.commit()

		return commentID

	except(Exception, psycopg2.DatabaseError) as error:
		print(error)
	finally:
		if conn is not None:
			conn.close()
