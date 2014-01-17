import urllib2

from bottle import route, run, template, response, redirect, template, HTTPError

import calendar

cal_url = "http://td.eng.cam.ac.uk/tod/public/view_ical.php?yearval=2013_14&term=L&course=IA"

@route('/')
def index():
	redirect('https://github.com/eric-wieser/engineering-calendar/blob/master/README.md')

@route('/IA/lent')
def ia_lent_list():
	from terms.IA.lent import timetable

	groups = sorted(timetable.keys(), key=lambda g: map(int, g.split('-')))

	return template('list', groups=groups)


@route('/IA/lent/<group>')
def ia_lent_calendar(group):
	response.content_type = 'text/calendar'
	cal_req = urllib2.urlopen(cal_url)
	cal = cal_req.read()
	try:
		return calendar.fix(cal, group)
	except KeyError:
		raise HTTPError(404)
		

run(host='efw27.user.srcf.net', port=8080)
