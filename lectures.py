import re
from collections import namedtuple
from datetime import datetime
import json

import icalendar
import pytz
import requests

from calendarmaker import cued_address, make_blank_calendar

with open("courselinks.json") as f:
	course_links = json.load(f)

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
MatchData = namedtuple('MatchData', 'code name week lecturer location')

def fixed_events_in(cal, name_format=None):
	if not name_format:
		name_format = '{code}: {name}'

	events = [
		event
		for event in cal.subcomponents
		if isinstance(event, icalendar.Event)
	]

	# add location information
	for event in events:
		d = MatchData(*pattern.match(event['summary']).groups())
		if d.code in course_links:
			resources = 'http://teaching.eng.cam.ac.uk' + course_links[d.code]
		else:
			resources = None

		event['summary'] = icalendar.vText(name_format.format(**d._asdict()))
		event['location'] = icalendar.vText(d.location + ', ' + cued_address)
		event['description'] = icalendar.vText(
			d.lecturer + ('\n\n{}'.format(resources) if resources else '')
		)
		event['dtstamp'] = icalendar.vDatetime(last_updated)

	return events

def aggregate_calendars(year, spec_data, **kwargs):
	events = []
	for term, courses in spec_data.items():
		cal = ical_for_term(year, term, courses)
		events += fixed_events_in(cal, **kwargs)

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
