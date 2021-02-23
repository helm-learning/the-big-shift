#!/home/myuser/bin/python
import sys; sys.path.append('/home/ec2-user/anaconda3/lib/python3.8/site-packages/mysql')
import smtplib as s
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import numpy
import mysql.connector
from mysql.connector import errorcode
import pandas as pd
import numpy as np
import time

config = {
    'user': 'helmlearning',
    'password': 'H3lml3arning',
    'host': 'helmlearningdatabase-1.cnoqlueuri3g.us-east-1.rds.amazonaws.com', #52.21.172.100:22
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

def connect():
    db = "HELM_Database"
    cnx = create_connection()
    cursor = cnx.cursor(buffered=True)
    return cursor

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
    print(sdate)
    start_date = months[int(sdate[1])] + ' ' + sdate[2] + ', ' + sdate[0]
    end_date = months[int(edate[1])] + ' ' + edate[2] + ', ' + edate[0]
    return [start_date, end_date]

def encrypt(val, change):
    enc = ""
    count = 0
    for a in val:
        if count % 2 == 0:
            enc += chr((ord(a) + change) % 127)
        else:
            enc += chr((ord(a) - change) % 127)
    return enc

def decrypt(val, change):
    enc = ""
    count = 0
    for a in val:
        if count % 2 == 0:
            enc += chr((ord(a) - change) % 127)
        else:
            enc += chr((ord(a) + change) % 127)
    return enc

# print(decrypt(encrypt("H3lping3v3ryon3", 26), 26))
# print(encrypt("admin.36912", 10))
# print(decrypt("knwsx8=@C;<", 10))
