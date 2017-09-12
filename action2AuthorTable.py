# -*- coding: utf-8 -*-
import psycopg2

from config import config

def createAuthorTable():
	command = ("""
		CREATE TABLE author (
			authorID SERIAL PRIMARY KEY,
			authorName varchar(300),
			authorMediumID varchar(300)
		)
		""")

	conn = None
	try:
		params = config()

		conn = psycopg2.connect(**params)

		cur = conn.cursor()
		print("creating author table....")

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

def insertAuthor(authorName, authorMediumID):
	command = ("""
		INSERT INTO author (
			authorName,
			authorMediumID
		)
		VALUES(
		%s, %s)

		RETURNING authorID;
		""")

	conn = None
	try:
		params = config()

		conn = psycopg2.connect(**params)

		cur = conn.cursor()
		print("before inserting into author table....")

		# for command in commands:
		cur.execute(command, (commentName, commentContent, authorID, commentTime, numLikes, corrStnID, articleID, ))
		print("after inserting into author table....")

		authorID = cur.fetchone()[0]

		cur.close()

		conn.commit()

		return authorID

	except(Exception, psycopg2.DatabaseError) as error:
		print(error)
	finally:
		if conn is not None:
			conn.close()

def existAuthor(authorName):
	command = ("""
		select exists(select 1 from author where authorName=%s)""")

	conn = None
	try:
		params = config()

		conn = psycopg2.connect(**params)

		cur = conn.cursor()
		print("before inserting into author table....")

		# for command in commands:
		cur.execute(command, (authorName, ))
		print("after inserting into author table....")

		existFlag = cur.fetchone()[0]

		cur.close()

		conn.commit()

		return existFlag

	except(Exception, psycopg2.DatabaseError) as error:
		print(error)
	finally:
		if conn is not None:
			conn.close()

def queryAuthorIDbyAuthorName(authorName):
	command = ("""
		SELECT
			authorID 
		FROM author
		WHERE authorName = %s		
		)
		""")

	conn = None
	try:
		params = config()

		conn = psycopg2.connect(**params)

		cur = conn.cursor()
		print("creating sentence table....")

		# for command in commands:
		cur.execute(command, (authorName,))
		print("after creating sentence table....")

		authorID = cur.fetchone()[0]

		cur.close()

		conn.commit()

		return authorID

	except(Exception, psycopg2.DatabaseError) as error:
		print(error)
	finally:
		if conn is not None:
			conn.close()
