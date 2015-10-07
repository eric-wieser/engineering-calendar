from bottle import route, template, response, redirect, template, HTTPError, request, view
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
			except HTTPError as e:
				rv = e

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
@view('index')
def index():
	import itertools
	key = lambda c: c.year

	parts = sorted(CourseYear.iter(), key=key, reverse=True)
	parts_by_year = itertools.groupby(parts, key)

	return dict(parts=parts_by_year)

@route(r'/<year:int>/<part:re:ia|ib>/<term:re:mich|lent|easter>')
@view('table')
def ia_term_table(year, part, term):
	timetable = CourseYear.get(part, year).term(term)
	return dict(part=part, term=term, tt=timetable)

@route(r'/<year:int>/<part:re:ia|ib>/<term:re:mich|lent|easter>/examples.ics')
def ia_term_calendar(year, part, term):
	course_year = CourseYear.get(part, year)
	return calendarmaker.construct(timetable, term, examples=True)


@route(r'/<year:int>/<part:re:ia|ib>/<term:re:mich|lent|easter>/<group:re:\d+-\d+>.ics')
def ia_term_calendar(year, part, term, group):
	course_year = CourseYear.get(part, year)
	return calendarmaker.construct(course_year, part, term, group)

app = bottle.default_app()
root = bottle.Bottle()
root.mount('/cued-labs', app)

if __name__ == '__main__':
	bottle.run(root, host='localhost', port=8090, debug=True)
