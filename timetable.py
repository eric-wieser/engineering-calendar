import itertools
import re
from datetime import timedelta, datetime, time
from collections import namedtuple

import cambridgeweekday as cw

parens = ('[]', '{}', '[]')

class Timetable(object):
	@staticmethod
	def _str_to_key(s):
		return tuple(map(int, s.split('-')))


	def _split_row(self, row):
		"""Splits a row into a set of comma-separated weeks"""
		# deal with parens replacing week barriers
		for start, end in parens:
			row = row.replace(start, '|' + start)
			row = row.replace(end, end + '|')

		weeks = row.split('|')
		weeks = [w for w in weeks if w]
		return weeks


	def _split_week(self, week):
		"""Splits a week into a set of LabInfo objects"""
		paren = ''
		for start, end in parens:
			if week.startswith(start):
				assert week.endswith(end)
				week = week[1:-1]
				paren = start + end

		return [self._lab_lookup[l.strip()] for l in week.split(',')], self._lab_lookup[paren]

	def _events(self, row):
		"""Produce the final list of events from the timetable"""
		num_days = 0
		for week_num, week in enumerate(self._split_row(row)):
			week_start = self.start_date + timedelta(week_num * 7)

			day_entries, week_entry = self._split_week(week)
			num_days += len(day_entries)

			entries = [(0, week_entry)] + zip(self.columns, day_entries)

			for offset, entry in entries:
				day_start = week_start + timedelta(offset)

				if entry is not None:
					for l in entry.on(day_start):
						yield l

		if self.num_days is not None and num_days != self.num_days:
			print weeks
			raise ValueError(
				"{} weeks found, previous rows had {}"
				.format(num_days, self.num_days))

		self.num_days = num_days


	def __init__(self, start_date, lab_info, columns, grid):
		self.start_date = start_date
		self.num_days = None
		self.columns = columns

		self._lab_lookup = {l.code: l for l in lab_info}
		self._lab_lookup[''] = None

		self.d = {}
		for k, v in grid.iteritems():
			k = self._str_to_key(k)
			v = sorted(self._events(v), key=lambda e: e.time.start)

			self.d[k] = v

	def __getitem__(self, key):
		if isinstance(key, basestring):
			try:
				key = self._str_to_key(key)
			except ValueError:
				raise KeyError
		if isinstance(key, int):
			i = (key - 1) // 3
			key = (i * 3 + 1, i * 3 +3)

		return self.d[key]

	@property
	def groups(self):
		return  sorted(self.d.keys())

class TimeSlot(namedtuple('TimeSlot', 'start end')):
	@classmethod
	def morning(cls, date):
		day = cw.of(date)
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

	@classmethod
	def full_week_of(cls, slot):
		offsets = (cw.thur, cw.fri, cw.mon, cw.tue, cw.wed)
		def make_slot_maker(day):
			return lambda date: slot(date + timedelta(day))

		return [make_slot_maker(day) for day in offsets]

class LabInfo(namedtuple('LabInfo', 'code name location time_slots')):
	def on(self, date):
		return [Lab(self, ctor(date)) for ctor in self.time_slots]

	__eq__ = object.__eq__
	__hash__ = object.__hash__

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
