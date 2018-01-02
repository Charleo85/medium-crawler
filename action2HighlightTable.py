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

def existHighlight(mediumID):
	command = ("""
		select exists(select 1 from author where corrArticleID=%s)""")

	conn = None
	try:
		params = config()

		conn = psycopg2.connect(**params)

		cur = conn.cursor()
		# print("exist author in the author table....")

		# for command in commands:
		cur.execute(command, (mediumID, ))
		# print("after existing author in the table....")

		existFlag = cur.fetchone()[0]

		cur.close()

		conn.commit()

		return existFlag

	except(Exception, psycopg2.DatabaseError) as error:
		print(error, file=sys.stderr)
	finally:
		if conn is not None:
			conn.close()
