def gettime(starttime, endtime):
    if (starttime == 'TBD'):
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
    if (startdate == None):
        return ['TBD', 'TBD']
    sdate = str(startdate).split("-")
    edate = str(enddate).split("-")
    start_date = months[int(sdate[1])] + ' ' + sdate[2] + ', ' + sdate[0]
    end_date = months[int(edate[1])] + ' ' + edate[2] + ', ' + edate[0]
    return [start_date, end_date]

def send(name_of_email, subject, content, student_fname, email, pemail, list_of_content):
    port = 465
    sender = "helmlearning2020@gmail.com"
    password = "h3lml3arning"
    input("Send?")
    message = MIMEMultipart("alternative")
    message["Subject"] = subject.format(list_of_content[0])
    message["From"] = "HELM Learning"
    message["To"] = email

    html = content.format(student_fname, list_of_content[0], list_of_content[1], list_of_content[2], list_of_content[3], list_of_content[4], list_of_content[7], list_of_content[5], list_of_content[7], list_of_content[6], list_of_content[8], list_of_content[8], list_of_content[9], list_of_content[1], list_of_content[0])
    print(html)
    part2 = MIMEText(html, "html")
    message.attach(part2)

    context = ssl.create_default_context()

    with s.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(sender, password)
        server.sendmail(sender, email, message.as_string())
        server.sendmail(sender, pemail, message.as_string())

import smtplib as s
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import numpy
import mysql.connector
from mysql.connector import errorcode
import pandas as pd
config = {
    'user': 'helmlearning',
    'password': 'H3lml3arning',
    'host': '127.0.0.1', #52.21.172.100:22
    'port': '3306',
    'database': 'HELM_Database'
}
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

class_name = "yoplait"
# student_fname = "Vikram Anantha"
#email = 'vikramanantha@gmail.com'

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
db = "HELM_Database"
cnx = create_connection()
cursor = cnx.cursor(buffered=True)
email_to_send = input("E1, E2,E3, or E4?").lower()
cursor.execute("show columns from {}.students".format(db))

sql = 'SELECT Email_Address, Parent_Email, Student_Name FROM students WHERE id = {}'
sql2 = 'SELECT name, teacher, e1_summary, starttime, endtime, startdate, enddate, day, zoom, e1_additionalwork FROM classes WHERE short_name = "%s";' % (class_name[0].upper() + class_name[1:])
sql3 = 'SELECT subject, content FROM templates WHERE name="{}"'.format(email_to_send)
sql4 = 'SELECT student_id FROM classes_to_students WHERE class_id = {}'
sql5 = 'SELECT id FROM classes WHERE short_name = "{}"'.format(class_name)

cursor.execute(sql5)
class_id = cursor.fetchall()[0][0]

cursor.execute(sql4.format(class_id))
student_ids = cursor.fetchall()

cursor.execute(sql2)
class_info = cursor.fetchall()[0]

cursor.execute(sql3)
stuff = cursor.fetchall()[0]
subject = stuff[0]
content = stuff[1]
print(class_info)
print(student_ids)
for j in student_ids:
    i = j[0]
    cursor.execute(sql.format(i))
    emails = cursor.fetchall()[0]
    email = emails[0]
    pemail = emails[1]
    student_fname = emails[2]
    print(email + " " + pemail)
    send(email_to_send, subject, content, student_fname, email, pemail, [class_info[0], class_info[1], class_info[2], gettime(class_info[3], class_info[4])[0], gettime(class_info[3], class_info[4])[1], getdate(class_info[5], class_info[6])[0], getdate(class_info[5], class_info[6])[1], class_info[7], class_info[8], class_info[9]])

cnx.commit()
cursor.close()
cnx.close()

#tutorial at https://realpython.com/python-send-email/
