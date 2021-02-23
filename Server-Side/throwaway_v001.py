# Vikram Anantha
# Get emails from every teacher at HELM
# Dec 2 2020

from helper_functions import *
cursor = connect()
sql = 'SELECT email FROM classes'
cursor.execute(sql)
emails = cursor.fetchall()
for i in emails:
    print(i[0])