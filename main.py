import urllib2

from bottle import route, run, template, response

import calendar

cal_url = "http://td.eng.cam.ac.uk/tod/public/view_ical.php?yearval=2013_14&term=L&course=IA"

@route('/')
def index():
	response.content_type = 'text/calendar'
	cal_req = urllib2.urlopen(cal_url)
	cal = cal_req.read()

	return calendar.fix(cal)

run(host='efw27.user.srcf.net', port=8080)
