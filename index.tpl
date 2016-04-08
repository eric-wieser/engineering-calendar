% from bottle import request
% from objects import NoTermData

<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
<html>
	<head>
		<link rel="icon" type="image/png" href="http://cdn.dustball.com/calendar.png">
		<title>CUED calendars</title>
		<link href="//maxcdn.bootstrapcdn.com/bootstrap/3.3.2/css/bootstrap.min.css" rel="stylesheet">
	</head>
	<body>
		<div class="container">
			<h1>Online web calendars for the CUED labs and example classes</h1>
			% for year, p in parts:
				<h2>{{ year }} &ndash; {{year + 1}}</h2>
				<div class="row">
					% for c in sorted(p, key=lambda c: c.part):
						<div class="col-md-6">
							<h3>Part {{ c.part.upper() }}</h3>
							% for tid, tname in [('mich', 'michaelmas'), ('lent',)*2, ('easter',)*2]:
								% try:
									% c.term(tid)
									<a class="btn btn-default btn-lg btn-block"
											href='{{ request.urlparts._replace(path=request.urlparts.path + '{}/{}/{}'.format(c.year, c.part, tid)).geturl() }}'>
										{{ tname.title() }} labs
									</a>
								% except NoTermData: pass
								% except Exception as e:
									<div class="alert alert-danger"><strong>Failed to load {{ tname.title() }} labs</strong> - {{ repr(e) }}</div>
								% end

								% try:
									% c.examples(tid)
									<a class="btn btn-default btn-lg btn-block"
											href='{{ request.urlparts._replace(scheme='webcal', path=request.urlparts.path + '{}/{}/{}/examples.ics'.format(c.year, c.part, tid)).geturl() }}'>
										{{ tname.title() }} example rota
									</a>
								% except NoTermData: pass
								% end
							% end
						</div>
					% end
				</div>
			% end
		</div>
		<a href="https://github.com/eric-wieser/engineering-calendar"><img style="position: absolute; top: 0; right: 0; border: 0;" src="https://s3.amazonaws.com/github/ribbons/forkme_right_orange_ff7600.png" alt="Fork me on GitHub"></a>
	</body>
</html>