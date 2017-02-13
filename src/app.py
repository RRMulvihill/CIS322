from flask import Flask, render_template, request
from config import dbname, dbhost, dbport, lost_priv, lost_pub, user_pub, prod_pub
import json
import psycopg2

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('rest.html')

@app.route('/rest')
def rest():
    return render_template('rest.html',dbname=dbname,dbhost=dbhost,dbport=dbport)

@app.route('/rest/lost_key', methods=('POST',))
def lost_key():
    # Try to handle as plaintext
    dat = dict()
    dat['timestamp'] = datetime.datetime.utcnow().isoformat()
    dat['result'] = 'OK'
    dat[key] = 'random_key'
    data = json.dumps(dat)
    return data

@app.route('/rest/activate_user', methods=('POST',))
#not finished
def activate_user():
    # Try to handle as plaintext
    if request.method=='POST' and 'arguments' in request.form:
        req=json.loads(request.form['arguments'])

    dat = dict()
    dat['timestamp'] = req['timestamp']
    dat['result'] = 'OK'
    data = json.dumps(dat)
    return data

@app.route('/rest/suspend_user', methods=('POST',))
def suspend_user():
    # Try to handle as plaintext
    if request.method=='POST' and 'arguments' in request.form:
        req=json.loads(request.form['arguments'])

    dat = dict()
    dat['timestamp'] = req['timestamp']
    dat['result'] = 'OK'
    data = json.dumps(dat)
    return data


@app.route('/rest/list_products', methods=('POST',))
def list_products():
        # Try to handle as plaintext
    if request.method=='POST' and 'arguments' in request.form:
        req=json.loads(request.form['arguments'])

    dat = dict()
    dat['timestamp'] = req['timestamp']
    dat['result'] = 'OK'
    data = json.dumps(dat)
    return data
    
@app.route('/rest/add_products', methods=('POST',))
def add_products():
        # Try to handle as plaintext
    if request.method=='POST' and 'arguments' in request.form:
        req=json.loads(request.form['arguments'])

    dat = dict()
    dat['timestamp'] = req['timestamp']
    dat['result'] = 'OK'
    data = json.dumps(dat)
    return data


@app.route('/rest/add_asset', methods=('POST',))
def add_asset():
        # Try to handle as plaintext
    if request.method=='POST' and 'arguments' in request.form:
        req=json.loads(request.form['arguments'])

    dat = dict()
    dat['timestamp'] = req['timestamp']
    dat['result'] = 'OK'
    data = json.dumps(dat)
    return data
    
@app.route('/goodbye')
def goodbye():
    if request.method=='GET' and 'mytext' in request.args:
        return render_template('rest.html',data=request.args.get('mytext'))

    # request.form is only populated for POST messages
    if request.method=='POST' and 'mytext' in request.form:
        return render_template('rest.html',data=request.form['mytext'])
    return render_template('rest.html')
if __name__=='__main__':
    app.run(host='0.0.0.0', port=8080)
