from __future__ import unicode_literals
from datetime import datetime, time
import re

import xlrd

def _strify(c):
	if isinstance(c, float):
		return str(int(c))
	return str(c)


def _dateify(value, wb):
	return datetime(*xlrd.xldate_as_tuple(value, wb.datemode))


class Slot(object):
	def __init__(self, name, times=None):
		self.times = times or {}
		self.name = name

	def on(self, date):
		day = '{:%a}'.format(date)  # 3-letter day names (Mon, Tue, etc)

		try:
			start, end = self.times.get(day) or self.times['']
		except KeyError:
			raise ValueError("No times for {} associated with {}, and no default found".format(day, self.name))

		return datetime.combine(date, start), datetime.combine(date, end)

	def __repr__(self):
		return "Slot({s.name!r}, {s.times!r})".format(s=self)


class Lab(object):
	def __init__(self, code, group, name, location, slots, link):
		self.group = group
		self.code = code
		self.name = name
		self.location = location
		self.slots = slots
		self.link = link

	def __repr__(self):
		return "Lab({s.code!r}, {s.group!r}, {s.name!r}, {s.location!r}, slot=<{sl}>)".format(
			s=self, sl=', '.join(s.name for s in self.slots))

	def times_on(self, day):
		return [slot.on(day) for slot in self.slots]


class Timetable(object):
	def __init__(self, table, dates, groups, course):
		self.dates = dates
		self.groups = groups
		self.table = table
		self.course = course

	def labs_for(self, lab_code):
		return self.table[lab_code]


class ExamplePaper(object):
	def __init__(self, name, sheet_no, paper_no, issue_date, class_date, class_location, class_lecturer):
		self.name = name
		self.sheet_no = sheet_no
		self.paper_no = paper_no

		self.issue_date = issue_date

		# TODO: remove hard-coded times
		self.class_start = datetime.combine(class_date, time(hour=11))
		self.class_end = datetime.combine(class_date, time(hour=12))
		self.class_location = class_location
		self.class_lecturer = class_lecturer


class CourseYear(object):
	def __init__(self, part, year, xls_fname):
		self.part = part
		self.year = year
		self._wb = xlrd.open_workbook(xls_fname, formatting_info=True)
		self.slots = self._get_slots()
		self.labs = self._get_labs()

		self._timetable = {}

	@classmethod
	def iter(cls):
		import os
		for fname in os.listdir():
			m = re.match(r'(\w+)-(\d+).xls', fname)
			if m:
				yield cls.get(m.group(1), int(m.group(2)))


	@classmethod
	def get(cls, part, year):
		return cls(part, year, '{}-{}.xls'.format(part, year))

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

		assert headers[:6] == ['Group', 'Code', 'Name', 'Location', 'Slot', 'Link']

		current_group = None


		labs = {}
		for i in range(1, sh.nrows):
			group, code, name, location, slots, link = [c.value for c in sh.row(i)[:6]]
			code = _strify(code)

			if group:
				current_group = group
				continue

			if slots:
				slots = [self.slots[slot] for slot in slots.split(',')]
			else:
				slots = []

			if code in labs:
				raise ValueError("Lab code {} refers to both {} and {}".format(code, labs[code].name, name))

			labs[code] = Lab(code, current_group, name, location, slots, link)

		return labs

	def examples(self, name='lent'):
		try:
			sh = self._wb.sheet_by_name('examples-{}'.format(name))
		except xlrd.XLRDError as e:
			raise LookupError("No data for example papers in term {!r}".format(name))

		issue_date = None

		def gen():
			for i in range(1, sh.nrows):
				week, n_issue_date, title, sheet_no, class_date, class_lecturer, class_location = [c.value for c in sh.row(i)[:7]]

				if n_issue_date:
					try:
						issue_date = _dateify(n_issue_date, self._wb)
					except ValueError:
						issue_date = None

				class_date = _dateify(class_date, self._wb)
				sheet_no = int(sheet_no)

				paper_no, name = re.match(r'^P(\d): (.*)$', title).groups()
				paper_no = int(paper_no)

				yield ExamplePaper(
					name=name,
					sheet_no=sheet_no,
					paper_no=paper_no,

					issue_date=issue_date,

					class_date=class_date,
					class_location=class_location,
					class_lecturer=class_lecturer
				)

		return gen()





	def term(self, name='lent'):
		try:
			sh = self._wb.sheet_by_name(name)
		except xlrd.XLRDError as e:
			raise LookupError("No data for term {!r}".format(name))

		col_area = range(1, sh.ncols)
		row_area = range(4, sh.nrows)

		def get_dates():
			# read start month
			assert sh.cell_value(0, 0) == 'Start month', "A1 should contain 'Start month:'"
			start_month = _dateify(sh.cell_value(0, 1), self._wb)

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
				if not '{:%a}'.format(date).startswith(day_name):
					raise ValueError("Day in column {}, {:%a %d %b} is not a {!r}".format(i, date, day_name))
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
					rrange = range(rlo, rhi)
					crange = range(clo, chi)

					yield rrange, crange, sh.cell_value(rlo, clo)

		dates = list(get_dates())
		groups = list(get_groups())
		merges = list(get_merges())

		results = {}

		def get_code(r, c):
			for merge_r, merge_c, code in merges:
				if r in merge_r and c in merge_c:
					return _strify(code)
			return _strify(sh.cell_value(r, c))

		# convert timetable to lab objects
		for group, r in zip(groups, row_area):
			results[group] = {}
			for date, c in zip(dates, col_area):
				codes = get_code(r, c).split(',')
				results[group][date] = [self.labs[code] for code in codes if code]

		return Timetable(dates=dates, groups=groups, table=results, course=self)
