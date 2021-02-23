# # def gettime(starttime, endtime):
# #     if (starttime == None):
# #         return ['TBD', 'TBD']
# #     stime = str(starttime).split(":")
# #     etime = str(endtime).split(":")
# #     if (int(stime[0]) >= 12):
# #         startam = "pm"
# #         if (int(stime[0]) > 12):
# #             stime[0] = int(stime[0]) - 12
# #     else:
# #         startam = "am"
# #     if (int(etime[0]) >= 12):
# #         endam = "pm"
# #         if (int(etime[0]) > 12):
# #             etime[0] = int(etime[0]) - 12
# #     else:
# #         endam = "am"
# #     time_est = str(stime[0]) + ":" + str(stime[1]) + startam + " - " + str(etime[0]) + ":" + str(etime[1]) + endam
# #     stime[0] = int(str(starttime).split(":")[0]) - 1
# #     etime[0] = int(str(endtime).split(":")[0]) - 1

# #     if (int(stime[0]) >= 12):
# #         startam = "pm"
# #         stime[0] = int(stime[0]) - 12
# #     else:
# #         startam = "am"
# #     if (int(etime[0]) >= 12):
# #         endam = "pm"
# #         etime[0] = int(etime[0]) - 12
# #     else:
# #         endam = "am"

# #     time_cst = str(stime[0]) + ":" + str(stime[1]) + startam + " - " + str(etime[0]) + ":" + str(etime[1]) + endam
# #     return [time_est, time_cst]

# # def getdate(startdate, enddate):
# #     if (startdate == None):
# #         return ['TBD', 'TBD']
# #     sdate = str(startdate).split("-")
# #     edate = str(enddate).split("-")
# #     print(sdate)
# #     start_date = months[int(sdate[1])] + ' ' + sdate[2] + ', ' + sdate[0]
# #     end_date = months[int(edate[1])] + ' ' + edate[2] + ', ' + edate[0]
# #     return [start_date, end_date]
# not_sent_emails = []
# import smtplib as s
# import ssl
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# import numpy
# import mysql.connector
# from mysql.connector import errorcode
# import pandas as pd
# import helper_functions
# def send(name_of_email, subject, content, student_fname, email, pemail, list_of_content):
#     port = 465
#     sender = "helmlearning2020@gmail.com"
#     password = "h3lml3arning"
    
#     message = MIMEMultipart("alternative")
#     message["Subject"] = subject.format(list_of_content[0])
#     message["From"] = "HELM Learning"
#     message["To"] = email
#     if name_of_email == "e1":
#         startday = list_of_content[7]
#         endday = list_of_content[7]
#         if "weeklong" in startday:
#             startday = "Monday"
#             endday = "Friday"
#             content = content.replace("5 Weeks, once per week)", "5 days in a week, Mon-Fri)")
#         html = content.format(
#             student_fname, 
#             list_of_content[0], 
#             list_of_content[1], 
#             list_of_content[2], 
#             list_of_content[3], 
#             list_of_content[4], 
#             startday, 
#             helper_functions.getdate(list_of_content[5],list_of_content[6])[0],
#             endday, 
#             helper_functions.getdate(list_of_content[5],list_of_content[6])[1], 
#             list_of_content[8], 
#             list_of_content[8], 
#             list_of_content[9], 
#             list_of_content[1], 
#             list_of_content[0])
#         import datetime
#         skipclass = None
#         for i in skipping_weeks:
#             if list_of_content[5] < datetime.date(i[0], i[1], i[2]) and list_of_content[6] > datetime.date(i[0], i[1], i[2]):
#                 skipclass = i[3]
#         if skipclass != None:
#             html = html.replace("5 Weeks, once per week)", "5 Weeks, once per week)<br><strong>{}</strong>".format(skipclass))
#     elif name_of_email == "esa":
#         html = content.format(
#             student_fname,
#             list_of_content[1], #previous class
#             list_of_content[0], #shortname
#             list_of_content[2], #classname
#             list_of_content[7], #signup
#             list_of_content[0], #shortname
#             list_of_content[3], #description
#             list_of_content[4], #teacher
#             list_of_content[5], #time
#             list_of_content[6], #week
            
#         )
#     elif name_of_email == "e3":
#         html = content.format(
#             student_fname[0].upper() + student_fname[1:],
#             list_of_content[0],
#             list_of_content[1],
#             list_of_content[2],
#             list_of_content[3],
#             list_of_content[4],
#             list_of_content[5],
#             list_of_content[6],
#             list_of_content[7],
#         )
        
#     elif name_of_email == "e2":
#         html = content.format(
#             student_fname[0].upper() + student_fname[1:],
#             list_of_content[0], #name
#             list_of_content[1], #teacher
#             list_of_content[2], #name
#         )
#     elif name_of_email == "e4":
#         html = content.format(
#             student_fname[0].upper() + student_fname[1:],
#             list_of_content[0],
#             list_of_content[1],
#             list_of_content[2],
#             list_of_content[3],
#             list_of_content[4],
#         )
#     elif name_of_email == "er1":
#         print(content)
#         print(list_of_content)
#         # for i in range(0, len(list_of_content)):
#         #     content = content.format(i)
#         # html = content
#         html = content.format(
#             student_fname[0].upper() + student_fname[1:],
#             list_of_content[0],
#             list_of_content[1],
#             list_of_content[2],
#             list_of_content[3],
#             list_of_content[4],
#             list_of_content[5],
#             list_of_content[6],
#             list_of_content[7],
#             list_of_content[8],
#             list_of_content[9],
#             list_of_content[10],
#             list_of_content[11],
#             list_of_content[12],
#         )
#     elif (name_of_email == "er2"):
#         html = content.format(
#             student_fname[0].upper() + student_fname[1:],
#             list_of_content[0],
#             list_of_content[1],
#             list_of_content[2],
#             list_of_content[3],
#             list_of_content[4],
#         )
#     #print(html)
    
#     part2 = MIMEText(html, "html")
#     message.attach(part2)
#     context = ssl.create_default_context()
    

#     with s.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
#         server.login(sender, password)
#         try:
#             #input("send?")
#             server.sendmail(sender, email, message.as_string())
#             server.sendmail(sender, pemail, message.as_string())
#             print("Sent!\n")
#         except:
#             print("NOT SENT\n")
#             not_sent_emails.append(email)
#             not_sent_emails.append(pemail)


# config = {
#     'user': 'helmlearning',
#     'password': 'H3lml3arning',
#     'host': '127.0.0.1', #52.21.172.100:22
#     'port': '3306',
#     'database': 'HELM_Database'
# }
# months = {
#     1: "Jan",
#     2: "Feb",
#     3: "March",
#     4: "April",
#     5: "May",
#     6: "June",
#     7: "July",
#     8: "Aug",
#     9: "Sept",
#     10: "Oct",
#     11: "Nov",
#     12: "Dec"
# }

# skipping_weeks = [
#     [2020, 11, 23, " (skipping the week of Thanksgiving, <br>Nov 23 2020 - Nov 29 2020)"],
#     [2020, 12, 21, " (skipping the weeks of Christmas and New Years, <br>Dec 21 2020 - Jan 3 2021)"]
# ]

# def create_connection():
#     """
#     Returns a database connection using mysql.connector
#     """
#     # open database connection
#     global cnx
#     try:
#         cnx = mysql.connector.connect(**config)
#         return cnx
#     except mysql.connector.Error as err:
#         if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
#             print("Something is wrong with your user name or password")
#         elif err.errno == errorcode.ER_BAD_DB_ERROR:
#             print("Database does not exist")
#         else:
#             print(err)
#         raise
    

# def e1(class_name, cursor):
#     sql5 = 'SELECT id, last_student FROM classes WHERE short_name = "{}"'.format(class_name)
#     sql4 = 'SELECT student_id FROM classes_to_students WHERE class_id = "{}" AND timestamp > "{}"'
#     sql2 = 'SELECT name, teacher, e1_summary, starttime, endtime, startdate, enddate, day, zoom, e1_additionalwork FROM classes WHERE short_name = "%s";' % (class_name[0].upper() + class_name[1:])
#     sql3 = 'SELECT subject, content FROM templates WHERE name="{}"'.format(email_to_send)
#     sql = 'SELECT Email_Address, Parent_Email, Student_Name FROM students WHERE id = {}'

#     cursor.execute(sql5)
#     class_asdf = cursor.fetchall()[0]
#     class_id = class_asdf[0]
#     last_stud = class_asdf[1]

#     if (last_stud == None):
#         last_stud = "0000-00-00 00:00:00"
#     cursor.execute(sql4.format(class_id, last_stud))
#     student_ids = cursor.fetchall()

#     cursor.execute(sql2)
#     class_info = cursor.fetchall()[0]

#     cursor.execute(sql3)
#     stuff = cursor.fetchall()[0]
#     email_info = []
#     email_info.append(stuff[0])
#     email_info.append(stuff[1])
#     print(class_info)
#     print(student_ids)
#     emails = []
#     for j in student_ids:
#         i = j[0]
#         print(i)
#         cursor.execute(sql.format(i))
#         theemails = cursor.fetchall()[0]
#         if ([theemails[0], theemails[1], theemails[2]] not in emails):
#             emails.append([theemails[0], theemails[1], theemails[2]])
#     prep_to_send("e1", emails, email_info, class_info)

# def e2(class_name, cursor):
#     emails = []
#     waitlist_emails = []
#     sql = 'SELECT id FROM classes WHERE short_name = "%s"' % class_name
#     sql2 = 'SELECT last_student, final_student FROM classes WHERE short_name = "%s"' % class_name
#     sql3 = 'SELECT student_id, timestamp FROM classes_to_students WHERE class_id = "{}" AND timestamp > "{}" AND timestamp <= "{}"'
#     sql35 = 'SELECT student_id, timestamp FROM classes_to_students WHERE class_id = "{}" AND timestamp > "{}"'
#     sql4 = 'SELECT Email_Address, Parent_Email, Student_Name FROM students WHERE id = "{}"'
#     sql5 = 'SELECT name, teacher, e1_summary, starttime, endtime, startdate, enddate, day, zoom, e1_additionalwork FROM classes WHERE short_name = "%s";' % class_name
#     sql55 = 'SELECT name, teacher, name FROM classes WHERE short_name = "%s";' % class_name
#     sql6 = 'SELECT subject, content FROM templates WHERE name="e1"'
#     sql65 = 'SELECT subject, content FROM templates WHERE name="e2"'
#     print("1")
#     cursor.execute(sql)
#     class_id = cursor.fetchall()[0][0]
#     print("2")
#     cursor.execute(sql2)
#     fila_student = cursor.fetchall()[0]
#     print(fila_student[0])
#     cursor.execute(sql3.format(class_id, fila_student[0], fila_student[1]))
#     welcome_studentids = cursor.fetchall()
#     print("4")
#     cursor.execute(sql35.format(class_id, fila_student[1]))
#     waitlist_studentids = cursor.fetchall()
#     for i in welcome_studentids:
#         cursor.execute(sql4.format(i[0]))
#         student_info = cursor.fetchall()[0]
#         if (student_info not in emails):
#             emails.append(student_info)
#     for i in waitlist_studentids:
#         cursor.execute(sql4.format(i[0]))
#         student_info = cursor.fetchall()[0]
#         if (student_info not in waitlist_emails):
#             waitlist_emails.append(student_info)
#     print("5")
#     cursor.execute(sql5)
#     welcome_classinfo = list(cursor.fetchall()[0])
#     timeest = helper_functions.gettime(welcome_classinfo[3], welcome_classinfo[4])[0]
#     timecst = helper_functions.gettime(welcome_classinfo[3], welcome_classinfo[4])[1]
#     startdate = helper_functions.getdate(welcome_classinfo[5], welcome_classinfo[6])[0]
#     enddate = helper_functions.getdate(welcome_classinfo[5], welcome_classinfo[6])[1]
#     welcome_classinfo[3] = timeest
#     welcome_classinfo[4] = timecst
#     welcome_classinfo[5] = startdate
#     welcome_classinfo[6] = enddate
#     print(welcome_classinfo)
#     print("6")
#     cursor.execute(sql55)
#     waitlist_classinfo = cursor.fetchall()[0]
#     print(waitlist_classinfo)
#     print("7")
#     cursor.execute(sql65)
#     waitlist_emailinfo = cursor.fetchall()[0]
#     print("7.5")
#     cursor.execute(sql6)
#     email_info = cursor.fetchall()[0]
#     print("8")
#     for i in range(0, len(welcome_classinfo)):
#         if (welcome_classinfo[i] == None):
#             welcome_classinfo[i] == ''
#     for i in range(0, len(waitlist_classinfo)):
#         if (waitlist_classinfo[i] == None):
#             waitlist_classinfo[i] == ''
#     prep_to_send("e2", emails, email_info, welcome_classinfo=welcome_classinfo, waitlist_emails=waitlist_emails, waitlist_emailinfo=waitlist_emailinfo, waitlist_classinfo=waitlist_classinfo)

# def esa(class_name, cursor):
#     classes = []
#     emails = []
#     #subject_area = input("Subject Area? ")
#     while True:
#         r = input("What classes? ").lower()
#         if (r == 'stop' or r == None or r== ''):
#             break
#         classes.append(r[0].upper() + r[1:])
        
#     sql = 'SELECT id FROM classes WHERE short_name = "{}"'
#     sql2 = 'SELECT student_id FROM classes_to_students WHERE class_id = "{}"'
#     sql3 = 'SELECT Email_Address, Parent_Email, Student_Name FROM students WHERE id = "{}"'
#     sql4 = 'SELECT short_name, name, description, teacher, starttime, endtime, startdate, enddate, day FROM classes WHERE short_name = "{}"'
#     sql5 = 'SELECT subject, content FROM templates WHERE name="esa"'


#     qwert = {}
#     print(classes)
#     for k in classes:
#         cursor.execute(sql.format(k))
#         class_id = cursor.fetchall()[0][0]
        
#         cursor.execute(sql2.format(class_id))
#         students = cursor.fetchall()
#         for qw in students:
#             cursor.execute(sql3.format(qw[0]))
#             emaillist = list(cursor.fetchall()[0])
#             if (emaillist not in emails):
#                 emails.append(emaillist)
#                 qwert[emaillist[0]] = k

#     cursor.execute(sql4.format(class_name))
#     class_info = list(cursor.fetchall()[0])

#     class_info.insert(1, "subject_area")
#     class_info[5] = helper_functions.gettime(class_info[5], class_info[6])[0]
#     class_info.remove(class_info[6])
#     if (helper_functions.getdate(class_info[6], class_info[7])[0] != "TBD"):
#         class_info[6] = class_info[8] + "s, " + helper_functions.getdate(class_info[6], class_info[7])[0] + " - " + helper_functions.getdate(class_info[6], class_info[7])[1]
#     else:
#         class_info[6] = "TBD"
#     class_info.remove(class_info[7])
#     class_info.remove(class_info[7])
#     class_info.append("signup.helmlearning.com/page1.html?class=" + class_name.lower().replace(" ", "-"))

#     print(class_info)

#     cursor.execute(sql5.format(email_to_send))
#     email_info = list(cursor.fetchall()[0])
#     prep_to_send("esa", emails, email_info, class_info, qwert=qwert)

# def e3(class_name, cursor):
#     emails = []
#     sql = 'SELECT id FROM classes WHERE short_name = "{}"'
#     sql2 = 'SELECT student_id, timestamp FROM classes_to_students WHERE class_id = "{}" AND timestamp > "{}" AND timestamp <= "{}"'
#     sql6 = 'SELECT final_student FROM classes WHERE short_name = "{}"'
#     sql3 = 'SELECT Email_Address, Parent_Email, Student_Name FROM students WHERE id = "{}"'
#     sql4 = 'SELECT short_name, starttime, endtime, e3_briefdescription, zoom, zoom, teacher, name, final_student, last_student FROM classes WHERE short_name = "{}"'
#     sql5 = 'SELECT subject, content FROM templates WHERE name="e3"'
#     cursor.execute(sql.format(class_name))
#     class_id = cursor.fetchall()[0][0]

#     cursor.execute(sql4.format(class_name))
#     class_info = list(cursor.fetchall()[0])
#     if (class_info[-1] == None):
#         class_info[-1] = "0000-00-00 00:00:00"

#     cursor.execute(sql2.format(class_id, class_info[-1], class_info[-2]))
#     student_ids = cursor.fetchall()
#     cursor.execute(sql6.format(class_name))
#     last_student = cursor.fetchall()[0][0]
#     for i in student_ids:
#         cursor.execute(sql3.format(i[0]))
#         des_emaux = cursor.fetchall()[0]
#         if (des_emaux not in emails):
#             emails.append(list(des_emaux))
#         print(i[1])
#         # print(final_student)
#         # if (i[1] == last_student):
#         #     print("BREAK")
#         #     break
#     #print(emails)
    
#     class_info[1] = helper_functions.gettime(class_info[1], class_info[2])[0]
#     class_info.remove(class_info[2])
#     class_info.insert(1, input("Drive link: "))
#     cursor.execute(sql5)
#     email_info = cursor.fetchall()[0]
#     print(class_info)
#     prep_to_send("e3", emails, email_info, class_info)

# def e4(class_name, cursor):
#     emails = []
#     #send e4
    
#     sql = 'SELECT id FROM classes WHERE short_name = "{}"'
#     sql2 = 'SELECT student_id, timestamp FROM classes_to_students WHERE class_id = "{}" AND timestamp > "{}" AND timestamp <= "{}"'
#     sql3 = 'SELECT Email_Address, Parent_Email, Student_Name FROM students WHERE id = "{}"'
#     sql4 = 'SELECT name, e4_continuingfurther, teacher, email, name, final_student, last_student FROM classes WHERE short_name = "{}"'
#     sql5 = 'SELECT subject, content FROM templates WHERE name="e4"'

#     cursor.execute(sql.format(class_name))
#     class_id = cursor.fetchall()[0][0]

#     cursor.execute(sql4.format(class_name))
#     class_info = list(cursor.fetchall()[0])
#     if (class_info[-1] == None):
#         class_info[-1] = "0000-00-00 00:00:00"
#     cursor.execute(sql2.format(class_id, class_info[-1], class_info[-2]))
#     student_ids = cursor.fetchall()
#     for i in student_ids:
#         cursor.execute(sql3.format(i[0]))
#         des_emaux = cursor.fetchall()[0]
#         if (des_emaux not in emails):
#             emails.append(list(des_emaux))
#         print(i[1])
#     cursor.execute(sql5)
#     email_info = cursor.fetchall()[0]
#     sql6 = "UPDATE classes SET final_student = null WHERE short_name = '{}'".format(class_name)
#     sql7 = "UPDATE classes SET last_student = '{}' WHERE short_name = '{}'".format(class_info[-2], class_name)
#     sql8 = "UPDATE classes SET class_started = 0 WHERE short_name = '{}'".format(class_name)
#     sql9 = "UPDATE classes SET day = '' WHERE short_name = '{}'".format(class_name)
#     sql10 = "UPDATE classes SET startdate = '0000-00-00' WHERE short_name = '{}'".format(class_name)
#     sql11 = "UPDATE classes SET enddate = '0000-00-00' WHERE short_name = '{}'".format(class_name)
#     cursor.execute(sql6)
#     cursor.execute(sql7)
#     cursor.execute(sql8)
#     cursor.execute(sql9)
#     cursor.execute(sql10)
#     cursor.execute(sql11)
#     #make sure to change the final student and the last student
#     #also make sure to change the class_started
#     #and the day and week
#     print(class_info)
#     prep_to_send("e4", emails, email_info, class_info)

# def er1(class_name, cursor):
#     emails = []
#     sql = 'SELECT id FROM classes WHERE short_name = "{}"'
#     sql2 = 'SELECT student_id, timestamp FROM classes_to_students WHERE class_id = "{}" AND timestamp > "{}" AND timestamp <= "{}"'
#     sql3 = 'SELECT Email_Address, Parent_Email, Student_Name FROM students WHERE id = "{}"'
#     sql4 = 'SELECT name, day, starttime, endtime, day, startdate, day, enddate, zoom, zoom, e1_additionalwork, teacher, name, final_student, last_student FROM classes WHERE short_name = "{}"'
#     sql5 = 'SELECT subject, content FROM templates WHERE name="er1"'
#     cursor.execute(sql.format(class_name))
#     class_id = cursor.fetchall()[0][0]

#     cursor.execute(sql4.format(class_name))
#     class_info = list(cursor.fetchall()[0])
#     if (class_info[-1] == None):
#         class_info[-1] = "0000-00-00 00:00:00"
#     if (class_info[-2] == "0000-00-00 00:00:00" or class_info[-2] == None):
#         class_info[-2] = "9999-99-99 99:99:99"

#     cursor.execute(sql2.format(class_id, class_info[-1], class_info[-2]))
#     student_ids = cursor.fetchall()
#     for i in student_ids:
#         cursor.execute(sql3.format(i[0]))
#         des_emaux = cursor.fetchall()[0]
#         if (des_emaux not in emails):
#             emails.append(list(des_emaux))
#         print(i[1])
    
#     est = helper_functions.gettime(class_info[2], class_info[3])[0]
#     cst = helper_functions.gettime(class_info[2], class_info[3])[1]
#     class_info[2] = est
#     class_info[3] = cst
#     stime = helper_functions.getdate(class_info[5], class_info[7])[0]
#     etime = helper_functions.getdate(class_info[5], class_info[7])[1]
#     class_info[5] = stime
#     class_info[7] = etime
#     class_info.remove(class_info[-2])
#     class_info.remove(class_info[-1])
#     cursor.execute(sql5)
#     email_info = cursor.fetchall()[0]
#     print(class_info)
#     prep_to_send("er1", emails, email_info, class_info)

# def er2(class_name, cursor):
#     emails = []
#     sql = 'SELECT id FROM classes WHERE short_name = "{}"'
#     sql2 = 'SELECT student_id, timestamp FROM classes_to_students WHERE class_id = "{}" AND timestamp > "{}" AND timestamp <= "{}"'
#     sql3 = 'SELECT Email_Address, Parent_Email, Student_Name FROM students WHERE id = "{}"'
#     sql4 = 'SELECT short_name, zoom, zoom, teacher, name, final_student, last_student FROM classes WHERE short_name = "{}"'
#     sql5 = 'SELECT subject, content FROM templates WHERE name="er2"'
#     cursor.execute(sql.format(class_name))
#     class_id = cursor.fetchall()[0][0]

#     cursor.execute(sql4.format(class_name))
#     class_info = list(cursor.fetchall()[0])
#     if (class_info[-1] == None):
#         class_info[-1] = "0000-00-00 00:00:00"
#     if (class_info[-2] == "0000-00-00 00:00:00" or class_info[-2] == None):
#         class_info[-2] = "9999-99-99 99:99:99"

#     cursor.execute(sql2.format(class_id, class_info[-1], class_info[-2]))
#     student_ids = cursor.fetchall()
#     for i in student_ids:
#         cursor.execute(sql3.format(i[0]))
#         des_emaux = cursor.fetchall()[0]
#         if (des_emaux not in emails):
#             emails.append(list(des_emaux))
#         print(i[1])
    
#     class_info.remove(class_info[-2])
#     class_info.remove(class_info[-1])
#     cursor.execute(sql5)
#     email_info = cursor.fetchall()[0]
#     print(class_info)

#     run_class_starting = input("Run class_starting.py? ")
#     if run_class_starting.lower() == "yes":
#         import class_starting
    
#     prep_to_send("er2", emails, email_info, class_info)
        

#     # sql = 'SELECT id, final_student FROM classes WHERE short_name = "{}"'
#     # sql2 = 'SELECT timestamp FROM classes_to_students WHERE class_id = "{}"'
#     # sql3 = 'UPDATE classes SET final_student = "{}" WHERE short_name="{}"'
#     # sql4 = 'UPDATE classes SET class_started = 1 WHERE short_name = "{}"'
#     # sql5 = 'SELECT short_name, starttime, endtime, day, startdate, final_student, last_student, id FROM classes WHERE short_name = "{}"'
#     # sql6 = 'SELECT student_id FROM classes_to_students WHERE class_id = "{}" AND timestamp > "{}" AND timestamp <= "{}"'
#     # sql7 = 'SELECT Email_Address, Parent_Email, Student_Name FROM students WHERE id = "{}"'


#     # cursor.execute(sql.format(class_name))
#     # class_id_stuff = cursor.fetchall()[0]
#     # class_id = class_id_stuff[0]
#     # final_student = class_id_stuff[1]
#     # if (final_student == "" or final_student == None):
#     #     cursor.execute(sql2.format(class_id))
#     #     timestamp = cursor.fetchall()[-1][0]
#     #     print(timestamp)
#     #     print(sql3.format(timestamp, class_name))
#     #     cursor.execute(sql3.format(timestamp, class_name))
#     #     input("Good?")

#     # cursor.execute(sql4.format(class_name))

#     # cursor.execute(sql5.format(class_name))
#     # class_info = list(cursor.fetchall()[0])

#     # if (class_info[-2] == None):
#     #     class_info[-2] = "0000-00-00 00:00:00"

#     # cursor.execute(sql6.format(class_info[-1], class_info[-2], class_info[-3]))
#     # stud_ids = cursor.fetchall()


# def ge(class_name, cursor):
#     emails = []
#     sql = 'SELECT id FROM classes WHERE short_name = "{}"'
#     sql4 = 'SELECT final_student, last_student FROM classes WHERE short_name = "{}"'
#     sql2 = 'SELECT student_id, timestamp FROM classes_to_students WHERE class_id = "{}" AND timestamp > "{}" AND timestamp <= "{}"'
#     sql3 = 'SELECT Email_Address, Parent_Email, Student_Name FROM students WHERE id = "{}"'
#     cursor.execute(sql.format(class_name))
#     class_id = cursor.fetchall()[0][0]
#     cursor.execute(sql4.format(class_name))
#     class_info = list(cursor.fetchall()[0])
#     if (class_info[-1] == None):
#         class_info[-1] = "0000-00-00 00:00:00"
#     if (class_info[-2] == "0000-00-00 00:00:00" or class_info[-2] == None):
#         class_info[-2] = "9999-99-99 99:99:99"
#     cursor.execute(sql2.format(class_id, class_info[-1], class_info[-2]))
#     student_ids = cursor.fetchall()
#     for i in student_ids:
#         cursor.execute(sql3.format(i[0]))
#         e = cursor.fetchall()[0]
#         if (e not in emails):
#             emails.append(list(e))
#     for i in emails:
#         print(i[0])
#         print(i[1])
#     input("good?")
#     quit()

# def prep_to_send(email_to_send, emails, email_info, class_info=[], welcome_classinfo=[], waitlist_emails=[], qwert=[], waitlist_emailinfo=[], waitlist_classinfo=[]):

#     if (email_to_send != "e2"):
#         class_info = list(class_info)
#         for c in range(0, len(class_info)):
#             if class_info[c] == None:
#                 class_info[c] = ""
#     for j in emails:
#         print(j)
#     input("Send?")
#     for j in emails:
#         print(j[0])
#         print(j[1])
#         if (email_to_send == "e1"):
#             print()
#             send(email_to_send, email_info[0], email_info[1], j[2], j[0], j[1], [class_info[0], class_info[1], class_info[2], helper_functions.gettime(class_info[3], class_info[4])[0], helper_functions.gettime(class_info[3], class_info[4])[1], class_info[5], class_info[6], class_info[7], class_info[8], class_info[9]])
#         elif (email_to_send == "esa" or email_to_send == "e3" or email_to_send == "e4" or email_to_send == "er1" or email_to_send == "er2"):
#             if (email_to_send == "esa"):
#                 class_info[1] = qwert[j[0]]
#             send(email_to_send, email_info[0], email_info[1], j[2], j[0], j[1], class_info)
#         elif (email_to_send == "e2"):
#             send("e1", email_info[0], email_info[1], j[2], j[0], j[1], welcome_classinfo)
#     if (email_to_send == "e2"):
#         for j in waitlist_emails:
#             print(j)
#         input("Send??")
#         for j in waitlist_emails:
#             print("Waitlist")
#             print(j[0])
#             print(j[1])
#             send(email_to_send, waitlist_emailinfo[0], waitlist_emailinfo[1], j[2], j[0], j[1], waitlist_classinfo)
#     print("\nEmails not sent: ")

# #tutorial at https://realpython.com/python-send-email/

# if __name__ == "__main__":
#     db = "HELM_Database"
#     cnx = create_connection()
#     cursor = cnx.cursor(buffered=True)
#     email_to_send = input("E1, E2, E3, E4, ESA, ER1, ER2, Get Emails? ").lower()
#     class_name = input("class?").lower()
#     class_name = class_name[0].upper() + class_name[1:]
#     if (email_to_send == "e1"):
#         e1(class_name, cursor)
#     elif (email_to_send == "e2"):
#         e2(class_name, cursor)
#     elif (email_to_send == "e3"):
#         e3(class_name, cursor)
#     elif (email_to_send == "e4"):
#         e4(class_name, cursor)
#     elif (email_to_send == "esa"):
#         esa(class_name, cursor)
#     elif (email_to_send == "er1"):
#         er1(class_name, cursor)
#     elif (email_to_send == "er2"):
#         er2(class_name, cursor)
#     elif (email_to_send == "ge"):
#         ge(class_name, cursor)
#     else:
#         print("You're bad and you should feel bad about yourself")
#     for i in not_sent_emails:
#         print(i)        
#     cnx.commit()
#     cursor.close()
#     cnx.close()