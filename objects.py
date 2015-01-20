from __future__ import unicode_literals
from datetime import datetime, time

import xlrd


class Slot(object):
	def __init__(self, name, times=None):
		self.times = times or {}
		self.name = name

	def on(self, date):
		day = '{:%a}'.format(date)  # 3-letter day names (Mon, Tue, etc)

		start, end = self.times.get(day) or self.times['']

		return datetime.combine(date, start), datetime.combine(date, end)

	def __repr__(self):
		return "Slot({s.name!r}, {s.times!r})".format(s=self)


class Lab(object):
	def __init__(self, code, group, name, location, slot):
		self.group = group
		self.code = code
		self.name = name
		self.location = location
		self.slot = slot

	def __repr__(self):
		return "Lab({s.code!r}, {s.group!r}, {s.name!r}, {s.location!r}, slot={sl})".format(
			s=self, sl='slots[{s.slot.name!r}]'.format(s=self) if self.slot else repr(None))


class Timetable(object):
	def __init__(self, table, dates, groups):
		self.dates = dates
		self.groups = groups
		self.table = table

	def labs_for(self, lab_code):
		return self.table[lab_code]


class CourseYear(object):
	def __init__(self, xls_fname):
		self._wb = xlrd.open_workbook(xls_fname, formatting_info=True)
		self.slots = self._get_slots()
		self.labs = self._get_labs()

		self._timetable = {}

	def _get_slots(self):
		sh = self._wb.sheet_by_name('slots')
		headers = [c.value for c in sh.row(0)]

		assert headers == ['Slot', 'Day', 'Start', 'End']

		slots = {}

		for i in range(1, sh.nrows):
			name, day, start, end = [c.value for c in sh.row(i)[:4]]
			start = time(*xlrd.xldate_as_tuple(start, self._wb.datemode)[3:])
			end = time(*xlrd.xldate_as_tuple(end, self._wb.datemode)[3:])

			if name not in slots:
				slots[name] = Slot(name)

			slot = slots[name]
			slot.times[day] = start, end

		return slots

	def _get_labs(self):
		sh = self._wb.sheet_by_name('labs')
		headers = [c.value for c in sh.row(0)]

		assert headers == ['Group', 'Code', 'Name', 'Location', 'Slot']

		current_group = None


		labs = {}
		for i in range(1, sh.nrows):
			group, code, name, location, slot = [c.value for c in sh.row(i)[:5]]

			if group:
				current_group = group
				continue

			if slot:
				slot = self.slots[slot]
			else:
				slot = None

			if code in labs:
				raise ValueError("Lab code {} refers to both {} and {}".format(code, labs[code].name, name))

			labs[code] = Lab(code, current_group, name, location, slot)

		return labs

	def term(self, name='lent'):
		try:
			sh = self._wb.sheet_by_name(name)
		except xlrd.XLRDError as e:
			raise LookupError("No data for term {!r}".format(name))

		col_area = xrange(1, sh.ncols)
		row_area = xrange(4, sh.nrows)

		def get_dates():
			# read start month
			assert sh.cell_value(0, 0) == 'Start month', "A1 should contain 'Start month:'"
			start_month = sh.cell_value(0, 1)
			start_month = datetime(*xlrd.xldate_as_tuple(start_month, self._wb.datemode))

			# parse column headers, check dates
			last_date_no = 0
			for i in range(1, sh.ncols):
				day_name, date_no = [c.value for c in sh.col(i)[1:3]]
				date_no = int(date_no)

				# increment the month if we roll over
				if date_no < last_date_no:
					month = start_month.month + 1
					start_month = datetime(
						year=start_month.year + (month - 1)//12,
						month=(month - 1)%12 + 1, day=1)

				# build and check the new date
				date = start_month.replace(day=date_no)
				assert '{:%a}'.format(date).startswith(day_name)
				yield date.date()

				last_date_no = date_no

		def get_groups():
			assert sh.cell_value(3, 0) == 'Groups', "A4 should contain 'Groups'"
			for i in range(4, sh.nrows):
				group = sh.cell_value(i, 0)
				yield group

		def get_merges():
			for rlo, rhi, clo, chi in sh.merged_cells:
				if rlo not in row_area or rhi-1 not in row_area:
					raise ValueError('Merged cell overflows range horizontally')
				elif clo not in col_area or chi-1 not in col_area:
					raise ValueError('Merged cell overflows range vertically')
				else:
					rrange = xrange(rlo, rhi)
					crange = xrange(clo, chi)

					yield rrange, crange, sh.cell_value(rlo, clo)

		dates = list(get_dates())
		groups = list(get_groups())
		merges = list(get_merges())

		results = {}

		def get_code(r, c):
			for merge_r, merge_c, code in merges:
				if r in merge_r and c in merge_c:
					return code
			return sh.cell_value(r, c)

		# convert timetable to lab objects
		for group, r in zip(groups, row_area):
			results[group] = {}
			for date, c in zip(dates, col_area):
				codes = get_code(r, c).split(',')
				results[group][date] = [self.labs[code] for code in codes if code]

		return Timetable(dates=dates, groups=groups, table=results)
