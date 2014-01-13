engineering-calendar
====================

ical mangler for the Cambridge engineering course

Takes the IA calendar distributed by the engineering department, and mixes in your lab/coursework schedules


contributing
------------

To add your lab group, take the pdf [here](http://teaching.eng.cam.ac.uk/download/file/84), and write out your row, putting `,` between each column, `|` between each week, and `[]` around the structural design week. For instance, for lab groups 178-180, the result is:

    | ,D, , | ,1,C, |9,D,C,10|IE,IE,IE,IE|11,D,S,3|12, ,S,4|S,D,S, [7,8, , ]
    
Add that to the bottom of [`terms/lent.py`](https://github.com/eric-wieser/engineering-calendar/blob/master/terms/lent.py) and save the file, and I'll put it live on the server. Or just email it to me and tell me your lab group

To access a calendar, add a url like `http://efw27.user.srcf.net:8080/179-180` to your calendar program of choice
