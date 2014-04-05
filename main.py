from bottle import route, run, template, response, redirect, template, HTTPError, request, install

import calendar

import terms.IA.lent
import terms.IA.easter
import lectures

import icalendar


class ICalPlugin(object):
	name = 'ical'
	api  = 2

	def apply(self, callback, route):
		def wrapper(*a, **ka):
			try:
				rv = callback(*a, **ka)
			except HTTPError:
				rv = _e()

			text_override = request.url.endswith('.txt')

			if isinstance(rv, icalendar.Calendar):
				ical_response = rv.to_ical()
				if text_override:
					response.content_type = 'text/plain'
				else:
					response.content_type = 'text/calendar'
					response.headers['Content-Disposition'] = 'attachment; filename="calendar.ics"'
				return ical_response
			elif isinstance(rv, HTTPResponse) and isinstance(rv.body, icalendar.Calendar):
				rv.body = rv.body.to_ical()
				if text_override:
					rv.content_type = 'text/plain'
				else:
					rv.content_type = 'text/calendar'
					rv.headers['Content-Disposition'] = 'attachment; filename="calendar.ics"'
			return rv

		return wrapper

install(ICalPlugin())

cal_url = {
	'lent': "http://td.eng.cam.ac.uk/tod/public/view_ical.php?yearval=2013_14&term=L&course=IA",
	'easter': "http://td.eng.cam.ac.uk/tod/public/view_ical.php?yearval=2013_14&term=E&course=IA"
}


@route('/')
def index():
	redirect('https://github.com/eric-wieser/engineering-calendar/blob/master/README.md')

@route(r'/IA/<term:re:lent|easter>')
def ia_lent_list(term):
	return template('list', term=term, groups=getattr(terms.IA, term).timetable.groups)


@route(r'/IA/<term:re:lent|easter>/<group:re:\d+-\d+>.ics')
@route(r'/IA/<term:re:lent|easter>/<group:re:\d+-\d+>')
@route(r'/IA/<term:re:lent|easter>/<group:re:\d+-\d+>.txt')
def ia_lent_calendar(term, group):
	cal = lectures.ical_for_term(term)

	try:
		term = getattr(terms.IA, term)
	except KeyError:
		raise HTTPError(404)

	return calendar.fix(cal, term, group)

@route(r'/IA/<term:re:lent|easter>/<group:re:\d+-\d+>.original.txt')
def ia_lent_calendar(term, group):
	response.content_type = 'text/plain'
	return lectures.ical_for_term(term)

run(host='efw27.user.srcf.net', port=8080)
