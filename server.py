from flask import Flask, jsonify, render_template
import sqlite3
import pandas as pd
from sqlalchemy import create_engine
import numpy as np

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn

db_url = 'sqlite:///data.db'
engine = create_engine(db_url, echo=False)
df = pd.read_sql('select * from airLineData', engine)
# print(df)

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get-datachart')
def get_datachart():
    df = pd.read_sql('SELECT Continents, AVG(Age) AS MeanAge FROM airLineData GROUP BY Continents;', engine)  #Betala3 el distincit nationalities whith their counts

    data = []
    for i in range(len(df)):
        data.append({"country":df.loc[i]["Continents"],"value":int(df.loc[i]["MeanAge"])})
        # data.append({"country":category[i],"value":int(values[i])})
    return jsonify(data)


@app.route('/get-datachart2')
def get_datachart2():
    df = pd.read_sql('SELECT "Flight Status", COUNT(*) AS Count FROM airLineData GROUP BY "Flight Status"', engine) #Betala3 el distincit nationalities whith their counts
    data = []
    for i in range(len(df)):
        data.append({"category": df.loc[i]["Flight Status"], "value": int(df.loc[i]["Count"])})
    return jsonify(data)

@app.route('/get-datachart3')
def get_datachart3():
    df = pd.read_sql('SELECT "Continents" AS category, COUNT(*) AS value FROM airLineData GROUP BY "Continents"', engine)  #Betala3 el distincit nationalities whith their counts
    data = []
    for i in range(len(df)):
        data.append({"category":df.loc[i]["category"],"value":int(df.loc[i]["value"])})
    return jsonify(data)

@app.route('/get-datachart4')
def get_datachart4():
    data = []
    df1 = pd.read_sql('SELECT Nationality, COUNT(*) AS Count FROM airLineData GROUP BY Nationality ORDER BY Count DESC LIMIT 5;', engine)  #Betala3 el distincit nationalities whith their counts
    for j in range(len(df1)):
        my_dict = dict()
        my_dict["category"] = df1.loc[j]['Nationality']
        my_dict["value"] = int(df1.loc[j]['Count'])
        sub_list = []
        query_string = "SELECT COUNT(\'PASSENGER ID\') AS PassengerCount, Gender FROM airLineData WHERE Nationality = \'"+str(df1.loc[j]["Nationality"]) + "\' GROUP BY GENDER;"
        df2 = pd.read_sql(query_string, engine)
        for i in range(len(df2)):
            sub_list.append({'category': df2.loc[i]['Gender'], 'value': int(df2.loc[i]['PassengerCount'])})
        my_dict["subData"] = sub_list
        data.append(my_dict)    
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)

# Working on data momken tefkeslaha
# df = pd.read_csv('Airline Dataset Updated')
# df['Age'] = np.random.randint(45, 80, size=len(df)/2)
# df.to_csv('Airline Dataset Updated', index=False)


# Creating the database
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as ex:
        print(ex)
    return conn


create_connection("data.db")
connection = create_connection("data.db")
df=pd.read_csv("Airline Dataset.csv")
df.to_sql("airLineData.csv", connection, if_exists="replace")


            