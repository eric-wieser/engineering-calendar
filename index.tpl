% from bottle import request

<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
<html>
	<head>
		<link rel="icon" type="image/png" href="http://cdn.dustball.com/calendar.png">
		<title>CUED calendars</title>
		<link href="//maxcdn.bootstrapcdn.com/bootstrap/3.3.2/css/bootstrap.min.css" rel="stylesheet">
	</head>
	<body>
		% seen_labs = set()
		<div class="container">
			<h1>Online web calendars for the CUED labs and example classes <small>2014-2015</small></h1>
			<div class="row">
				<div class="col-md-6">
					<h2>Part IA</h2>
					<a class="btn btn-default btn-lg btn-block" href='{{ request.urlparts._replace(path=request.urlparts.path + 'ia/lent').geturl() }}'>Lent labs</a>
					<a class="btn btn-default btn-lg btn-block" href='{{ request.urlparts._replace(path=request.urlparts.path + 'ia/easter').geturl() }}'>Easter labs</a>
				</div>
				<div class="col-md-6">
					<h2>Part IB</h2>
					<a class="btn btn-default btn-lg btn-block" href='{{ request.urlparts._replace(path=request.urlparts.path + 'ib/mich').geturl() }}'>Michaelmas labs</a>
					<a class="btn btn-default btn-lg btn-block" href='{{ request.urlparts._replace(path=request.urlparts.path + 'ib/lent').geturl() }}'>Lent labs</a>
					<a class="btn btn-default btn-lg btn-block" href='{{ request.urlparts._replace(scheme='webcal', path=request.urlparts.path + 'ib/lent/examples.ics').geturl() }}'>Lent example classes</a>
				</div>
		</div>
		<a href="https://github.com/eric-wieser/engineering-calendar"><img style="position: absolute; top: 0; right: 0; border: 0;" src="https://s3.amazonaws.com/github/ribbons/forkme_right_orange_ff7600.png" alt="Fork me on GitHub"></a>
	</body>
</html>