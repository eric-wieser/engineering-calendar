import urllib2
import icalendar
import re

pattern = re.compile(r'(.*\])[CL] (.*)\((.*)\)')

def fix(ical_string):
	cal = icalendar.Calendar.from_ical(ical_string)

	for event in cal.subcomponents:
		if not isinstance(event, icalendar.Event):
			print event
			continue

		m = pattern.match(event['summary'])
		name, speaker, location = m.groups()

		event['summary'] = icalendar.vText(name)
		event['location'] = icalendar.vText(location)
		event['description'] = icalendar.vText(speaker)

	return cal.to_ical()
