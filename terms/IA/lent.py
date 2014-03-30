from datetime import date

from ..IA import lab_info
from timetable import Timetable

start_date=date(2014, 1, 16)

timetable = Timetable({
	#           +-----------+-----------+-----------+-----------+-----------+-----------+-----------+-----------+
	#           +     1     +     2     +     3     +     4     +     5     +     6     +     7     +     8     +
	#           +-----------+-----------+-----------+-----------+-----------+-----------+-----------+-----------+
	#           |Th  F  M Tu|Th  F  M Tu|Th  F  M Tu|Th  F  M Tu|Th  F  M Tu|Th  F  M Tu|Th  F  M Tu|Th  F  M Tu|
	#           |16 17 20 21|23 24 27 28|30 31  3  4| 6  7 10 11|13 14 17 18|20 21 24 25|27 28  3  4| 6  7 10 11|
	#           +-----------+-----------+-----------+-----------+-----------+-----------+-----------+-----------+
	'1-3':     "|  ,  , 4,  | D,  ,  , C| 8, 9,11, C| D, 3,  ,12|IE,IE,IE,IE| D,  , 1,15| 2,10,  ,13| D, 7,  ,  |",
	'4-6':     "|  ,  , 4,  | D,  ,  , C| 8, 9,11, C| D, 3,  ,12|IE,IE,IE,IE| D,  , 1,15| 2,10,  ,13| D, 7,  ,  |",
	'7-9':     "|  ,  ,  , 8| D,  ,  , C|  , 4,  , C| D, 3,11,  |IE,IE,IE,IE| D, 9,  ,10| 7, 1,13,15| D, 2,12,  |",
	'10-12':   "|  ,  ,  , 8| D,  ,  , C|  , 4,  , C| D, 3,11,  |IE,IE,IE,IE| D, 9,  ,10| 7, 1,13,15| D, 2,12,  |",
	'13-15':   "|  ,  , 9,  | D,10,  , C| 4, 8,14, C| D, 3,13,  |IE,IE,IE,IE| D,11,  , 2|12,  ,15,  | D, 1,  ,  |",

	'16-18':   "|  ,  , 9, T| D,10,  , C| 4, 8,14, C| D,  ,13, 3|IE,IE,IE,IE| D,11,  , 2|12,  ,15,  | D, 1,  ,  |",
	'19-21':   "|  ,  ,  , T| D, 8,  , C|14,  , 4, C| D,10,  , 3|IE,IE,IE,IE| D,  ,13,12| 1,15,  , 2| D, 9,11,  |",
	'22-24':   "|  ,  ,  , T| D, 8,  , C|14,  , 4, C| D,10,  , 3|IE,IE,IE,IE| D,  ,13,12| 1,15,  , 2| D, 9,11,  |",
	'25-27':   "|  ,  ,  , T| D,  , 4, C|15,  ,  , C| D, 8,  , 3|IE,IE,IE,IE| D,12,10, 1|11,14, 2,  | D,13,  ,9 |",
	'28-30':   "|  ,  ,  , T| D,  , 4, C|15,  ,  , C| D, 8,  , 3|IE,IE,IE,IE| D,12,10, 1|11,14, 2,  | D,13,  ,9 |",

	'31-33':   "| D,  ,  ,  [  , 4, 8,10] D,14,  , T|IE,IE,IE,IE| D,12, 9, C| 1, 3,  , C| D,  ,  ,11| 2,  ,15,13|",
	'34-36':   "| D,  ,  ,  [  , 4, 8,10] D,14,  , T|IE,IE,IE,IE| D,12, 9, C| 1, 3,  , C| D,  ,  ,11| 2,  ,15,13|",
	'37-39':   "| D,  ,10,  [ 4,  ,  ,15] D,  , 8, T|IE,IE,IE,IE| D,  , 1, C|11, 3, 9, C| D, 2,  ,12|13,  ,  ,14|",
	'40-42':   "| D,  ,10,  [ 4,  ,  ,15] D,  , 8, T|IE,IE,IE,IE| D,  , 1, C|11, 3, 9, C| D, 2,  ,12|13,  ,  ,14|",
	'43-45':   "| D, 1, 8,  [  ,  ,15,  ] D,  ,  , T|IE,IE,IE,IE| D, 4,  , C|  , 3, 2, C| D, 9,12,14|  ,10,13,11|",

	'46-48':   "[  , 1, 8,  ] D,  ,15, T|IE,IE,IE,IE| D,  , C,  | 3, 4, C,  | D,  , 2,  |  , 9,12,14| D,10,13,11|",
	'49-51':   "[  ,  , 2,  ] D,  ,10, T|IE,IE,IE,IE| D, 1, C, 8| 3,  , C, 4| D,14,  ,11|13,12,  , 9| D,  ,  ,15|",
	'52-54':   "[  ,  , 2,  ] D,  ,10, T|IE,IE,IE,IE| D, 1, C, 8| 3,  , C, 4| D,14,  ,11|13,12,  , 9| D,  ,  ,15|",
	'55-57':   "[ 8, 2,  ,  ] D,  ,  , T|IE,IE,IE,IE| D,13, C,  | 3, 9, C,11| D, 1,  ,14| 4,  ,  ,  | D,15,10,  |",
	'58-60':   "[ 8, 2,  ,  ] D,  ,  , T|IE,IE,IE,IE| D,13, C,  | 3, 9, C,11| D, 1,  ,14| 4,  ,  ,  | D,15,10,  |",

	'61-63':   "| D, 8,  ,  |  ,  ,  ,14| D, 2,10,  |  , 4, C,  | D, 3, C,13|IE,IE,IE,IE| D,11, 9, 1|15,  ,  ,  |",
	'64-66':   "| D, 8,  ,  |  ,  ,  ,14| D, 2,10,  |  , 4, C,  | D, 3, C,13|IE,IE,IE,IE| D,11, 9, 1|15,  ,  ,  |",
	'67-69':   "| D,10,  ,  |  ,  , 2,  | D, 1,15, 4| 8, 9, C,  | D, 3, C,  |IE,IE,IE,IE| D,13,  ,  |11,14,  ,  |",
	'70-72':   "| D,10,  ,  |  ,  , 2,  | D, 1,15, 4| 8, 9, C,  | D, 3, C,  |IE,IE,IE,IE| D,13,  ,  |11,14,  ,  |",
	'73-75':   "| D,  ,  ,  |  , 9,14, 2| D,15,  , 8|13,11, C,  | D, 3, C, 1|IE,IE,IE,IE| D, 4,10,  |  ,  ,  ,  |",

	'76-78':   "| D,  ,  ,  |  , 9,14, 2| D,15, 3, 8|13,11, C,  | D,  , C, 1|  ,  ,  ,  | D, 4,10,  |IE,IE,IE,IE|",
	'79-81':   "| D, 4,  ,  | 8, 2,  ,  | D,  , 3,13|11,  , C, 9| D, 1, C,10|  ,15,14,  | D,  ,  ,  |IE,IE,IE,IE|",
	'82-84':   "| D, 4,  ,  | 8, 2,  ,  | D,  , 3,13|11,  , C, 9| D, 1, C,10|  ,15,14,  | D,  ,  ,  |IE,IE,IE,IE|",
	'85-87':   "| D,  ,  ,  | 2,  ,  , 4| D,  , 3,  |10,  , C, 1| D,  , C,  |15,13,  , 9| D, 8,  ,  |IE,IE,IE,IE|",
	'88-90':   "| D,  ,  ,  | 2,  ,  , 4| D,  , 3,  |10,  , C, 1| D,  , C,  |15,13,  , 9| D, 8,  ,  |IE,IE,IE,IE|",

	'91-93':   "| 1,  ,  ,10|  , D, S, C| 2, S, S, C| 4, D, S,  [13,  ,  ,  ] 3, D,15, T|IE,IE,IE,IE| 9, D, 8,  |",
	'94-96':   "| 1,  ,  ,10|  , D, S, C| 2, S, S, C| 4, D, S,  [13,  ,  ,  ] 3, D,15, T|IE,IE,IE,IE| 9, D, 8,  |",
	'97-99':   "| 2, 9,  ,  |10, D, S, C| 1, S, S, C|  , D, S, 4[  , 8,  , 7] 3, D,  , T|IE,IE,IE,IE|  , D,  ,  |",
	'100-102': "| 2, 9,  ,  |10, D, S, C| 1, S, S, C|  , D, S, 4[  , 8,  , 7] 3, D,  , T|IE,IE,IE,IE|  , D,  ,  |",
	'103-105': "| 9,  ,  , 2|  , D, S, C|  , S, S, C|  , D, S,10[  ,  , 8,  ] 3, D, 4, T|IE,IE,IE,IE| 1, D, 7,  |",

	'106-108': "| 9,  ,  , 2|  , D,  ,  |IE,IE,IE,IE| S, D, 3,10| S, S, 8, C| S, D, 4, C[  ,  ,  ,  ] 1, D, 7, T|",
	'109-111': "|10,  ,  , 9|  , D, 1,  |IE,IE,IE,IE| S, D, 3,  | S, S,  , C| S, D,  , C[ 8,  , 7, 4]  , D,  , T|",
	'112-114': "|10,  ,  , 9|  , D, 1,  |IE,IE,IE,IE| S, D, 3,  | S, S,  , C| S, D,  , C[ 8,  , 7, 4]  , D,  , T|",
	'115-117': "| 4,  ,  ,  |  , D, 9,  |IE,IE,IE,IE| S, D, 3,  | S, S,  , C| S, D, 8, C[  , 7, 1,  ]10, D,  , T|",
	'118-120': "| 4,  ,  ,  |  , D, 9,  |IE,IE,IE,IE| S, D, 3,  | S, S,  , C| S, D, 8, C[  , 7, 1,  ]10, D,  , T|",

	'121-123': "| S,  , S,  |SA, D,SA,  [  ,10, 1, 9]  , D, 4, T| 8, 7, 3, C|  , D,  , C|IE,IE,IE,IE|  , D,  ,  |",
	'124-126': "| S,  , S,  |SA, D,SA,  [  ,10, 1, 9]  , D, 4, T| 8, 7, 3, C|  , D,  , C|IE,IE,IE,IE|  , D,  ,  |",
	'127-129': "| S,  , S,  |SA, D,SA,  [  ,  , 9, 1]  , D,  , T| 4,10, 3, C|  , D, 7, C|IE,IE,IE,IE|  , D,  , 8|",
	'130-132': "| S,  , S,  |SA, D,SA,  [  ,  , 9, 1]  , D,  , T| 4,10, 3, C|  , D, 7, C|IE,IE,IE,IE|  , D,  , 8|",
	'133-135': "| S,  , S,  |SA, D,SA,  [  ,  ,  ,  ] 1, D, 8, T| 7,  , 3, C|  , D,  , C|IE,IE,IE,IE| 4, D, 9,10|",

	'136-138': "|  , D,  , S| S,  , C, S| S, D, C, 3[ 1,  , 8,  ] 7, D,  , T|IE,IE,IE,IE|  , D,  ,  | 4,  , 9,10|",
	'139-141': "|  , D,  , S| S,  , C, S| S, D, C, 3[ 9,  ,10,  ] 1, D, 4, T|IE,IE,IE,IE|  , D, 8, 7|14,12,  ,  |",
	'142-144': "|  , D,  , S| S,  , C, S| S, D, C, 3[ 9,  ,10,  ] 1, D, 4, T|IE,IE,IE,IE|  , D, 8, 7|14,12,  ,  |",
	'145-147': "|  , D,  , S| S,  , C, S| S, D, C, 3[  ,  , 1,  ]  , D,10, T|IE,IE,IE,IE| 9, D,  , 8|12, 4,14, 7|",
	'148-150': "|  , D,  , S| S,  , C, S| S, D, C, 3[  ,  , 1,  ]  , D,10, T|IE,IE,IE,IE| 9, D,  , 8|12, 4,14, 7|",

	'151-153': "|  , D,  , 1|  ,  , C,  |  , D, C, S| 3, S, 9, S|  , D,12, S[ 4, 7,  , 8]10, D,14, T|IE,IE,IE,IE|",
	'154-156': "|  , D,  , 1|  ,  , C,  |  , D, C, S| 3, S, 9, S|  , D,12, S[ 4, 7,  , 8]10, D,14, T|IE,IE,IE,IE|",
	'157-159': "|  , D, 1,  |  ,  , C, 8|  , D, C, S| 3, S,  , S|10, D, 7, S[ 9,  ,12,  ]14, D, 4, T|IE,IE,IE,IE|",
	'160-162': "|  , D, 1,  |  ,  , C, 8|  , D, C, S| 3, S,  , S|10, D, 7, S[ 9,  ,12,  ]14, D, 4, T|IE,IE,IE,IE|",
	'163-165': "|  , D,  , 4| 9,  , C, 1|10, D, C, S| 3, S,  , S|12, D,  , S[  , 8,  , 7]  , D,  , T|IE,IE,IE,IE|",

	'166-168': "|  , D,  , 4| 9,  , C, 1|10, D, C,  |IE,IE,IE,IE|12, D, S, 3|  , 8, S, 7| S, D, S,  [  ,  ,  ,  ]",
	'169-171': "|  , D,  ,  | 1,  , C, 9|  , D, C,  |IE,IE,IE,IE|  , D, S, 3| 7, 4, S,  | S, D, S,10[ 8,11,  ,12]",
	'172-174': "|  , D,  ,  | 1,  , C, 9|  , D, C,  |IE,IE,IE,IE|  , D, S, 3| 7, 4, S,  | S, D, S,10[ 8,11,  ,12]",
	'175-177': "|  , D,  ,  |  , 1, C,  | 9, D, C,10|IE,IE,IE,IE|11, D, S, 3|12,  , S, 4| S, D, S,  [ 7, 8,  ,  ]",
	'178-180': "|  , D,  ,  |  , 1, C,  | 9, D, C,10|IE,IE,IE,IE|11, D, S, 3|12,  , S, 4| S, D, S,  [ 7, 8,  ,  ]"
})
