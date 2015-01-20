from bottle import route, template, response, redirect, template, HTTPError, request
import bottle
import icalendar

import calendar
from objects import CourseYear

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

@route(r'/<part:re:ia|ib>/<term:re:mich|lent|easter>')
def ia_term_list(part, term):
	timetable = CourseYear('{}.xls'.format(part)).term(term)
	return template('list', term=term, groups=timetable.groups)


@route(r'/<part:re:ia|ib>/<term:re:mich|lent|easter>/<group:re:\d+-\d+>.ics')
def ia_term_calendar(part, term, group):
	return calendar.construct(part, term, group)

if __name__ == '__main__':
	bottle.run(host='localhost', port=8090)
