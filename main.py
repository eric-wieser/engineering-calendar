from bottle import route, template, response, redirect, template, HTTPError, request
import bottle
import icalendar

import calendar
import lectures

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
			elif isinstance(rv, bottle.HTTPResponse) and isinstance(rv.body, icalendar.Calendar):
				rv.body = rv.body.to_ical()
				if text_override:
					rv.content_type = 'text/plain'
				else:
					rv.content_type = 'text/calendar'
					rv.headers['Content-Disposition'] = 'attachment; filename="calendar.ics"'
			return rv

		return wrapper

bottle.install(ICalPlugin())

@route('/')
def index():
	redirect('https://github.com/eric-wieser/engineering-calendar/blob/master/README.md')

@route(r'/IA/<term:re:lent|easter>')
def ia_term_list(term):
	return template('list', term=term, groups=getattr(terms.IA, term).timetable.groups)


@route(r'/IA/<term:re:lent|easter>/<group:re:\d+-\d+>.ics')
@route(r'/IA/<term:re:lent|easter>/<group:re:\d+-\d+>')
@route(r'/IA/<term:re:lent|easter>/<group:re:\d+-\d+>.txt')
def ia_term_calendar(term, group):
	try:
		return calendar.construct('IA', term, group)
	except KeyError:
		raise HTTPError(404)

@route(r'/IA/<term:re:lent|easter>/<group:re:\d+-\d+>.original.txt')
def ia_term_raw_calendar(term, group):
	response.content_type = 'text/plain'
	return lectures.ical_for_term(term)

if __name__ == '__main__':
	bottle.run(host='localhost', port=8080)
