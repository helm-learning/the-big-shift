# Making a df file
# Version 3
# Vikram Anantha
# Feb 6 2021
"""

ID | Timestamp  | Name | Email         | Pemail            | Grade | Town | State | Found out about HELM | Class | Took_class_3 | Took_class_4 | Took_class_5 ... | Probs_of_taking_class
22 | 2020-09-07 | Tom  | tom@gmail.com | tomsmom@gmail.com | 6     | Lex  | MA    | Whatsapp Group       | [5]   | 0            | 1            | 0            ... | 1 or 0


"""

import pandas
from helper_functions import *

def main():
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
        'took_classes': [],
        'class': [],
        'probs': [],
    }
    numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']

    sql0 = 'SELECT id FROM classes'
    cursor.execute(sql0)
    cid = cursor.fetchall()
    for l in range(3, cid[-1][0]+1):
        master["took_class_%s" % l] = []

    sql = 'SELECT id, Timestamp, Student_Name, Email_Address, Parent_Email, Grade, City, State, Heard_about_us FROM students ORDER BY Timestamp'
    sql2 = 'SELECT class_id FROM classes_to_students WHERE student_id = "{}" ORDER BY timestamp'
    cursor.execute(sql)
    students = cursor.fetchall()
    count = 1
    student = 1
    columns = ['student_id', 'timestamp', 'name', 'email', 'pemail', 'grade', 'town', 'state', 'heard_about','took_classes', 'class', 'probs', ]
    for i in range(3, cid[-1][0]+1):
        columns.append('took_class_%s' % i)
    for i in students:
        cursor.execute(sql2.format(i[0]))
        theclasses = cursor.fetchall()
        classes = []
        for l in theclasses:
            #print("%s %s" % (i[2], j[0]))
            if l[0] not in classes:
                classes.append(l[0])

        tag1 = []
        for k in classes:
                cursor.execute('SELECT tag_id FROM classes_to_tags WHERE class_id = "{}"'.format(k))
                tags1 = cursor.fetchall()
                
                
                for taqwerg in tags1:
                    tag1.append(taqwerg[0])
        for j in range(3, cid[-1][0]+1):  
            for k in range(3, cid[-1][0]+1):
                hasclass = 0
                if k in classes and k != j:
                    hasclass = 1
                master['took_class_%s' % k].append(hasclass)

            sb = str(i[5])
            gradenum = ''
            for ily in sb:
                if ily == '.':
                    break
                if (ily in numbers):
                    gradenum += ily
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
            master['took_classes'].append(classes)
            master['class'].append(j)

            prob = 0
            cursor.execute('SELECT tag_id FROM classes_to_tags WHERE class_id = "{}"'.format(j))
            tags2 = cursor.fetchall()
            tag2 = list(np.reshape(tags2, (1, len(tags2)))[0])

            # for taqwerg in tags2:
            #     tag2.append(taqwerg[0])
            
            # print(tag1)
            # print(tag1)
            numtags = 0
            # for k in tag2:
            #     if k in tag1:
            #         numtags+=1
            numtags = len(set(tag1) & set(tag2))
            #         cursor.execute('SELECT tag FROM tags WHERE id="{}"'.format(k))
            #         ifjnsk = cursor.fetchall()[0][0]
            #         print(">>> %s" % ifjnsk)
            # input("Class: %s" % j)
            if numtags >= 1:
                probs = 2
            if numtags >= 2:
                probs = 5
            if numtags >= 3:
                probs = 7
            if numtags >= 4:
                probs = 8
            if j in classes:
                probs = 10
            # print(probs)
            master['probs'].append(probs)

        if (student % 5 == 0):
            print("Student %s" % student)
        if student % 20 == 0:
            print("Updating Dataframe...", end='')
            df = pd.DataFrame(master, columns = columns)
            df.to_csv ('students_v3.csv', index = False, header=True)
            print("   Updated!")
        student += 1        


    df = pd.DataFrame(master, columns = columns)
    print(df)
    df.to_csv ('students_v3.csv', index = False, header=True)

if __name__ == '__main__':
    main()