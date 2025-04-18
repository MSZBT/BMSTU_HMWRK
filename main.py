from flask import Flask, render_template, jsonify, request
import sqlite3




def initDb():
    connection = sqlite3.connect("./database.db")
    cursor = connection.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Couples (
        id TEXT,
        date INTEGER,
        pairindex INTEGER,
        pairname TEXT,
        homework TEXT UNIQE,
        cab TEXT,
        pairtype TEXT
    )''')
    #ID - комбинация из даты и пары 
    connection.commit()
    connection.close()

def addValues():
    connection = sqlite3.connect("./database.db")
    cursor = connection.cursor()
    
    cursor.execute('''
        INSERT INTO Couples(id, date, pairindex, pairname, homework, cab, pairtype) 
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (str(26) + str(1), 26, 1, 'pairname', 'homework1', 'cab', 'pairtype'))

    connection.commit()
    connection.close()

def getValues():
    connection = sqlite3.connect("./database.db")
    cursor = connection.cursor()

    cursor.execute('''SELECT * FROM Couples''')
    selection = cursor.fetchall()

    connection.commit()
    connection.close()
    print(selection)
app = Flask(__name__)

#initDb()
#addValues()
getValues()

@app.route('/')
def renderMain():
    return render_template("mainPage.html")

@app.route('/studentPage.html')
def renderStudent():
    return render_template("studentPage.html")

@app.route('/mainPage.html')
def renderMain_fromstudent():
    return render_template("mainPage.html")


@app.route('/api/endpoint', methods=['POST'])
def handle_post():
    transmitdata = request.get_json()

    date = transmitdata["date"]
    pairindex = transmitdata["pairindex"]
    pairname = transmitdata["pairname"]
    homework = transmitdata["homework"]
    print(date, pairindex, pairname, homework)

if __name__ == '__main__':
    app.run()