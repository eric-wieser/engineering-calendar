% from bottle import request
% from objects import NoTermData

<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
<html>
	<head>
		<link rel="icon" type="image/png" href="http://cdn.dustball.com/calendar.png">
		<title>CUED calendars</title>
		<link href="//maxcdn.bootstrapcdn.com/bootstrap/3.3.2/css/bootstrap.min.css" rel="stylesheet">
                <style> footer{	padding-top: 5em;}</style>
	</head>
	<body>
		<div class="container">
			<h1>Online web calendars for the CUED labs</h1>
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
   			<footer>		
      				<p>
        			The software used to generate these pages was written by Eric Wieser, an undergraduate at CUED. If you wish to contribute any fixes or changes to this software an active fork of his original code can be found on
        			<a href="https://github.com/S-Stephen/engineering-calendar">GitHub</a>.
      				</p>
  			</footer>
		</div>
	</body>
</html>
