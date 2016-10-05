import re
from collections import namedtuple
from datetime import datetime

import icalendar
import pytz
import requests

from calendarmaker import cued_address, make_blank_calendar

last_updated = pytz.utc.localize(datetime.utcnow())

def ical_for_term(year, term, courses):
	year_str = '{:4d}_{:02d}'.format(year, (year + 1)%100)
	cal_url = "http://td.eng.cam.ac.uk/tod/public/view_ical.php?yearval={year}&term={term}&course={course}".format(
		year=year_str,
		term=term[0].upper(),
		course=','.join(courses)
	)
	cal_req = requests.get(cal_url)
	cal_req.raise_for_status()
	return icalendar.Calendar.from_ical(cal_req.text)

pattern = re.compile(r'(.*?)/(.*)\[(\d+)\][CL] (.*)\((.*)\)')
MatchData = namedtuple('MatchData', 'module name week speaker location')

def fixed_events_in(cal):
	events = [
		event
		for event in cal.subcomponents
		if isinstance(event, icalendar.Event)
	]

	# add location information
	for event in events:
		d = MatchData(*pattern.match(event['summary']).groups())
		event['summary'] = icalendar.vText(d.module + ': ' + d.name)
		event['location'] = icalendar.vText(d.location + ', ' + cued_address)
		event['description'] = icalendar.vText(
			d.speaker + '\n\n' +
			'Resources: http://to.eng.cam.ac.uk/teaching/courses/y1/'
		)
		event['dtstamp'] = icalendar.vDatetime(last_updated)

	return events

def aggregate_calendars(year, spec_data):
	events = []
	for term, courses in spec_data.items():
		cal = ical_for_term(year, term, courses)
		events += fixed_events_in(cal)

	cal = make_blank_calendar(
		'CUED Lectures {}'.format(year),
		description=repr(spec_data)
	)
	cal.subcomponents = events
	return cal

def parse_lecture_spec(spec_str):
	"""
	Takes a string describing courses and terms, and converts it to a dictionary:

	>>> parse_lecture_spec('IA') == dict(michaelmas={'IA'}, lent={'IA'}, easter={'IA'})
	True
	>>> parse_lecture_spec('IA,IB:m') == dict(michaelmas={'IA', 'IB'}, lent={'IA'}, easter={'IA'})
	True
	"""
	all_terms = ['michaelmas', 'lent', 'easter']
	by_term = {t: set() for t in all_terms}
	for entry in spec_str.split(','):
		# parse out the term specifier
		parts = entry.split(':')
		if len(parts) > 2:
			raise ValueError('Too many colons in {!r} - expected course:term'.format(entry))
		name = parts[0]
		if not name:
			raise ValueError('Course name must not be empty!')
		if len(parts) == 1:
			terms = all_terms
		else:
			term_name = parts[1]
			if not term_name:
				raise ValueError('Term name, if specified, must not be empty!')
			term = next((t for t in all_terms if t.startswith(term_name)), None)
			if not term:
				raise ValueError("Unknown term {!r}".format(term_name))
			terms = [term]

		# populate the data
		for term in terms:
			by_term[term].add(name)

	return by_term


if __name__ == '__main__':
	import doctest
	doctest.testmod()
	# print(fixed_events_in(ical_for_term(2016, term='lent', courses=['IIB'])))
	spec = parse_lecture_spec('IA:lent,IB:m,IIB')
	c = aggregate_calendars(2016, spec)
	print(c)
