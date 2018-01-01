# -*- coding: utf-8 -*-
import psycopg2,sys

from config import config

def createHighlightTable():
	command = ("""
		CREATE TABLE highlight (
			highlightID SERIAL PRIMARY KEY,
			content text,
			numberlikes int,
			corrStnID varchar(300),
			articleID int
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

def insertHighlight(stnName, articleID, stnContent):
	command = ("""
		INSERT INTO stn (
			content text,
			numberlikes,int,
			corrStnID varchar(300),
			articleID int,
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
		cur.execute(command, (content, numberlikes, corrStnID, articleID, ))
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

# def queryHighlightIDbyStnName(stnName):
#
# 	command = ("""
# 		SELECT
# 			stnID
# 		FROM highlight
# 		WHERE stnName = %s
# 		""")
#
#
# 	conn = None
# 	try:
# 		params = config()
#
# 		conn = psycopg2.connect(**params)
#
# 		cur = conn.cursor()
# 		# print("querying sentence table....")
# 		# print("inserting into sentence:", file=sys.stderr)
# 		# print(commentName, commentContent, authorID, commentTime, numLikes, corrStnID, articleID, sep=", ", file=sys.stderr)
# 		# for command in commands:
# 		cur.execute(command, (stnName,))
# 		# print("after querying sentence table....")
#
# 		stnID = cur.fetchone()
# 		if stn is None:
# 			print("no stn fetched" % stnName)
# 			return
# 		cur.close()
#
# 		conn.commit()
#
# 		return stnID[0]
#
# 	except(Exception, psycopg2.DatabaseError) as error:
# 		print(error, file=sys.stderr)
# 	finally:
# 		if conn is not None:
# 			conn.close()
