from email.policy import default
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///schedules.db'
db = SQLAlchemy(app)

class reminders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reminder = db.Column(db.String(200), nullable=False)
    reminder_type = db.Column(db.Integer, db.ForeignKey('type_of_reminder.id'), nullable=False, default=4)
    reminder_urgency = db.Column(db.Integer, db.ForeignKey('type_of_urgency.id'), nullable=False, default=5)
    reminder_deadline = db.Column(db.DateTime)
    reminder_set = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<reminders %r>' % reminders.id

class type_of_reminder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_of_reminder_type = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return '<type_of_reminder %r>' % type_of_reminder.id

class type_of_urgency(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_of_reminder_urgency = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return '<type_of_urgency %r>' % type_of_urgency.id

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)