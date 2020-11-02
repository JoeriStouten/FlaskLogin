from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import sqlite3

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///FlaskLoginDataBase.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(10), nullable=False)
    password = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(10), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return '<User %r>' % self.id

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        new_username = request.form['username']
        new_password = request.form['password']

        con = sqlite3.connect("FlaskLoginDataBase.db") 
        cursor = con.cursor()
        cursor.execute("SELECT * FROM User WHERE username = ?", [new_username])

        if cursor.fetchone() is not None:
            user = User.query.filter_by(username=new_username).first()
            if user.password == new_password:
                return render_template('user_home.html', user=user)
            else:
                users = User.query.order_by(User.date_created).all()
                return render_template('index_wrong.html', users=users)
        else:
            users = User.query.order_by(User.date_created).all()
            return render_template('index_wrong.html', users=users)
    else:
        users = User.query.order_by(User.date_created).all()
        return render_template('index.html', users=users)

@app.route('/create_account/', methods=['POST', 'GET'])
def create_account():
    if request.method == 'POST':
        new_username = request.form['username']
        new_password = request.form['password']
        new_email = request.form['email']

        con = sqlite3.connect("FlaskLoginDataBase.db") 
        cursor = con.cursor()
        cursor.execute("SELECT * FROM User WHERE username = ?", [new_username])

        if cursor.fetchone() is not None:
            return render_template('create_account_wrong.html')
        else:
            new_user = User(username=new_username, password=new_password, email=new_email)

        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect('/')
        except:
            return "Something went wrong..."
    else:
        return render_template('create_account.html')

@app.route('/delete/<int:id>')
def delete(id):
    user_to_delete = User.query.get_or_404(id)

    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "There was a problem deleting the user..."

if __name__ == "__main__":
    app.run(debug=True)
