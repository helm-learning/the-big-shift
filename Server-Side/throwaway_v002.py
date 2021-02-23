# Vikram Anantha
# Get emails from every teacher at HELM
# Dec 11 2020

from helper_functions import *
cursor = connect()
sql = 'SELECT Email_Address, Parent_Email FROM students'
cursor.execute(sql)
emails = cursor.fetchall()

count = 0
for i in emails:
    print(i[0])
    print(i[1])
    count+= 1
    if (count % 50 == 0):
        input("\n---------------------\n")