from flask import Flask, render_template, request
from config import dbname, dbhost, dbport
import json
import psycopg2

app = Flask(__name__)

@app.route('/')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method =='GET':
        return render_template('login.html')
    if request.method == 'POST':
        username = request.form['uname']
        password = request.form['pass']
        conn = psycopg2.connect(dbname=dbname,host=dbhost,port=dbport)
        cur  = conn.cursor()
        cur.execute("SELECT username,password FROM users WHERE username = '%s' and password = '%s'", (username,password))
        if cur.fetchone() is not None:
            #session['user'] = username
            return render_template('dashboard.html')
        else:
            return render_template('no_user.html')



@app.route('/create_user', methods=['GET', 'POST'])
def create_user():
    if request.method =='GET':
        return render_template('create_user.html')
    if request.method == 'POST':
        username = request.form['uname']
        password = request.form['pass']
        conn = psycopg2.connect(dbname=dbname,host=dbhost,port=dbport)
        cur  = conn.cursor()
        cur.execute("SELECT username FROM users WHERE username = '%s'"%(username))
        #session['user'] = username
        if cur.fetchone() is not None:
            return render_template('user_exists.html')
        else:
            cur.execute("INSERT INTO users(username,password) VALUES ('%s', '%s');"%(username,password))
            return render_template('user_created.html')
    
@app.route('/dashboard', methods=['GET',])
def dashboard():
    return render_template('create_user.html')

if __name__=='__main__':
    app.run(host='0.0.0.0', port=8080)
