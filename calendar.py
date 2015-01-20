import icalendar

import labs
import lectures

def construct(part, term, lab_group):
	lcs = lectures.events_for_term(part, term)
	lbs = labs.events_for_term(part, term, lab_group)

	if lbs is None:
		raise KeyError("No such group")

	cal = icalendar.Calendar()
	cal['X-WR-CALDESC'] = 'Filtered with location changes'
	cal['X-WR-CALNAME'] = 'CUED {part} {term} timetable - groups {groups}'.format(
		part=part,
		term=term.title(),
		groups=lab_group
	)
	cal['VERSION'] = '2.0'
	cal['PRODID'] = '-//td.eng.cam.ac.uk/tod//'
	cal.subcomponents += lcs
	cal.subcomponents += lbs

	return cal


if __name__ == '__main__':
	ical = construct('lent', '178-180')
	with open('fixed.ics', 'wb') as f:
		f.write(ical.to_ical())
