from flask import Flask, render_template, request
from config import dbname, dbhost, dbport, lost_priv, lost_pub, user_pub, prod_pub
import json
import psycopg2
import datetime

app = Flask(__name__)

@app.route('/')

@app.route('/create_user' methods=['GET', 'POST'])
def create_user():
    if request.method =='POST':
        return render_template('create_user.html')
    if request.method == 'POST':
        username = request.form['uname']
        password = request.form['pass']
        session['user'] = username
        conn = psycopg2.connect(dbname=dbname,host=dbhost,port=dbport)
        cur  = conn.cursor()
        cur.execute('SELECT username FROM users WHERE username = %s', (username))
        res = cur.fetchall()
        return render_template('create_user.html')

if __name__=='__main__':
    app.run(host='0.0.0.0', port=8080)
