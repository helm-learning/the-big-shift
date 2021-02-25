# Doing the Experiment
# Version 1
# Vikram Anantha
# Feb 7 2021

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

cnx = create_connection()
cursor = cnx.cursor(buffered=True)

time_for_models = []
diff_scores = []

def main():
    df = get_data()
    cols = ['grade']
    for j in range(3, 49):
        cols.append('took_class_%s' % j)
    test = test_data()
    different_types = ['rf', 'lr', 'mlp']
    # different_types.remove('mlp')
    all_data = []
    diff_models = []
    
    for i in different_types:
        input("\n\n\n\nTRAINING MODEL: %s\n\n\n\n" % i)
        # print("\n\n\n\nTRAINING MODEL: %s\n\n\n\n" % i)
        models_and_scores = setup_models(i, cols, df)
        models, scores = models_and_scores[0], models_and_scores[1]
        diff_models.append(models)
        diff_scores.append(scores)
        predictions = test_v1(models=models, test=test)
        all_data.append(predictions)
    for i in all_data:
        print(i)
    # print(">>> %s" % all_data)
    # print(diff_scores)
    for i in range(len(diff_scores)):
        print("AVG for %s = %s" % (different_types[i], avg(diff_scores[i])))
    graph1()
    print("--------------------")
    graph2()
    print("--------------------")
    graph3()

def get_data():
    return pd.read_csv("/Users/vikramanantha/Documents/Codes/[P] HELM Big Shift Codes/students_v3.csv")

def setup_models(model_name, cols, df):
    models = [None, None, None]
    scores = [None, None, None]
    sql0 = 'SELECT id FROM classes'
    cursor.execute(sql0)
    num_classes = cursor.fetchall()[-1][0]
    time_for_models.append([])
    for i in range(3, num_classes+1): # this is for each model
        if i == 40 or i == 46:
            models.append(None)
            scores.append(None)
            time_for_models[-1].append(None)
            continue
        
        x_cols = df.loc[df['class'] == i]
        x = np.array(x_cols[cols])
        y = x_cols[['probs']]
        x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=0)
        
        if model_name == "lr":
            m_v1 = LogisticRegression()
        elif model_name == "rf":
            m_v1 = RandomForestClassifier()
        elif model_name == "mlp":
            m_v1 = MLPClassifier()
        start = clock()
        m_v1.fit(x_train, y_train)
        end = clock()
        time_for_models[-1].append(duration(start, end))
        # print(m_v1.score(x_test, y_test))
        # print("\n\n\n\n\n\n\n")
        acc = score(m_v1, x_test, y_test)
        models.append(m_v1)
        scores.append(acc)
    return [models,scores]

def test_data():
    test = [7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    test[3-2] = 10
    test[4-2] = 10
    test[12-2] = 10
    test = np.array(test)
    return test

def test_v1(test, models):
    predictions1 = []
    for m in models:
        if m == None:
            continue
        pred = list(m.predict(test.reshape(1, -1)))[0]
        cool = [pred, models.index(m)]
        predictions1.append(cool)
    predictions1.sort()
    return predictions1[-5:]

def test_v2(test, models):
    predictions2 = []
    for m in models:
        if m == None:
            continue
        mclass = list(m.classes_)
        pred = list(m.predict_proba(test.reshape(1, -1))[0])
        for p in range(len(pred)):
            pred[p] = int(pred[p] * 100)
        print(pred)
        print(mclass)
        q = 0
        for p in range(len(pred)-2,len(pred)):
            q += pred[p]*(mclass[p]**2)
        cool = [int(q), models.index(m)]
        predictions2.append(cool)
        print(cool)
        print()
    predictions2.sort()
    return predictions2[-5:]

def score(model, x, y):
    one_counter = 0
    zip_counter = 0
    for i in range(len(x)):
        # print(np.reshape(list(x[i]), (1,-1)))
        # print()
        y_probs = model.predict_proba(np.reshape(list(x[i]), (1,-1)))
        y_class = model.classes_
        # print(y_probs)
        # print(y_class)
        prediction = y_class[numpy.where(y_probs[0] == numpy.amax(y_probs))][0]
        actual = np.array(y)[i][0]
        # print("Prediction: %s" % prediction)
        # print("Actual: %s" % actual)
        
        if prediction != actual:
            zip_counter += 1
        else:
            one_counter += 1
    # print("%s, %s" % (one_counter, zip_counter))
    print("\n%s\n\n\n" % (100*one_counter / (one_counter + zip_counter)))
    return int(10 * (100*one_counter / (one_counter + zip_counter)))/10
        
def avg(arr):
    none_counter = 0
    sum = 0
    for i in arr:
        if i != None:
            sum += i
        else:
            none_counter += 1
    return sum / (len(arr)-none_counter)

def clock():
    return int(round(time.time() * 10000000))

def duration(start, end):
    return (end-start)/10000

def graph1():
    for i in time_for_models:
        print(avg(i))

def graph2():
    for i in range(len(diff_scores)):
        print("%s" % avg(diff_scores[i]))
    indexes = []
    for i in range(0, len(diff_scores[0])):
        indexes.append(i)
    cols = {
        "Indexes": indexes,
        "RF": diff_scores[0],
        "LR": diff_scores[1],
        "MLP": diff_scores[2]
    }
    df = pd.DataFrame(cols, columns = ["Indexes", "RF", "LR", "MLP"])
    # print(df)
    df.to_csv ('graph2.csv', index = False, header=True)

def graph3():
    
    cursor.execute("SELECT id FROM classes")
    ids = cursor.fetchall()
    num_signups = [None]* (ids[-1][0]+1)
    for i in ids:
        cursor.execute("SELECT student_id FROM classes_to_students WHERE class_id = '{}'".format(i[0]))
        students = []
        sss = cursor.fetchall()
        for j in sss:
            if j[0] not in students:
                students.append(j[0])
        num_signups[i[0]] = len(students)
        
    
    cols = {
        "RF": diff_scores[0],
        "LR": diff_scores[1],
        "MLP": diff_scores[2],
        "NoS": num_signups
    }
    df = pd.DataFrame(cols, columns = ["RF", "LR", "MLP", "NoS"])
    # print(df)
    df.to_csv ('graph3.csv', index = True, header=True)
main()