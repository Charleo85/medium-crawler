# -*- coding: utf-8 -*-
import psycopg2,sys

from db.config import config

def createTopicTable():
	command = ("""
		CREATE TABLE topic (
			topicID SERIAL PRIMARY KEY,
			name text,
			mediumID varchar(20),
			description text
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

def insertTopic(name, mediumID, description):
	command = ("""
		INSERT INTO topic (
			name,
			mediumID,
			description
		)
		VALUES(
		%s, %s, %s)

		RETURNING topicID;
		""")

	conn = None
	try:
		params = config()

		conn = psycopg2.connect(**params)

		cur = conn.cursor()
		# print("before inserting into author table....")
		# print("inserting into author:", file=sys.stderr)
		# print(name, mediumID, sep=", ", file=sys.stderr)
		# for command in commands:
		cur.execute(command, (name, mediumID, description, ))
		# print("after inserting into author table....")

		topicID = cur.fetchone()[0]

		cur.close()

		conn.commit()

		return topicID

	except(Exception, psycopg2.DatabaseError) as error:
		print(error, file=sys.stderr)
	finally:
		if conn is not None:
			conn.close()

def queryTopicIDbyMediumID(mediumID):
	command = ("""
		SELECT
			topicID
		FROM topic
		WHERE mediumID = %s
		""")

	conn = None
	try:
		params = config()

		conn = psycopg2.connect(**params)

		cur = conn.cursor()
		# print("queryAuthorIDbyMediumID....")

		# for command in commands:
		cur.execute(command, (mediumID,))
		# print("after queryAuthorIDbyMediumID....")

		topicID = cur.fetchone()
		if topicID is None:
			# print("no topic fetched: " + mediumID)
			return -1;

		cur.close()

		conn.commit()

		return topicID[0]

	except(Exception, psycopg2.DatabaseError) as error:
		print(error, file=sys.stderr)
	finally:
		if conn is not None:
			conn.close()

def queryAllTopicMediumID():
	command = ("SELECT mediumID FROM topic")

	conn = None
	try:
		params = config()

		conn = psycopg2.connect(**params)

		cur = conn.cursor()

		# for command in commands:
		cur.execute(command)

		topicIDs = cur.fetchall()
		if topicIDs is None:
			return [];

		cur.close()

		conn.commit()

		return topicIDs

	except(Exception, psycopg2.DatabaseError) as error:
		print(error, file=sys.stderr)
	finally:
		if conn is not None:
			conn.close()
