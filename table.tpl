% from bottle import request
% import re
<%
def natural_key(x):
	x = re.split(r'(\d+)', x)
	x[1::2] = map(int, x[1::2])
	return x
end

def color(code, alpha=0.1):
	codes = sorted(tt.course.labs.keys(), key=natural_key)
	i = 360 * codes.index(code) // len(codes)
	return "hsla({}, 100%, 50%, {})".format(i, alpha)
end

def stripes(codes, alpha=0.1):
	import math
	colors = [color(c, alpha) for c in codes]
	step = 22 / math.sqrt(2)

	return "repeating-linear-gradient(45deg, {stops})".format(
		stops=', '.join(
			'{c} {pos1:.2f}px, {c} {pos2:.2f}px'.format(
				c=c, pos1=i*step, pos2=(i + 1)*step
			) for i, c in enumerate(colors)
		)
	)
end

def stripe_class(codes):
	cls = 'lab-colored_'+'-'.join(codes)
	stripe_class.data[cls] = codes
	return cls
end
stripe_class.data = {}
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
			<div class="row">
				<div class="col-md-6">
					<p>The table below should match the one issued to you by the department. Group names in the left column link to the web calendars</p>
					<p>If you spot a mistake, please report it to <code>efw27</code>. I continue to claim no responsibility for missed labs due to false information.</p>
				</div>
				<div class="col-md-6">
					<p>Known to work with google calendar, assumed to work with iCalendar and live calendar.</p>
					<p>If you're lucky, clicking on the links should open the calendars in your default program. If you're not, copy the url of your group link, and follow online instructions for subscribing to an "ICS" or "iCal" web calendar.</p>
				</div>
			</div>
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
							% first = tt.dates[0]
							% last_w = 0
							% n = 0
							% for d in tt.dates:
								% w = (d - first).days // 7
								% if w != last_w:
									<th class="we" colspan="{{n}}">{{ last_w + 1 }}</th>
									% last_w = w
									% n = 1
								% else:
									% n += 1
								% end
							% end
							<th class="we" colspan="{{n}}">{{ last_w + 1 }}</th>
						</tr>
						<tr>
							<th colspan="2"></th>
							% for d in tt.dates:
								<th title="{{d.isoformat()}}">{{ '{:%a}'.format(d) }}<br />{{ '{:%d}'.format(d) }}</th>
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
									<a href="{{ url }}" style="white-space: nowrap;">{{group}}</a>
								</th>
								% for d in tt.dates:
									% if (group, d) in skip:
										% continue
									% end
									% ls = labs[d]
									% for l in ls:
										% try:
											% l.times_on(d)
										% except e:
											% raise ValueError(e, l)
										% end
									% end

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
										    class="{{ stripe_class([l.code]) }}">
											<tt>{{ l.code }}</tt>
										</td>
									% elif len(labs[d]) == 2:
										% l1, l2 = ls;
										<td rowspan="{{nrows}}"
										    data-group="{{ ','.join(this_groups) }}"
										    title="{{l1.name}}&NewLine;{{l1.location}}&NewLine;&NewLine;{{l2.name}}&NewLine;{{l2.location}}"
										    class="{{ stripe_class([l1.code, l2.code]) }}">
											<tt>
												% if nrows > 1:
													{{ l1.code }}<br />{{l2.code}}
												% else:
													{{ l1.code }}&middot;{{l2.code}}
												% end
											</tt>
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
							% first = tt.dates[0]
							% last_w = 0
							% n = 0
							% for d in tt.dates:
								% w = (d - first).days // 7
								% if w != last_w:
									<th class="we" colspan="{{n}}">{{ last_w + 1 }}</th>
									% last_w = w
									% n = 1
								% else:
									% n += 1
								% end
							% end
							<th class="we" colspan="{{n}}">{{ last_w + 1 }}</th>
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
				labs = sorted(seen_labs, key=lambda l: (l.group, natural_key(l.code)))

				grouped = [(group, list(l)) for group, l in itertools.groupby(labs, key=lambda l: l.group)]
				grouped = sorted(grouped, key=lambda i: len(i[1]), reverse=True)
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
									<tt class="key" style="background-color: {{color(lab.code, 0.3) }}">{{ lab.code }}</tt>
									% if lab.link:
										<a target="_blank" href="{{ lab.link }}">{{ lab.name }}</a>
									% else:
										{{lab.name}}
									% end
									<br />
									<small class="text-muted">{{ lab.location }}</small>
								</p>
							% end
						</div>
					% end
				</div>
			</div>
		</div>
		<a href="https://github.com/eric-wieser/engineering-calendar"><img style="position: absolute; top: 0; right: 0; border: 0;" src="https://s3.amazonaws.com/github/ribbons/forkme_right_orange_ff7600.png" alt="Fork me on GitHub"></a>
		<style>
			% for cls, codes in stripe_class.data.items():
				.{{cls}} { background-image: {{ stripes(codes) }}; }
				.{{cls}}.active { background-image: {{ stripes(codes, 0.3) }}; }
			% end
		</style>
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
</html
