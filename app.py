from flask import Flask, render_template, request
from datetime import datetime
import pandas as pd

app = Flask(__name__)

#Create test dataframe
days_with_classes = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]
timeslots = ["Morning","Afternoon","Evening"]
scheduleFillers = ["","",""]

testdf = pd.DataFrame(timeslots,columns=["Time"])
for day in days_with_classes:
    testdf[day] = scheduleFillers

@app.route('/')
def index():
    return render_template('index.html', table = testdf)

@app.route('/newclass', methods= ['POST','GET'])
def add_new_class():
    if request.method == "POST":
        pass
    else:
        return render_template('newclass.html', table = testdf, days = days_with_classes, times=timeslots)

if __name__ == '__main__':
    app.run(debug=True)