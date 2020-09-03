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
    if (startdate == 'TBD'):
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
    input("Send?")
    #email

    # student_fname = "Vikram"
    # class_name = "Fun & Games with Python"
    # teacher_name = "Vikram Anantha"
    # brief_summary = "Python. In the beginning, we will go over fundamentals of Python / Coding, so if you don't know how to code, then that's fine. We will then go over a graphics module named tkinter, and then we will code games that you probably know"
    # time_est = "1:00 - 2:30 pm"
    # time_cst = "12:00 - 1:30 pm"
    # first_day = "Aug 31"
    # last_day = "Sept 4"
    # zoom_link = "https://us02web.zoom.us/j/82884263265?pwd=TzA1NkhqbFl0ZjlobldJU0VtMEEvQT09"
    # prerequisite = """\
    # Make sure you also download Python IDLE. A video on how to do that is linked <a href="https://drive.google.com/open?id=1QOzSMw_XUD9836v7px5y0fp3wGpVKbSa">here</a>.
    # Make sure you download Python IDLE on the computer you will use for class, and try to use the same computer for class the whole week. If you are having trouble downloading it, then we will spend the first few minutes of class downloading it. To make sure that Python IDLE downloaded correctly, open Python IDLE, and paste this command in: <br>
    # <br>
    # <i>print("Hello World")</i><br>
    # <br>
    # When you press enter, IDLE should reply with "Hello World" in blue. If that happens, then IDLE works. Make sure you download and test IDLE before class on Monday.
    # """
    message = MIMEMultipart("alternative")
    message["Subject"] = subject.format(class_name)
    message["From"] = "HELM Learning"
    message["To"] = email

    # html = """\
    # <html>
    # <body>
    #     <p>Hello %s,<br>
    #     Thank you for signing up for %s at HELM Learning! My name is %s, and I am excited to be your teacher! In this class, we will be learning about %s. I am excited to have you, and I can’t wait to start! Please read some logistical information about our class, and email me back if you have any questions!<br>
    #     <br>
    #     <strong>Class Time:</strong> <br>%s EST, <br>%s CST <br>

    #     <br>
    #     <strong>Dates:</strong> <br>%s, %s - %s, %s (5 Weeks, once per week)<br>
    #     <br>
    #     <strong>How to access:</strong> <br>Here is a Zoom meeting link: <a href="%s">%s</a>. When you click on the link, it will open Zoom, or if you do not have it, it will download Zoom.<br>
    #     <br>
    #     <strong>What to do before class:</strong> <br>Before class starts on Monday, make sure you have a way to access zoom, preferably by a laptop or a tablet. %s.<br>
    #     <br>
    #     <strong>If you cannot make this course or any of the classes, please let me know.</strong><br>
    #     <br>
    #     Please stay safe, and let me know if you have any questions.<br>
    #     <br>
    #     Thank you,<br>
    #     <br>
    #     %s,<br>
    #     %s<br>
    #     HELM Learning<br>

    #     (this email was sent with Python)

    #     </p>
    # </body>
    # </html>
    # """ % (student_fname, class_name, teacher_name, brief_summary, time_est, time_cst, day, first_day, day, last_day, zoom_link, zoom_link, prerequisite, teacher_name, class_name)

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

class_name = "python"
student_fname = "Vikram Anantha"
email = 'vikramanantha@gmail.com'

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
