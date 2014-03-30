<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
<html>
	<head>
		<link rel="icon" type="image/png" href="http://cdn.dustball.com/calendar.png">
		<title>Lent calendars</title>
		<style type="text/css">
		  html {background-color: #eee; font-family: sans;}
		  body {background-color: #fff; border: 1px solid #ddd;
				padding: 15px; margin: 15px;}
		  pre {background-color: #eee; border: 1px solid #ddd; padding: 5px;}
		</style>
	</head>
	<body>
		<h1>IA Lent calendars</h1>
		<ul>
			% for g in groups:
				% name = "{}-{}".format(g[0], g[-1])
				<li><a href="webcal://efw27.user.srcf.net:8080/IA/lent/{{name}}">{{name}}</a></li>
			% end
		</ul>
		<a href="https://github.com/eric-wieser/engineering-calendar"><img style="position: absolute; top: 0; right: 0; border: 0;" src="https://s3.amazonaws.com/github/ribbons/forkme_right_orange_ff7600.png" alt="Fork me on GitHub"></a>
	</body>
</html>