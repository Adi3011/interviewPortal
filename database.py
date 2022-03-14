import sqlite3
from datetime import datetime
with sqlite3.connect("portal.db") as conn:
	c=conn.cursor()

	query1 = """ CREATE TABLE interviewers (name VARCHAR(100) NOT NULL,email_id VARCHAR(100) NOT NULL,PRIMARY KEY (email_id));"""
	query2 = """ CREATE TABLE participants (name VARCHAR(100) NOT NULL,email_id VARCHAR(100) NOT NULL,PRIMARY KEY (email_id));"""
	query3 = """ CREATE TABLE interviews (id INTEGER PRIMARY KEY AUTOINCREMENT,interviewName VARCHAR(20),interviewerName VARCHAR(20) NOT NULL,intervieweeName VARCHAR(200) NOT NULL,email1 VARCHAR(100) NOT NULL,email2 VARCHAR(200) NOT NULL,dt text,startTime text NOT NULL,endTime text NOT NULL)"""
	c.execute(query1)
	c.execute(query2)
	c.execute(query3)

	query = """ INSERT into participants (name,email_id) VALUES ("Aditya","19bcs1084@gmail.com")"""
	c.execute(query)
	query = """ INSERT into participants (name,email_id) VALUES ("Akash","19bcs1090@gmail.com")"""
	c.execute(query)
	query = """ INSERT into participants (name,email_id) VALUES ("Aman","19bcs1087@gmail.com")"""
	c.execute(query)

	query = """ INSERT into participants (name,email_id) VALUES ("Aman","19bcs1089@gmail.com")"""
	c.execute(query)
	query = """ INSERT into participants (name,email_id) VALUES ("Anish","19bcs1010@gmail.com")"""
	c.execute(query)
	query = """ INSERT into participants (name,email_id) VALUES ("Amit","19bcs1187@gmail.com")"""
	c.execute(query)
	query = """ INSERT into participants (name,email_id) VALUES ("Amitesh","19bcs1000@gmail.com")"""
	c.execute(query)
	query = """ INSERT into participants (name,email_id) VALUES ("Anna","19bcs1092@gmail.com")"""
	c.execute(query)
	query = """ INSERT into participants (name,email_id) VALUES ("Anushi","19bcs1023@gmail.com")"""
	c.execute(query)

	query = """ INSERT into interviewers (name,email_id) VALUES ("Anubhav","anubhav@gmail.com")"""
	c.execute(query)
	query = """ INSERT into interviewers (name,email_id) VALUES ("Anirudh","anirudh@gmail.com")"""
	c.execute(query)
	query = """ INSERT into interviewers (name,email_id) VALUES ("Animesh","Animesh@gmail.com")"""
	c.execute(query)

	query = """ INSERT into interviewers (name,email_id) VALUES ("Animesh","animesh@gmail.com")"""
	c.execute(query)
	query = """ INSERT into interviewers (name,email_id) VALUES ("Anushree","anushreeh@gmail.com")"""
	c.execute(query)
	query = """ INSERT into interviewers (name,email_id) VALUES ("Anamika","Anamika@gmail.com")"""
	c.execute(query)
	# c.execute(query2)
	# c.execute(query3)

	conn.commit()
