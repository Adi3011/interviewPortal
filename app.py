#import libraries
from flask import jsonify
import os
from flask import Flask, flash, request, redirect, url_for, render_template, Response
from werkzeug.utils import secure_filename
from datetime import datetime,date
import sqlite3
import json
import pprint
#entry to the flask application
app = Flask(__name__)




app.secret_key = "secret key" 


def insertInterview(interviewName,interviewerName,intervieweeName,email1,email2,date,startTime,endTime):
	try:
	    with sqlite3.connect('portal.db') as conn:
	        cur = conn.cursor()
	        print("Successfully Connected to SQLite")
	        cur.execute("INSERT INTO interviews (interviewName,interviewerName,intervieweeName,email1,email2,dt,startTime,endTime) VALUES (?,?,?,?,?,?,?,?)",
	        	(interviewName,interviewerName,intervieweeName,email1,email2,date,startTime,endTime)) 
	        conn.commit()
	        print("Interview Scheduled")
	except sqlite3.Error as error:
		print("Failed to connect", error)

	finally:
		if conn:
			conn.close()
			print("connection is closed")




def getAllInterviews():
	interviews = []
	try:
		with sqlite3.connect('portal.db') as conn:
			cur = conn.cursor()
			print("Successfully Connected to SQLite")

			cur.execute("Select * from interviews")
			interviews = cur.fetchall()    
			conn.commit()
			print("Interviews Fetched")

	except sqlite3.Error as error:
		print("Failed to connect", error)
	finally:
		if conn:
			conn.close()
			print("connection is closed")
	return interviews




def getAllInterviewers():
	interviewers = []
	try:
		with sqlite3.connect('portal.db') as conn:
			cur = conn.cursor()
			print("Successfully Connected to SQLite")

			cur.execute("Select name,email_id from interviewers")
			interviewers = cur.fetchall()    
			conn.commit()
			print("Interviews Fetched")

	except sqlite3.Error as error:
		print("Failed to connect", error)
	finally:
		if conn:
			conn.close()
			print("connection is closed")
	return interviewers


def validate(startTime,endTime,sTime,eTime):

	startTimeHrs, startTimeMin = int(startTime.split(':')[0]), int(startTime.split(':')[1])
	endTimeHrs, endTimeMin = int(endTime.split(':')[0]), int(endTime.split(':')[1])
	sTimeHrs, sTimeMin = int(sTime.split(':')[0]), int(sTime.split(':')[1])
	eTimeHrs, eTimeMin = int(eTime.split(':')[0]), int(eTime.split(':')[1])

	if startTimeHrs > eTimeHrs or endTimeHrs < sTimeHrs:
		return True 
	elif startTimeHrs == eTimeHrs and startTimeMin - eTimeMin > 15:
		return True
	elif startTimeHrs < sTimeHrs and endTimeHrs == sTimeHrs and sTimeMin - endTimeMin > 15:
		return True
	else:
		return False	



def checkAvailablity(emails,startTime,endTime,dt):
	print(startTime,endTime)
	try:
		with sqlite3.connect('portal.db') as conn:
			cur = conn.cursor()
			print("Successfully Connected to SQLite")
			dt=str(dt)

			cur.execute("SELECT * from interviews where dt = ?", (dt,))
			rows = cur.fetchall()

			for row in rows:
				sTime=row[7]
				eTime=row[8]
				print(sTime,eTime)

				if validate(startTime,endTime,sTime,eTime) == False:
					intervieweeEmails = row[5].split(',')
					print(emails,intervieweeEmails)

					if len(set(intervieweeEmails).intersection(emails)):
						return False
						

			print("validation")

	except sqlite3.Error as error:
		print("Failed to connect", error)
	finally:
		if conn:
			conn.close()
			print("connection is closed")

	return True			


def updatetable(_id,interviewName,interviewerName,intervieweeName,email1,email2,date,startTime,endTime):
	try:
		with sqlite3.connect('portal.db') as conn:
			cur = conn.cursor()
			print("Successfully Connected to SQLite")

			cur.execute("UPDATE interviews SET interviewName=? ,interviewerName=?,intervieweeName=?,email1=?,email2=?,dt=?,startTime=?,endTime=? where id=?",(interviewName,interviewerName,intervieweeName,email1,email2,date,startTime,endTime,_id))
			conn.commit()
			print("Partcipants Fetched")

	except sqlite3.Error as error:
		print("Failed to connect", error)
	finally:
		if conn:
			conn.close()
			print("connection is closed")


def getAllPartcipants():
	participants = []
	try:
		with sqlite3.connect('portal.db') as conn:
			cur = conn.cursor()
			print("Successfully Connected to SQLite")

			cur.execute("Select name,email_id from participants")
			participants = cur.fetchall()    
			conn.commit()
			print("Partcipants Fetched")

	except sqlite3.Error as error:
		print("Failed to connect", error)
	finally:
		if conn:
			conn.close()
			print("connection is closed")
	return participants	




@app.route('/')
def home():
	
	interviews = getAllInterviews()
	interviewers = getAllInterviewers()	
	participants = getAllPartcipants()
	return render_template('index.html',interviews=interviews,jsonInterviews=json.dumps(interviews),interviewers= interviewers, participants= participants)



@app.route('/schedule',methods=['POST'])
def schedule():
	if request.method=='POST':
		interviewName = request.form['name']
		date = request.form['date']
		startTime = request.form['startTime']
		endTime = request.form['endTime']
		interviewerName= request.form['interviewername']
		email1 = request.form['intervieweremail']
		intervieweeNames = request.form.getlist('candidatesName')
		intervieweeEmails = request.form.getlist('candidatesEmail')
		candidates = zip(intervieweeNames,intervieweeEmails)

		if len(list(candidates)) < 2:
			flash("Select More participants to schedule interview")
			return redirect(url_for('home'))

		flag = 1	
		if(checkAvailablity(intervieweeEmails,startTime,endTime,date) == False):
			flag =0
			flash("Partcipants are Busy in Another Interview. Please select another timing")

		if flag==0:
			return redirect(url_for('home'))
		else:
			intervieweeNames = ','.join(intervieweeNames)
			intervieweeEmails = ','.join(intervieweeEmails)
			insertInterview(interviewName,interviewerName,intervieweeNames,email1,intervieweeEmails,date,startTime,endTime)

		    
	return redirect(url_for('home'))


@app.route('/update',methods=['POST'])
def update():
	flag=1
	if request.method=='POST':
		_id = request.form['_id']
		interviewName = request.form['uname']
		date = request.form['udate']
		startTime = request.form['ustartTime']
		endTime = request.form['uendTime']
		interviewerName= request.form['uinterviewername']
		email1 = request.form['uintervieweremail']
		intervieweeNames = request.form.getlist('ucandidatesName')
		intervieweeEmails = request.form.getlist('ucandidates')
		candidates = zip(intervieweeNames,intervieweeEmails)

		if len(list(candidates)) < 2:
			flash("Select More participants to schedule interview")
			return redirect(url_for('home'))

		flag = 1	
		
		if(checkAvailablity(intervieweeEmails,startTime,endTime,date) == False):
			flag =0
			flash("Partcipants are Busy in Another Interview. Please select another timing")

		if flag==0:
			return redirect(url_for('home'))
		else:
			intervieweeNames = ','.join(intervieweeNames)
			intervieweeEmails = ','.join(intervieweeEmails)
			updatetable(_id,interviewName,interviewerName,intervieweeNames,email1,intervieweeEmails,date,startTime,endTime)

	interviews = getAllInterviews()
	interviewers = getAllInterviewers()	
	participants = getAllPartcipants()
	return render_template('index.html',interviews=interviews,jsonInterviews=json.dumps(interviews),interviewers= interviewers, participants= participants)



if __name__ == "__main__":
    app.run(debug=True)	