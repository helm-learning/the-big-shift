#!/home/myuser/bin/python
not_sent_emails = []
import smtplib as s
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import numpy
import sys; sys.path.append('/home/ec2-user/anaconda3/lib/python3.8/site-packages/mysql')
import mysql.connector
from mysql.connector import errorcode
import pandas as pd
import helper_functions
def send(name_of_email, subject, content, student_fname, email, pemail, list_of_content, extra_content = None):
    port = 465
    sender = "helmlearning2020@gmail.com"
    password = "h3lml3arning"
    
    message = MIMEMultipart("alternative")
    message["Subject"] = subject.format(list_of_content[0])
    message["From"] = "HELM Learning"
    message["To"] = email

    if name_of_email == "e1":
        if extra_content != None: content = content.replace("5 Weeks, once per week)", extra_content)
        if "weeklong" in list_of_content[5]:
            content = content.replace("5 Weeks, once per week)", "5 days in a week, Mon-Fri)")
    
    elif name_of_email == "esa":
        breaf = list_of_content[0]
        list_of_content[0] = list_of_content[1]
        list_of_content[1] = breaf

    html = content.format(
        student_fname[0].upper() + student_fname[1:], 
        *list_of_content
    )

    
    # print(html)
    
    part2 = MIMEText(html, "html")
    message.attach(part2)
    context = ssl.create_default_context()
    

    with s.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(sender, password)
        try:
            #input("send?")
            server.sendmail(sender, email, message.as_string())
            server.sendmail(sender, pemail, message.as_string())
            print("Sent!\n")
        except:
            print("NOT SENT\n")
            not_sent_emails.append(email)
            not_sent_emails.append(pemail)


config = {
    'user': 'helmlearning',
    'password': 'H3lml3arning',
    'host': 'helmlearningdatabase-1.cnoqlueuri3g.us-east-1.rds.amazonaws.com', #52.21.172.100:22
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

skipping_weeks = [
    [2020, 11, 23, " (skipping the week of Thanksgiving, <br>Nov 23 2020 - Nov 29 2020)"],
    [2020, 12, 21, " (skipping the weeks of Christmas and New Years, <br>Dec 21 2020 - Jan 3 2021)"]
]

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
    

def e1(class_name, cursor):
    sql5 = 'SELECT id, last_student FROM classes WHERE short_name = "{}"'.format(class_name)
    sql4 = 'SELECT student_id FROM classes_to_students WHERE class_id = "{}" AND timestamp > "{}"'
    sql2 = 'SELECT name, teacher, e1_summary, starttime, endtime, day, startdate, day, enddate, zoom, zoom, e1_additionalwork, teacher, email, name FROM classes WHERE short_name = "%s";' % (class_name[0].upper() + class_name[1:])
    sql3 = 'SELECT subject, content FROM templates WHERE name="{}"'.format("e1")
    sql = 'SELECT Email_Address, Parent_Email, Student_Name FROM students WHERE id = {}'
    sql_e2 = 'SELECT student_cap FROM classes WHERE short_name = "{}"'.format(class_name)
    cursor.execute(sql_e2)
    student_cap = cursor.fetchall()[0][0]
    if student_cap != -1:
        e2(class_name, cursor)
        return
    cursor.execute(sql5)
    class_asdf = cursor.fetchall()[0]
    class_id = class_asdf[0]
    last_stud = class_asdf[1]

    if (last_stud == None):
        last_stud = "0000-00-00 00:00:00"
    cursor.execute(sql4.format(class_id, last_stud))
    student_ids = cursor.fetchall()

    cursor.execute(sql2)
    class_info = list(cursor.fetchall()[0])

    cursor.execute(sql3)
    stuff = cursor.fetchall()[0]
    email_info = []
    email_info.append(stuff[0])
    email_info.append(stuff[1])
    time_est = helper_functions.gettime(class_info[3], class_info[4])[0]
    time_cst = helper_functions.gettime(class_info[3], class_info[4])[1]
    class_info[3] = time_est
    class_info[4] = time_cst
    startdate = helper_functions.getdate(class_info[6], class_info[8])[0]
    enddate = helper_functions.getdate(class_info[6], class_info[8])[1]

    import datetime
    skipclass = None
    for i in skipping_weeks:
        if class_info[6] < datetime.date(i[0], i[1], i[2]) and class_info[8] > datetime.date(i[0], i[1], i[2]):
            skipclass = "5 Weeks, once per week)<br><strong>{}</strong>".format(i[3])

    class_info[6] = startdate
    class_info[8] = enddate

    if "weeklong" in class_info[5]:
        class_info[5] = "Monday"
        class_info[7] = "Friday"

    print(class_info)
    emails = []
    for j in student_ids:
        i = j[0]
        print(i)
        cursor.execute(sql.format(i))
        theemails = cursor.fetchall()[0]
        if (list(theemails) not in emails):
            emails.append(list(theemails))
    sql_teacher_email = "SELECT email,email,teacher FROM classes WHERE id = '{}'".format(class_id)
    cursor.execute(sql_teacher_email)
    teacher_info = list(cursor.fetchall()[0])
    print(emails.append(teacher_info))
    

    prep_to_send("e1", emails, email_info, class_info, qwert=[skipclass])

def e2(class_name, cursor):
    emails = []
    waitlist_emails = []
    sql = 'SELECT id FROM classes WHERE short_name = "%s"' % class_name
    sql2 = 'SELECT last_student, final_student FROM classes WHERE short_name = "%s"' % class_name
    sql3 = 'SELECT student_id, timestamp FROM classes_to_students WHERE class_id = "{}" AND timestamp > "{}" AND timestamp <= "{}"'
    sql35 = 'SELECT student_id, timestamp FROM classes_to_students WHERE class_id = "{}" AND timestamp > "{}"'
    sql4 = 'SELECT Email_Address, Parent_Email, Student_Name FROM students WHERE id = "{}"'
    sql5 = 'SELECT name, teacher, e1_summary, starttime, endtime, day, startdate, day, enddate, zoom, zoom, e1_additionalwork, teacher, email, name FROM classes WHERE short_name = "%s";' % (class_name[0].upper() + class_name[1:])
    sql55 = 'SELECT name, teacher, name FROM classes WHERE short_name = "%s";' % class_name
    sql6 = 'SELECT subject, content FROM templates WHERE name="e1"'
    sql65 = 'SELECT subject, content FROM templates WHERE name="e2"'
    print("1")
    cursor.execute(sql)
    class_id = cursor.fetchall()[0][0]
    print("2")
    cursor.execute(sql2)
    fila_student = cursor.fetchall()[0]
    print(fila_student[0])
    cursor.execute(sql3.format(class_id, fila_student[0], fila_student[1]))
    welcome_studentids = cursor.fetchall()
    print("4")
    cursor.execute(sql35.format(class_id, fila_student[1]))
    waitlist_studentids = cursor.fetchall()
    for i in welcome_studentids:
        cursor.execute(sql4.format(i[0]))
        student_info = cursor.fetchall()[0]
        if (student_info not in emails):
            emails.append(student_info)
    for i in waitlist_studentids:
        cursor.execute(sql4.format(i[0]))
        student_info = cursor.fetchall()[0]
        if (student_info not in waitlist_emails):
            waitlist_emails.append(student_info)
    print("5")
    cursor.execute(sql5)
    welcome_classinfo = list(cursor.fetchall()[0])
    # timeest = helper_functions.gettime(welcome_classinfo[3], welcome_classinfo[4])[0]
    # timecst = helper_functions.gettime(welcome_classinfo[3], welcome_classinfo[4])[1]
    # startdate = helper_functions.getdate(welcome_classinfo[5], welcome_classinfo[6])[0]
    # enddate = helper_functions.getdate(welcome_classinfo[5], welcome_classinfo[6])[1]
    # welcome_classinfo[3] = timeest
    # welcome_classinfo[4] = timecst
    # welcome_classinfo[5] = startdate
    # welcome_classinfo[6] = enddate
    # print(welcome_classinfo)
    time_est = helper_functions.gettime(welcome_classinfo[3], welcome_classinfo[4])[0]
    time_cst = helper_functions.gettime(welcome_classinfo[3], welcome_classinfo[4])[1]
    welcome_classinfo[3] = time_est
    welcome_classinfo[4] = time_cst
    startdate = helper_functions.getdate(welcome_classinfo[6], welcome_classinfo[8])[0]
    enddate = helper_functions.getdate(welcome_classinfo[6], welcome_classinfo[8])[1]

    import datetime
    skipclass = None
    for i in skipping_weeks:
        if welcome_classinfo[6] < datetime.date(i[0], i[1], i[2]) and welcome_classinfo[8] > datetime.date(i[0], i[1], i[2]):
            skipclass = "5 Weeks, once per week)<br><strong>{}</strong>".format(i[3])

    welcome_classinfo[6] = startdate
    welcome_classinfo[8] = enddate

    if "weeklong" in welcome_classinfo[5]:
        welcome_classinfo[5] = "Monday"
        welcome_classinfo[7] = "Friday"

    for i in range(len(welcome_classinfo)):
        if welcome_classinfo[i] == None:
            welcome_classinfo[i] = ''
    print("6")
    cursor.execute(sql55)
    waitlist_classinfo = cursor.fetchall()[0]
    print(waitlist_classinfo)
    print("7")
    cursor.execute(sql65)
    waitlist_emailinfo = cursor.fetchall()[0]
    print("7.5")
    cursor.execute(sql6)
    email_info = cursor.fetchall()[0]
    print("8")
    for i in range(0, len(welcome_classinfo)):
        if (welcome_classinfo[i] == None):
            welcome_classinfo[i] == ''
    for i in range(0, len(waitlist_classinfo)):
        if (waitlist_classinfo[i] == None):
            waitlist_classinfo[i] == ''

    sql_teacher_email = "SELECT email,email,teacher FROM classes WHERE id = '{}'".format(class_id)
    cursor.execute(sql_teacher_email)
    teacher_info = list(cursor.fetchall()[0])
    print(emails.append(teacher_info))
    prep_to_send("e2", emails, email_info, welcome_classinfo=welcome_classinfo, waitlist_emails=waitlist_emails, waitlist_emailinfo=waitlist_emailinfo, waitlist_classinfo=waitlist_classinfo)

def esa(class_name, cursor):
    classes = []
    emails = []
    #subject_area = input("Subject Area? ")
    while True:
        r = input("What classes? ").lower()
        if (r == 'stop' or r == None or r== ''):
            break
        classes.append(r[0].upper() + r[1:])
        
    sql = 'SELECT id FROM classes WHERE short_name = "{}"'
    sql2 = 'SELECT student_id FROM classes_to_students WHERE class_id = "{}"'
    sql3 = 'SELECT Email_Address, Parent_Email, Student_Name FROM students WHERE id = "{}"'
    sql4 = 'SELECT short_name, name, short_name, description, teacher, starttime, endtime, startdate, enddate, day FROM classes WHERE short_name = "{}"'
    sql5 = 'SELECT subject, content FROM templates WHERE name="esa"'


    qwert = {}
    print(classes)
    for k in classes:
        cursor.execute(sql.format(k))
        class_id = cursor.fetchall()[0][0]
        
        cursor.execute(sql2.format(class_id))
        students = cursor.fetchall()
        for qw in students:
            cursor.execute(sql3.format(qw[0]))
            emaillist = list(cursor.fetchall()[0])
            emaillist.append(k)
            if (list(emaillist) not in emails):
                emails.append(list(emaillist))
                qwert[emaillist[0]] = k

    cursor.execute(sql4.format(class_name))
    class_info = list(cursor.fetchall()[0])

    #class_info.insert(0, input("subject_area"))
    class_info[5] = helper_functions.gettime(class_info[5], class_info[6])[0]
    class_info.remove(class_info[6])
    if (helper_functions.getdate(class_info[6], class_info[7])[0] != "TBD"):
        if ("weeklong" in class_info[8]):
            class_info[6] = "Monday - Friday, " + helper_functions.getdate(class_info[6], class_info[7])[0] + " - " + helper_functions.getdate(class_info[6], class_info[7])[1]
        else:
            class_info[6] = class_info[8] + "s, " + helper_functions.getdate(class_info[6], class_info[7])[0] + " - " + helper_functions.getdate(class_info[6], class_info[7])[1]
    else:
        class_info[6] = "TBD"
    class_info.remove(class_info[7])
    class_info.remove(class_info[7])
    class_info.insert(2, "signup.helmlearning.com/page1.html?class=" + class_name.lower().replace(" ", "-"))
    class_info.insert(1, "[prev classes]")
    cursor.execute(sql5.format(email_to_send))
    email_info = list(cursor.fetchall()[0])

    
    prep_to_send("esa", emails, email_info, class_info, qwert=qwert)

def e3(class_name, cursor):
    emails = []
    sql = 'SELECT id FROM classes WHERE short_name = "{}"'
    sql2 = 'SELECT student_id, timestamp FROM classes_to_students WHERE class_id = "{}" AND timestamp > "{}" AND timestamp <= "{}"'
    sql6 = 'SELECT final_student FROM classes WHERE short_name = "{}"'
    sql3 = 'SELECT Email_Address, Parent_Email, Student_Name FROM students WHERE id = "{}"'
    sql4 = 'SELECT short_name, starttime, endtime, e3_briefdescription, zoom, zoom, teacher, name, final_student, last_student FROM classes WHERE short_name = "{}"'
    sql5 = 'SELECT subject, content FROM templates WHERE name="e3"'
    cursor.execute(sql.format(class_name))
    class_id = cursor.fetchall()[0][0]

    cursor.execute(sql4.format(class_name))
    class_info = list(cursor.fetchall()[0])
    if (class_info[-1] == None):
        class_info[-1] = "0000-00-00 00:00:00"

    cursor.execute(sql2.format(class_id, class_info[-1], class_info[-2]))
    student_ids = cursor.fetchall()
    cursor.execute(sql6.format(class_name))
    last_student = cursor.fetchall()[0][0]
    for i in student_ids:
        cursor.execute(sql3.format(i[0]))
        des_emaux = cursor.fetchall()[0]
        if (list(des_emaux) not in emails):
            emails.append(list(des_emaux))
        print(i[1])
        # print(final_student)
        # if (i[1] == last_student):
        #     print("BREAK")
        #     break
    #print(emails)
    
    class_info[1] = helper_functions.gettime(class_info[1], class_info[2])[0]
    class_info.remove(class_info[2])
    class_info.insert(1, input("Drive link: "))
    cursor.execute(sql5)
    email_info = cursor.fetchall()[0]
    print(class_info)

    sql_teacher_email = "SELECT email,email,teacher FROM classes WHERE id = '{}'".format(class_id)
    cursor.execute(sql_teacher_email)
    teacher_info = list(cursor.fetchall()[0])
    print(emails.append(teacher_info))

    prep_to_send("e3", emails, email_info, class_info)

def e4(class_name, cursor):
    emails = []
    #send e4
    
    sql = 'SELECT id FROM classes WHERE short_name = "{}"'
    sql2 = 'SELECT student_id, timestamp FROM classes_to_students WHERE class_id = "{}" AND timestamp > "{}" AND timestamp <= "{}"'
    sql3 = 'SELECT Email_Address, Parent_Email, Student_Name FROM students WHERE id = "{}"'
    sql4 = 'SELECT name, e4_continuingfurther, teacher, email, name, final_student, last_student FROM classes WHERE short_name = "{}"'
    sql5 = 'SELECT subject, content FROM templates WHERE name="e4"'

    cursor.execute(sql.format(class_name))
    class_id = cursor.fetchall()[0][0]

    cursor.execute(sql4.format(class_name))
    class_info = list(cursor.fetchall()[0])
    if (class_info[-1] == None):
        class_info[-1] = "0000-00-00 00:00:00"
    cursor.execute(sql2.format(class_id, class_info[-1], class_info[-2]))
    student_ids = cursor.fetchall()
    for i in student_ids:
        cursor.execute(sql3.format(i[0]))
        des_emaux = cursor.fetchall()[0]
        if (list(des_emaux) not in emails):
            emails.append(list(des_emaux))
        print(i[1])
    cursor.execute(sql5)
    email_info = cursor.fetchall()[0]
    print(class_info[-2])
    sql6 = "UPDATE classes SET final_student = null WHERE short_name = '{}'".format(class_name)
    sql7 = "UPDATE classes SET last_student = '{}' WHERE short_name = '{}'".format(class_info[-2], class_name)
    sql8 = "UPDATE classes SET class_started = 0 WHERE short_name = '{}'".format(class_name)
    sql9 = "UPDATE classes SET day = '' WHERE short_name = '{}'".format(class_name)
    sql10 = "UPDATE classes SET startdate = '0000-00-00' WHERE short_name = '{}'".format(class_name)
    sql11 = "UPDATE classes SET enddate = '0000-00-00' WHERE short_name = '{}'".format(class_name)
    cursor.execute(sql6)
    cursor.execute(sql7)
    cursor.execute(sql8)
    cursor.execute(sql9)
    cursor.execute(sql10)
    cursor.execute(sql11)

    #make sure to change the final student and the last student
    #also make sure to change the class_started
    #and the day and week
    print(class_info)

    sql_teacher_email = "SELECT email, email,teacher FROM classes WHERE id = '{}'".format(class_id)
    cursor.execute(sql_teacher_email)
    teacher_info = list(cursor.fetchall()[0])
    print(emails.append(teacher_info))

    prep_to_send("e4", emails, email_info, class_info)

def er1(class_name, cursor):
    emails = []
    sql = 'SELECT id FROM classes WHERE short_name = "{}"'
    sql2 = 'SELECT student_id, timestamp FROM classes_to_students WHERE class_id = "{}" AND timestamp > "{}" AND timestamp <= "{}"'
    sql3 = 'SELECT Email_Address, Parent_Email, Student_Name FROM students WHERE id = "{}"'
    sql4 = 'SELECT name, day, starttime, endtime, day, startdate, day, enddate, zoom, zoom, e1_additionalwork, teacher, name, final_student, last_student FROM classes WHERE short_name = "{}"'
    sql5 = 'SELECT subject, content FROM templates WHERE name="er1"'
    cursor.execute(sql.format(class_name))
    class_id = cursor.fetchall()[0][0]

    cursor.execute(sql4.format(class_name))
    class_info = list(cursor.fetchall()[0])
    if (class_info[-1] == None):
        class_info[-1] = "0000-00-00 00:00:00"
    if (class_info[-2] == "0000-00-00 00:00:00" or class_info[-2] == None):
        class_info[-2] = "9999-99-99 99:99:99"

    cursor.execute(sql2.format(class_id, class_info[-1], class_info[-2]))
    student_ids = cursor.fetchall()
    for i in student_ids:
        cursor.execute(sql3.format(i[0]))
        des_emaux = cursor.fetchall()[0]
        if (list(des_emaux) not in emails):
            emails.append(list(des_emaux))
        print(i[1])
    
    import datetime
    skipclass = None
    for i in skipping_weeks:
        if class_info[5] < datetime.date(i[0], i[1], i[2]) and class_info[7] > datetime.date(i[0], i[1], i[2]):
            skipclass = "5 Weeks, once per week)<br><strong>{}</strong>".format(i[3])

    if "weeklong" in class_info[1]:
        class_info[1] = "Monday"
        class_info[4] = "Monday"
        class_info[6] = "Friday"

    est = helper_functions.gettime(class_info[2], class_info[3])[0]
    cst = helper_functions.gettime(class_info[2], class_info[3])[1]
    class_info[2] = est
    class_info[3] = cst
    stime = helper_functions.getdate(class_info[5], class_info[7])[0]
    etime = helper_functions.getdate(class_info[5], class_info[7])[1]
    class_info[5] = stime
    class_info[7] = etime
    class_info.remove(class_info[-2])
    class_info.remove(class_info[-1])
    cursor.execute(sql5)
    email_info = cursor.fetchall()[0]
    # print(class_info)

    sql_teacher_email = "SELECT email, email,teacher FROM classes WHERE id = '{}'".format(class_id)
    cursor.execute(sql_teacher_email)
    teacher_info = list(cursor.fetchall()[0])
    emails.append(teacher_info)

    prep_to_send("er1", emails, email_info, class_info, qwert=[skipclass])

def er2(class_name, cursor):
    emails = []
    sql = 'SELECT id FROM classes WHERE short_name = "{}"'
    sql2 = 'SELECT student_id, timestamp FROM classes_to_students WHERE class_id = "{}" AND timestamp > "{}" AND timestamp <= "{}"'
    sql3 = 'SELECT Email_Address, Parent_Email, Student_Name FROM students WHERE id = "{}"'
    sql4 = 'SELECT short_name, zoom, zoom, teacher, name, final_student, last_student FROM classes WHERE short_name = "{}"'
    sql5 = 'SELECT subject, content FROM templates WHERE name="er2"'
    cursor.execute(sql.format(class_name))
    class_id = cursor.fetchall()[0][0]

    cursor.execute(sql4.format(class_name))
    class_info = list(cursor.fetchall()[0])
    if (class_info[-1] == None):
        class_info[-1] = "0000-00-00 00:00:00"
    if (class_info[-2] == "0000-00-00 00:00:00" or class_info[-2] == None):
        class_info[-2] = "9999-99-99 99:99:99"

    cursor.execute(sql2.format(class_id, class_info[-1], class_info[-2]))
    student_ids = cursor.fetchall()
    for i in student_ids:
        cursor.execute(sql3.format(i[0]))
        des_emaux = cursor.fetchall()[0]
        if (list(des_emaux) not in emails):
            emails.append(list(des_emaux))
        print(i[1])
    
    class_info.remove(class_info[-2])
    class_info.remove(class_info[-1])
    cursor.execute(sql5)
    email_info = cursor.fetchall()[0]
    # print(class_info)

    if __name__ == "__main__":
        run_class_starting = input("Run class_starting.py? ")
        if run_class_starting.lower() == "yes":
            import class_starting
    
    sql_teacher_email = "SELECT email, email,teacher FROM classes WHERE id = '{}'".format(class_id)
    cursor.execute(sql_teacher_email)
    teacher_info = list(cursor.fetchall()[0])
    emails.append(teacher_info)

    prep_to_send("er2", emails, email_info, class_info)


def ge(class_name, cursor):
    emails = []
    sql = 'SELECT id FROM classes WHERE short_name = "{}"'
    sql4 = 'SELECT final_student, last_student FROM classes WHERE short_name = "{}"'
    sql2 = 'SELECT student_id, timestamp FROM classes_to_students WHERE class_id = "{}" AND timestamp > "{}" AND timestamp <= "{}"'
    sql3 = 'SELECT Email_Address, Parent_Email, Student_Name FROM students WHERE id = "{}"'
    cursor.execute(sql.format(class_name))
    class_id = cursor.fetchall()[0][0]
    cursor.execute(sql4.format(class_name))
    class_info = list(cursor.fetchall()[0])
    if (class_info[-1] == None):
        class_info[-1] = "0000-00-00 00:00:00"
    if (class_info[-2] == "0000-00-00 00:00:00" or class_info[-2] == None):
        class_info[-2] = "9999-99-99 99:99:99"
    cursor.execute(sql2.format(class_id, class_info[-1], class_info[-2]))
    student_ids = cursor.fetchall()
    for i in student_ids:
        cursor.execute(sql3.format(i[0]))
        e = cursor.fetchall()[0]
        if (list(e) not in emails):
            emails.append(list(e))
    for i in emails:
        print(i[0])
        print(i[1])
    #input("good?")
    return emails

def prep_to_send(email_to_send, emails, email_info, class_info=[], welcome_classinfo=[], waitlist_emails=[], qwert=[1], waitlist_emailinfo=[], waitlist_classinfo=[]):
    
    if (email_to_send != "e2"):
        class_info = list(class_info)
        for c in range(0, len(class_info)):
            if class_info[c] == None:
                class_info[c] = ""
    for j in emails:
        print(j)
    if __name__ == "__main__":
        input("Send?")
    for j in emails:
        print(j[0])
        print(j[1])
        print(j[2])
        if (email_to_send == "e1" or email_to_send == "esa" or email_to_send == "e3" or email_to_send == "e4" or email_to_send == "er1" or email_to_send == "er2"):
            if (email_to_send == "esa"):
                class_info[1] = j[3]
                
                send(email_to_send, email_info[0], email_info[1], j[2], j[0], j[1], class_info, extra_content=qwert[j[0]])
            else:
                print("\n\n\n%s\n\n\n" % class_info)
                send(email_to_send, email_info[0], email_info[1], j[2], j[0], j[1], class_info)
            
        elif (email_to_send == "e2"):
            print("\n\n\n%s\n\n\n" % welcome_classinfo)
            send("e1", email_info[0], email_info[1], j[2], j[0], j[1], welcome_classinfo)
    if (email_to_send == "e2"):
        for j in waitlist_emails:
            print(j)
        if __name__ == "__main__":
            input("Send??")
        for j in waitlist_emails:
            print("Waitlist")
            print(j[0])
            print(j[1])
            send(email_to_send, waitlist_emailinfo[0], waitlist_emailinfo[1], j[2], j[0], j[1], waitlist_classinfo)
    print("\nEmails not sent: ")

#tutorial at https://realpython.com/python-send-email/

if __name__ == "__main__":
    db = "HELM_Database"
    cnx = create_connection()
    cursor = cnx.cursor(buffered=True)
    email_to_send = input("E1, E2, E3, E4, ESA, ER1, ER2, Get Emails? ").lower()
    class_name = input("class?").lower()
    class_name = class_name[0].upper() + class_name[1:]
    if (email_to_send == "e1"):
        e1(class_name, cursor)
    elif (email_to_send == "e2"):
        e2(class_name, cursor)
    elif (email_to_send == "e3"):
        e3(class_name, cursor)
    elif (email_to_send == "e4"):
        e4(class_name, cursor)
    elif (email_to_send == "esa"):
        esa(class_name, cursor)
    elif (email_to_send == "er1"):
        er1(class_name, cursor)
    elif (email_to_send == "er2"):
        er2(class_name, cursor)
    elif (email_to_send == "ge"):
        ge(class_name, cursor)
    else:
        print("You're bad and you should feel bad about yourself")
    for i in not_sent_emails:
        print(i)        
    cnx.commit()
    cursor.close()
    cnx.close()

# final student for Python 5 week class: 2020-12-05 20:26:44
# last student for Py: 2020-08-09 20:38:18

# last student: 2020-12-05 20:26:44
