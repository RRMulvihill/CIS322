L.O.S.T. REPOSITORY


What is LOST?
LOST is an inventory management web application developed as a final project for CIS 322 at the University of Oregon. 
Disclaimer: This program is intended for academic purposes and not intended for deployment.

INSTALLATION
LOST requires an Archlinux virtual box with Postgres and Apache installed

RUNNING THE APPLICATION
A database cluster must be set up using the following commands:

$ initdb -D $1
$ pg_ctl -D $1 -l logfile start
where $1 is the specified directory on your system to store the database.

Next, create the database by running:
$ createdb -p $1 $2
where $1 is the port number and $2 is the name of the database.

Finally, change into the OSNAP directory and run the preflight script by running:

$ ./preflight.sh $1
where $1 is the name of the database you created.

Open a web browser and go to http://127.0.0.1:8080 to use access LOST.

DIRECTORIES
Preflight: Creates database tables and moves files to WSGI
/clients: contains web service python files
/SQl: contains script to create tables
/src: contains files to create web service
/testdoc: contains testing procedure for web app
