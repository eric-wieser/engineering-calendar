import urllib2
import icalendar
import re
from datetime import datetime

import labs
import terms.lent

last_updated = datetime(2014, 1, 13)

pattern = re.compile(r'(.*\])[CL] (.*)\((.*)\)')

def fix(ical_string):
	cal = icalendar.Calendar.from_ical(ical_string)
	cal['X-WR-CALDESC'] = 'Filtered with location changes'

	# parse data
	data = {}
	for event in cal.subcomponents:
		if not isinstance(event, icalendar.Event):
			print event
			continue

		m = pattern.match(event['summary'])
		data[id(event)] = (event,) + m.groups()

	# find duplicate coursework events
	duplicates = set()
	seen = set()
	for event, name, speaker, location in data.values():
		if name in seen:
			duplicates.add(name)
		elif name.startswith('1CW'):
			seen.add(name)

	print '\n'.join(sorted(duplicates))

	#remove all of them
	for event, name, speaker, location in data.values():
		if name in duplicates:
			cal.subcomponents.remove(event)
			del data[id(event)]

	# add location information
	for event, name, speaker, location in data.values():
		event['summary'] = icalendar.vText(name)
		event['location'] = icalendar.vText(location)
		event['description'] = icalendar.vText(speaker)

	# add the labs
	for l in labs.lab_events(terms.lent):
		event = icalendar.Event()
		event['summary']  = icalendar.vText(l.info.name)
		event['location'] = icalendar.vText(l.info.location)
		event['dtstart']  = icalendar.vDatetime(l.time.start)
		event['dtend']    = icalendar.vDatetime(l.time.end)

		event['dtstamp']  = icalendar.vDatetime(last_updated)

		event['uid'] = l.uid

		cal.subcomponents.append(event)

	return cal.to_ical()

if __name__ == '__main__':
	with open('original.ics') as f:
		ical = f.read()
	ical = fix(ical)
	with open('fixed.ics', 'wb') as f:
		f.write(ical)
