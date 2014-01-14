engineering-calendar
====================

Takes the IA calendar distributed by the engineering department, and mixes in your lab/coursework schedules

Add the calendar URL of `http://efw27.user.srcf.net:8080/IA/lent/[lab group range from table]` (such as `http://efw27.user.srcf.net:8080/IA/lent/178-180`) to your program of choice

Who does it work for?
---------------------
* lab groups 169-171
* lab groups 172-174
* lab groups 175-177
* lab groups 178-180

I'm not on that list!
---------------------

Before you can use it, someone needs to copy out your timetable row from [here](http://teaching.eng.cam.ac.uk/download/file/84). For instance, for lab groups 178-180, this:

![](clipping.png)

becomes:

    timetable['178-180'] = parse_row("| ,D, , | ,1,C, |9,D,C,10|IE,IE,IE,IE|11,D,S,3|12, ,S,4|S,D,S, [7,8, , ]")
    
Where the `|` are borders between weeks, and the `[` and `]` show the structural design project

Then either:

* **You know how to use github** - Add that to the bottom of [`terms/lent.py`](https://github.com/eric-wieser/engineering-calendar/blob/master/terms/lent.py), and submit a pull request
* **What?** - send me that short piece of text in an email/facebook message, and I'll update the calendar for you.
