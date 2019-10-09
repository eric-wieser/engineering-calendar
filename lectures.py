import re
from collections import namedtuple, OrderedDict
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
	if not courses:
		return icalendar.Calendar()

	year_str = '{:4d}_{:02d}'.format(year, (year + 1)%100)

	cal_url = "http://td.eng.cam.ac.uk/tod/public/view_ical.php?yearval={year}&term={term}&course={course}".format(
		year=year_str,
		term=term[0].upper(),
		course=','.join(courses)
	)
	cal_req = requests.get(cal_url)
	cal_req.raise_for_status()
	if cal_req.text.startswith('no timetable committed for '):
		return icalendar.Calendar()

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
	for term, courses in spec_data.terms:
		cal = ical_for_term(year, term, courses)
		events += fixed_events_in(cal, **kwargs)

	cal = make_blank_calendar(
		'CUED Lectures {}'.format(year),
		description='Courses: {}/nLast updated:{}'.format(spec_data, last_updated)
	)
	cal.subcomponents = events
	return cal

class LectureSpec:
	all_terms = ['michaelmas', 'lent', 'easter']

	def __init__(self, spec_str):
		"""
		Takes a string describing courses and terms, and converts it to a dictionary:

		>>> LectureSpec('IA')._data == dict(michaelmas={'IA'}, lent={'IA'}, easter={'IA'})
		True
		>>> LectureSpec('IA,IB:m')._data == dict(michaelmas={'IA', 'IB'}, lent={'IA'}, easter={'IA'})
		True
		"""
		by_term = OrderedDict(
			(t, set())
			for t in LectureSpec.all_terms
		)
		for entry in spec_str.split(','):
			entry = entry.strip()
			# parse out the term specifier
			parts = entry.split(':')
			if len(parts) > 2:
				raise ValueError('Too many colons in {!r} - expected course:term'.format(entry))
			name = parts[0]
			if not name:
				raise ValueError('Course name must not be empty!')
			if len(parts) == 1:
				terms = LectureSpec.all_terms
			else:
				term_name = parts[1]
				if not term_name:
					raise ValueError('Term name, if specified, must not be empty!')
				term = next((t for t in LectureSpec.all_terms if t.startswith(term_name)), None)
				if not term:
					raise ValueError("Unknown term {!r}".format(term_name))
				terms = [term]

			# populate the data
			for term in terms:
				by_term[term].add(name)

		self._data = by_term

	@property
	def terms(self):
		return self._data.items()

	def __str__(self):
		in_all_terms = set.intersection(*self._data.values())
		rest = OrderedDict(
			(k, v - in_all_terms)
			for k, v in self._data.items()
		)
		return ', '.join(
			[str(v) for v in sorted(in_all_terms)] +
			[
				'{}:{}'.format(v, term)
				for term, values in rest.items()
				for v in sorted(values)
			]
		)

	def __repr__(self):
		"""
		>>> LectureSpec('IA:lent,IB:m,IIB')
		LectureSpec('IIB, IB:michaelmas, IA:lent')
		>>> eval(repr(_))
		LectureSpec('IIB, IB:michaelmas, IA:lent')
		"""
		return '{}({!r})'.format(type(self).__name__, str(self))


if __name__ == '__main__':
	import doctest
	doctest.testmod()
	# print(fixed_events_in(ical_for_term(2016, term='lent', courses=['IIB'])))
	spec = LectureSpec('IA:lent,IB:m,IIB')
	c = aggregate_calendars(2016, spec)
	print(c)
