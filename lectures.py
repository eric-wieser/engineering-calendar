import urllib2

cal_url = {
	'lent': "http://td.eng.cam.ac.uk/tod/public/view_ical.php?yearval=2013_14&term=L&course=IA",
	'easter': "http://td.eng.cam.ac.uk/tod/public/view_ical.php?yearval=2013_14&term=E&course=IA"
}

def ical_for_term(term):
	cal_req = urllib2.urlopen(cal_url[term])
	cal = cal_req.read()
	return cal
