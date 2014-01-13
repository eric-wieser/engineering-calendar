from collections import namedtuple
from datetime import time, timedelta, date, datetime

class TimeSlot(namedtuple('TimeSlot', 'start end')):
	@classmethod
	def morning(cls, day):
		if day in ('mon', 'fri'):
			return cls(time(9), time(11))
		elif day in ('tue', 'thur'):
			return cls(time(11), time(13))

	@classmethod
	def morning_short(cls, day):
		if day in ('mon', 'fri'):
			return cls(time(9), time(10))
		elif day in ('tue', 'thur'):
			return cls(time(11), time(12))

	@classmethod
	def afternoon_short(cls, day):
		return cls(time(14), time(16))

	@classmethod
	def afternoon(cls, day):
		return cls(time(14), time(16, 30))

	@classmethod
	def afternoon_long(cls, day):
		return cls(time(14), time(17))


class LabInfo(namedtuple('LabInfo', 'code name location time_slots')):
	def times_on(self, day):
		return [ctor(day) for ctor in self.time_slots]

def parse_row(row):
	import re
	row = row.replace('[', '|[').replace(']', ']|')
	weeks = row.split('|')
	weeks = weeks[1:-1]
	assert len(weeks) == 8

	data = []
	sd_week = None

	for i, week in enumerate(weeks):
		if week.startswith('['):
			assert week.endswith(']')
			week = week[1:-1]
			sd_week = i
		labs = week.split(',')
		data.append(labs)

	return data, sd_week


def print_lab_events(term):
	# build a lookup table
	lab_lookup = {l.code: l for l in term.lab_info}
	lab_lookup[' '] = None

	#day offsets
	days = [(0, 'thur'), (1, 'fri'), (4, 'mon'), (5, 'tue'), (6, 'wed')]

	regular, sd_week = term.timetable

	for week_num, week in enumerate(regular):
		for column, lab_code in enumerate(week):
			lab_info = lab_lookup[lab_code]
			if lab_info is None:
				continue
			day_offset, day_name = days[column]
			lab_date = term.start_date + timedelta(day_offset + week_num * 7)

			times = lab_info.times_on(day_name)
			for t in times:
				print lab_info.name
				print lab_info.location
				print datetime.combine(lab_date, t.start) 
				print datetime.combine(lab_date, t.end) 
				print

	lab_info = lab_lookup["SW"]
	for day_offset, day_name in days:
		lab_date = term.start_date + timedelta(day_offset + sd_week * 7)

		times = lab_info.times_on(day_name)
		for t in times:
			print lab_info.name
			print lab_info.location
			print datetime.combine(lab_date, t.start) 
			print datetime.combine(lab_date, t.end) 
			print

