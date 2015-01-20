from datetime import datetime

import icalendar
import pytz

last_updated = pytz.utc.localize(datetime.utcnow())
timezone = pytz.timezone("Europe/London")

cued_address = 'Cambridge University Engineering Department, Cambridge, United Kingdom'

from objects import CourseYear


def construct(part, term, lab_group):
	labs = events_for_term(part, term, lab_group)

	cal = icalendar.Calendar()
	cal['X-WR-CALNAME'] = 'CUED {part} {term} lab timetable - groups {groups}'.format(
		part=part,
		term=term.title(),
		groups=lab_group
	)
	cal['VERSION'] = '2.0'
	cal['PRODID'] = '-//ericwieser.me//CUED lab calendars//EN'
	cal.subcomponents += labs

	return cal

def events_for_term(part, term, lab_group):
	assert part == 'ib'

	timetable = CourseYear('{}.xls'.format(part)).term(term)

	events = []

	# add the labs
	for day, labs in timetable.labs_for(lab_group).items():
		for lab in labs:
			if not lab.slot:
				continue
			startt, endt = lab.slot.on(day)

			events.append(icalendar.Event(
				summary=icalendar.vText(
					'{}: {}'.format(lab.code, lab.name)
					if any(c.isdigit() for c in lab.code) else
					lab.name
				),
				location=icalendar.vText(
					"{} - {}".format(lab.location, cued_address)
					if lab.location else
					cued_address
				),
				dtstart=icalendar.vDatetime(timezone.localize(startt).astimezone(pytz.utc)),
				dtend=  icalendar.vDatetime(timezone.localize(endt).astimezone(pytz.utc)),
				dtstamp=icalendar.vDatetime(last_updated),

				uid='{code}.d{day}.{term}.{part}@efw27.user.srcf.net'.format(
					code=lab.code,
					day=(day - timetable.dates[0]).days,
					term=term,
					part=part
				),

				description=icalendar.vText('Feedback: http://www-g.eng.cam.ac.uk/ssjc/labs.html')
			))

	return events

if __name__ == '__main__':
	print events_for_term('ib', 'lent', '142-144')
