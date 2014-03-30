from labs import parse_row

class Timetable(object):
	@staticmethod
	def _str_to_key(s):
		return tuple(map(int, s.split('-')))

	def __init__(self, start_date, d):
		self.start_date = start_date

		l = None

		self.d = {}
		for k, v in d.iteritems():
			k = self._str_to_key(k)
			v = parse_row(v)

			self.d[k] = v

			# check rows are the same length
			if l is not None and l != len(v):
				raise ValueError("Not all groups have the same length timetable!")

			l = len(v)

	def __getitem__(self, key):
		if isinstance(key, basestring):
			try:
				key = self._str_to_key(key)
			except ValueError:
				raise KeyError
		return self.d[key]

	@property
	def groups(self):
	    return  sorted(self.d.keys())
