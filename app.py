from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime
from numpy import record
import pandas as pd
import json

app = Flask(__name__)

#Create Schedule Base dataframe
days_of_week = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]
startTime = 700 
endTime = 2200
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
scheduleTable = pd.DataFrame(timeSlots,columns=["Time"])
generalTable = pd.DataFrame(timeSlots,columns=["Time"])
for day in days_of_week:
    scheduleTable[day] = scheduleFillers
    generalTable[day] = scheduleFillers
timeslot_and_index = dict(zip(timeSlots, scheduleTable.index)) #Same for generalTable

#Create Global Variables and Lists
classRecords = list()
currentUser = ""
pathToRecords = ".\\records\\users.json"
pathToSchedules = ".\\records\\schedules.json"
currentlyBusy = list()
currentlyFree = list()

#Function that updates schedule table
def edit_schedule_table(record, action):
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
                scheduleTable.loc[time][day] = record["class_name"]
    elif action == "Delete":
        for time in timeSlotIndeces:
            for day in days_with_classes:
                scheduleTable.loc[time][day] = ""

#Function that adds to general table
def edit_general_table(record, user):
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
    #Perform Add to table
    for time in timeSlotIndeces:
        for day in days_with_classes:
            if generalTable.loc[time][day] == "":
                generalTable.loc[time][day] = list()
                generalTable.loc[time][day].append(f"{user}: {record['class_name']}")
            else:
                generalTable.loc[time][day].append(f"{user}: {record['class_name']}")

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
        edit_schedule_table(record, "Add")

#Function that deletes all classes
def del_classes_in_table():
    for record in classRecords:
        edit_schedule_table(record, "Delete")

#App Code for Login Page
@app.route('/', methods= ['POST','GET'])
def login():
    if request.method == "POST":
        formResponse = request.form
        if "newUser" in formResponse:
            #Check if username already exists
            listOfUsers = get_users()
            for users in listOfUsers:
                if users == formResponse.get("newUser"):
                    return render_template('login.html', listOfUsers = listOfUsers, table = generalTable, timeSlots = timeSlots, error = "Username Already Taken!")
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
        return redirect(url_for('login'))
    else:
        listOfUsers = get_users()
        listOfUserSchedules = get_user_schedule()
        del_classes_in_table()
        classRecords.clear()

        #Clear General table and user availability
        for day in days_of_week:
            generalTable[day] = scheduleFillers
        currentlyBusy.clear()
        currentlyFree.clear()

        #Get current time
        timeNow = int(datetime.now().strftime('%H%M'))
        dayNow = datetime.now().strftime('%A')

        #Check for New Users with no Sched
        listOfUsersWithSched = listOfUsers.copy()
        for user in listOfUsers:
            if user not in listOfUserSchedules.keys():
                listOfUsersWithSched.remove(user)

        #Display Combined Calendar
        for user in listOfUsersWithSched:
            busy = 0
            for record in listOfUserSchedules[user]:
                edit_general_table(record, user)
                #Get user availability
                daysWithClasses = record["days"].split(",")
                if timeNow >= int(record["class_time_start"]) and timeNow < int(record["class_time_end"]) and dayNow in daysWithClasses:
                    busy += 1
            #Add user availability
            if busy == 0:
                currentlyFree.append(user)
            elif busy >= 1:
                currentlyBusy.append(user)

        if len(currentlyFree) == 0:
            currentlyFree.append("None")
        if len(currentlyBusy) == 0:
            currentlyBusy.append("None")
        return render_template('login.html', listOfUsers = listOfUsers, table = generalTable, timeSlots = timeSlots, currentlyFree = currentlyFree, currentlyBusy = currentlyBusy)

#App Code for Calendar Page
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
    return render_template('calendar.html', table = scheduleTable, currentUser = currentUser, currentClass = currentClass, timeSlots = timeSlots)

#App Code for New Class Page
@app.route('/newclass', methods= ['POST','GET'])
def add_new_class():
    if request.method == "POST":
        formResponse = request.form
        form_start = int(formResponse.get("class_time_start"))
        form_end = int(formResponse.get("class_time_end"))
        formDaysWithClasses = formResponse.get("days").split(",")
        #Check if class exists
        for records in classRecords:
            record_start = int(records["class_time_start"])
            record_end = int(records["class_time_end"])
            record_name = records["class_name"]
            daysWithClasses = records["days"].split(",")
            if record_name == formResponse.get("class_name"):
                error = f"Class '{record_name}' already exists! Write a new name or edit the class instead!"
                return render_template('newclass.html', table = scheduleTable, error = error, formResponse = formResponse, currentUser = currentUser)
            elif form_start == record_start or form_end == record_end or (form_start > record_start and form_end < record_end) or (form_start > record_start and form_start < record_end) or (form_end > record_start and form_end < record_end) or (form_start < record_start and form_end > record_end):
                for classDay in daysWithClasses:
                    if classDay in formDaysWithClasses:
                        error = f"Schedule is in conflict with {record_name}!"
                        return render_template('newclass.html', error = error, formResponse = formResponse, currentUser = currentUser)
        classRecords.append(formResponse)
        return redirect(url_for('index'))
    else:
        return render_template('newclass.html', currentUser = currentUser)

#App Code for Edit Class Page
@app.route('/update/<className>', methods= ['POST','GET'])
def update(className):
    recordToUpdate = dict()
    for records in classRecords:
        if records["class_name"] == className:
            recordToUpdate.update(records)
            break
    
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
            daysWithClasses = records["days"].split(",")
            if record_name == formResponse.get("class_name") and formResponse.get("class_name") != className:
                error = f"Class '{record_name}' already exists! Write a new name instead!"
                return render_template('update.html', recordToUpdate = recordToUpdate, error = error, currentUser = currentUser, className = className)
            if (form_start == record_start or form_end == record_end or (form_start > record_start and form_end < record_end) or (form_start > record_start and form_start < record_end) or (form_end > record_start and form_end < record_end) or (form_start < record_start and form_end > record_end)) and record_name != className:
                for classDay in daysWithClasses:
                    if classDay in formDaysWithClasses:
                        error = f"Schedule is in conflict with {record_name}!"
                        return render_template('update.html', recordToUpdate = recordToUpdate, error = error, currentUser = currentUser, className = className)
        #Update Class when Clear
        for records in classRecords:
            if records["class_name"] == className:
                edit_schedule_table(records, "Delete")
                classRecords.remove(records)
                classRecords.append(formResponse)
                return redirect(url_for('index'))
    else:
        return render_template('update.html', recordToUpdate = recordToUpdate, currentUser = currentUser, className = className)

#App Code for Delete Class Page
@app.route('/delete/', methods= ['POST','GET'])
def delete():
    if request.method == "POST":
        formResponse = request.form
        if formResponse["submit"] == "Delete Class":
            for records in classRecords:
                if records["class_name"] == formResponse.get("class_name"):
                    edit_schedule_table(records, "Delete")
                    classRecords.remove(records)
        elif formResponse["submit"] == "Delete All Classes":
            recordsToDelete = classRecords.copy()
            for records in recordsToDelete:
                edit_schedule_table(records, "Delete")
                classRecords.remove(records)
        return redirect(url_for('index'))
    else:
        return render_template('delete.html', classRecords = classRecords, currentUser = currentUser)

if __name__ == '__main__':
    app.run(debug=True)