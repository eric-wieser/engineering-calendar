import urllib2
import re
from collections import namedtuple
from datetime import datetime

import icalendar
import pytz

last_updated = pytz.utc.localize(datetime.utcnow())

def ical_for_term(part, term):
	cal_url = "http://td.eng.cam.ac.uk/tod/public/view_ical.php?yearval={year}&term={term}&course={part}".format(
		year='2013_14',
		term=term[0].upper(),
		part=part
	)
	cal_req = urllib2.urlopen(cal_url)
	cal = cal_req.read()
	return cal


pattern = re.compile(r'(.*?)/(.*)\[(\d+)\][CL] (.*)\((.*)\)')
MatchData = namedtuple('MatchData', 'module name week speaker location')

def events_for_term(part, term):
	ical_string = ical_for_term(part, term)
	cal = icalendar.Calendar.from_ical(ical_string)

	events = []
	for event in cal.subcomponents:
		if not isinstance(event, icalendar.Event):
			print event
		else:
			events.append(event)


	data = {}
	for event in events:
		m = pattern.match(event['summary'])
		data[id(event)] = MatchData(*m.groups())

	# find duplicate coursework events
	duplicates = set()
	seen = set()
	for event in events:
		d = data[id(event)]
		if d.name in seen:
			duplicates.add(d.name)
		elif d.module == '1CW' and 'Examples' not in d.name:
			seen.add(d.name)

	#remove all of them
	events = [event for event in events if data[id(event)].name not in duplicates]

	# add location information
	for event in events:
		d = data[id(event)]
		event['summary'] = icalendar.vText(d.module + ': ' + d.name)
		event['location'] = icalendar.vText(d.location)
		event['description'] = icalendar.vText(
			d.speaker + '\n\n' +
			'Resources: http://to.eng.cam.ac.uk/teaching/courses/y1/'
		)
		event['dtstamp'] = icalendar.vDatetime(last_updated)

	return events

if __name__ == '__main__':
	print events_for_term('IA', 'lent')
