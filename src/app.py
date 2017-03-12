from flask import Flask, render_template, request, session
from config import dbname, dbhost, dbport
import json
import psycopg2
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'secret'

def query(sql,params):
	conn = psycopg2.connect(dbname=dbname,host=dbhost,port=dbport)
	cur  = conn.cursor()
	if not (params):
		cur.excecute(sql)
	else:
		cur.execute(sql,params)
	try:
		result = cur.fetchall()
	except psycopg2.ProgrammingError:
		result = ''
	conn.commit()
	cur.close()
	con.close()
	return result
@app.route('/')
def index():
	return render_template('login.html')
@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method =='GET':
		return render_template('login.html')
	if request.method == 'POST':
		username = request.form['uname']
		session['username'] = username
		password = request.form['pass']
		sql = ("SELECT username,password FROM users WHERE username = '%s' and password = '%s';")
		res = query(sql,(username,password))
		if not (res):
			sql = ("SELECT role FROM roles JOIN users ON roles.role_pk = users.role_fk WHERE users.username = '%s';")
		        session['role'] = query(sql,username)
			return render_template('dashboard.html')
		else:
		       session['error_msg'] = 'Error! User already exists'
			return render_template('error.html')
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
			cur.execute("INSERT INTO users(username,password,role_fk) VALUES ('%s', '%s', '%s');"%(username,password,role_fk[0]))
			conn.commit()
			session['user'] = username
			return render_template('entry_created.html')
@app.route('/add_facility', methods=['GET', 'POST'])
def add_facility():
	if request.method =='GET':
		return render_template('add_facility.html')
	if request.method == 'POST':
		session['entry_type'] = "Facility"
		fname = request.form['fname']
		fcode = request.form['fcode']
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
		fac_code = request.form['fac']
		cur.execute("SELECT asset_tag FROM assets WHERE asset_tag = '%s';"%(asset_tag))
		if cur.fetchone() is not None:
			return render_template('entry_exists.html')
		else:
			cur.execute("SELECT fac_pk FROM facilities where fac_code = '%s'"%(fac_code))
			fac_fk = cur.fetchone()[0]
			cur.execute("INSERT INTO assets(asset_tag,description,fac_fk,disposed) VALUES ('%s', '%s','%s','%s');"%(asset_tag,description,fac_fk,'FALSE'))
			conn.commit()
			return render_template('entry_created.html')  
@app.route('/dispose_asset', methods=['GET', 'POST'])
def dispose_asset():
	cur.execute("SELECT * FROM assets WHERE disposed = 'FALSE';")
	res = cur.fetchall()
	assets = []
	for asset in res:
		assets.append("{}: {}".format(asset[1], asset[2]))
	#return render_template('dispose_asset.html', assets=assets)
	if session['role'] != "Logistics Officer":
		session['msg'] = 'Error! Access Denied for non Logistics Officers'
		return render_template('dashboard.html')
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
			cur.execute("UPDATE assets SET disposed = 'TRUE' WHERE asset_tag = '%s';"%(tag))
			conn.commit()
			return render_template('dashboard.html')
@app.route('/dashboard', methods=['GET',])
def dashboard():
	blank=iter([])
	if session['role'] == "Logistics Officer":
		columns=[('Transit ID'),('Asset Tag'),('Source Facility'),('Destination Facilility'),('Approval Date')]
		cur.execute("SELECT transits.req_fk, assets.asset_tag,facilities.fac_name,facilities.fac_name,requests.approved_dt FROM transits AS t INNER JOIN assets AS a ON a.asset_pk = t.asset_fk INNER JOIN facilities AS f ON (f.fac_pk = t.source_fk) or (f.fac_pk = t.destination_fk) INNER JOIN requests AS r ON r.req_pk = t.req_fk")
		ltasks = cur.fetchall()
		return render_template('dashboard.html',columns=columns,ltasks = ltasks,ftasks=blank)
	else:
		headers=[('Transit ID'), ('Asset Tag'), ('Source Facilitiy'), ('Destination Facility'), ('Request Date')]
		cur.execute("SELECT transits.req_fk, assets.asset_tag,facilities.fac_name,facilities.fac_name,requests.approved_dt FROM transits AS t INNER JOIN assets AS a ON a.asset_pk = t.asset_fk INNER JOIN facilities AS f ON (f.fac_pk = t.source_fk) or (f.fac_pk = t.destination_fk) INNER JOIN requests AS r ON r.req_pk = t.req_fk WHERE r.approved='FALSE'")
		ftasks = cur.fetchall()
		return render_template('dashboard.html',columns=columns,ltasks = blank,ftasks=ftasks)
@app.route('/transfer_req', methods=['GET','POST'])
def transfer_req():
	if session['role'] != 'Logistics Officer':
		session['error_msg'] = 'Only Logistics Officers May make Transfer Requests, nice try Larry.'
		return render_template('error.html')
	if request.method == 'GET':
		return render_template('transfer_req.html')
	if request.method == 'POST':
		source = request.form['source']
		destination = request.form['destination']
		tag = request.form['tag']
		user_pk = session['user_pk']
		conn = psycopg2.connect(dbname=dbname,host=dbhost,port=dbport)
		cur  = conn.cursor()
		timestamp = datetime.now()
		cur.execute("SELECT fac_code FROM facilities WHERE fac_code = '%s';"%(source))
		if cur.fetchone() is None:
			session['error_msg'] = 'Source Facility not found'
			return render_template('error.html')
		cur.execute("SELECT fac_code FROM facilities WHERE fac_code = '%s';"%(destination))	
		if cur.fetchone() is None:
			session['error_msg'] = 'Destination Facility not found'
			return render_template('error.html')
		cur.execute("SELECT asset_tag FROM assets WHERE asset_tag = '%s';"%(tag))
		if cur.fetchone() is None:
			session['error_msg'] = 'asset tag not found'
			return render_template('error.html')
		cur.execute("INSERT INTO requests(submitter_fk,submit_dt,fac_fk,approver__fk,approved_dt,approved) VALUES ('%s', '%s'));"%(user_pk,timestamp,destination,'NULL','NULL','FALSE'))
		conn.commit()
		session['entry'] = 'request'
		return render_template('entry_created.html') 
@app.route('/approve_req', methods=['GET','POST'])
def approve_req():
	if session['role'] != 'Facilities Officer':
		session['error_msg'] = 'Only Facilities Officers can approve Transfer Requests.'
		return render_template('error.html')
	if method.request == 'GET':
		req_pk = request.args['req_pk']
		columns=[('request tag'),('Asset tag'),('Source Facility'),('Destination Facility'),('Request Date')]
		cur.execute("SELECT requests.req_pk, assests.asset_tag, requests.source_fk, requests.destination.fk, requests.submit_dt FROM requests inner join assets on requests.asset_fk = assets.asset_pk inner join facilities on facilities.fac_pk=request.fac_fk WHERE requests.approved = 'False' AND requests.req_tag='%s'"(req_pk))
		request_data = cur.fetchall()
		return render_template('approve_req',columns=columns, req_pk=req_pk, request_data=request_data,)
	if method.request == "POST":
		decision = request.form['Decision']
		if (decision == 'Reject'):
			cur.execute("DELETE FROM requests WHERE req_pk = '%s'"%(req_pk))
			conn.commit()
			return render_template('dashboard.html')
		else:
			cur.execute("UPDATE requests SET approved ='TRUE' WHERE req_pk = '%s'"%(req_pk))
			cur.execute("INSERT INTO transit(req_fk,source_fk,destination_fk,load_dt,unload_dt) VALUES ('%s','%s','%s','NULL','NULL')"%(request_data[0],request_data[2],request_data[3]))
			cur.commit()
			return render_template('dashboard.html')
		
@app.route('/update_transit', methods=['GET','POST'])
def update_transit():
	if session['role'] != 'Logistics Officer':
		session['error_msg'] = 'Only Logistics Officers May make Updates Transits.'
		return render_template('error.html')
	if request.method=='GET':
		req_fk=request.form['req_pk']
		cur.execute("SELECT load_dt,unload_dt FROM transit WHERE req_fk = '%s'"%(req_fk))
		transit = cur.fetchone()
		if transit is None:
			session['error_msg'] = 'transit entry not found'
			return render_template('error.html')
		if transit[1] != null:
			session['error_msg'] = 'transit has already been unloaded'
			return render_template('error.html')
		columns=[('Transit ID'), ('Asset Tag'), ('Source Facilitiy'), ('Destination Facility'), ('Request Date')]
		cur.execute("SELECT requests.req_pk, assests.asset_tag, requests.source_fk, requests.destination.fk, requests.submit_dt FROM requests inner join assets on requests.asset_fk = assets.asset_pk inner join facilities on facilities.fac_pk=request.fac_fk WHERE requests.approved = 'False' AND requests.req_tag='%s'"(req_fk))
		transit_data = cur.fetchall()
		return render_template('update_transit.html', columns = columns, transit_data = transit_data)
	if request.method=='POST':
		req_fk=request.form['req_fk']
		load = request.form['load']
		unload = request.form['unload']
		cur.execute("UPDATE transits SET load_dt = '%s', unload_dt='%s' where req_fk = '%s'"%(req_fk,load,unload))
		cur.commit()
		session['msg'] = 'Transit Request Updated!'
		return render_template('dashboard.html')
@app.route('/asset_report', methods=['GET','POST'])
def asset_report():
	return render_template('asset_report.html')
@app.route('/transfer_report', methods=['GET','POST'])
def transfer_report():
	return render_template('transfer_report.html')
if __name__=='__main__':
	app.run(host='0.0.0.0', port=8080)
