# Recommendation Algorithm
# Vikram Anantha
# Feb 16 2021
from helper_functions import *
# import make_df_v3
from helper_functions import *
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import LinearRegression
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
import math
import random

import warnings
warnings.filterwarnings('ignore') 


cursor = connect()
def get_data():
    # make_df_v2.main()
    df = pd.read_csv("students_v3.csv")
    cols = []
    cursor.execute("SELECT id FROM classes")
    num_classes = cursor.fetchall()[-1][0]
    for j in range(3, num_classes+1):
        cols.append('took_class_%s' % j)
    return cols, df

def train():
    cols, df = get_data()
    models = [None, None, None]
    sql0 = 'SELECT id FROM classes'
    cursor.execute(sql0)
    num_classes = cursor.fetchall()[-1][0]
    for i in range(3, num_classes+1): # this is for each model
        if i == 40 or i == 46 or i == 45:
            models.append(None)
            continue
        
        x_cols = df.loc[df['class'] == i]
        x = np.array(x_cols[cols])
        y = x_cols[['probs']]
        if (len(x) == 0):
            models.append(None)
            continue
        x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=0, shuffle=True, test_size=0.25, train_size = 0.75)
        
        m_v1 = LogisticRegression()
        m_v1.fit(x, y)
        if __name__ == "__main__":
            print("\n\n%s\n\n" % i)
        models.append(m_v1)
    return models

def predict(fname, email, class_taken=None):
    sql0 = 'SELECT id FROM classes'
    cursor.execute(sql0)
    num_classes = cursor.fetchall()[-1][0] 
    cursor.execute("SELECT id FROM students WHERE Student_Name = '{}' and Email_Address = '{}'".format(fname, email))
    id = cursor.fetchall()[0][0]
    data = [0]*(num_classes-2)
    # cursor.execute("SELECT Grade FROM students WHERE id = '{}'".format(id))
    cursor.execute("SELECT class_id FROM classes_to_students WHERE student_id = '{}'".format(id))
    cids = cursor.fetchall()
    classes = list(set(np.reshape(cids, (1, len(cids)))[0]))

    # for i in range(3, num_classes): 
    #     probs = 0
    #     # cursor.execute('SELECT tag_id FROM classes_to_tags WHERE class_id = "{}"'.format(i))
    #     # tags2 = cursor.fetchall()
    #     # tag2 = list(np.reshape(tags2, (1, len(tags2)))[0])
    #     # numtags = len(set(tag1) & set(tag2))
    #     # if numtags < 1:
    #     #     probs = 0
    #     # if numtags >= 1:
    #     #     probs = 2
    #     # if numtags >= 2:
    #     #     probs = 5
    #     # if numtags >= 3:
    #     #     probs = 7
    #     # if numtags >= 4:
    #     #     probs = 8
    #     if i in classes:
    #         probs = 1
    #     data[i-3] = probs

    for i in classes:
        data[i-3] = 1

        #### MAKE IT SO IT WILL TAKE IN TAGS ####
    print(classes)
    models = train()
    predictions = []
    for m in models:
        if m == None:
            continue
        pred = list(m.predict(np.array(data).reshape(1, -1)))[0]
        cool = [pred, models.index(m)]
        predictions.append(cool)
    predictions.sort()
    predictions.reverse()
    # print(predictions)
    recommended = []
    
    count = 0
    recommended_classes_number = 3
    random_classes_number = 1
    for i in predictions:
        if count == recommended_classes_number:
            break
        if i[1] not in recommended and i[1] not in classes:
            cursor.execute("SELECT short_name FROM classes WHERE id = '{}'".format(i[1]))
            class_name = cursor.fetchall()[0][0]
            # print(class_name, i[1])
            if class_name != class_taken:
                recommended.append(class_name)
                count += 1
        # print(recommended)
    
    count = 0
    while count < random_classes_number:
        choice = random.choice(predictions)[1]
        if choice not in classes:
            cursor.execute("SELECT short_name FROM classes WHERE id = '{}'".format(choice))
            class_name = cursor.fetchall()[0][0]
            if class_name not in recommended and class_name != class_taken:
                recommended.append(class_name)
            count += 1
    # print(recommended)
    classes.sort()
    print(classes)
    cursor.execute("SELECT class_id FROM classes_to_students WHERE student_id = '{}'".format(id))
    sb = list(np.reshape(list(set(cursor.fetchall())), (1, -1))[0])
    sb.sort()
    print(sb)
    return recommended

if __name__ == "__main__":  
    class_predicted = predict("Sabina", "dasmartone3141@gmail.com")
    # fname = input("Name? ")
    # email = input("Email? ")
    # class_predicted = use(fname, email)
    print(class_predicted)

