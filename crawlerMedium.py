# -*- coding: utf-8 -*-

import psycopg2

from config import config

def create_tables():

	command = ("""
		CREATE TABLE article (
			authorid SERIAL PRIMARY KEY,
			authorName varchar(50),
			authorTime timestamp
		)
		""")

	conn = None
	try:
		params = config()

		conn = psycopg2.connect(**params)

		cur = conn.cursor()
		print "before execute...."

		# for command in commands:
		cur.execute(command)
		print "after execute...."

		cur.close()

		conn.commit()

	except(Exception, psycopg2.DatabaseError) as error:
		print(error)
	finally:
		if conn is not None:
			conn.close()

def insertContent(authorName, authorTime):
	command = ("""
		INSERT INTO article (
			authorName,
			authorTime
		)
		VALUES(
		%s, %s);
		""")

	conn = None
	try:
		params = config()

		conn = psycopg2.connect(**params)

		cur = conn.cursor()
		print "before execute...."

		# for command in commands:
		cur.execute(command, (authorName, authorTime, ))
		print "after execute...."

		cur.close()

		conn.commit()

	except(Exception, psycopg2.DatabaseError) as error:
		print(error)
	finally:
		if conn is not None:
			conn.close()

def readContent(authorName):
	command = ("""
		SELECT 
			content
		FROM article
		WHERE authorName = %s
		""")

	conn = None
	try:
		params = config()

		conn = psycopg2.connect(**params)

		cur = conn.cursor()
		print "before execute...."

		# for command in commands:
		cur.execute(command, (authorName, ))
		print "after execute...."

		content = cur.fetchone()
		print "authorName\t", content[0]
		# print "~~~~~~~~~~~~~~~", content[1]

		cur.close()

		conn.commit()

	except(Exception, psycopg2.DatabaseError) as error:
		print(error)
	finally:
		if conn is not None:
			conn.close()

def existContent(authorName):
	command = ("""
		select exists(select 1 from article where authorName=%s)""")

	conn = None
	try:
		params = config()

		conn = psycopg2.connect(**params)

		cur = conn.cursor()
		print "before execute...."

		# for command in commands:
		cur.execute(command, (authorName, ))
		print "after execute...."

		existFlag = cur.fetchone()[0]

		if existFlag == True:
			print "authorName\t",
		else:
			print "no exist"
		# print "~~~~~~~~~~~~~~~", content[1]

		cur.close()

		conn.commit()

	except(Exception, psycopg2.DatabaseError) as error:
		print(error)
	finally:
		if conn is not None:
			conn.close()


if __name__ == '__main__':
	# create_tables()
	authorName = "Jibang1"
	content = "test1"
	authorTime = "1999-01-08 04:05:06"
	insertContent(authorName, authorTime)
	# readContent(authorName)
	# existContent(authorName)