from flask import Flask, render_template, request
from config import dbname, dbhost, dbport, lost_priv, lost_pub, user_pub, prod_pub
import json
import psycopg2
import datetime

app = Flask(__name__)

@app.route('/')

if __name__=='__main__':
    app.run(host='0.0.0.0', port=8080)
