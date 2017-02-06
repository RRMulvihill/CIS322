from flask import Flask, render_template, request
from config import dbname, dbhost, dbport

app = Flask(__name__)

@app.route('/')
def login():
    return render_template('login.html',dbname=dbname,dbhost=dbhost,dbport=dbport)

@app.route('/data')
def data():
    return render_template('data.html')



@app.route('/logout')
def logout():
    if request.method=='GET' and 'mytext' in request.args:
        return render_template('logout.html',data=request.args.get('mytext'))

    # request.form is only populated for POST messages
    if request.method=='POST' and 'mytext' in request.form:
        return render_template('logout.html',data=request.form['mytext'])
    return render_template('login.html')
if __name__=='__main__':
    app.run(host='0.0.0.0', port=8080)
