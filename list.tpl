<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
<html>
	<head>
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
				<li><a href="webcal://efw27.user.srcf.net:8080/IA/lent/{{g}}">{{g}}</a></li>
			% end
		</ul>
	</body>
</html>