#from timed_email_sending import getdate, gettime
import smtplib as s
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import numpy
import mysql.connector
from mysql.connector import errorcode
import pandas as pd
from helper_functions import *

db = "HELM_Database"
cnx = create_connection()
cursor = cnx.cursor(buffered=True)
choice = input("Add or Edit? ").lower()
class_name = input("class / short_name? ").lower()
class_name = class_name[0].upper() + class_name[1:]
if (choice == "add"):
    n = input("name? ")
    t = input("Teacher_name? ")
    e = input("email? ")
    d = input("description? ")
    st = input("starttime? ")
    et = input("endtime? ")
    sd = input("startdate? ")
    ed = input("enddate? ")
    da = input("day? ")
    a = input("ages? ")
    z = input("zoom? ")
    sc = input("student_cap? ")
    cs = input("class_started? ")
    sql = "INSERT INTO classes (name, short_name, teacher, email, description, starttime, endtime, startdate, enddate, day, ages, zoom, student_cap, class_started) VALUES('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')"
    sql = sql.format(n, class_name, t, e, d, st, et, sd, ed, da, a, z, sc, cs)
    cursor.execute(sql)
    while True:
        more = input("Anything else? (type !help to see options)")
        if (more == "!help"):
            print("You can choose from")
            print("  e1_summary\n  e1_additionalwork\n  e3_briefdescription\n  e4_continuingfurther")
            continue
        if (more == "" or more == None):
            break
        res = input("What is the input for this? ")
        sql2 = "UPDATE classes SET {} = '{}' WHERE short_name = '{}'".format(more, res, class_name)
        cursor.execute(sql2)
        cnx.commit()
elif (choice == "edit"):
    while True:
        more = input("What do you want to update? (type !help to see options) ")
        if (more == "!help"):
            print("You can choose from")
            print("  teacher\n  email\n  starttime\n  endtime\n  startdate\n  enddate\n  day\n  zoom\n  student_cap\n  e1_summary\n  e1_additionalwork\n  e3_breifdescription\n  e4_continuingfurther\n  class_started")
            continue
        if (more == "" or more == None):
            break
        res = input("What is the input for this? ")
        sql2 = "UPDATE classes SET {} = '{}' WHERE short_name = '{}'".format(more, res, class_name)
        sql3 = "SELECT {} FROM classes WHERE short_name = '{}'".format(more, class_name)
        cursor.execute(sql3)
        before = cursor.fetchall()[0][0]
        cursor.execute(sql2)
        cursor.execute(sql3)
        after = cursor.fetchall()[0][0]

        print("Updated {} from {} to {}".format(more, before, after))
        cnx.commit()
    send_e1 = input("Should I send E1/E2? ")
    if (send_e1 == "yes"):
        import timed_email_sending

cnx.commit()
cursor.close()
cnx.close()
