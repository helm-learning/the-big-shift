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
app = flask.Flask(__name__)
app.config["DEBUG"] = True

config = {
    'user': 'helmlearning',
    'password': 'H3lml3arning',
    'host': '127.0.0.1', #52.21.172.100:22
    'port': '3306',
    'database': 'HELM_Database'
}
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


# conn=MySQLdb.connect(host='helmlearningdatabase-1.cnoqlueuri3g.us-east-1.rds.amazonaws.com', database='HELM_Test_Database', user='helmlearning',passwd='H3lml3arning')
@app.route('/page1/v1/resources/page1-receive', methods=['GET'])
def page1_receive():
    cnx = create_connection()
    cursor = cnx.cursor(buffered=True)
    fhandle = "page1-send.json"

    with open(fhandle, 'r') as j:
        contents = json.loads(j.read())
        print(contents)

    fname = ''
    email = ''
    #for item in contents:
    fname = contents['fname']
    email = contents['email']
    class_name = contents['class']
    print('Name: ', fname)
    print('Email: ', email)
    print('Class: ', class_name)


    # query_count = "SELECT COUNT(name) FROM students WHERE id=107"
    query = "SELECT * FROM students WHERE Student_Name = '{}' AND Email_Address = '{}'".format(fname, email)
    sql2 = "SELECT * FROM classes WHERE short_name = '{}'".format(class_name)
    # query_count = "SELECT COUNT(name) FROM students WHERE name = %s AND email = %s"

    # count = cursor.execute(query_count, adr)
    # count = cursor.execute(query_count)

    determinator = 4
        
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.execute(sql2)
    classes = cursor.fetchall()
        
    print(result)
        
    if result == []:
        print('none')
        determinator = 2
        
    # else:
    #     for r in result:
    #         print(r)

    if classes == []:
        determinator = -1

    print(determinator)
    cnx.commit()

    # close the cursor and database connection
    cursor.close()
    cnx.close()

    data = {
        "output": determinator
    }

    # with open('page1-receive.json', 'w') as outfile:
    #     json.dump(data, outfile)
    return jsonify(data)



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
app.run()