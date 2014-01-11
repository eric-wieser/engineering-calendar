import urllib2
import icalendar
import re

pattern = re.compile(r'(.*\])(.*)\((.*)\)')


cal_url = "http://td.eng.cam.ac.uk/tod/public/view_ical.php?yearval=2013_14&term=L&course=IA"

response = urllib2.urlopen(cal_url)
cal = response.read()
cal = icalendar.Calendar.from_ical(cal)
with open('lecturesold.ics', 'wb') as f:
	f.write(cal.to_ical())


for event in cal.subcomponents:
	if not isinstance(event, icalendar.Event):
		print event
		continue

	m = pattern.match(event['summary'])
	name, speaker, location = m.groups()

	if 'see rota' in name:
		print name

	event['summary'] = icalendar.vText(name)
	event['location'] = icalendar.vText(location)
	event['description'] = icalendar.vText(speaker)

with open('lectures.ics', 'wb') as f:
	f.write(cal.to_ical())
