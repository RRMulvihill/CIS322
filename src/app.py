from flask import Flask, render_template, request, request, url_for, session
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
		session['username'] = username
		sql = "SELECT user_pk FROM users WHERE username = %s;"
		session['user_pk'] = query(sql,(username,))[0][0]
		password = request.form['pass']
		sql = ("SELECT username,password FROM users WHERE username = %s and password = %s;")
		res = query(sql,(username,password))
		if (res):
			sql = ("SELECT role FROM roles JOIN users ON roles.role_pk = users.role_fk WHERE users.username = %s;")
			session['role'] = query(sql,(username,))[0][0]
			return render_template('dashboard.html')
		else:
			session['msg'] = 'Error! User does not exist'
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
		sql = ("SELECT username FROM users WHERE username = %s;")
		user = query(sql,(username,))
		if (user):
			return render_template('entry_exists.html')
		else:
			#get role_fk
			sql = "SELECT role_pk FROM roles WHERE role = %s;"
			role_fk = query(sql,(role,))
			sql = "INSERT INTO users(username,password,role_fk) VALUES (%s, %s, %s);"
			query(sql,(username,password,role_fk[0][0]))
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
		sql = "SELECT fac_name FROM facilities WHERE fac_name =%s or fac_code = %s;"
		entry_exists = query(sql,(fname,fcode))
		if (entry_exists):
			session['msg'] = 'facility already exists'
			return render_template('dashboard.html')
		else:
			sql = "INSERT INTO facilities(fac_name,fac_code) VALUES (%s, %s);"
			query(sql,(fname,fcode))
			session['msg'] = 'Facility Created!'
			return render_template('dashboard.html')  
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
		sql = "SELECT asset_tag FROM assets WHERE asset_tag = %s;"
		tag = query(sql,(asset_tag))
		if (tag):
			session['msg'] = 'asset already exists with the given tag'
			return render_template('dashboard.html')
		else:
			sql = "SELECT fac_pk FROM facilities where fac_code = %s;"
			fac_fk = (query(sql,(fac_code,)))
			sql = "INSERT INTO assets(asset_tag,description,fac_fk,disposed) VALUES (%s, %s,%s,%s);"
			query(sql,(asset_tag,description,fac_fk[0][0],'FALSE'))
			session['msg'] = 'asset created!'
			return render_template('dashboard.html')  
@app.route('/dispose_asset', methods=['GET', 'POST'])
def dispose_asset():
	sql = "SELECT * FROM assets WHERE disposed = 'FALSE';"
	res = query(sql,())
	assets = []
	for asset in res[0]:
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
		sql = "SELECT asset_tag FROM assets WHERE asset_tag = %s;"
		tag_exists = query(sql,(asset_tag,))
		if not (tag_exists):
			session['msg'] = 'Asset not found!'
			return render_template('dashboard.html') 
		else:
			sql = "UPDATE assets SET disposed = 'TRUE' WHERE asset_tag = %s;"
			query(sql,(tag,))
			session['msg'] = 'Asset removed'
			return render_template('dashboard.html')
@app.route('/dashboard', methods=['GET',])
def dashboard():
	to_approve = None
	to_load = None
	
	if session['role'] == 'Logistics Officer':
		sql = "SELECT r.req_pk,a.asset_tag,s.fac_pk,d.fac_pk,r.submit_dt FROM requests AS r INNER JOIN assets AS a ON r.asset_fk = a.asset_pk INNER JOIN facilities AS s ON s.fac_pk = r.source_fk INNER JOIN facilities AS d ON d.fac_pk = r.destination_fk;"
		lres = query(sql,())
		ltasks = list()
		session['msg'] = fres[0]
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
		sql = "SELECT r.req_pk,a.asset_tag,s.fac_pk,d.fac_pk,r.submit_dt FROM requests AS r INNER JOIN assets AS a ON r.asset_fk = a.asset_pk INNER JOIN facilities AS s ON s.fac_pk = r.source_fk INNER JOIN facilities AS d ON d.fac_pk = r.destination_fk;"
		fres = query(sql,())
		session['msg'] = fres[0]
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
		return render_template('dashboard.html')
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
			return render_template('dashboard.html')
		sql = "SELECT fac_pk FROM facilities WHERE fac_code = %s;"
		src = query(sql,(source,))
		if not (src):
			session['msg'] = 'ERROR: Source Facility not found'
			return render_template('dashboard.html')
		sql = "SELECT fac_pk FROM facilities WHERE fac_code = %s;"
		dst = query(sql,(destination,))
		if not (dst):
			session['msg'] = 'ERROR: Destination Facility not found'
			return render_template('dashboard.html')
		sql = "SELECT asset_tag FROM assets WHERE asset_tag = %s;"

		sql = "INSERT INTO requests(submitter_fk,submit_dt,source_fk,destination_fk,asset_fk,approved) VALUES (%s,%s,%s,%s,%s,%s);"
		query(sql,(user_pk,timestamp,src[0][0],dst[0][0],asset_fk[0][0],'FALSE'))
		session['msg'] = 'request created'
		return render_template('dashboard.html')
@app.route('/approve_req', methods=['GET','POST'])
def approve_req():
	req_pk = int(request.args['id'])
	if session['role'] != 'Facilities Officer':
		session['msg'] = 'Only Facilities Officers can approve Transfer Requests.'
		return render_template('dashboard.html')
	if request.method == 'GET':
		sql = "SELECT r.req_pk,a.asset_tag,s.fac_name,d.fac_name,r.submit_dt,r.approved FROM requests AS r INNER JOIN assets AS a ON r.asset_fk = a.asset_pk INNER JOIN facilities AS s ON s.fac_pk = r.source_fk INNER JOIN facilities AS d ON d.fac_pk = r.destination_fk WHERE r.req_pk = %s;"
		req_data = query(sql,(req_pk,))
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
			return render_template('dashboard.html')
		return render_template('approve_req.html',data=data,)
	if request.method == "POST":
		submitted = request.form['submit']
		if submitted =='cancel':
			pass
		if submitted=='reject':
			sql = "DELETE FROM requests WHERE req_pk = %s;"
			query(sql,(req_pk,))
			session['msg'] = 'Request Removed'
		if submitted =='approve':
			sql = "UPDATE requests SET approved ='TRUE' WHERE req_pk = %s:"
			query(sql,(req_pk,))
			sql = "INSERT INTO transit(req_fk,asset_tag,source_fk,destination_fk,load_dt,unload_dt) VALUES (%s,%s,%s,%s,'NULL','NULL');"
			query(sql,(request_data[0][0],request_data[0][1],request_data[0][2],request_data[0][3]))
			session['msg'] = 'request approved'
		return redirect('dashboard.html')
		
@app.route('/update_transit', methods=['GET','POST'])
def update_transit():
	if session['role'] != 'Logistics Officer':
		session['error_msg'] = 'Only Logistics Officers May make Updates Transits.'
		return render_template('error.html')
	if request.method=='GET':
		req_fk=request.form['req_pk']
		sql = "SELECT load_dt,unload_dt FROM transit WHERE req_fk = %s;"
		transit = query(sql,(req_fk,))
		if not (transit):
			session['msg'] = 'ERROR: transit entry not found'
			return render_template('dashboard.html')
		if transit[1] != null:
			session['msg'] = 'transit has already been unloaded'
			return render_template('dashboard.html')
		columns=[('Transit ID'), ('Asset Tag'), ('Source Facilitiy'), ('Destination Facility'), ('Request Date')]
		sql = "SELECT requests.req_pk, assests.asset_tag, requests.source_fk, requests.destination.fk, requests.submit_dt FROM requests inner join assets on requests.asset_fk = assets.asset_pk inner join facilities on facilities.fac_pk=request.fac_fk WHERE requests.approved = 'False' AND requests.req_tag=%s;"
		transit_data = query(sql,(req_fk,))
		return render_template('update_transit.html', columns = columns, transit_data = transit_data)
	if request.method=='POST':
		req_fk=request.form['req_fk']
		load = request.form['load']
		unload = request.form['unload']
		sql = "UPDATE transits SET load_dt = '%s', unload_dt='%s' where req_fk = %s;"
		query(sql,(req_fk,load,unload))
		session['msg'] = 'Transit Request Updated!'
		return render_template('dashboard.html')
@app.route('/asset_report', methods=['GET','POST'])
def asset_report():
	sql = "SELECT fac_name FROM facilities;"
	facilities = query(sql,())
	if request.method =='GET':
		blank=[]
		return render_template('asset_report.html', facilities=facilities,report =blank)
	if request.method == 'POST':
		facility=request.form['facility']
		if (facility=='0'):
			sql = "SELECT a.asset_tag, a.description, f.fac_name FROM assets AS a INNER JOIN facilities AS f ON a.fac_fk = f.fac_pk;"
			report = query(sql,())
			return render_template('asset_report.html', facilities=facilities,report = report)
		else:
			sql = "SELECT a.asset_tag, a.description, f.fac_name FROM assets AS a INNER JOIN facilities AS f ON a.fac_fk = f.fac_pk WHERE f.fac_code = %s;"
			report = query(sql,(facility[0][0]))
			return render_template('asset_report.html', facilities=facilities, report = report)
@app.route('/transfer_report', methods=['GET','POST'])
def transfer_report():
	return render_template('transfer_report.html')
if __name__=='__main__':
	app.run(host='0.0.0.0', port=8080)
