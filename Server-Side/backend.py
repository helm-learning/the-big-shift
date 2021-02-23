#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 22 12:53:56 2020
Author: Vikram Anantha
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
from flask import request, jsonify, make_response
from flask_cors import CORS
import smtplib as s
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import numpy
import mysql.connector
from mysql.connector import errorcode
import pandas as pd
from datetime import datetime, timedelta
import helper_functions as hf
import recommendation_alg as reco
import string
import random
import time
app = flask.Flask(__name__)
app.config["DEBUG"] = True
CORS(app, resources = {r"/api/v1/*": {"origins": "*"}})
#print("Alloo")
config = {
    'user': 'helmlearning',
    'password': 'H3lml3arning',
    'host': 'helmlearningdatabase-1.cnoqlueuri3g.us-east-1.rds.amazonaws.com', #52.21.172.100:22
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
        if (int(stime[0]) > 12):
            stime[0] = int(stime[0]) - 12
    else:
        startam = "am"
    if (int(etime[0]) >= 12):
        endam = "pm"
        if (int(etime[0]) > 12):
            etime[0] = int(etime[0]) - 12
    else:
        endam = "am"
    time_est = str(stime[0]) + ":" + str(stime[1]) + startam + " - " + str(etime[0]) + ":" + str(etime[1]) + endam
    stime[0] = int(str(starttime).split(":")[0]) - 1
    etime[0] = int(str(endtime).split(":")[0]) - 1

    if (int(stime[0]) >= 12):
        startam = "pm"
        if (int(stime[0]) > 12):
            stime[0] = int(stime[0]) - 12
    else:
        startam = "am"
    if (int(etime[0]) >= 12):
        endam = "pm"
        if (int(etime[0]) > 12):
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
    start_date = months[int(sdate[1])] + ' ' + sdate[2] + ' ' + sdate[0]
    end_date = months[int(edate[1])] + ' ' + edate[2] + ' ' + edate[0]
    return [start_date, end_date]

def sende0(subject, content, student_fname, email, pemail, class_name, teacher_name, teacher_email, description):
    port = 465
    sender = "helmlearning2020@gmail.com"
    password = "h3lml3arning"
    #input("Send?")
    message = MIMEMultipart("alternative")
    message["Subject"] = subject.format(class_name)
    message["From"] = "HELM Learning"
    message["To"] = email

    html = content.format(student_fname, class_name, class_name, teacher_name, teacher_email, description, teacher_name, class_name)
    #print(html)
    #part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")
    #message.attach(part1)
    message.attach(part2)

    context = ssl.create_default_context()

    with s.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(sender, password)
        server.sendmail(sender, email, message.as_string())
        server.sendmail(sender, pemail, message.as_string())
        print()
        print("%s, %s, %s" % (student_fname, email, pemail))
        print(class_name)
        print("Sent E0!")
        print()

def sende1(subject, content, student_fname, email, pemail, class_name, teacher_name, brief_summary, time_est, time_cst, first_day, last_day, day, zoom_link, prerequisite, temail, skipclass=None):
    weeklongdates = {
        "winter": "Dec 28 2020 - Jan 1 2021"
    }
    port = 465
    sender = "helmlearning2020@gmail.com"
    password = "h3lml3arning"
    #input("Send?")
    message = MIMEMultipart("alternative")
    message["Subject"] = subject.format(class_name)
    message["From"] = "HELM Learning"
    message["To"] = email
    #print(zoom_link + "asdf")
    #print(zoom_link == "")
    #print(zoom_link == None)
    if zoom_link == "":
        zoom_link = "TBD"
    if day == "":
        day = "TBD"
    if (" and " in teacher_name):
        content = content.replace("My name is", "We are")
        content = content.replace(", and I am excited to be your teacher!", ", and we are excited to be your teachers!")
    if (skipclass != None):
        content = content.replace("5 Weeks, once per week)", "5 Weeks, once per week)<br><strong>{}</strong>".format(skipclass))
    if(prerequisite == None):
        prerequisite = ""
    
    if "weeklong" in day:
        content = content.replace("5 Weeks, once per week)", "5 days in one week, Mon-Fri)")
        html = content.format(student_fname, class_name, teacher_name, brief_summary, time_est, time_cst, "Monday", first_day, "Friday", last_day, zoom_link, zoom_link, prerequisite, teacher_name, temail, class_name)
    else:
        html = content.format(student_fname, class_name, teacher_name, brief_summary, time_est, time_cst, day, first_day, day, last_day, zoom_link, zoom_link, prerequisite, teacher_name, temail, class_name)
    #print(html)
    #part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")
    #message.attach(part1)
    message.attach(part2)

    context = ssl.create_default_context()

    with s.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(sender, password)
        server.sendmail(sender, email, message.as_string())
        server.sendmail(sender, pemail, message.as_string())
        print()
        print("%s, %s, %s" % (student_fname, email, pemail))
        print(class_name)
        print("Sent E1!")
        print()

def sende2(subject, content, student_fname, email, pemail, class_name, teacher_name):
    port = 465
    sender = "helmlearning2020@gmail.com"
    password = "h3lml3arning"
    #input("Send?")
    message = MIMEMultipart("alternative")
    message["Subject"] = subject.format(class_name)
    message["From"] = "HELM Learning"
    message["To"] = email

    html = content.format(student_fname, class_name, teacher_name, class_name)
    #print(html)
    #part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")
    #message.attach(part1)
    message.attach(part2)

    context = ssl.create_default_context()

    with s.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(sender, password)
        server.sendmail(sender, email, message.as_string())
        server.sendmail(sender, pemail, message.as_string())
        print()
        print("%s, %s, %s" % (student_fname, email, pemail))
        print(class_name)
        print("Sent E2!")
        print()

def connect_to_send(student_fname, email, class_name):
    db = "HELM_Database"
    cnx = create_connection()
    cursor = cnx.cursor(buffered=True)
    cursor.execute("show columns from {}.students".format(db))
    sql0 = 'SELECT class_started, day, student_cap, final_student, last_student FROM classes WHERE short_name = "%s"' % (class_name[0].upper() + class_name[1:])
    cursor.execute(sql0)
    le_stuffe = cursor.fetchall()[0]
    #print(le_stuffe)
    #print(zoom)
    sql = 'SELECT Email_Address, Parent_Email FROM students WHERE Student_Name = "%s" AND Email_Address = "%s"' % (student_fname, email)
    if (le_stuffe[0] == 0 and le_stuffe[1] != ''):
        if (le_stuffe[2] > -1 and le_stuffe[3] != None):
            sql2 = 'SELECT name, teacher FROM classes WHERE short_name = "%s";' % (class_name)
            email_name = "e2"
        elif (le_stuffe[2] == -1):
            email_name = "e1"
            sql2 = 'SELECT name, teacher, e1_summary, starttime, endtime, startdate, enddate, day, zoom, e1_additionalwork, email FROM classes WHERE short_name = "%s";' % (class_name[0].upper() + class_name[1:])
        else:
            email_name = "e1"
            sql2 = 'SELECT name, teacher, e1_summary, starttime, endtime, startdate, enddate, day, zoom, e1_additionalwork, email FROM classes WHERE short_name = "%s";' % (class_name[0].upper() + class_name[1:])
            sqlwl2 = 'SELECT id FROM classes WHERE short_name = "%s"' % class_name
            cursor.execute(sqlwl2)
            class_id = cursor.fetchall()[0][0]
            sqlwl1 = 'SELECT timestamp FROM classes_to_students WHERE class_id = "%s" AND timestamp > "%s"' % (class_id, le_stuffe[4])
            cursor.execute(sqlwl1)
            wl_info = cursor.fetchall()
            #print(wl_info)
            if (len(wl_info) > le_stuffe[2]):
                
                # print(class_id)
                # sqlwl2 = 'SELECT id FROM students WHERE Student_Name = "%s"' % student_fname
                # cursor.execute(sqlwl2)
                # student_id = cursor.fetchall()[0][0]
                # print(student_id)
                # sqlwl3 = 'SELECT timestamp FROM classes_to_students WHERE class_id = "%s" AND student_id = "%s"' % (class_id, student_id)
                # cursor.execute(sqlwl3)
                # timestamp_for_ssu = cursor.fetchall()
                # print(">>>" + str(timestamp_for_ssu))
                # timestamp_for_ssu = timestamp_for_ssu[len(timestamp_for_ssu)-1][0]
                # print(timestamp_for_ssu)
                # sqlwl4 = 'UPDATE classes SET final_student = "%s"' % timestamp_for_ssu
                # print(sqlwl4)
                # cursor.execute(sqlwl4)

                #print(">>>" + str(le_stuffe[2]))
                #print(">>>" + str(wl_info[le_stuffe[2]]))
                sqlwl3 = 'UPDATE classes SET final_student = "%s" WHERE short_name = "%s"' % (wl_info[le_stuffe[2]-1][0], class_name)
                #print(sqlwl3)
                cursor.execute(sqlwl3)
                sql2 = 'SELECT name, teacher FROM classes WHERE short_name = "%s";' % (class_name)
                email_name = "e2"
            
    else: 
        email_name = "e0"
        sql2 = 'SELECT name, teacher, email, description FROM classes WHERE short_name = "%s";' % (class_name[0].upper() + class_name[1:])
    sql3 = 'SELECT subject, content FROM templates WHERE name="%s"' % email_name
    #print(sql2)
    #print(email_name)
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
    #print(class_info)
    #print(email)
    # if (le_stuffe[0] == 0 and le_stuffe[1] != ''):
    #     if (le_stuffe[2] > -1 and le_stuffe[3] != None):
    #         sende2(subject, content, student_fname, email, pemail, class_info[0], class_info[1])
    #     else:
    #         sende1(subject, content, student_fname, email, pemail, class_info[0], class_info[1], class_info[2], gettime(class_info[3], class_info[4])[0], gettime(class_info[3], class_info[4])[1], getdate(class_info[5], class_info[6])[0], getdate(class_info[5], class_info[6])[1], class_info[7], class_info[8], class_info[9])
    # else:
    #     sende0(subject, content, student_fname, email, pemail, class_info[0], class_info[1], class_info[2], class_info[3])

    if email_name == "e0":
        sende0(subject, content, student_fname, email, pemail, class_info[0], class_info[1], class_info[2], class_info[3])
    elif email_name == "e1":
        import datetime
        skipclass = None
        for i in skipping_weeks:
            if class_info[5] < datetime.date(i[0], i[1], i[2]) and class_info[6] > datetime.date(i[0], i[1], i[2]):
                skipclass = i[3]
        from datetime import datetime
        sende1(subject, content, student_fname, email, pemail, class_info[0], class_info[1], class_info[2], gettime(class_info[3], class_info[4])[0], gettime(class_info[3], class_info[4])[1], getdate(class_info[5], class_info[6])[0], getdate(class_info[5], class_info[6])[1], class_info[7], class_info[8], class_info[9], skipclass)

    else:
        sende2(subject, content, student_fname, email, pemail, class_info[0], class_info[1])

    cnx.commit()
    cursor.close()
    cnx.close()

    if (email_name == "e2"):
        return 1
    else:
        return 0

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
    return "<h1>Welcome!!</h1>"

@app.route('/api/v1/resources/page0-to-next-page', methods=['GET'])
def page0_receive():
    cnx = create_connection()
    cursor = cnx.cursor(buffered=True)
    query_params = request.args
    id = query_params.get('id')
    #print(class_name)
    id = decode(id)
    sql = "SELECT * FROM students WHERE id='{}'".format(id)
    cursor.execute(sql)
    stufe = cursor.fetchall()
    is_correct = False
    if len(stufe) > 0:
        is_correct = True
    is_correct = False
    if len(stufe) > 0:
        data = {
            "is_correct": True
        }
    else:
        data = {
            "is_correct": False
        }
    
    cnx.commit()
    cursor.close()
    cnx.close()
    
    return jsonify(data)


@app.route('/api/v1/resources/page0-data', methods=['GET'])
def page0_data():
    cnx = create_connection()
    cursor = cnx.cursor(buffered=True)
    query_params = request.args
    id = query_params.get('id')
    class_name = query_params.get('class')
    class_name = class_name.replace('-', ' ')
    id = decode(id)
    sql = "SELECT * FROM students WHERE id='{}'".format(id)
    cursor.execute(sql)
    stufe = cursor.fetchall()
    if (len(stufe) == 0):
        return jsonify({})
    timestamp = datetime.now()
    cursor.execute("SELECT id FROM classes WHERE short_name = '{}'".format(class_name))
    sb = cursor.fetchall()[0][0]
    sql = 'INSERT INTO classes_to_students_viewing (timestamp, class_id, student_id) VALUES("{}", "{}", "{}")'.format(timestamp, sb, id)
    cursor.execute(sql)

    print("\n\nPAGE0 DATA\n%s %s\n\n" % (id, class_name))

    cnx.commit()
    cursor.close()
    cnx.close()
    return jsonify({})

@app.route('/api/v1/resources/page4-data', methods=['GET'])
def page4_data():
    cnx = create_connection()
    cursor = cnx.cursor(buffered=True)
    query_params = request.args
    id = query_params.get('id')
    class_name = query_params.get('class')
    ranking = query_params.get('ranking')
    class_name = class_name.replace('-', ' ')
    id = decode(id)
    time.sleep(2)
    sql = "SELECT * FROM students WHERE id='{}'".format(id)
    cursor.execute(sql)
    stufe = cursor.fetchall()
    if (len(stufe) == 0):
        return jsonify({})
    timestamp = datetime.now()
    cursor.execute("SELECT id FROM classes WHERE short_name = '{}'".format(class_name))
    sb = cursor.fetchall()[0][0]
    sql = 'INSERT INTO classes_to_students_reco (timestamp, class_id, student_id, ranking) VALUES("{}", "{}", "{}", "{}")'.format(timestamp, sb, id, ranking)
    cursor.execute(sql)  
    print("\n\nPAGE4 DATA\n%s %s %s\n\n" % (id, class_name, ranking))
    cnx.commit()
    cursor.close()
    cnx.close()
    return jsonify({})  


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
    class_name = class_name.replace('-', ' ')
    #print(class_name)
    print()
    print('Name: ', fname)
    print('Email: ', email)
    print('Class: ', class_name)
    cnx.commit()
    query = "SELECT * FROM students WHERE Student_Name = '{}' AND (Email_Address = '{}' OR Parent_Email = '{}')".format(fname, email, email)
    sql2 = "SELECT * FROM classes WHERE short_name = '{}'".format(class_name)
    determinator = 4
    cursor.execute(query)
    result = cursor.fetchall()
    print(result)
    cursor.execute(sql2)
    classes = cursor.fetchall()
    some_random_data = get_student_id(fname=fname, email=email, status=1)
    print(type(some_random_data))
    if classes == []:
        determinator = -1
        data = {
            "output":determinator, 
            "fname": fname,
            "email": email,
            "Student_id_hashed": some_random_data["Student_id_hashed"],
            }
    elif result == []:
        determinator = 2
        fname = fname.replace(' ', '$')
        data = {
            "output":determinator, 
            "fname": fname,
            "email": email,
            "Student_id_hashed": some_random_data["Student_id_hashed"],
            }
    else:
        data = {
            "output": determinator,
            "fname": result[0][2].replace(' ', '$'),
            "email": result[0][3],
            "pemail": result[0][4],
            "Student_id_hashed": some_random_data["Student_id_hashed"],
        }
    
    print("Next Page: %s" % determinator)
    print()
    cnx.commit()
    cursor.close()
    cnx.close()
    
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
    timestamp = datetime.now()
    #sql2 = 'INSERT INTO students (Timestamp, Student_Name, Email_Address, Parent_Email) VALUES("{}", "{}", "{}", "{}")'.format(timestamp, "Ria", "vikramanantha@gmail.com", "dasmartone3141@gmail.com")
    sql = 'INSERT INTO students (Timestamp, Student_Name, Email_Address, Parent_Email, City, State, Grade, Heard_about_us) VALUES("{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}")'.format(timestamp, fname, email, pemail, town, state, age, hearabout)
    #print("PAGE 2 IS WORKING %s" % sql)
    # print(sql)
    cnx.commit()
    cursor.execute(sql)

    cnx.commit()
    cursor.close()
    cnx.close()

    some_random_data = get_student_id(fname=fname, email=email, status=1)

    data = {
        "Student_id_hashed": some_random_data['Student_id_hashed'],
    }
    return jsonify(data)

@app.route('/api/v1/resources/page4-receive', methods=['GET'])
def get_class_info():
    cnx = create_connection()
    cursor = cnx.cursor(buffered=True)
    query_params = request.args
    if (query_params.get('pemail') != None):
        timestamp = datetime.now()
        sql2 = 'INSERT INTO students (Timestamp, Student_Name, Email_Address, Parent_Email) VALUES("{}", "{}", "{}", "{}")'.format(timestamp, "Siddhi", "vikramanantha@gmail.com", "dasmartone3141@gmail.com")
        cursor.execute(sql2)
        return "<h1></h1>"
    short_name_of_class = query_params.get('class')
    short_class_name = short_name_of_class[0].upper() + short_name_of_class[1:]
    short_class_name = short_name_of_class.replace('-', ' ')
    sql = "SELECT name, description, teacher, email, starttime, endtime, startdate, enddate, zoom, day, class_started, ages FROM classes WHERE short_name = '{}'".format(short_class_name)
    cursor.execute(sql)
    result = cursor.fetchall()
    #print(result)
    class_name = result[0][0]
    description = result[0][1]
    teacher = result[0][2]
    email = result[0][3]
    starttime = result[0][4]
    endtime = result[0][5]
    startdate = result[0][6]
    enddate = result[0][7]
    zoom = result[0][8]
    day = result[0][9]
    class_started = result[0][10]
    ages = result[0][11]
    time = gettime(starttime, endtime)[0]
    date0 = getdate(startdate, enddate)[0]
    date1 = getdate(startdate, enddate)[1]
    cnx.commit()
    cursor.close()
    cnx.close()
    if (class_started == 1 or day == ""):
        #print("Hello")
        weekoutput = "TBD"
        zoom = "TBD"
    else:
        if "weeklong" in day:
            weekoutput = "Monday - Friday, " + date0 + " - " + date1
        else:
            weekoutput = day + ", " + date0 + " - " + day + ", " + date1
        import datetime
        for i in skipping_weeks:
            if startdate < datetime.date(i[0], i[1], i[2]) and enddate > datetime.date(i[0], i[1], i[2]):
                weekoutput += i[3]
        from datetime import datetime
    output = {
        "Name": class_name,
        "Description": description,
        "Teacher": teacher,
        "Email": email,
        "Time": time,
        "Week": weekoutput,
        "Zoom": zoom,
        "Age": ages
    }
    return jsonify(output)

skipping_weeks = [
    [2020, 11, 23, " (skipping the week of Thanksgiving, <br>Nov 23 2020 - Nov 29 2020)"],
    [2020, 12, 21, " (skipping the weeks of Christmas and New Years, <br>Dec 21 2020 - Jan 3 2021)"],
    [2021, 2, 15, " (skipping the week of Feb break, <br>Feb 15 2021 - Feb 19 2021)"]
]

@app.route('/api/v1/resources/sendemail', methods=['GET'])
def to_send_email():
    cnx = create_connection()
    cursor = cnx.cursor(buffered=True)
    query_params = request.args
    short_name_of_class = query_params.get('class')
    short_name_of_class = short_name_of_class.replace("-", " ")
    
    

    sql_cid = 'SELECT id FROM classes WHERE short_name = "{}"'.format(short_name_of_class[0].upper() + short_name_of_class[1:])
    sql_check = 'SELECT COUNT(timestamp) FROM classes_to_students WHERE class_id = "{}" AND student_id = "{}" AND timestamp > "{}"'

    timestamp = datetime.now()
    sql_su = 'INSERT INTO classes_to_students (timestamp, class_id, student_id) VALUES("{}", "{}", "{}")'
    
    sid = query_params.get('id')

    some_random_data = get_student_id(id=sid, status=2)
    student_fname = some_random_data["Student_fname"]
    email = some_random_data["Student_email"]

    cursor.execute(sql_cid)
    cid = cursor.fetchall()[0][0]
    sb = 1
    output = 0
    if (sid != 2272):
        cursor.execute(sql_check.format(cid, sid, timestamp - timedelta(5)))
        num_of_sus = cursor.fetchall()[0][0]
        if num_of_sus == 0:
            cursor.execute(sql_su.format(timestamp,cid, sid))
            print("\nSuccessfully signed %s up!" % student_fname)
            sb = 0
            output = connect_to_send(student_fname, email, short_name_of_class)
    #print(sid)
    cnx.commit()
    cursor.close()
    cnx.close()
    return jsonify({"output": output, "su_success": sb})


@app.route('/api/v1/admin/getstudents', methods=['GET'])
def get_students():
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
    cnx = create_connection()
    cursor = cnx.cursor(buffered=True)
    query_params = request.args
    username = 'hElMlEaRnInG'
    password = 'mvemjsun'
    un = query_params.get('un')
    pw = query_params.get('pw')
    if (username != un or password != pw):
        return "<h1>You're bad and you should feel bad about yourself</h1>"
    class_name = query_params.get('class_name')
    class_name = class_name.replace('-', ' ')
    other_params = query_params.get('filter')
    if class_name == "[[class name]]" or class_name == "all":
        string = "<h2>Click on a link below to see the students for your class</h2>"
        cursor.execute("SELECT short_name FROM classes")
        classes_names_short = cursor.fetchall()
        cnx.commit()
        cursor.close()
        cnx.close()
        string += "<p>You can choose from <br>"
        for j in classes_names_short:
            i = j[0].lower()
            string += '<a href=http://52.21.172.100:5000/api/v1/admin/getstudents?un=hElMlEaRnInG&pw=mvemjsun&class_name=%s&filter=none>%s</a><br>' % (i.replace(' ', '-'), i[0].upper() + i[1:])
        return string
    sql = 'SELECT id, final_student, last_student FROM classes WHERE short_name = "%s"' % class_name
    sql2 = 'SELECT student_id, timestamp FROM classes_to_students WHERE class_id = "{}" AND student_id != "1925" AND student_id != "2272" AND student_id != "325" AND student_id != "2261"'
    sql3 = 'SELECT Student_Name, Email_Address, City, State, Grade, Heard_about_us FROM students WHERE id = "{}"'
    sql4 = 'SELECT COUNT(student_id) FROM classes_to_students WHERE class_id = "{}" AND student_id != "1925" AND student_id != "2272" AND student_id != "325" AND student_id != "2261"'

    cursor.execute(sql)
    
    class_info = cursor.fetchall()[0]
    class_id = class_info[0]
    cursor.execute(sql2.format(class_id))
    student_ids = cursor.fetchall()
    cursor.execute(sql4.format(class_id))
    num_students = cursor.fetchall()[0][0]
    student_info = []
    count = 0
    if class_info[-1] == None:
        other_params= "none"
    #student_info.append("Total Students: %s" % num_students)
    curr_count = 0
    for i in student_ids:
        count += 1
        cursor.execute(sql3.format(i[0]))
        students = cursor.fetchall()[0]
        if (other_params == "current"):
            if (i[1] > class_info[-1]):
                if (class_info[-2] == None or i[1] <= class_info[-2]):
                    student_info.append({
                        "1. Name": students[0], 
                        "2. State": students[3], 
                        "3. Grade": students[4],
                        "4. How they know about HELM": students[5],
                        "5. When they signed up": str(i[1])
                    })
                    curr_count += 1
        else:
            student_info.append({
                "1. Name": students[0], 
                "2. State": students[3], 
                "3. Grade": students[4],
                "4. How they know about HELM": students[5],
                "5. When they signed up": str(i[1])
            }
        )
    #print(student_info)
    cnx.commit()
    cursor.close()
    cnx.close()
    return_string = ""
    
    if (other_params == "current"):
        return_string = '<h1>You are viewing: Students in your current session of the {} class</h1><h2>Click <a href="http://52.21.172.100:5000/api/v1/admin/getstudents?un=hElMlEaRnInG&pw=mvemjsun&class_name={}&filter=none">here</a> to see all your students</h2>'.format(class_name, class_name)
    else:
        return_string = '<h1>You are viewing: All Students of the {} class</h1><h2>Click <a href="http://52.21.172.100:5000/api/v1/admin/getstudents?un=hElMlEaRnInG&pw=mvemjsun&class_name={}&filter=current">here</a> to see students in your current session</h2>'.format(class_name, class_name)
    return_string += "Total Students: %s<br>" % num_students
    if (other_params == "current"):
        return_string += "Current Students: %s<br>" % curr_count
    for i in student_info:
        return_string += "<br>"
        for j in i:
            return_string += "%s: %s <br>" % (j, i[j])
    return return_string


@app.route('/api/v1/resources/admin_get_class_info', methods=['GET'])
def admin_class_info():
    cnx = create_connection()
    cursor = cnx.cursor(buffered=True)
    query_params = request.args
    short_name_of_class = query_params.get('class')
    short_class_name = short_name_of_class.replace('-', ' ')
    the_filter = query_params.get('filter')
    sql = "SELECT name, short_name,description, starttime, endtime, startdate, enddate, zoom, day, ages FROM classes WHERE short_name = '{}'".format(short_class_name)
    cursor.execute(sql)
    result = cursor.fetchall()[0]
    class_name = result[0]
    short_name = result[1]
    description = result[2]
    starttime = result[3]
    endtime = result[4]
    startdate = result[5]
    enddate = result[6]
    zoom = result[7]
    day = result[8]
    age = result[9]

    time = gettime(starttime, endtime)[0] + " EST"
    date0 = getdate(startdate, enddate)[0]
    date1 = getdate(startdate, enddate)[1]
    if "weeklong" in day:
        weekoutput = "Monday - Friday, " + date0 + " - " + date1
    else:
        weekoutput = day + ", " + date0 + " - " + day + ", " + date1
    if startdate != None:
        import datetime 
        for i in skipping_weeks:
            if startdate < datetime.date(i[0], i[1], i[2]) and enddate > datetime.date(i[0], i[1], i[2]):
                weekoutput += i[3]
        from datetime import datetime
    else:
        weekoutput = "No session is currently scheduled"
        time = "No session is currently scheduled"
    

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
    sql = 'SELECT id, final_student, last_student FROM classes WHERE short_name = "%s"' % short_class_name
    sql2 = 'SELECT student_id, timestamp FROM classes_to_students WHERE class_id = "{}" AND student_id != "1925" AND student_id != "2272" AND student_id != "325" AND student_id != "2261" ORDER BY timestamp'
    sql25 = 'SELECT student_id, timestamp FROM classes_to_students WHERE class_id = "{}" AND timestamp > "{}" AND timestamp <= "{}" AND student_id != "1925" AND student_id != "2272" AND student_id != "325" AND student_id != "2261" ORDER BY timestamp'
    sql3 = 'SELECT Student_Name, Email_Address, City, State, Grade, Heard_about_us FROM students WHERE id = "{}"'
    sql4 = 'SELECT COUNT(student_id) FROM classes_to_students WHERE class_id = "{}" AND student_id != "1925" AND student_id != "2272" AND student_id != "325" AND student_id != "2261"'
    sql45 = 'SELECT COUNT(student_id) FROM classes_to_students WHERE class_id = "{}" AND timestamp > "{}" AND timestamp <= "{}" AND student_id != "1925" AND student_id != "2272" AND student_id != "325" AND student_id != "2261"'
    cursor.execute(sql)
    
    class_info = list(cursor.fetchall()[0])
    if class_info[-1] == None or class_info[-1] == "":
        class_info[-1] = "0000-00-00 00:00:00"
    if class_info[-2] == None or class_info[-2] == "":
        class_info[-2] = "9999-99-99 99:99:99"
    class_id = class_info[0]
    if (the_filter == "all"):
        cursor.execute(sql2.format(class_id))
    else:
        cursor.execute(sql25.format(class_id, class_info[-1], class_info[-2]))
    student_ids = cursor.fetchall()
    cursor.execute(sql4.format(class_id))
    num_students = cursor.fetchall()[0][0]
    cursor.execute(sql45.format(class_id, class_info[-1], class_info[-2]))
    num_students2 = cursor.fetchall()[0][0]
    
    student_info = []
    count = 0
    if (the_filter == "all"):
        student_info.append("Total Students: %s" % (num_students))
    else:
        student_info.append("Total Students: %s<br>Current Students: %s" % (num_students, num_students2))
    for i in student_ids:
        count += 1
        cursor.execute(sql3.format(i[0]))
        students = list(cursor.fetchall()[0])
        if students[2] == "" or students[2] == None:
            students[2] = "?"
        if students[4] == "" or students[4] == None:
            students[4] = "?"
        if students[5] == "" or students[5] == None:
            students[5] = "?"
        student_info.append([
            students[0], # name
            students[2] + ", " + students[3], # state
            students[4], # grade
            students[5], # know about us
            i[1].strftime("%b %d, %Y at %H:%M") # timestamp
        ])
    cnx.commit()
    cursor.close()
    cnx.close()



    output = {
        "Name": class_name,
        "Short name": short_name,
        "Description": description,
        "Time": time,
        "Week": weekoutput,
        "Age": age,
        "Zoom": zoom,
        "Students": student_info
    }
    
    return jsonify(output)  

@app.route('/api/v1/resources/get_all_classes', methods=['GET'])
def select_class():
    cnx = create_connection()
    cursor = cnx.cursor(buffered=True)
    sql = "SELECT name, short_name FROM classes ORDER BY short_name"
    cursor.execute(sql)
    classes = cursor.fetchall()
    cnx.commit()
    cursor.close()
    cnx.close()
    return jsonify(classes)

@app.route('/api/v1/resources/verifyteacher', methods=['GET'])
def verify_teacher():
    cnx = create_connection()
    cursor = cnx.cursor(buffered=True)
    query_params = request.args
    short_name_of_class = query_params.get('class')
    class_name = short_name_of_class.replace('-', ' ')
    email = query_params.get('email')
    pw = query_params.get('pw')

    ily = "SELECT email, teacher FROM classes WHERE short_name = '{}'"
    sb = "SELECT pw, cipher FROM verify"
    cursor.execute(ily.format(class_name))
    qwert = cursor.fetchall()
    class_email = qwert[0][0]
    teacher_name = qwert[0][1]
    print("\n%s is checking their class details!\n" % teacher_name)
    cursor.execute(sb)
    pws = list(cursor.fetchall())
    the_real_ones = []
    for i in pws:
        
        i = list(i)
        the_real_ones.append(hf.decrypt(i[0], i[1]))
    cnx.commit()
    cursor.close()
    cnx.close()
    if ((("and" in class_email and email in class_email.split(" and ")) or (email == the_real_ones[1]) or (email == class_email)) and (pw == the_real_ones[0])):
        return jsonify(
            {"output": 1}
        )
    else:
        return jsonify(
            {"output": 0}
        )

@app.route('/api/v1/resources/admin_action_buttons', methods=["GET"])
def action_buttons():
    cnx = create_connection()
    cursor = cnx.cursor(buffered=True)
    query_params = request.args
    action = query_params.get('action')
    short_name_of_class = query_params.get('class')
    class_name = short_name_of_class.replace('-', ' ')
    if (action == "copy"):
        #sql = 'SELECT id, final_student, last_student FROM classes WHERE short_name = "%s"' % class_name
        import timed_email_sending
        emails = timed_email_sending.ge(class_name, cursor)
        toreturn = ""
        for i in emails:
            toreturn += i[0] + ", " + i[1] + ", "
        return jsonify([toreturn])
    else:
        import timed_email_sending as tes
        tes.er2(class_name, cursor)
    cnx.commit()
    cursor.close()
    cnx.close()
    return jsonify(["hello"])

@app.route('/api/v1/resources/reco', methods=["GET"])
def run_reco():
    cnx = create_connection()
    cursor = cnx.cursor(buffered=True)
    query_params = request.args
    # fname = query_params.get('fname')
    # email = query_params.get('email')
    id = query_params.get('id')
    short_name_of_class = query_params.get('class')
    class_name = short_name_of_class.replace('-', ' ')

    some_random_data = get_student_id(id=id, status=2)
    fname = some_random_data["Student_fname"]
    email = some_random_data["Student_email"]

    cnx.commit()
    predictions = reco.predict(fname, email, class_name)
    print(predictions)
    biglist = []
    for i in predictions:
        cursor.execute("SELECT short_name, description FROM classes WHERE short_name = '{}'".format(i))
        class_detail_stuff_meaning_name_and_description = list(cursor.fetchall()[0])
        cursor.execute("SELECT name, description FROM classes WHERE short_name = '{}'".format(i))
        full_class_name = cursor.fetchall()[0][0]
        class_detail_stuff_meaning_name_and_description[1] = "<i>" + full_class_name + "</i>: " + class_detail_stuff_meaning_name_and_description[1]
        class_detail_stuff_meaning_name_and_description[1] = class_detail_stuff_meaning_name_and_description[1][:150] + "..."
        # Just a btw, the height of the box is set in page4.html around line 216, currently set at 140px
        biglist.append(class_detail_stuff_meaning_name_and_description)
    cnx.commit()
    cursor.close()
    cnx.close()
    return jsonify(biglist)

@app.route('/api/v1/resources/get_id', methods=["GET"])
def get_student_id(fname=None, email=None, id=None, status=0):
    # status 0: being called by js
    # status 1: being called to get id
    # status 2: being called to get name
    og_status = -1
    cnx = create_connection()
    cursor = cnx.cursor(buffered=True)
    if status == 0:
        og_status = 0
        query_params = request.args
        id = query_params.get('id')
        fname = query_params.get('fname')
        email = query_params.get('email')
        if fname == "__" or fname == None:
            status = 2
        else:
            status = 1
    cnx.commit()
    if status == 1:
        cursor.execute("SELECT id FROM students WHERE Student_Name = '{}' AND (Email_Address = '{}' OR Parent_Email = '{}')".format(fname, email, email))
        id = cursor.fetchall()
        if len(id) != 0:
            id = id[0][0]
            id = encode(id)
        else:
            id = 'fname=' + fname.replace(' ', '$') + '&email=' + email
    elif status == 2:
        id = decode(id)
        cursor.execute("SELECT Student_Name, Email_Address FROM students WHERE id = '{}'".format(id))
        student_info = cursor.fetchall()[0]
        fname = student_info[0]
        email = student_info[1]

    cnx.commit()
    cursor.close()
    cnx.close()

    if og_status == 0:
        return jsonify({
            "Student_fname": fname,
            "Student_email": email,
            "Student_id_hashed": id,
        })
    else:
        return {
            "Student_fname": fname,
            "Student_email": email,
            "Student_id_hashed": id,
        }


def encode(x):
    x = str(x)
    y = ""
    for i in x:
        for j in range(int(i)):
            y += random.choice(string.ascii_letters)
        y += "-"
    y = y[:-1]
    return y

def decode(y):
    ys = y.split('-')
    x = ""
    for i in ys:
        x += str(len(i))
    x = int(x)
    print(x)
    return x
    

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