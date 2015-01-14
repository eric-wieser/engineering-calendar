import unittest
import main
import re


class TestRegression(unittest.TestCase):
	def test_for_IA(self):
		self.maxDiff = 60000
		with open('test_regression_lent_178.ics', 'rb') as f:
			old = f.read()

		new = main.ia_term_calendar('lent', '178-180').to_ical()

		new = re.sub(r'\r\nDTSTAMP:[0-9TZ]+', '\r\nDTSTAMP:<snip>', new)
		old = re.sub(r'\r\nDTSTAMP:[0-9TZ]+', '\r\nDTSTAMP:<snip>', old)

		self.assertMultiLineEqual(old, new)


if __name__ == '__main__':
    unittest.main()