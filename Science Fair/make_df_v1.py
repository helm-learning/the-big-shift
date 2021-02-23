# Making a df file
# Version 1
# Vikram Anantha
# Feb 1 2021
"""

ID | Timestamp  | Name | Email         | Pemail            | Grade | Town | State | Found out about HELM | Prev Classes | Next 3 classes
22 | 2020-09-07 | Tom  | tom@gmail.com | tomsmom@gmail.com | 6     | Lex  | MA    | Whatsapp Group       | [1, 4, 2, 3] | [5, 29, 23]


"""

import pandas
from helper_functions import *

db = "HELM_Database"
cnx = create_connection()
cursor = cnx.cursor(buffered=True)

master = {
    'id': [],
    'student_id': [],
    'timestamp': [],
    'name': [],
    'email': [],
    'pemail': [],
    'grade': [],
    'town': [],
    'state': [],
    'heard_about': [],
    'next_classes': []
}
numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
sql0 = 'SELECT id FROM classes'
cursor.execute(sql0)
cid = cursor.fetchall()
for l in cid:
    master["took_class_%s" % l[0]] = []
    master["next_class_%s" % l[0]] = []


sql = 'SELECT id, Timestamp, Student_Name, Email_Address, Parent_Email, Grade, City, State, Heard_about_us FROM students ORDER BY Timestamp'
sql2 = 'SELECT class_id FROM classes_to_students WHERE student_id = "{}" ORDER BY timestamp'
cursor.execute(sql)
students = cursor.fetchall()
count = 1
student = 1
for i in students:
    cursor.execute(sql2.format(i[0]))
    theclasses = cursor.fetchall()
    classes = []
    for j in theclasses:
        #print("%s %s" % (i[2], j[0]))
        if j[0] not in classes:
            classes.append(j[0])
    for j in range(1, len(classes)):
        prev_classes = classes[:j]
        next_classes = classes[j:] # make it the next 1 class

        grade = str(i[5])
        gradenum = ''
        for q in grade:
            if q == '.':
                break
            if (q in numbers):
                gradenum += q
        if gradenum == '':
            gradenum = '0'
        gradenum = int(gradenum)

        master['id'].append(count)
        count+= 1
        # print(str(type(i)) + " " + str(i))
        master['student_id'].append(i[0])
        master['timestamp'].append(i[1])
        master['name'].append(i[2])
        master['email'].append(i[3])
        master['pemail'].append(i[4])
        master['grade'].append(gradenum)
        master['town'].append(i[6])
        master['state'].append(i[7])
        master['heard_about'].append(i[8])
        master['next_classes'].append(next_classes)
        for l in cid:
            master['took_class_%s' % l[0]].append(0)
            master['next_class_%s' % l[0]].append(0)
        for k in prev_classes:
            # print('took_class_%s' % k)
            master['took_class_%s' % k][-1] = 1
        for k in next_classes:
            master['next_class_%s' % k][-1] = 1

    if (student % 10 == 0):
        print("Student %s" % student)
    student += 1


# for a in range(996, 999):
#     print("\n------------Signup %s:" % a)
#     print("%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n" % (
#         master['student_id'][a],
#         master['timestamp'][a],
#         master['name'][a],
#         master['email'][a],
#         master['pemail'][a],
#         master['grade'][a],
#         master['town'][a],
#         master['state'][a],
#         master['heard_about'][a],
#         master['prev_classes'][a],
#         master['next_classes'][a]
#     ))
columns = ['student_id', 'timestamp', 'name', 'email', 'pemail', 'grade', 'town', 'state', 'heard_about','next_classes']
for i in cid:
    columns.append('took_class_%s' % i[0])
for i in cid:
    columns.append('next_class_%s' % i[0])
df = pd.DataFrame(master, columns = columns)
print(df)
df.to_csv ('students.csv', index = False, header=True)


        
