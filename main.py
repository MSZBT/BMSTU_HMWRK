from flask import Flask, render_template, jsonify, request
import sqlite3, jinja2


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


def getListForRender(start, stop):
    connection = sqlite3.connect("./database.db")
    cursor = connection.cursor()

    listForRender = []

    for day in range(start, stop + 1):
        cursor.execute(f'''SELECT * FROM Couples WHERE date = {day}''')
        middleList = cursor.fetchall()
        if (middleList):
            listForRender.append(middleList)
    connection.commit()
    connection.close()
    return listForRender



app = Flask(__name__)


startDay = 20
endDay = 26
#initDb()
#addValues()
#getListForRender(startDay, endDay)




#Указатели начала и канца отслеживаемых данных

@app.route('/')
def renderMain():
    return render_template("mainPage.html")

@app.route('/studentPage.html')
def renderStudent():
    listTransmit = getListForRender(startDay, endDay)
    print(listTransmit)
    return render_template("studentPage.html", listTransmit=listTransmit)

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