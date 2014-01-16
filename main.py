import urllib2

from bottle import route, run, template, response, redirect, template

import calendar

cal_url = "http://td.eng.cam.ac.uk/tod/public/view_ical.php?yearval=2013_14&term=L&course=IA"

@route('/')
def index():
	redirect('https://github.com/eric-wieser/engineering-calendar/blob/master/README.md')

@route('/IA/lent')
def ia_lent_list():
	from terms.IA.lent import timetable

	return template('list', groups=timetable.keys())


@route('/IA/lent/<group>')
def ia_lent_calendar(group):
	response.content_type = 'text/calendar'
	cal_req = urllib2.urlopen(cal_url)
	cal = cal_req.read()

	return calendar.fix(cal, group)

run(host='efw27.user.srcf.net', port=8080)
