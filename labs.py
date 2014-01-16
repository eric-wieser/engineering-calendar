from collections import namedtuple
from datetime import time, timedelta, date, datetime


def cambridge_weekday(date):
	return (date.weekday() + 4) % 7

cambridge_weekday.thur = 0
cambridge_weekday.fri = 1
cambridge_weekday.sat = 2
cambridge_weekday.sun = 3
cambridge_weekday.mon = 4
cambridge_weekday.tue = 5
cambridge_weekday.wed = 6

cw = cambridge_weekday

class TimeSlot(namedtuple('TimeSlot', 'start end')):
	@classmethod
	def morning(cls, date):
		day = cambridge_weekday(date)
		if day in (cw.mon, cw.fri):
			return cls(
				datetime.combine(date, time(9)),
				datetime.combine(date, time(11))
			)
		elif day in (cw.tue, cw.thur):
			return cls(
				datetime.combine(date, time(11)),
				datetime.combine(date, time(13))
			)

	morning_short = morning

	@classmethod
	def afternoon_short(cls, date):
		return cls(
			datetime.combine(date, time(14)), 
			datetime.combine(date, time(16))
		)

	@classmethod
	def afternoon(cls, date):
		return cls(
			datetime.combine(date, time(14)), 
			datetime.combine(date, time(16, 30))
		)

	@classmethod
	def afternoon_long(cls, date):
		return cls(
			datetime.combine(date, time(14)), 
			datetime.combine(date, time(17))
		)


class LabInfo(namedtuple('LabInfo', 'code name location time_slots')):
	def on(self, date):
		return [Lab(self, ctor(date)) for ctor in self.time_slots]

class Lab(namedtuple('Lab', 'info time')):
	@property
	def uid(self):
		return '.'.join([
			'',
			self.info.code,
			self.time.start.isoformat(),
			'IA',
			'lent'
		]) + '@efw27.user.srcf.net'
	

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
		labs = [l.strip() for l in week.split(',')]
		data.append(labs)

	return data, sd_week


def lab_events(term, lab_group):

	# build a lookup table
	lab_lookup = {l.code: l for l in term.lab_info}
	lab_lookup[''] = None

	#day offsets
	columns = [cw.thur, cw.fri, cw.mon, cw.tue, cw.wed]

	regular, sd_week = term.timetable[lab_group]

	for week_num, week in enumerate(regular):
		for day_offset, lab_code in zip(columns, week):
			lab_info = lab_lookup[lab_code]
			if lab_info is None:
				continue
			lab_date = term.start_date + timedelta(day_offset + week_num * 7)

			for l in lab_info.on(lab_date):
				yield l

	if sd_week is not None:
		lab_info = lab_lookup["SW"]
		for day_offset in columns:
			lab_date = term.start_date + timedelta(day_offset + sd_week * 7)

			for l in lab_info.on(lab_date):
				yield l
