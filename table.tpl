% from bottle import request
<%
def color(code):
	codes = sorted(tt.course.labs.keys())
	i = 360 * codes.index(code) // len(codes)
	return "hsla({}, 100%, 75%, 1)".format(i)
end
%>
<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
<html>
	<head>
		<link rel="icon" type="image/png" href="http://cdn.dustball.com/calendar.png">
		<title>{{term.title()}} calendars</title>
		<link href="//maxcdn.bootstrapcdn.com/bootstrap/3.3.2/css/bootstrap.min.css" rel="stylesheet">
	</head>
	<body>
		<div class="container">
			<h1>Part {{part.upper()}}, {{term.title()}} lab calendars</h1>
			<table class="table table-hover table-bordered table-condensed small" style="table-layout: fixed">
				<thead>
					<tr>
						<th colspan="2"></th>
						% last = None
						% n = 0
						% for d in tt.dates:
							% if not last:
								% last = d
								% n = 1
							% elif d.month != last.month:
								<th class="mo" colspan="{{n}}">{{ '{:%B}'.format(last) }}</th>
								% last = d
								% n = 1
							% else:
								% n += 1
							% end
						% end
						<th class="mo" colspan="{{n}}">{{ '{:%B}'.format(last) }}</th>
					</tr>
					<tr>
						<th colspan="2"></th>
						% for d in tt.dates:
							<th>{{ '{:%d}'.format(d) }}</th>
						% end
					</tr>
					<tr>
						<th colspan="2"></th>
						% for d in tt.dates:
							<th>{{ '{:%a}'.format(d) }}</th>
						% end
					</tr>
				</thead>
				<tbody>
					% for group in tt.groups:
						% labs = tt.labs_for(group)
						<tr>
							<th colspan="2">{{group}}</th>
							% for d in tt.dates:
								% if len(labs[d]) == 1:
									% l = labs[d][0];
									<td class="small" style="background-color: {{ color(l.code) }}">
										{{ l.code }}
									</td>
								% else:
									<td class="small">
										{{ ','.join(l.code for l in labs[d]) }}
									</td>
								% end
							% end
						</tr>
					% end
				</tbody>
			</table>
		</div>
		<a href="https://github.com/eric-wieser/engineering-calendar"><img style="position: absolute; top: 0; right: 0; border: 0;" src="https://s3.amazonaws.com/github/ribbons/forkme_right_orange_ff7600.png" alt="Fork me on GitHub"></a>
	</body>
</html>