from flask import Flask, render_template, jsonify, request
import sqlite3, jinja2
from datetime import datetime, timedelta
import calendar


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

def split_array(arr, chunk_size=6):
    return [arr[i:i + chunk_size] for i in range(0, len(arr), chunk_size)]

def dataUpdate(idPair, homework):
    connection = sqlite3.connect("./database.db")
    cursor = connection.cursor()

    cursor.execute('''
    UPDATE Couples
    SET
        homework = ?
    WHERE id = ?
    ''', (homework, idPair)) 

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

def getlistTransmitData():
    year = datetime.now().year
    month = datetime.now().month

    date = datetime.now().day
    dates = calendar.monthcalendar(year, month) + calendar.monthcalendar(year if month != 12 else year + 1, month + 1 if month != 12 else 1)
    
    for datelist in dates:
        if date in datelist:
            dates = dates[dates.index(datelist) : dates.index(datelist) + 4] 
            dates = [date for datelist in dates for date in datelist if date != 0]
            
            break
    dates.pop(20)
    dates.pop(13)
    dates.pop(6)
    dates = split_array(dates, 6)
    return dates, dates[0][0], dates[-1][-1], date

app = Flask(__name__)



#initDb()
#addValues()
#getListForRender(startDay, endDay)




#Указатели начала и канца отслеживаемых данных

@app.route('/')
def renderMain():
    return render_template("mainPage.html")

@app.route('/studentPage.html')
def renderStudent():
    
    returnDateList = getlistTransmitData()

    listTransmitDate = returnDateList[0]
    startDay = returnDateList[1]
    endDay = returnDateList[2]
    currentday = returnDateList[3]

    listTransmit = getListForRender(startDay, endDay)

    return render_template("studentPage.html", listTransmit=listTransmit, listTransmitDate=listTransmitDate, dayNameList = ['пн', 'вт', 'ср', 'чт', 'пт', 'сб'], currentday=currentday)

@app.route('/mainPage.html')
def renderMain_fromstudent():
    return render_template("mainPage.html")


@app.route('/api/endpoint', methods=['POST'])
def handle_post():
    transmitdata = request.get_json()

    date = transmitdata["date"]
    pairindex = transmitdata["pairindex"]
    homework = transmitdata["homework"]
    
    idPair = date + str(int(pairindex) - 1)
    print(idPair, homework)
    dataUpdate(idPair, homework)    

if __name__ == '__main__':
    app.run()