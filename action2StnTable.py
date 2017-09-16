# -*- coding: utf-8 -*-
import psycopg2,sys

from config import config

def createSTNTable():
	command = ("""
		CREATE TABLE stn (
			stnID SERIAL PRIMARY KEY,
			stnName varchar(300),
			articleID int,
			content text
		)
		""")

	conn = None
	try:
		params = config()

		conn = psycopg2.connect(**params)

		cur = conn.cursor()
		print("creating sentence table....")

		# for command in commands:
		cur.execute(command)
		print("after creating sentence table....")

		cur.close()

		conn.commit()

	except(Exception, psycopg2.DatabaseError) as error:
		print(error)
	finally:
		if conn is not None:
			conn.close()

def insertSTN(stnName, articleID, stnContent):
	command = ("""
		INSERT INTO stn (
			stnName,
			articleID,
			content
		)
		VALUES(
		%s, %s, %s)

		RETURNING stnID;
		""")

	conn = None
	try:
		params = config()

		conn = psycopg2.connect(**params)

		cur = conn.cursor()
		print("before inserting into article table....")

		# for command in commands:
		cur.execute(command, (stnName, articleID, stnContent, ))
		print("after inserting into article table....")

		stnID = cur.fetchone()[0]

		cur.close()

		conn.commit()

		return stnID

	except(Exception, psycopg2.DatabaseError) as error:
		print(error)
	finally:
		if conn is not None:
			conn.close()

def queryStnIDbyStnName(stnName):

	command = ("""
		SELECT
			stnID
		FROM stn
		WHERE stnName = %s
		""")


	conn = None
	try:
		params = config()

		conn = psycopg2.connect(**params)

		cur = conn.cursor()
		print("querying sentence table....")
		print("inserting into sentence:", file=sys.stderr)
		print(commentName, commentContent, authorID, commentTime, numLikes, corrStnID, articleID, sep=", ", file=sys.stderr)
		# for command in commands:
		cur.execute(command, (stnName,))
		print("after querying sentence table....")

		stnID = cur.fetchone()[0]

		cur.close()

		conn.commit()

		return stnID

	except(Exception, psycopg2.DatabaseError) as error:
		print(error)
	finally:
		if conn is not None:
			conn.close()
