import urllib2

from bottle import route, run, template, response, redirect, template, HTTPError, request

import calendar

import terms.IA.lent
import terms.IA.easter

cal_url = {
	'lent': "http://td.eng.cam.ac.uk/tod/public/view_ical.php?yearval=2013_14&term=L&course=IA",
	'easter': "http://td.eng.cam.ac.uk/tod/public/view_ical.php?yearval=2013_14&term=E&course=IA"
}


@route('/')
def index():
	redirect('https://github.com/eric-wieser/engineering-calendar/blob/master/README.md')

@route('/IA/lent')
def ia_lent_list():
	from terms.IA.lent import timetable

	print timetable

	return template('list', groups=timetable.groups)


@route(r'/IA/<term:re:lent|easter>/<group:re:\d+-\d+>.ics')
@route(r'/IA/<term:re:lent|easter>/<group:re:\d+-\d+>')
@route(r'/IA/<term:re:lent|easter>/<group:re:\d+-\d+>.txt')
def ia_lent_calendar(term, group):
	cal_req = urllib2.urlopen(cal_url[term])
	cal = cal_req.read()

	try:
		cal = calendar.fix(cal, getattr(terms.IA, term), group)
	except KeyError:
		raise HTTPError(404)

	if request.url.endswith('.txt'):
		response.content_type = 'text/plain'
	else:
		response.headers['Content-Disposition'] = 'attachment; filename="calendar.ics"'
		response.content_type = 'text/calendar'
	return cal

run(host='efw27.user.srcf.net', port=8080)
