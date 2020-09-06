#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 22 12:53:56 2020

@author: sidharthanantha
"""


'''
Determinator key:
    D = 2 --> student is new and no interests, proceeed to page 2
    D = 3 --> student is returning but no interests, proceeed to page 3
    D = 4 --> student is returning and interests, proceeed to page 4
'''

# This is the code that runs all the operations for the first page of the webpage set
# The operations that are done are:
#   1. Read in info from the JSON file (name + email)
#   2. Read the credentials and store them. Parse through the SQL database to verify whether or not the credentials exist
#   3. Give back an output JSON that tells the webclient which page to proceed to

import json
#import MySQLdb
import numpy
import mysql.connector
from mysql.connector import errorcode
import flask
from flask import request, jsonify
from flask_cors import CORS
import smtplib as s
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import numpy
import mysql.connector
from mysql.connector import errorcode
import pandas as pd
from datetime import datetime
app = flask.Flask(__name__)
app.config["DEBUG"] = True
CORS(app, resources = {r"/api/*": {"origins": "*"}})
print("Alloo")
config = {
    'user': 'helmlearning',
    'password': 'H3lml3arning',
    'host': '127.0.0.1', #52.21.172.100:22
    'port': '3306',
    'database': 'HELM_Database'
}

def gettime(starttime, endtime):
    if (starttime == None):
        return ['TBD', 'TBD']
    stime = str(starttime).split(":")
    etime = str(endtime).split(":")
    if (int(stime[0]) >= 12):
        startam = "pm"
        stime[0] = int(stime[0]) - 12
    else:
        startam = "am"
    if (int(etime[0]) >= 12):
        endam = "pm"
        etime[0] = int(etime[0]) - 12
    else:
        endam = "am"
    time_est = str(stime[0]) + ":" + str(stime[1]) + startam + " - " + str(etime[0]) + ":" + str(etime[1]) + endam
    stime[0] = int(str(starttime).split(":")[0]) - 1
    etime[0] = int(str(endtime).split(":")[0]) - 1

    if (int(stime[0]) >= 12):
        startam = "pm"
        stime[0] = int(stime[0]) - 12
    else:
        startam = "am"
    if (int(etime[0]) >= 12):
        endam = "pm"
        etime[0] = int(etime[0]) - 12
    else:
        endam = "am"

    time_cst = str(stime[0]) + ":" + str(stime[1]) + startam + " - " + str(etime[0]) + ":" + str(etime[1]) + endam
    return [time_est, time_cst]

def getdate(startdate, enddate):
    months = {
        1: "Jan",
        2: "Feb",
        3: "March",
        4: "April",
        5: "May",
        6: "June",
        7: "July",
        8: "Aug",
        9: "Sept",
        10: "Oct",
        11: "Nov",
        12: "Dec"
    }
    if (startdate == None):
        return ['TBD', 'TBD']
    sdate = str(startdate).split("-")
    edate = str(enddate).split("-")
    start_date = months[int(sdate[1])] + ' ' + sdate[2] + ', ' + sdate[0]
    end_date = months[int(edate[1])] + ' ' + edate[2] + ', ' + edate[0]
    return [start_date, end_date]

def send(subject, content, student_fname, email, pemail, class_name, teacher_name, brief_summary, time_est, time_cst, first_day, last_day, day, zoom_link, prerequisite):
    port = 465
    sender = "helmlearning2020@gmail.com"
    password = "h3lml3arning"
    #input("Send?")
    message = MIMEMultipart("alternative")
    message["Subject"] = subject.format(class_name)
    message["From"] = "HELM Learning"
    message["To"] = email

    html = content.format(student_fname, class_name, teacher_name, brief_summary, time_est, time_cst, day, first_day, day, last_day, zoom_link, zoom_link, prerequisite, teacher_name, class_name)
    print(html)
    #part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")
    #message.attach(part1)
    message.attach(part2)

    context = ssl.create_default_context()

    with s.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(sender, password)
        server.sendmail(sender, email, message.as_string())
        server.sendmail(sender, pemail, message.as_string())


def connect_to_send(student_fname, email, class_name):
    db = "HELM_Database"
    cnx = create_connection()
    cursor = cnx.cursor(buffered=True)
    cursor.execute("show columns from {}.students".format(db))
    sql = 'SELECT Email_Address, Parent_Email FROM students WHERE Student_Name = "%s" AND Email_Address = "%s"' % (student_fname, email)
    sql2 = 'SELECT name, teacher, e1_summary, starttime, endtime, startdate, enddate, day, zoom, e1_additionalwork FROM classes WHERE short_name = "%s";' % (class_name[0].upper() + class_name[1:])
    sql3 = 'SELECT subject, content FROM templates WHERE name="e1"'
    print(sql2)
    print(sql)
    cursor.execute(sql)
    emails = cursor.fetchall()[0]
    email = emails[0]
    pemail = emails[1]
    cursor.execute(sql2)
    class_info = cursor.fetchall()[0]
    cursor.execute(sql3)
    stuff = cursor.fetchall()[0]
    subject = stuff[0]
    content = stuff[1]
    print(class_info)
    print(email)

    send(subject, content, student_fname, email, pemail, class_info[0], class_info[1], class_info[2], gettime(class_info[3], class_info[4])[0], gettime(class_info[3], class_info[4])[1], getdate(class_info[5], class_info[6])[0], getdate(class_info[5], class_info[6])[1], class_info[7], class_info[8], class_info[9])

    cnx.commit()
    cursor.close()
    cnx.close()

    #tutorial at https://realpython.com/python-send-email/


def get_data(fhandle):
    with open(fhandle, 'r') as j:
        contents = json.loads(j.read())
        print(contents)
    return contents

def create_connection():
    """
    Returns a database connection using mysql.connector
    """
    # open database connection
    global cnx
    try:
        cnx = mysql.connector.connect(**config)
        return cnx
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
        raise


@app.route('/', methods=['GET'])
def basic_stuff():
    print("Yoyoma")
    return "<h1>Welcome!!</h1>"

# conn=MySQLdb.connect(host='helmlearningdatabase-1.cnoqlueuri3g.us-east-1.rds.amazonaws.com', database='HELM_Test_Database', user='helmlearning',passwd='H3lml3arning')
@app.route('/api/v1/resources/page1-receive', methods=['GET'])
def page1_receive():
    cnx = create_connection()
    cursor = cnx.cursor(buffered=True)
    query_params = request.args
    fname = query_params.get('fname')
    fname = fname.replace('$', ' ')
    email = query_params.get('email')
    class_name = query_params.get('class')
    class_name = class_name[0].upper() + class_name[1:]
    print('Name: ', fname)
    print('Email: ', email)
    print('Class: ', class_name)
    query = "SELECT * FROM students WHERE Student_Name = '{}' AND Email_Address = '{}'".format(fname, email)
    sql2 = "SELECT * FROM classes WHERE short_name = '{}'".format(class_name)
    determinator = 4
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.execute(sql2)
    classes = cursor.fetchall()
    print(result)
    if result == []:
        print('none')
        determinator = 2
    if classes == []:
        determinator = -1
    print(determinator)
    cnx.commit()
    cursor.close()
    cnx.close()
    data = {
        "output": determinator
    }
    return jsonify(data)

@app.route('/api/v1/resources/page2-receive', methods=['GET'])
def page2():
    cnx = create_connection()
    cursor = cnx.cursor(buffered=True)
    query_params = request.args
    fname = query_params.get('fname')
    fname = fname.replace('$', ' ')
    email = query_params.get('email')
    pemail = query_params.get('pemail')
    age = query_params.get('age')
    town = query_params.get('town')
    town = town.replace('$', ' ')
    state = query_params.get('state')
    state = state.replace('$', ' ')
    hearabout = query_params.get('hearabout')
    hearabout = hearabout.replace('$', ' ')
    # print('Name: ', fname)
    # print('Email: ', email)
    # print('Town: ', class_name)
    # query = "SELECT * FROM students WHERE Student_Name = '{}' AND Email_Address = '{}'".format(fname, email)
    timestamp = datetime.now()
    sql = 'INSERT INTO students (Timestamp, Student_Name, Email_Address, Parent_Email, City, State, Grade, Heard_about_us) VALUES("{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}")'.format(timestamp, fname, email, pemail, town, state, age, hearabout)
    print(sql)
    cursor.execute(sql)

    cnx.commit()
    cursor.close()
    cnx.close()
    data = {}
    return jsonify(data)

@app.route('/api/v1/resources/page4-receive', methods=['GET'])
def get_class_info():
    cnx = create_connection()
    cursor = cnx.cursor(buffered=True)
    #contents = get_data("page4-send.json")
    #short_class_name = contents[]
    query_params = request.args
    short_name_of_class = query_params.get('class')
    short_class_name = short_name_of_class[0].upper() + short_name_of_class[1:]
    sql = "SELECT name, description, teacher, email, starttime, endtime, startdate, enddate, zoom FROM classes WHERE short_name = '{}'".format(short_class_name)
    cursor.execute(sql)
    result = cursor.fetchall()
    print(result)
    class_name = result[0][0]
    description = result[0][1]
    teacher = result[0][2]
    email = result[0][3]
    starttime = result[0][4]
    endtime = result[0][5]
    startdate = result[0][6]
    enddate = result[0][7]
    zoom = result[0][8]
    time = gettime(starttime, endtime)[0]
    date = getdate(startdate, enddate)[0]
    output = {
        "Name": class_name,
        "Description": description,
        "Teacher": teacher,
        "Email": email,
        "Time": time,
        "Date": date,
        "Zoom": zoom
    }
    return jsonify(output)

@app.route('/api/v1/resources/sendemail', methods=['GET'])
def to_send_email():
    cnx = create_connection()
    cursor = cnx.cursor(buffered=True)
    query_params = request.args
    short_name_of_class = query_params.get('class')
    student_fname = query_params.get('fname')
    student_fname = student_fname.replace('$', ' ')
    email = query_params.get('email')
    connect_to_send(student_fname, email, short_name_of_class)
    sql_sid = 'SELECT id FROM students WHERE Student_Name = "{}" AND Email_Address = "{}"'.format(student_fname, email)
    sql_cid = 'SELECT id FROM classes WHERE short_name = "{}"'.format(short_name_of_class[0].upper() + short_name_of_class[1:])
    timestamp = datetime.now()
    sql_su = 'INSERT INTO classes_to_students (timestamp, class_id, student_id) VALUES("{}", "{}", "{}")'
    
    cursor.execute(sql_sid)
    sid = cursor.fetchall()[0][0]
    cursor.execute(sql_cid)
    cid = cursor.fetchall()[0][0]
    cursor.execute(sql_su.format(timestamp,cid, sid))
    print(sid)
    cnx.commit()

    # close the cursor and database connection
    cursor.close()
    cnx.close()
    return {}
'''
Steps to do:
    
PAGE 1:
    1. connect to correct database (line 34)
    2. update existing query (line 59) to search for name and email in table
    3. write new queries to search database to see if student has interests already
    4. write and send a JSON file with the determinator key in it
    

PAGE 2: receive JSON with user data and store in database
    1. read in a JSON file that has user data (lines 42-55), store in variables
    2. write and execute a query stores user data in a table (line 59)
    
    
PAGE 3: select interest fields from database and package into JSON, send to client. Receive JSON on interests, interpret and store in database
    1. search database for interests, select the interest (key name, key id) -- fetchall(), iterate through tuple and select data, reformat in a JSON file
    2. take interest data, write it into a JSON file, and export to webclient
    ---- user inputs data, JS collects user input and stores in JSON file ----
    3. read JSON file and store user interests in variables
    4. write query that inserts the user insterests into the database
    
PAGE 4: select class information from database and send it to webclient as JSON
    1. write a query that gets class info from the database and stores it as strings
    2. write a JSON file, and format that data inside the JSON file in JSON format
    3. push JSON file to webclient
    
    
'''
    










'''
UNUSED CODE:

data_in = json.loads(fhandle)

for item in data_in:
    print('Name: ', item['fname'])
    print('Email: ', item['email'])
'''
app.run(host='0.0.0.0', debug=True, port=5000)