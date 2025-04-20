from flask import Flask, render_template, jsonify, request
import sqlite3, jinja2

from datetime import datetime, timedelta
import calendar

def split_array(arr, chunk_size=6):
    return [arr[i:i + chunk_size] for i in range(0, len(arr), chunk_size)]

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

    #date = datetime.now().day
    date = 21
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

def DBrenew():
    flag = 0 #отвечает за изменение числителся / знаменателя
    lastRunDay =0
    while True:
        date = datetime.now().day
        dates = getlistTransmitData()
        executionList_flag0 = [
            (str(dates[3][0] + 0), dates[3][0], 0, "Пар нет", "Отдыхай", "дом", "Солнышко"),

            (str(dates[3][1] + 0), dates[3][1], 0, "Химия", "Нет | еще не занесено", "327.1", "Лекция"),
            (str(dates[3][1] + 1), dates[3][1], 1, "Информатика", "Нет | еще не занесено", "601к", "Семинар"),
            (str(dates[3][1] + 2), dates[3][1], 2, "ФЛИТА", "Нет | еще не занесено", "601к", "Семинар"),

            (str(dates[3][2] + 0), dates[3][2], 0, "Информатика", "Нет | еще не занесено", "221х", "Лекция"),
            (str(dates[3][2] + 1), dates[3][2], 1, "ИниДу", "Нет | еще не занесено", "221х", "Лекция"),
            (str(dates[3][2] + 2), dates[3][2], 2, "ИниДу", "Нет | еще не занесено", "216х", "Семинар"),

            (str(dates[3][3] + 0), dates[3][3], 0, "Физика", "Нет | еще не занесено", "ФН4", "Лабы"),
            (str(dates[3][3] + 1), dates[3][3], 1, "Физика", "Нет | еще не занесено", "323", "Лекция"),
            (str(dates[3][3] + 2), dates[3][3], 2, "Химия", "Нет | еще не занесено", "241", "Лабы"),
            (str(dates[3][3] + 3), dates[3][3], 3, "Бассейн", "Нет | еще не занесено", "СК", "Семинар"),

            (str(dates[3][4] + 0), dates[3][4], 0, "Бассейн", "Нет | еще не занесено", "СК", "Семинар"),
            (str(dates[3][4] + 1), dates[3][4], 1, "История", "Нет | еще не занесено", "520к", "Семинар"),
            (str(dates[3][4] + 2), dates[3][4], 2, "ИниДу", "Нет | еще не занесено", "520к", "Семинар"),

            (str(dates[3][5] + 0), dates[3][5], 0, "Ин. язык", "Нет | еще не занесено", "523к/514к", "Семинар"),
            (str(dates[3][5] + 1), dates[3][5], 1, "Линал", "Нет | еще не занесено", "527к", "Семинар"),
            (str(dates[3][5] + 2), dates[3][5], 2, "Линал", "Нет | еще не занесено", "535к", "Лекция"),
        ]

        executionList_flag1 = [
            (str(dates[3][0] + 0), dates[3][0], 0, "Пар нет", "Отдыхай", "дом", "Солнышко"),

            (str(dates[3][1] + 0), dates[3][1], 0, "Химия", "Нет | еще не занесено", "327.1", "Лекция"),
            (str(dates[3][1] + 1), dates[3][1], 1, "Информатика", "Нет | еще не занесено", "601к", "Семинар"),
            (str(dates[3][1] + 2), dates[3][1], 2, "ФЛИТА", "Нет | еще не занесено", "601к", "Семинар"),

            (str(dates[3][2] + 0), dates[3][2], 0, "Информатика", "Нет | еще не занесено", "221х", "Лекция"),
            (str(dates[3][2] + 1), dates[3][2], 1, "ИниДу", "Нет | еще не занесено", "221х", "Лекция"),
            (str(dates[3][2] + 2), dates[3][2], 2, "ФЛИТА", "Нет | еще не занесено", "221х", "Лекция"),
            (str(dates[3][2] + 2), dates[3][2], 3, "История", "Нет | еще не занесено", "221х", "Лекция"),

            (str(dates[3][3] + 0), dates[3][3], 0, "Физика", "Нет | еще не занесено", "304", "Семинар"),
            (str(dates[3][3] + 1), dates[3][3], 1, "Физика", "Нет | еще не занесено", "323", "Лекция"),
            (str(dates[3][3] + 2), dates[3][3], 2, "Химия", "Нет | еще не занесено", "241", "Лабы"),
            (str(dates[3][3] + 3), dates[3][3], 3, "Бассейн", "Нет | еще не занесено", "СК", "Семинар"),

            (str(dates[3][4] + 0), dates[3][4], 0, "Бассейн", "Нет | еще не занесено", "СК", "Семинар"),
            (str(dates[3][4] + 1), dates[3][4], 1, "История", "Нет | еще не занесено", "520к", "Семинар"),
            (str(dates[3][4] + 2), dates[3][4], 2, "ИниДу", "Нет | еще не занесено", "520к", "Семинар"),

            (str(dates[3][5] + 0), dates[3][5], 0, "Ин. язык", "Нет | еще не занесено", "523к/514к", "Семинар"),
            (str(dates[3][5] + 1), dates[3][5], 1, "Линал", "Нет | еще не занесено", "527к", "Семинар"),
            (str(dates[3][5] + 2), dates[3][5], 2, "Линал", "Нет | еще не занесено", "535к", "Лекция"),
        ]

        dates = [data for subdates in dates for data in subdates]

        if dates.index(date) in [0, 6, 12]:
            connection = sqlite3.connect("./database.db")
            cursor = connection.cursor()

            cursor.execute('''
            DELETE FROM Couples WHERE date < {date}
            ''')
            cursor.executemany('INSERT INTO Couples(id, date, pairindex, pairname, homework, cab, pairtype) VALUES (?, ?, ?, ?, ?, ?, ?)', executionList_flag0 if flag == 0 else executionList_flag1)
            flag = not(flag)

        connection.commit()
        connection.close()


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

    print(listTransmitDate)

    return render_template("studentPage.html", listTransmit=listTransmit, listTransmitDate=listTransmitDate, dayNameList = ['пн', 'вт', 'ср', 'чт', 'пт', 'сб', 'вс'], currentday=currentday)

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