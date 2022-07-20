from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime
import pandas as pd
import json

app = Flask(__name__)
app.secret_key = b'wOwIdonTRealLYKnowWhatThisIsfor'

#Create Schedule Base dataframe
days_of_week = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]
startTime = 700
endTime = 2130
timeSlots = list()
intervalStart = startTime
while intervalStart < endTime:
    if intervalStart%100 == 0:
        intervalEnd = intervalStart + 30
    else:
        intervalEnd = intervalStart + 70
    newInterval = str(intervalStart)+"-"+str(intervalEnd)
    timeSlots.append(newInterval)
    intervalStart = intervalEnd
scheduleFillers = list()
for timeslots in timeSlots:
    scheduleFillers.append("")
testdf = pd.DataFrame(timeSlots,columns=["Time"])
for day in days_of_week:
    testdf[day] = scheduleFillers
timeslot_and_index = dict(zip(timeSlots, testdf.index))

#Create JSON file to store basic info
calendarInfo = {"days": days_of_week, "timeslots": timeSlots}
with open(".\\records\\calendarInfo.json", "w") as f:
    json.dump(calendarInfo,f)

#Create Classes List
classRecords = list()
currentUser = ""
pathToRecords = ".\\records\\users.json"
pathToSchedules = ".\\records\\schedules.json"

#Function that updates table
def edit_table(record, action):
    startTime = int(record['class_time_start'])
    endTime = int(record['class_time_end'])
    intervalStart = startTime
    timeSlotIndeces = list()
    while intervalStart < endTime:
        if intervalStart%100 == 0:
            intervalEnd = intervalStart + 30
        else:
            intervalEnd = intervalStart + 70
        newInterval = str(intervalStart)+"-"+str(intervalEnd)
        timeSlotIndeces.append(timeslot_and_index[newInterval])
        intervalStart = intervalEnd
    #Get Days
    days_with_classes = list(record['days'].split(","))
    #Perform Action
    if action == "Add":
        for time in timeSlotIndeces:
            for day in days_with_classes:
                testdf.loc[time][day] = record["class_name"]
    elif action == "Delete":
        for time in timeSlotIndeces:
            for day in days_with_classes:
                testdf.loc[time][day] = ""

#Function that get users
def get_users():
    try:
        with open(pathToRecords, "r") as f:
            listOfUsers = json.load(f)
    except:
        listOfUsers = list()
    finally:
        return listOfUsers

#Function that gets users' schedules
def get_user_schedule():
    try:
        with open(pathToSchedules, "r") as f:
            listOfUserSchedules = json.load(f)
    except:
        listOfUserSchedules = dict()
    finally:
        return listOfUserSchedules

#Function that adds schedules to table
def add_classes_to_table():
    for record in classRecords:
        edit_table(record, "Add")

#Function that deletes all classes
def del_classes_in_table():
    for record in classRecords:
        edit_table(record, "Delete")

#Function that checks if new/updated class is in conflict
def check_time_conflict(record, formResponse, webpage):
    record_start = int(record["class_time_start"])
    record_end = int(record["class_time_end"])
    form_start = int(formResponse.get("class_time_start"))
    form_end = int(formResponse.get("class_time_end"))
    class_name = record["class_name"]

    if form_start > record_start and form_start < record_end or form_end > record_start and form_end < record_end:
        error = f"Schedule is in conflict with {class_name}!"
        return render_template(webpage, table = testdf, error = error)

#App Code
@app.route('/', methods= ['POST','GET'])
def login():
    if request.method == "POST":
        formResponse = request.form
        if "newUser" in formResponse:
            #Check if username already exists
            listOfUsers = get_users()
            for users in listOfUsers:
                if users == formResponse.get("newUser"):
                    return redirect(url_for('newUser'))
            #Add new username to database
            listOfUsers.append(formResponse.get("newUser"))
            with open(pathToRecords, "w") as f:
                    json.dump(listOfUsers,f)
        elif "deleteUser" in formResponse:
            #Check if username already exists and then delete it
            listOfUsers = get_users()
            if formResponse.get("deleteUser") in listOfUsers:
                userToDelete = formResponse.get("deleteUser")
                listOfUsers.remove(userToDelete)
                listOfUserSchedules = get_user_schedule()
                if userToDelete in listOfUserSchedules.keys():
                    del listOfUserSchedules[userToDelete]
                    with open(pathToSchedules, "w") as f:
                        json.dump(listOfUserSchedules,f)
            #Update database            
            with open(pathToRecords, "w") as f:
                json.dump(listOfUsers,f)
        return render_template('login.html', listOfUsers = listOfUsers)
    else:
        listOfUsers = get_users()
        del_classes_in_table()
        classRecords.clear()
        return render_template('login.html', listOfUsers = listOfUsers)

@app.route('/calendar', methods= ['POST','GET'])
def index():
    global currentUser
    if request.method == "POST":
        username = request.form.get("username")
        currentUser = username
        #Check if user has an existing schedule
        listOfUserSchedules = get_user_schedule()
        if username in listOfUserSchedules.keys():
            for record in listOfUserSchedules[username]:
                classRecords.append(record)
            add_classes_to_table()
    else:
        add_classes_to_table()
        #Update Database
        listOfUserSchedules = get_user_schedule()
        updateUserInfo = {currentUser: classRecords}
        listOfUserSchedules.update(updateUserInfo)
        with open(pathToSchedules, "w") as f:
            json.dump(listOfUserSchedules,f)

    #Check current class
    timeNow = int(datetime.now().strftime('%H%M'))
    dayNow = datetime.now().strftime('%A')
    currentClass = "none"
    for record in classRecords:
        daysWithClasses = record["days"].split(",")
        if timeNow >= int(record["class_time_start"]) and timeNow < int(record["class_time_end"]) and dayNow in daysWithClasses:
            currentClass = record["class_name"]
            break
    return render_template('calendar.html', table = testdf, currentUser = currentUser, currentClass = currentClass)

@app.route('/newclass', methods= ['POST','GET'])
def add_new_class():
    if request.method == "POST":
        formResponse = request.form
        form_start = int(formResponse.get("class_time_start"))
        form_end = int(formResponse.get("class_time_end"))
        class_name = formResponse.get("class_name")
        formDaysWithClasses = formResponse.get("days").split(",")
        #Check if class exists
        for records in classRecords:
            record_start = int(records["class_time_start"])
            record_end = int(records["class_time_end"])
            daysWithClasses = records["days"].split(",")
            if records["class_name"] == formResponse.get("class_name"):
                error = f"Class '{class_name}' already exists! Write a new name or edit the class instead!"
                return render_template('newclass.html', table = testdf, error = error)
            elif form_start >= record_start and form_start <= record_end or form_end >= record_start and form_end <= record_end:
                for classDay in daysWithClasses:
                    if classDay in formDaysWithClasses:
                        error = f"Schedule is in conflict with {class_name}!"
                        return render_template('newclass.html', error = error)
        classRecords.append(formResponse)
        return redirect(url_for('index'))
    else:
        return render_template('newclass.html')

@app.route('/update/<className>', methods= ['POST','GET'])
def update(className):
    if request.method == "POST":
        #First Check for Conflicts
        formResponse = request.form
        form_start = int(formResponse.get("class_time_start"))
        form_end = int(formResponse.get("class_time_end"))
        formDaysWithClasses = formResponse.get("days").split(",")
        for records in classRecords:
            record_name = records["class_name"]
            record_start = int(records["class_time_start"])
            record_end = int(records["class_time_end"])
            record_className = records["class_name"]
            daysWithClasses = records["days"].split(",")
            if (form_start >= record_start and form_start <= record_end or form_end >= record_start and form_end <= record_end) and record_className != className:
                for classDay in daysWithClasses:
                    if classDay in formDaysWithClasses:
                        error = f"Schedule is in conflict with {record_name}!"
                        return render_template('update.html', recordToUpdate = formResponse, error = error)
        #Update Class when Clear
        for records in classRecords:
            if records["class_name"] == className:
                edit_table(record = records, action = "Delete")
                classRecords.remove(records)
                classRecords.append(formResponse)
                return redirect(url_for('index'))
    else:
        #Find Record
        recordToUpdate = dict()
        for records in classRecords:
            if records["class_name"] == className:
                recordToUpdate.update(records)
                break
        return render_template('update.html', recordToUpdate = recordToUpdate)

@app.route('/delete/', methods= ['POST','GET'])
def delete():
    if request.method == "POST":
        formResponse = request.form
        for records in classRecords:
            if records["class_name"] == formResponse.get("class_name"):
                edit_table(record = records, action = "Delete")
                #Remove from record
                classRecords.remove(records)
                return redirect(url_for('index'))
    else:
        return render_template('delete.html', classRecords = classRecords)

if __name__ == '__main__':
    app.run(debug=True)