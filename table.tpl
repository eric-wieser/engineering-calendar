% from bottle import request
% import re
<%
def color(code):
	codes = sorted(tt.course.labs.keys())
	i = 360 * codes.index(code) // len(codes)
	return "hsla({}, 75%, 50%, 0.1)".format(i)
end

def single_color(code1):
	c1 = color(code1)
	return """repeating-linear-gradient(45deg,
		{0},
		{0} 11.31px)
	""".format(c1)
end

def striped_color(code1, code2):
	c1 = color(code1)
	c2 = color(code2)
	return """repeating-linear-gradient(45deg,
		{0},
		{0} 11.31px,
		{1} 11.31px,
		{1} 22.62px)
	""".format(c1, c2)
end
%>
<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
<html>
	<head>
		<link rel="icon" type="image/png" href="http://cdn.dustball.com/calendar.png">
		<title>{{term.title()}} calendars</title>
		<link href="//maxcdn.bootstrapcdn.com/bootstrap/3.3.2/css/bootstrap.min.css" rel="stylesheet">
		<script src="https://code.jquery.com/jquery-2.1.3.min.js"></script>
		<style>
			th, td {
				vertical-align: middle !important;
				text-align: center;
			}
			tt.key {
				display: block;
				width: 25px;
				height: 25px;
				line-height: 25px;
				float: left;
				margin-left: -40px;
				text-align: center;
				margin-top: -3px;
			}
			.table-condensed>*>tr>td,
			.table-condensed>*>tr>th  {
				padding: 2px !important;
			}
			td.active, th.active{
				background-color: #f5f5f5;
			}
			table {
				min-width: {{ 25 * (len(tt.dates) + 2) }}px !important;
				max-width: auto !important;
			}
			/* */
		</style>
	</head>
	<body>
		% seen_labs = set()
		<div class="container">
			<h1>Part {{part.upper()}}, {{term.title()}} lab calendars</h1>
			<p>Group names in the left column link to the web calendars</p>
			<div class="table-responsive">
				<table class="table table-bordered table-condensed small" style="table-layout: fixed">
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
								<th>{{ '{:%a}'.format(d) }}<br />{{ '{:%d}'.format(d) }}</th>
							% end
						</tr>
					</thead>
					<tbody>
						% skip = set()
						% urlparts = request.urlparts._replace(scheme='webcal')
						% for gi, group in enumerate(tt.groups):
							% labs = tt.labs_for(group)
							<tr>
								<th colspan="2" scope="row" data-group="{{ group }}">
									% url = urlparts._replace(path=urlparts.path + '/{}.ics'.format(group)).geturl()
									<a href="{{ url }}">{{group}}</a>
								</th>
								% for d in tt.dates:
									% if (group, d) in skip:
										% continue
									% end
									% ls = labs[d]

									% seen_labs |= set(ls)

									<%
									# iterate over adjacent entries which match vertically
									this_groups = [group]
									for g in tt.groups[gi+1:]:
										if tt.labs_for(g)[d] == ls and ls:
											this_groups.append(g)
											skip.add((g, d))
										else:
											break
										end
									end
									nrows = len(this_groups)
									%>

									% if len(ls) == 0:
										<td data-group="{{ group }}"></td>
									% elif len(ls) == 1:
										% l = ls[0];


										<td rowspan="{{nrows}}"
										    data-group="{{ ','.join(this_groups) }}"
										    title="{{l.name}}&NewLine;{{l.location}}"
										    style="background-image: {{ single_color(l.code) }}">
											<tt>{{ l.code }}</tt>
										</td>
									% elif len(labs[d]) == 2:
										% l1, l2 = ls;
										<td rowspan="{{nrows}}"
										    data-group="{{ ','.join(this_groups) }}"
										    title="{{l1.name}}&NewLine;{{l1.location}}&NewLine;&NewLine;{{l2.name}}&NewLine;{{l2.location}}"
										    style="background-image: {{ striped_color(l1.code, l2.code) }}">
											<tt>{{ l1.code }}<br />{{l2.code}}</tt>
										</td>
									% else:
										<td rowspan="{{nrows}}" class="small">
											{{ ','.join(l.code for l in labs[d]) }}
										</td>
									% end
								% end
							</tr>
						% end
					</tbody>
					<thead>
						<tr>
							<th colspan="2"></th>
							% for d in tt.dates:
								<th>{{ '{:%a}'.format(d) }}<br />{{ '{:%d}'.format(d) }}</th>
							% end
						</tr>
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
					</thead>
				</table>
			</div>
			<div>
				<h2>Key</h2>
				<%
				import itertools
				labs = sorted(seen_labs, key=lambda l: (l.group, l.code))

				grouped = [(group, list(l)) for group, l in itertools.groupby(labs, key=lambda l: l.group)]
				grouped = sorted(grouped, key=lambda (g, l): len(l), reverse=True)
				%>
				<div class="row">
					% for group, labs in grouped:
						<div class="col-md-4 col-sm-6">
							<h3>
								% m = re.match(r'^([A-Z]{2,}(?: [A-Z]+)*)(.*)$', group)
								% if m:
									{{ m.group(1).title() }}
									<small>{{ m.group(2) }}</small>
								% else:
									{{ group }}
								% end
							</h3>

							% for lab in labs:
								<p style="padding-left: 40px">
									<tt class="key" style="background-color: {{color(lab.code) }}">{{ lab.code }}</tt>
									{{lab.name}}<br />
									<small class="text-muted">{{ lab.location }}</small>
								</p>
							% end
						</div>
					% end
				</div>
			</div>
		</div>
		<a href="https://github.com/eric-wieser/engineering-calendar"><img style="position: absolute; top: 0; right: 0; border: 0;" src="https://s3.amazonaws.com/github/ribbons/forkme_right_orange_ff7600.png" alt="Fork me on GitHub"></a>
		<script>
		$(function() {
			var by_group = {};
			var $a = $('[data-group]');
			$a.each(function() {
				var $elem = $(this);
				var dgroups = $elem.data('group').split(',');
				$.each(dgroups, function() {
					if(!by_group[this])
						by_group[this] = $elem;
					else
						by_group[this] = by_group[this].add($elem);
				});
			});
			$a.hover(function() {
				var dgroups = $(this).data('group').split(',');
				$.each(dgroups, function() {
					by_group[this].addClass('active');
				});
			}, function() {
				var dgroups = $(this).data('group').split(',');
				$.each(dgroups, function() {
					by_group[this].removeClass('active');
				});
			});
		});
		</script>
	</body>
</html>