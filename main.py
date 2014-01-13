import urllib2

from bottle import route, run, template

import calendar

cal_url = "http://td.eng.cam.ac.uk/tod/public/view_ical.php?yearval=2013_14&term=L&course=IA"

@route('/')
def index(name):
	response.content_type = 'text/calendar'
	response = urllib2.urlopen(cal_url)
	cal = response.read()

	return calendar.fix(cal)

run(host='efw.user.srcf.net', port=8080)
