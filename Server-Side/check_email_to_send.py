#!/home/myuser/bin/python

# Vikram Anantha
# Dec 28 2020
# Check email to send

from helper_functions import *
import sys; sys.path.append('/home/ec2-user/anaconda3/lib/python3.8/site-packages/mysql')
import timed_email_sending as tes
import datetime
import pytz
import random
cursor = connect()
est = pytz.timezone('America/New_York') 
today = datetime.date.today()
rn = datetime.datetime.now(est)
sql = "SELECT short_name FROM classes WHERE startdate = '{}' AND starttime = '{}'"
sql22222 = "SELECT short_name FROM classes WHERE enddate = '{}' AND endtime = '{}'"
# today = datetime.date(2020, 12, 19)
# rn = datetime.datetime(2021, 1, 27, 17, 30, 48, 698821)

# ---------------------------------------------ER2
day_er2 = today.strftime("%Y-%m-%d")
time_er2 = rn.strftime("%H:%M")

cursor.execute(sql.format(day_er2, time_er2))
classes_er2 = cursor.fetchall()

for i in classes_er2:
    print(i[0])
    tes.er2(class_name = i[0], cursor=cursor)



# ---------------------------------------------ER1
day_er1 = (today + datetime.timedelta(days=4)).strftime("%Y-%m-%d")
time_er1 = rn.strftime("%H:%M")

cursor.execute(sql.format(day_er1, time_er1))
classes_er1 = cursor.fetchall()

for i in classes_er1:
    print(i[0])
    tes.er1(class_name = i[0], cursor=cursor)



# ---------------------------------------------E1
day_e1 = (today + datetime.timedelta(days=9)).strftime("%Y-%m-%d")
time_e1 = rn.strftime("%H:%M")

cursor.execute(sql.format(day_e1, time_e1))
classes_e1 = cursor.fetchall()

for i in classes_e1:
    print(i[0])
    tes.e1(class_name = i[0], cursor=cursor)



# ---------------------------------------------E4
day_e4 = (today + datetime.timedelta(days=9)).strftime("%Y-%m-%d")
time_e4 = (rn - datetime.timedelta(hours=2)).strftime("%H:%M")

cursor.execute(sql22222.format(day_e1, time_e1))
classes_e4 = cursor.fetchall()

for i in classes_e4:
    print(i[0])
    tes.e4(class_name = i[0], cursor=cursor)