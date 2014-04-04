import urllib2
import icalendar
import re
import pytz
from datetime import datetime

import labs
import students

last_updated = pytz.utc.localize(datetime.utcnow())

timezone = pytz.timezone("Europe/London")

pattern = re.compile(r'(.*?)/(.*)\[(\d+)\][CL] (.*)\((.*)\)')

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
		for event, module, name, week, speaker, location in data.values():
			if name in seen:
				duplicates.add(name)
			elif module == '1CW' and 'Examples' not in name:
				seen.add(name)

		#remove all of them
		for event, module, name, week, speaker, location in data.values():
			if name in duplicates:
				cal.subcomponents.remove(event)
				del data[id(event)]

		# add the labs
		for l in term.timetable[lab_group]:
			attendees = students.at_event(l)


			event = icalendar.Event()
			if l.info.code.isdigit():
				event['summary']  = icalendar.vText('1CW: ' + l.info.code + ' ' + l.info.name)
			else:
				event['summary']  = icalendar.vText('1CW: ' + l.info.name)
			event['location'] = icalendar.vText(l.info.location)
			event['dtstart']  = icalendar.vDatetime(timezone.localize(l.time.start).astimezone(pytz.utc))
			event['dtend']    = icalendar.vDatetime(timezone.localize(l.time.end).astimezone(pytz.utc))

			event['dtstamp']  = icalendar.vDatetime(last_updated)

			event['uid'] = lab_group + l.uid

			event['description'] = icalendar.vText('Feedback: http://www-g.eng.cam.ac.uk/ssjc/labs.html')

			for a in sorted(attendees, key=lambda a: a.name):
				attendee = icalendar.vCalAddress('MAILTO:' + a.email)
				attendee.params['cn'] = icalendar.vText(a.name)
				attendee.params['ROLE'] = icalendar.vText('REQ-PARTICIPANT')
				event.add('attendee', attendee)

			cal.subcomponents.append(event)

	# add location information
	for event, module, name, week, speaker, location in data.values():
		event['summary'] = icalendar.vText(module + ': ' + name)
		event['location'] = icalendar.vText(location)
		event['description'] = icalendar.vText(
			speaker + '\n\n' +
			'Resources: http://to.eng.cam.ac.uk/teaching/courses/y1/'
		)


	return cal.to_ical()

if __name__ == '__main__':
	import terms.IA.lent
	with open('original.ics') as f:
		ical = f.read()
	ical = fix(ical, terms.IA.lent, '178-180')
	with open('fixed.ics', 'wb') as f:
		f.write(ical)
