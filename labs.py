from datetime import datetime

import icalendar
import pytz

import students
import terms

last_updated = pytz.utc.localize(datetime.utcnow())
timezone = pytz.timezone("Europe/London")

def events_for_term(part, term, lab_group):
	try:
		course = getattr(terms, part)
		term = getattr(course, term)
	except ImportError:
		return None

	events = []

	# add the labs
	for l in term.timetable[lab_group]:
		attendees = students.at_event(l)

		event = icalendar.Event()
		if l.info.code.isdigit():
			event['summary'] = icalendar.vText('1CW: ' + l.info.code + ' ' + l.info.name)
		else:
			event['summary'] = icalendar.vText('1CW: ' + l.info.name)
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

		events.append(event)

	return events

if __name__ == '__main__':
	print events_for_term('lent', '178-180')
