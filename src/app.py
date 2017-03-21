from flask import Flask, render_template, redirect, request, url_for, session
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
		cur.execute(sql)
	else:
		cur.execute(sql,params)
	try:
		result = cur.fetchall()
	except psycopg2.ProgrammingError:
		result = ''
	conn.commit()
	cur.close()
	conn.close()
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
		password = request.form['pass']
		session['username'] = username
		#sql = "SELECT user_pk FROM users WHERE username = %s;"
		#session['user_pk'] = query(sql,(username,))[0][0]

		sql = ("SELECT user_pk, active FROM users WHERE username = %s and password = %s;")
		res = query(sql,(username,password))
		if (res):
			print(res[0][1])
			if res[0][1] == False:
				print('user is revoked')
				session['msg'] = 'Error! User not active'
				return redirect('login')
			session['user_pk'] = res[0][0]
			sql = ("SELECT role FROM roles JOIN users ON roles.role_pk = users.role_fk WHERE users.username = %s;")
			session['role'] = query(sql,(username,))[0][0]
			return redirect('dashboard')
		else:
			session['msg'] = 'Error! User does not exist'
			return redirect('login')
@app.route('/activate_user', methods=('POST',))
def activate_user():
	if request.method=='POST':
		username= request.form['username']
		password= request.form['password']
		role = request.form['role']
		
		sql = ("SELECT username FROM users WHERE username = %s;")
		user = query(sql,(username,))
		if (user):
			sql= "Update users SET password = %s, role_fk = %s, active = TRUE WHERE username = %s;"
			query(sql,(password,role, username))
			return 'User has been activated! The Username already exists, if the password and role were changed when unput, they have been updated to match.'
			
		else:

			sql = "INSERT INTO users(username,password,role_fk,active) VALUES (%s, %s, %s, TRUE);"
			query(sql,(username,password,role))
			return 'User Created!'

@app.route('/revoke_user', methods=('POST',))
def revoke_user():
	if request.method=='POST':
		username = request.form['username']
		sql = ("SELECT username FROM users WHERE username = %s;")
		user = query(sql,(username,))
		if (user):
			sql = 'UPDATE users SET active = FALSE WHERE username = %s'
			query(sql,(username,))
			return 'User revoked!'
		else:
			return 'User not found!'
		
	
@app.route('/add_facility', methods=['GET', 'POST'])
def add_facility():
	if request.method =='GET':
		return render_template('add_facility.html')
	if request.method == 'POST':
		session['entry_type'] = "Facility"
		fname = request.form['fname']
		fcode = request.form['fcode']
		sql = "SELECT fac_name FROM facilities WHERE fac_name =%s or fac_code = %s;"
		entry_exists = query(sql,(fname,fcode))
		if (entry_exists):
			session['msg'] = 'facility already exists'
			return redirect('dashboard')
		else:
			sql = "INSERT INTO facilities(fac_name,fac_code) VALUES (%s, %s);"
			query(sql,(fname,fcode))
			session['msg'] = 'Facility Created!'
			return redirect('dashboard')  
@app.route('/add_asset', methods=['GET', 'POST'])
def add_asset():
	if request.method =='GET':
		sql = "SELECT fac_code FROM facilities;"
		facilities = query(sql,())
		return render_template('add_asset.html', facilities = facilities)
	if request.method == 'POST':
		asset_tag = request.form['tag']
		description = request.form['desc']
		date = request.form['date']
		fac_code = request.form['facility']
		print("SELECT asset_tag FROM assets WHERE asset_tag = %s;"%asset_tag)
		tag = query(sql,(asset_tag,))
		if (tag):
			session['msg'] = 'asset already exists with the given tag'
			return redirect('dashboard')
		else:
			sql = "SELECT fac_pk FROM facilities where fac_code = %s;"
			fac_fk = query(sql,(fac_code,))
			sql = "INSERT INTO assets (asset_tag,date,description,fac_fk,disposed) VALUES (%s,%s,%s,%s,False);"
			query(sql,(asset_tag,date, description,fac_fk[0][0]))
			session['msg'] = 'asset created!'
			return redirect('dashboard')  
@app.route('/dispose_asset', methods=['GET', 'POST'])
def dispose_asset():
	if session['role'] != "Logistics Officer":
		session['msg'] = 'Error! Access Denied for non Logistics Officers'
		return ridirect('dashboard')
	if request.method =='GET':
		return render_template('dispose_asset.html')
	if request.method == 'POST':
		asset_tag = request.form['tag']
		sql = "SELECT asset_tag, disposed FROM assets WHERE asset_tag = %s;"
		tag = query(sql,(asset_tag,))
		print(tag)
		if not (tag):
			session['msg'] = 'Asset not found!'
			return redirect('dashboard') 
		else:
			if tag[0][1] == 'True':
				session['msg'] = 'Error! Asset already disposed'
				return ridirect('dashboard')
			sql = "UPDATE assets SET disposed = 'TRUE' WHERE asset_tag = %s;"
			query(sql,(tag[0][0],))
			session['msg'] = 'Asset removed'
			return redirect('dashboard')
@app.route('/dashboard', methods=['GET',])
def dashboard():
	to_approve = None
	to_load = None
	
	if session['role'] == 'Logistics Officer':
		sql = "SELECT t.req_fk,a.asset_tag,s.fac_pk,d.fac_pk,r.approved_dt FROM transits AS t INNER JOIN requests AS r ON t.req_fk = r.req_pk INNER JOIN assets AS a ON r.asset_fk = a.asset_pk INNER JOIN facilities AS s ON s.fac_pk = r.source_fk INNER JOIN facilities AS d ON d.fac_pk = r.destination_fk WHERE t.unload_dt is NULL;"
		lres = query(sql,())
		ltasks = list()
		for r in lres:
			e = dict()
			e['id']=r[0]
			e['tag']=r[1]
			e['src']=r[2]
			e['dst']=r[3]
			e['date']=r[4]
			ltasks.append(e)
		to_load = ltasks
	if session['role'] == 'Facilities Officer':
		sql = "SELECT r.req_pk,a.asset_tag,s.fac_pk,d.fac_pk,r.submit_dt FROM requests AS r INNER JOIN assets AS a ON r.asset_fk = a.asset_pk INNER JOIN facilities AS s ON s.fac_pk = r.source_fk INNER JOIN facilities AS d ON d.fac_pk = r.destination_fk WHERE r.approved = 'f';"
		fres = query(sql,())
		ftasks = list()
		for r in fres:
			e = dict()
			e['id']=r[0]
			e['tag']=r[1]
			e['src']=r[2]
			e['dst']=r[3]
			e['date']=r[4]
			ftasks.append(e)
		to_approve = ftasks
	return render_template('dashboard.html', to_approve=to_approve, to_load=to_load)

@app.route('/transfer_req', methods=['GET','POST'])
def transfer_req():
	if session['role'] != 'Logistics Officer':
		session['msg'] = 'ERROR: Only Logistics Officers May make Transfer Requests, nice try Larry.'
		return redirect('dashboard')
	if request.method == 'GET':
		return render_template('transfer_req.html')
	if request.method == 'POST':
		source = request.form['source']
		destination = request.form['destination']
		tag = request.form['tag']
		user_pk = session['user_pk']
		timestamp = datetime.now() 
		sql = "SELECT asset_pk FROM assets WHERE asset_tag = %s;"
		asset_fk = query(sql,(tag,))
		if not (asset_fk):
			session['msg'] = 'ERROR: asset tag not found'
			return redirect('dashboard')
		sql = "SELECT fac_pk FROM facilities WHERE fac_code = %s;"
		src = query(sql,(source,))
		if not (src):
			session['msg'] = 'ERROR: Source Facility not found'
			return redirect('dashboard')
		sql = "SELECT fac_pk FROM facilities WHERE fac_code = %s;"
		dst = query(sql,(destination,))
		if not (dst):
			session['msg'] = 'ERROR: Destination Facility not found'
			return redirect('dashboard')
		sql = "SELECT asset_tag FROM assets WHERE asset_tag = %s;"

		sql = "INSERT INTO requests(submitter_fk,submit_dt,source_fk,destination_fk,asset_fk,approved) VALUES (%s,%s,%s,%s,%s,%s);"
		query(sql,(user_pk,timestamp,src[0][0],dst[0][0],asset_fk[0][0],'FALSE'))
		session['msg'] = 'request created'
		return redirect('dashboard')
@app.route('/approve_req', methods=['GET','POST'])
def approve_req():
	print('starting approval_request')
	
	if session['role'] != 'Facilities Officer':
		session['msg'] = 'Only Facilities Officers can approve Transfer Requests.'
		return redirect('dashboard')
	if request.method == 'GET':
		session['req_pk'] = int(request.args['id'])
		print('through to get')
		sql = "SELECT r.req_pk,a.asset_tag,s.fac_name,d.fac_name,r.submit_dt,r.approved FROM requests AS r INNER JOIN assets AS a ON r.asset_fk = a.asset_pk INNER JOIN facilities AS s ON s.fac_pk = r.source_fk INNER JOIN facilities AS d ON d.fac_pk = r.destination_fk WHERE r.req_pk = %s;"
		req_data = query(sql,(session['req_pk'],))
		res=dict()
		res['id']=req_data[0][0]
		res['tag']=req_data[0][1]
		res['src']=req_data[0][2]
		res['dst']=req_data[0][3]
		res['date']=req_data[0][4]
		res['approved']=req_data[0][5]
		data = res
		if res['approved'] == 'TRUE':
			session['msg']='ERROR:request already approved'
			return redirect('dashboard')
		print('finished get')
		return render_template('approve_req.html',data=data)
	if request.method == 'POST':
		print('through to post')
		print(request.form['submit'])
		submitted= request.form['submit']
		print('submitted: ' + submitted)
		if not 'submit' in request.form:
			session['msg'] = 'ERROR: Fail on submit'
		if submitted =='approve':
			print('approved')
			sql = "UPDATE requests SET approved ='TRUE' WHERE req_pk = %s;"
			query(sql,(session['req_pk'],))
			sql = "INSERT INTO transits(req_fk) VALUES (%s);"
			query(sql,(session['req_pk'],))
			session['msg'] = 'request approved'
		else:
			print('rejected')
			sql = "DELETE FROM requests WHERE req_pk = %s;"
			query(sql,(session['req_pk'],))
			session['msg'] = 'Request Removed'
		print('at end of post')
		return redirect('dashboard')
		
@app.route('/update_transit', methods=['GET','POST'])
def update_transit():
	if session['role'] != 'Logistics Officer':
		session['msg'] = 'Only Logistics Officers May make Updates Transits.'
		return redirect('dashboard')
	if request.method=='GET':
		session['req_fk'] = int(request.args['id'])
		sql = "SELECT r.req_pk,a.asset_tag,s.fac_name,d.fac_name,r.submit_dt FROM requests AS r INNER JOIN assets AS a ON r.asset_fk = a.asset_pk INNER JOIN facilities AS s ON s.fac_pk = r.source_fk INNER JOIN facilities AS d ON d.fac_pk = r.destination_fk WHERE r.req_pk = %s;"
		req_data = query(sql,(session['req_fk'],))
		res=dict()
		res['id']=req_data[0][0]
		res['tag']=req_data[0][1]
		res['src']=req_data[0][2]
		res['dst']=req_data[0][3]
		res['date']=req_data[0][4]
		data = res 
		return render_template('update_transit.html',data=data)
	if request.method=='POST':
		load = request.form['load']
		unload = request.form['unload']
		sql = "UPDATE transits SET load_dt = %s, unload_dt=%s where req_fk = %s;"
		query(sql,(load,unload,session['req_fk']))
		session['msg'] = 'Transit Request Updated!'
		return redirect('dashboard')
@app.route('/asset_report', methods=['GET','POST'])
def asset_report():
	sql = "SELECT fac_code FROM facilities;"
	facilities = query(sql,())
	if request.method =='GET':
		blank=[]
		return render_template('asset_report.html', facilities=facilities,report =blank)
	if request.method == 'POST':
		facility=request.form['facility']
		date = request.form['date']
		if date == '':
			sql = "SELECT a.asset_tag, a.date, a.description, f.fac_name FROM assets AS a INNER JOIN facilities AS f ON a.fac_fk = f.fac_pk;"
			report = query(sql,())
			return render_template('asset_report.html', facilities=facilities,report = report)
		if (facility=='All'):
			sql = "SELECT a.asset_tag, a.date, a.description, f.fac_name FROM assets AS a INNER JOIN facilities AS f ON a.fac_fk = f.fac_pk WHERE a.date = %s;"
			report = query(sql,(date,))
			return render_template('asset_report.html', facilities=facilities,report = report)
		else:
			sql = "SELECT a.asset_tag, a.description, f.fac_name FROM assets AS a INNER JOIN facilities AS f ON a.fac_fk = f.fac_pk WHERE f.fac_code = %s AND a.date = %s;"
			report = query(sql,(facility,date))
			return render_template('asset_report.html', facilities=facilities, report = report)
@app.route('/transfer_report', methods=['GET','POST'])
def transfer_report():
	return render_template('transfer_report.html')
if __name__=='__main__':
	app.run(host='0.0.0.0', port=8080)
