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
			)
			for i, c in enumerate(colors)
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
		<title>{{tt.term.title()}} calendars - new</title>
		<link href="//maxcdn.bootstrapcdn.com/bootstrap/3.3.2/css/bootstrap.min.css" rel="stylesheet">
		<script src="https://code.jquery.com/jquery-2.1.3.min.js"></script>
		<style>
			th, td {
				vertical-align: middle !important;
				text-align: center;
			}
			.lab_pad_small{
					padding-bottom: 2px;
					padding-top: 2px;
					margin-bottom: 0px;
					margin-top: 0px;
					float:left;
					width: 25%;

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
				/* padding: 2px !important;  */
			}
			td.active, th.active{
				background-color: #f5f5f5;
			}
			table {
				min-width: {{ 25 * (len(tt.dates) + 2) }}px !important;
				max-width: auto !important;
			}
			/* kludge to make these table printable on A4 (hopefully)*/
			@media print {
				a[href]:after {
				content: none !important;
				}
				h1{
					font-size: 200%;
					text-align: center;
				
				}
				.table-condensed>*>tr>th  {
					padding: 1px !important;
				}
				h1{
					font-size: 200%;
					text-align: center;

				}
				.footer{
					font-size:bold;
					font-size: 100%;
					border: solid thin;
				}
				table {
					width: 100% !important;
					margin: 0px;

				}
				.lab_pad_small{
					border: solid thin;
					border-width: 1px;
					margin-left: -1px;
					margin-top: -1px;
				}
				.table{
				margin-bottom: 0px;
				}
				.footer{
					font-size:bold;
					font-size: 100%;
					border: solid thin;
				}
				.no_print{
					display: none;
				}
				.container{
					width: 100%;
				}
				.day_name{
					/* font-size: 50%; */
				}
				th, td, tr {
					font-size: 80%;
					padding: 0px !important;
					margin: 0px !important;
				}
				tbody tr td{
					font-size: 140%;
				}
				tbody tr th{
					font-size: 110%;
				}
				h2 {
					font-size: 100%;
					margin: 0px;
				}
				h3 {
					font-size: 150%;
					margin: 0px ;
				}
				body {
					font-size: 80% !important;
				}
				table {
					min-width: 1px !important;
					max-width: auto !important;
				}

				tbody tr:nth-child(even){
					border-bottom: solid #000;
					border-width: 0 1px !important;
				}


			}
			@page {
				/*size: 21cm 29.7cm;*/
				margin: 1mm 1mm 1mm 1mm; /* change the margins as you want them to be. */
			}
		</style>
	</head>
	<body>
		% seen_labs = set()
		<div class="container">
			<h1>Part {{tt.course.part.upper()}}, {{tt.term.title()}} lab calendars {{ tt.course.year }} <small>(last modified {{ tt.course.last_mod }})</small></h1>
			<div class="no_print">
			<div class="row">
				<div class="col-md-6">
					<p>Group names in the left column link to the web calendars</p>
					<p>If you spot a mistake, please report it to the <code>teaching-office</code></p>
				</div>
				<div class="col-md-6">
					<p>Known to work with google calendar, assumed to work with iCalendar and live calendar.</p>
					<p>Clicking on the links should open the calendars in your default program. If you're not, copy the url of your group link, and follow online instructions for subscribing to an "ICS" or "iCal" web calendar.</p>
				</div>
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
								<th class="day_name" title="{{d.isoformat()}}">{{ '{:%a}'.format(d) }}<br />{{ '{:%d}'.format(d) }}</th>
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
										    class="{{ stripe_class([l.code]) }} code_{{l.code}}">
											<tt>{{ l.code }}</tt>
										</td>
									% elif len(labs[d]) == 2:
										% l1, l2 = ls;
										<td rowspan="{{nrows}}"
										    data-group="{{ ','.join(this_groups) }}"
										    title="{{l1.name}}&NewLine;{{l1.location}}&NewLine;&NewLine;{{l2.name}}&NewLine;{{l2.location}}"
										    class="{{ stripe_class([l1.code, l2.code]) }} code_{{l1.code}} code_{{l2.code}}">
											<tt>
												% if nrows > 1:
													{{ l1.code }}<br />{{l2.code}}
												% else:
													{{ l1.code }}&middot;{{l2.code}}
												% end
											</tt>
										</td>
									% else:
										<td rowspan="{{nrows}}" class="small {{ ' '.join("code_"+l.code for l in labs[d]) }}">
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
				<h2 class="no_print">Key</h2>
				<%
				import itertools
				labs = sorted(seen_labs, key=lambda l: (l.group, natural_key(l.code)))

				grouped = [(group, group!='Other', list(l) ) for group, l in itertools.groupby(labs, key=lambda l: l.group)]
				grouped = sorted(grouped, key=lambda i: (i[1], len(i[2])), reverse=True)
				%>
				<div class="row">
					% for group, isother, labs in grouped:
						<div class="col-md-12 col-sm-6 col-xs-12">
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
								<p style="padding-left: 40px" class="lab_pad_small">
									<tt class="key" style="background-color: {{color(lab.code, 0.3) }}">{{ lab.code }}</tt>
									<span class="key_text">
									% if lab.link:
										<a target="_blank" href="{{ lab.link }}">{{ lab.name }}</a>
									% else:
										{{lab.name}}
									% end
									</span>
									<br />
									<small class="text-muted">{{ lab.location }}</small>
								</p>
							% end
						</div>
					% end
				</div>
			</div>
			<div class="footer">
				<br class="no_print"/>
				Morning labs are timetabled in the main lecture timetable. <b> IA </b>: Mon &amp; Fri, 09.00-11.00; Tue &amp; Thu, 11:00-13:00. <b> IB </b>: Mon, 11:00-13:00; Tue, Wed &amp; Thu, 09.00-11.00.
				<br/>
				Afternoon labs start at 2pm. The end time may vary, consult the corresponding lab information.
				<br/>
				 Laboratory sessions begin five minutes past the hour. Latecomers will be penalised and may be excluded.
				<br/>
				file located at: {{ request.urlparts.geturl() }}
				<br class="no_print"/>
				<br class="no_print"/>
			</div>
		</div>
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
</html>
