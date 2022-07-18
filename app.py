from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime
import pandas as pd

app = Flask(__name__)

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

#Create Classes List
classRecords = list()

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

#App Code
@app.route('/')
def index():
    return render_template('index.html', table = testdf)

@app.route('/newclass', methods= ['POST','GET'])
def add_new_class():
    if request.method == "POST":
        formResponse = request.form
        #Check if class exists
        for records in classRecords:
            if records["class_name"] == formResponse.get("class_name"):
                return redirect(url_for('index'))
        classRecords.append(formResponse)
        edit_table(record = formResponse, action = "Add")
        return redirect(url_for('index'))
    else:
        return render_template('newclass.html', table = testdf)

@app.route('/update/<className>', methods= ['POST','GET'])
def update(className):
    if request.method == "POST":
        formResponse = request.form
        for records in classRecords:
            if records["class_name"] == className:
                edit_table(record = records, action = "Delete")
                classRecords.remove(records)
                edit_table(record = formResponse, action = "Add")
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