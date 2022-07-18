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
        #Get Time
        startTime = int(formResponse.get('class_time_start'))
        endTime = int(formResponse.get('class_time_end'))
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
        days_with_classes = list(formResponse.get('days').split(","))
        #Add to Schedule
        for time in timeSlotIndeces:
            for day in days_with_classes:
                testdf.loc[time][day] = formResponse.get('class_name')
        return redirect(url_for('index'))
        
    else:
        return render_template('newclass.html', table = testdf)

@app.route('/update/<className>', methods= ['POST','GET'])
def update(className):
    #Find Record
    recordToUpdate = dict()
    for records in classRecords:
        if records["class_name"] == className:
            recordToUpdate.update(records)
            break
    return render_template('update.html', recordToUpdate = recordToUpdate)

@app.route('/delete/', methods= ['POST','GET'])
def delete():
    #Find Record
    return render_template('delete.html', classRecords = classRecords)

if __name__ == '__main__':
    app.run(debug=True)