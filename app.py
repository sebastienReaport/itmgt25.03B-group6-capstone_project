from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///schedules.db'
db = SQLAlchemy(app)

class classes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    class_name = db.Column(db.string(200), nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)