from flask import Flask, render_template, request, session
from config import dbname, dbhost, dbport
import json
import psycopg2

app = Flask(__name__)
app.secret_key = 'secret'

@app.route('/')
def index():
	return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method =='GET':
        return render_template('login.html')
    if request.method == 'POST':
        username = request.form['uname']
        password = request.form['pass']
        conn = psycopg2.connect(dbname=dbname,host=dbhost,port=dbport)
        cur  = conn.cursor()
        cur.execute("SELECT username,password FROM users WHERE username = '%s' and password = '%s';"%(username,password))
        if cur.fetchone() is not None:
            cur.excecute("SELECT role FROM roles JOIN users on roles(role_pk) = users(role_fk) WHERE users.username = '%s';"%(username))
            session['role'] = cur.fetchone()[0]
            return render_template('dashboard.html')
        else:
            return render_template('no_user.html')



@app.route('/create_user', methods=['GET', 'POST'])
def create_user():
    if request.method =='GET':
        return render_template('create_user.html')
    if request.method == 'POST':
        session['entry_type'] = "User"
        username = request.form['uname']
        password = request.form['pass']
        role = request.form['role']
        conn = psycopg2.connect(dbname=dbname,host=dbhost,port=dbport)
        cur  = conn.cursor()
        cur.execute("SELECT username FROM users WHERE username = '%s';"%(username))
        if cur.fetchone() is not None:
            return render_template('entry_exists.html')
        else:
            #get role_fk
            cur.execute("SELECT role_pk FROM roles WHERE role = '%s';"%(role))
            role_fk = cur.fetchone()
            cur.execute("INSERT INTO users(username,password,role_fk) VALUES ('%s', '%s', '%s');"%(username,password,role_fk))
            conn.commit()
            session['user'] = username
            return render_template('entry_created.html')
@app.route('/create_facility', methods=['GET', 'POST'])
def create_facility():
    if request.method =='GET':
        return render_template('create_facility.html')
    if request.method == 'POST':
        session['entry_type'] = "Facility"
        fname = request.form['fname']
        fcode = request.form['fcode']
        conn = psycopg2.connect(dbname=dbname,host=dbhost,port=dbport)
        cur  = conn.cursor()
        cur.execute("SELECT fac_name FROM facilities WHERE fac_name = '%s' or fac_code = '%s';"%(fname,fcode))
        if cur.fetchone() is not None:
            return render_template('entry_exists.html')
        else:
            cur.execute("INSERT INTO facilities(fac_name,fac_code) VALUES ('%s', '%s');"%(fname,fcode))
            conn.commit()
            return render_template('entry_created.html')  
@app.route('/add_asset', methods=['GET', 'POST'])
def add_asset():
    if request.method =='GET':
        return render_template('add_asset.html')
    if request.method == 'POST':
        session['entry_type'] = "Asset"
        asset_tag = request.form['tag']
        description = request.form['desc']
        date = request.form['date']
        facility = request.form['fac']
        conn = psycopg2.connect(dbname=dbname,host=dbhost,port=dbport)
        cur  = conn.cursor()
        cur.execute("SELECT asset_tag FROM assets WHERE asset_tag = '%s';"%(asset_tag))
        if cur.fetchone() is not None:
            return render_template('entry_exists.html')
        else:
            cur.excecute("SELECT fac_pk FROM facilities where fac_name = '%s'"%(facility))
            fac_fk = cur.fetchone()
            cur.excecute("SELECT status_pk FROM asset_at where status = 'at_facility';")
            fac_fk = cur.fetchone()[0]
            cur.execute("INSERT INTO assets(asset_tag,description,fac_fk,status_fk) VALUES ('%s', '%s'));"%(asset_tag,description,fac_fk,status_fk))
            conn.commit()
            return render_template('entry_created.html')  
@app.route('/dispose_asset', methods=['GET', 'POST'])
def dispose_asset():
        conn = psycopg2.connect(dbname=dbname, host=dbhost,port=dbport)
	cur = conn.cursor()
        cur.excecute("SELECT status_pk FROM asset_at where status = 'disposed';")
        status_fk = cur.fetchone()[0]
	    cur.execute("SELECT * FROM assets WHERE status_fk = '%s';"%(status_fk))
	    res = cur.fetchall()
	    assets = []
	    for asset in res:
		assets.append("{}: {}".format(asset[1], asset[2]))

		return render_template('dispose_asset.html', assets=assets)
    	if session['role'] != "Logistics Officer":
       		return render_template('access_denied.html')
    	if request.method =='GET':
        	return render_template('dispose_asset.html')
    	if request.method == 'POST':
            session['entry_type'] = "asset"
            asset_tag = request.form['tag']
            conn = psycopg2.connect(dbname=dbname,host=dbhost,port=dbport)
            cur  = conn.cursor()
            cur.execute("SELECT asset_tag FROM assets WHERE asset_tag = '%s';"%(asset_tag))
            if cur.fetchone() is None:
                return render_template('error.html')
            else:
            	cur.excecute("SELECT status_pk FROM asset_at where status = 'disposed';")
            	status_fk = cur.fetchone()[0]
                cur.execute("UPDATE assets SET status_fk = '%s' WHERE asset_tag = '%s';"%(status_fk,tag))
                conn.commit()
            	return render_template('dashboard.html')
@app.route('/dashboard', methods=['GET',])
def dashboard():
    return render_template('dashboard.html')

if __name__=='__main__':
    app.run(host='0.0.0.0', port=8080)
