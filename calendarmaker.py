from datetime import datetime
import itertools

import icalendar
import pytz

last_updated = pytz.utc.localize(datetime.utcnow())
timezone = pytz.timezone("Europe/London")

cued_address = 'Cambridge University Engineering Department, Cambridge, United Kingdom'

def construct(course_year, term, lab_group=None, examples=False):
	if lab_group:
		evts = labs_for_term(course_year, term, lab_group)
		name = 'CUED {part} {term} lab timetable - Groups {groups}'.format(
			part=course_year.part.upper(),
			term=term.title(),
			groups=lab_group
		)
	elif examples:
		evts = examples_for_term(course_year, term)
		name = 'CUED {part} {term} example class timetable'.format(
			part=part.upper(),
			term=term.title()
		)
	else:
		raise TypeError('Invalid arguments')

	cal = icalendar.Calendar()
	cal['X-WR-CALNAME'] = name
	cal['VERSION'] = '2.0'
	cal['PRODID'] = '-//ericwieser.me//CUED calendars//EN'
	cal.subcomponents += evts

	return cal

def examples_for_term(course_year, term):
	examples = list(course_year.examples(term))

	events = []

	for example in examples:
		events.append(icalendar.Event(
			summary='P{0.paper_no}: {0.name} - Example paper {0.sheet_no}'.format(example),
			dtstart=icalendar.vDatetime(timezone.localize(example.class_start).astimezone(pytz.utc)),
			dtend=icalendar.vDatetime(timezone.localize(example.class_end).astimezone(pytz.utc)),
			dtstamp=icalendar.vDatetime(last_updated),

			location=icalendar.vText(
				"{} - {}".format(example.class_location, cued_address)
				if example.class_location else
				cued_address
			),

			uid='{0.paper_no}-{0.sheet_no}.{term}.{part}@efw27.user.srcf.net'.format(
				example,
				term=term,
				part=course_year.part
			),

			description=icalendar.vText('Lecturer: {.class_lecturer}'.format(example))
		))

	# group and order by issue date, ignoring those issued the previous term
	issue_key = lambda e: e.issue_date
	examples = filter(issue_key, examples)
	examples = sorted(examples, key=issue_key)
	examples = itertools.groupby(examples, issue_key)

	for i, (issue_date, papers) in enumerate(examples):
		# consume the iterable so that we can len() it
		papers = list(papers)
		events.append(icalendar.Event(
			summary='Collect {} example paper{}'.format(len(papers), '' if len(papers) == 1 else 's'),
			dtstart=icalendar.vDate(timezone.localize(issue_date).astimezone(pytz.utc)),
			dtend=icalendar.vDate(timezone.localize(issue_date).astimezone(pytz.utc)),
			dtstamp=icalendar.vDatetime(last_updated),

			location=icalendar.vText(cued_address),

			uid='collection-{i}.{term}.{part}@efw27.user.srcf.net'.format(
				i=i,
				term=term,
				part=course_year.part
			),

			description=icalendar.vText('\n'.join(
				'P{0.paper_no}: {0.name} - Example paper {0.sheet_no}'.format(p)
				for p in papers
			))
		))

	return events


def labs_for_term(course_year, term, lab_group):
	timetable = course_year.term(term)

	events = []

	# add the labs
	for day, labs in timetable.labs_for(lab_group).items():
		for lab in labs:
			if not lab.slots:
				continue
			for i, (startt, endt) in enumerate(lab.times_on(day)):
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

					uid='{code}-{i}.d{day}.{term}.{part}@efw27.user.srcf.net'.format(
						i=i,
						code=lab.code,
						day=(day - timetable.dates[0]).days,
						term=term,
						part=course_year.part
					),

					description=icalendar.vText(
						'{}Feedback: http://www-g.eng.cam.ac.uk/ssjc/labs.html'.format(
							"Information: {}\n\n".format(lab.link) if lab.link else ""
						)
					)
				))

	return events

if __name__ == '__main__':
	from objects import CourseYear
	print(construct(CourseYear.get('ib', 2014), 'lent', '142-144').to_ical())
