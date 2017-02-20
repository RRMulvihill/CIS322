from flask import Flask, render_template, request
from config import dbname, dbhost, dbport, lost_priv, lost_pub, user_pub, prod_pub
import json
import psycopg2

app = Flask(__name__)

@app.route('/')

@app.route('/login' methods=['GET', 'POST'])
def login():
    if request.method =='GET':
        return render_template('login.html')
    if request.method == 'POST':
        username = request.form['uname']
        password = request.form['pass']
        conn = psycopg2.connect(dbname=dbname,host=dbhost,port=dbport)
        cur  = conn.cursor()
        cur.execute('SELECT username FROM users WHERE username = %s', (username))
        if cur.fetchone() > 0:
            session['user'] = username
            return render_template('dashboard.html')
        else:
            return render_template('no_user.html')
        return render_template('create_user.html')



@app.route('/create_user' methods=['GET', 'POST'])
def create_user():
    if request.method =='GET':
        return render_template('create_user.html')
    if request.method == 'POST':
        username = request.form['uname']
        password = request.form['pass']
        conn = psycopg2.connect(dbname=dbname,host=dbhost,port=dbport)
        cur  = conn.cursor()
        cur.execute('SELECT username FROM users WHERE username = %s', (username))
        session['user'] = username
        if cur.fetchone() > 0:
            return render_template('create_user.html')
        else:
            cur.execute('INSERT INTO users(username,password) VALUES (%s, %s);'%(username,password))
            return render_template('create_user.html')
        return render_template('create_user.html')

if __name__=='__main__':
    app.run(host='0.0.0.0', port=8080)
