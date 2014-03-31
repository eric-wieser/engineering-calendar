import urllib2
import icalendar
import re
import pytz
from datetime import datetime

import labs

last_updated = pytz.utc.localize(datetime.utcnow())

timezone = pytz.timezone("Europe/London")

pattern = re.compile(r'(.*\])[CL] (.*)\((.*)\)')

def fix(ical_string, term, lab_group=None):
	cal = icalendar.Calendar.from_ical(ical_string)
	cal['X-WR-CALDESC'] = 'Filtered with location changes'
	cal['X-WR-CALNAME'] += ' ({} - groups {})'.format(term.__name__.split('.')[-1].title(), lab_group)

	# parse data
	data = {}
	for event in cal.subcomponents:
		if not isinstance(event, icalendar.Event):
			print event
			continue

		m = pattern.match(event['summary'])
		data[id(event)] = (event,) + m.groups()

	if lab_group != None:
		# find duplicate coursework events
		duplicates = set()
		seen = set()
		for event, name, speaker, location in data.values():
			if name in seen:
				duplicates.add(name)
			elif name.startswith('1CW'):
				seen.add(name)

		#remove all of them
		for event, name, speaker, location in data.values():
			if name in duplicates:
				cal.subcomponents.remove(event)
				del data[id(event)]

		# add the labs
		for l in term.timetable[lab_group]:
			event = icalendar.Event()
			event['summary']  = icalendar.vText(l.info.name)
			event['location'] = icalendar.vText(l.info.location)
			event['dtstart']  = icalendar.vDatetime(timezone.localize(l.time.start).astimezone(pytz.utc))
			event['dtend']    = icalendar.vDatetime(timezone.localize(l.time.end).astimezone(pytz.utc))

			event['dtstamp']  = icalendar.vDatetime(last_updated)

			event['uid'] = lab_group + l.uid

			cal.subcomponents.append(event)

	# add location information
	for event, name, speaker, location in data.values():
		event['summary'] = icalendar.vText(name)
		event['location'] = icalendar.vText(location)
		event['description'] = icalendar.vText(speaker)


	return cal.to_ical()

if __name__ == '__main__':
	with open('original.ics') as f:
		ical = f.read()
	ical = fix(ical, '178-180')
	with open('fixed.ics', 'wb') as f:
		f.write(ical)
