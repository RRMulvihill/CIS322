from flask import Flask, render_template, request
from config import dbname, dbhost, dbport

app = Flask(__name__)

@app.route('/')
def login():
    return render_template('login.html',dbname=dbname,dbhost=dbhost,dbport=dbport)

@app.route('/report')
def report():
    return render_template('report.html')

@app.route('/facility')
def facility():
     if request.method=='GET' and 'fcName' in request.args:
        return render_template('facility.html',data=request.args.get('fcName'))
    return render_template('facility.html',data=request.args.get('fcName'))

@app.route('/transit')
def transit():
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
 
