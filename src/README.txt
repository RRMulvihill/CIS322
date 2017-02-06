app.py : Flask app run by mod_wsgi
config.py - logic for arguements
lost.wsgi - imports sys and makes app an application
lost_config.json - complimentary to config for variables
templates/
  facility.html - creates a table of invintory by facility /todo allow for sort by facility
  login.html - welcome page, sakes a username
  logout.html - logout page /todo show username
  report.html - gives user chance to enter varaible for report pages
  transit.html - creates a table of all in inventory in transit by its arrival and expunge dates
