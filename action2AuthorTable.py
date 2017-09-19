# -*- coding: utf-8 -*-
import psycopg2,sys

from config import config

def createAuthorTable():
	command = ("""
		CREATE TABLE author (
			authorID SERIAL PRIMARY KEY,
			authorName varchar(300),
			authorMediumID varchar(300),
			authorUserName varchar(300),
			bio text
		)
		""")

	conn = None
	try:
		params = config()

		conn = psycopg2.connect(**params)

		cur = conn.cursor()
		# print("creating author table....")

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

def insertAuthor(authorName, authorMediumID, authorUserName, bio):
	command = ("""
		INSERT INTO author (
			authorName,
			authorMediumID,
			authorUserName,
			bio
		)
		VALUES(
		%s, %s, %s, %s)

		RETURNING authorID;
		""")

	conn = None
	try:
		params = config()

		conn = psycopg2.connect(**params)

		cur = conn.cursor()
		# print("before inserting into author table....")
		# print("inserting into author:", file=sys.stderr)
		# print(authorName, authorMediumID, sep=", ", file=sys.stderr)
		# for command in commands:
		cur.execute(command, (authorName, authorMediumID, authorUserName, bio, ))
		# print("after inserting into author table....")

		authorID = cur.fetchone()[0]

		cur.close()

		conn.commit()

		return authorID

	except(Exception, psycopg2.DatabaseError) as error:
		print(error, file=sys.stderr)
	finally:
		if conn is not None:
			conn.close()

def existAuthor(authorMediumID):
	command = ("""
		select exists(select 1 from author where authorMediumID=%s)""")

	conn = None
	try:
		params = config()

		conn = psycopg2.connect(**params)

		cur = conn.cursor()
		# print("exist author in the author table....")

		# for command in commands:
		cur.execute(command, (authorMediumID, ))
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

def queryAuthorIDbyMediumID(MediumID):
	command = ("""
		SELECT
			authorID
		FROM author
		WHERE authorMediumID = %s
		""")

	conn = None
	try:
		params = config()

		conn = psycopg2.connect(**params)

		cur = conn.cursor()
		# print("queryAuthorIDbyMediumID....")

		# for command in commands:
		cur.execute(command, (MediumID,))
		# print("after queryAuthorIDbyMediumID....")

		authorID = cur.fetchone()
		if authorID is None:
			print("no author fetched" % MediumID)
			return

		cur.close()

		conn.commit()

		return authorID[0]

	except(Exception, psycopg2.DatabaseError) as error:
		print(error, file=sys.stderr)
	finally:
		if conn is not None:
			conn.close()
