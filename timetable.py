import itertools
import re

parens = ('[]', '{}', '[]')

class Timetable(object):
	@staticmethod
	def _str_to_key(s):
		return tuple(map(int, s.split('-')))

	@staticmethod
	def _parse_row(row):
		# deal with parens replacing week barriers
		for start, end in parens:
			row = row.replace(start, '|' + start)
			row = row.replace(end, end + '|')

		weeks = row.split('|')
		weeks = weeks[1:-1]

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

	def __init__(self, start_date, d):
		self.start_date = start_date

		self.num_days = None

		self.d = {}
		for k, v in d.iteritems():
			k = self._str_to_key(k)
			v = self._parse_row(v)

			self.d[k] = v

			# check rows are the same length
			if self.num_days is not None and self.num_days != len(v):
				raise ValueError("Not all groups have the same length timetable!")

			self.num_days = len(v)

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
