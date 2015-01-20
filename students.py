class Student(object):
	def __init__(self, name, college, crsid, lab_group):
		self.name = name
		self.college = college
		self.crsid = crsid
		self.lab_group = int(lab_group)

	@property
	def email(self):
		return self.crsid + '@eng.cam.ac.uk'

	def __repr__(self):
		return "<Student {}>".format(self.crsid)

import csv
from collections import defaultdict

groups_at_event = defaultdict(set)
students_in_group = defaultdict(set)

from terms.y2013.IA.easter import timetable as t1
from terms.y2013.IA.easter import timetable as t2

for t in (t1, t2):
	for g in t.groups:
		for event in t[g]:
			groups_at_event[event].add(g)

with open('terms/y2013/IA/EGT0.csv') as f:
	for s in csv.DictReader(f):
		s = Student(name=s['Name'], college=s['College'], crsid=s['Userid'], lab_group=int(s['Lab group']))


		i = (s.lab_group - 1) // 3
		group_range = (i * 3 + 1, i * 3 +3)
		students_in_group[group_range].add(s)

def at_event(e):
	return [s for g in groups_at_event[e] for s in students_in_group[g]]
