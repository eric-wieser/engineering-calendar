import icalendar

import labs
import lectures

def construct(term, lab_group):
	lcs = lectures.events_for_term(term)
	lbs = labs.events_for_term(term, lab_group)

	if lbs is None:
		raise KeyError("No such group")

	cal = icalendar.Calendar()
	cal['X-WR-CALDESC'] = 'Filtered with location changes'
	cal['X-WR-CALNAME'] = 'CUED IA {} timetable - groups {}'.format(term.title(), lab_group)
	cal['VERSION'] = '2.0'
	cal['PRODID'] = '-//td.eng.cam.ac.uk/tod//'
	cal.subcomponents += lcs
	cal.subcomponents += lbs

	return cal


if __name__ == '__main__':
	ical = construct('lent', '178-180')
	with open('fixed.ics', 'wb') as f:
		f.write(ical.to_ical())
