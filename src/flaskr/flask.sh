pip install --editable .
export FLASK_APP=flaskr
export FLASK_DEBUG=true
flask run
sqlite3 /tmp/flaskr.db < schema.sql
flask initdb
Initialized the database.
py.test
python setup.py test
