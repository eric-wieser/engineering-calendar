from collections import namedtuple
from datetime import time, timedelta, date, datetime

import cambridgeweekday as cw

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
