from flask import Flask, render_template, request, session
from config import dbname, dbhost, dbport
import psycopg2
import requests

app = Flask(__name__)
app.secret_key = 'secret'


conn = psycopg2.connect("dbname=lost host='/tmp/'")
cur = conn.cursor()

@app.route('/')
def login():
    return render_template('login.html',dbname=dbname,dbhost=dbhost,dbport=dbport)

@app.route('/report')
def report():
    return render_template('report.html')

@app.route('/facility')
def facility():
    cur.execute("SELECT asset_tag,description FROM assets;")
    res = cur.fetchall()
    processed_data = []
    for r in res:
        processed_data.append( dict(zip(('column_name3', 'column_name4'), r)) )
        session['processed_data_session_name'] = processed_data 
    if request.method=='GET' and 'fcName' in request.args:
        return render_template('facility.html',data=request.args.get('fcName'))
    return render_template('facility.html',data=request.args.get('fcName'))

@app.route('/transit')
def transit():
    cur.execute("SELECT arrive_dt,depart_dt FROM assets_at;")
    res = cur.fetchall()
    processed_data = []
    for r in res:
        processed_data.append( dict(zip(('column_name1','column_name2', 'column_name3', 'column_name4'), r)) )
        session['processed_data_session_name'] = processed_data 
    return render_template('transit.html',data=request.args.get('tranName'))
                               
@app.route('/logout')
def logout():
    if request.method=='GET' and 'mytext' in request.args:
        return render_template('logout.html',data=request.args.get('mytext'))

    # request.form is only populated for POST messages
    if request.method=='POST' and 'mytext' in request.form:
        return render_template('logout.html',data=request.form['mytext'])
    return render_template('logout.html')
if __name__=='__main__':
    app.run(host='0.0.0.0', port=8080)
 
