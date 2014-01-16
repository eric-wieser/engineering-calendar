from labs import TimeSlot, LabInfo, parse_row
from datetime import date

start_date = date(2014, 1, 16)
lab_info = [
	LabInfo('D',
		'Drawing',
		'LT1',
		[TimeSlot.morning, TimeSlot.afternoon]),

	LabInfo('C',
		'Computing',
		'LR4',
		[TimeSlot.morning, TimeSlot.afternoon_short]),

	LabInfo('IE',
		'Integrated Electrical Project',
		'IEP',
		[TimeSlot.morning, TimeSlot.afternoon]),

	LabInfo('1',
		'Kinematics of plane mechanism',
		'DPO',
		[TimeSlot.morning]),

	LabInfo('2',
		'Gas engine',
		'Inglis Thermodynamics Lab',
		[TimeSlot.morning]),

	LabInfo('3',
		'Elastic beams',
		'Inglis Structures Lab',
		[TimeSlot.morning]),

	LabInfo('4',
		'Plasticity and fracture',
		'Inglis Materials Lab',
		[TimeSlot.morning]),

	LabInfo('7',
		'Vibration modes',
		'Baker S. Wing Mechanics Lab',
		[TimeSlot.morning_short]),

	LabInfo('8',
		'Energy and power',
		'Baker S. Wing Mechanics Lab',
		[TimeSlot.morning_short]),

	LabInfo('9',
		'Turbocharger',
		'Inglis Thermodynamics Lab',
		[TimeSlot.morning_short]),

	LabInfo('10',
		'Inviscid fluid flow',
		'Inglis Hydraulics Lab',
		[TimeSlot.morning_short]),

	LabInfo('11',
		'Non-destructive testing',
		'Inglis Materials Lab',
		[TimeSlot.morning_short]),

	LabInfo('12',
		'Iron-cored transformer',
		'EIETL',
		[TimeSlot.morning_short]),

	LabInfo('13',
		'AC Power',
		'EIETL',
		[TimeSlot.morning_short]),

	LabInfo('14',
		'Combinational logic',
		'EIETL',
		[TimeSlot.morning_short]),

	LabInfo('15',
		'Sequential logic, memory & counting',
		'EIETL',
		[TimeSlot.morning_short]),


	LabInfo('S',
		'Structural Design',
		'LR3A',
		[TimeSlot.morning]),

	LabInfo('SA',
		'Structural Design (pm session)',
		'LR3A',
		[TimeSlot.afternoon_short]),

	LabInfo('T',
		'Structural Design Test',
		'Inglis Structures Lab',
		[TimeSlot.morning]),


	LabInfo('SW',
		'Structural Design Workshop',
		'Inglis Instrument Shop',
		[TimeSlot.afternoon_long])
]

timetable = {
	#                     +-----------+-----------+-----------+-----------+-----------+-----------+-----------+-----------+
	#                     +     1     +     2     +     3     +     4     +     5     +     6     +     7     +     8     +
	#                     +-----------+-----------+-----------+-----------+-----------+-----------+-----------+-----------+
	#                     |Th  F  M Tu|Th  F  M Tu|Th  F  M Tu|Th  F  M Tu|Th  F  M Tu|Th  F  M Tu|Th  F  M Tu|Th  F  M Tu|
	#                     |16 17 20 21|23 24 27 28|30 31  3  4| 6  7 10 11|13 14 17 18|20 21 24 25|27 28  3  4| 6  7 10 11|
	#                     +-----------+-----------+-----------+-----------+-----------+-----------+-----------+-----------+
	'1-3':     parse_row("|  ,  , 4,  | D,  ,  , C| 8, 9,11, C| D, 3,  ,12|IE,IE,IE,IE| D,  , 1,15| 2,10,  ,13| D, 7,  ,  |"),
	'4-6':     parse_row("|  ,  , 4,  | D,  ,  , C| 8, 9,11, C| D, 3,  ,12|IE,IE,IE,IE| D,  , 1,15| 2,10,  ,13| D, 7,  ,  |"),
	'7-9':     parse_row("|  ,  ,  , 8| D,  ,  , C|  , 4,  , C| D, 3,11,  |IE,IE,IE,IE| D, 9,  ,10| 7, 1,13,15| D, 2,12,  |"),
	'10-12':   parse_row("|  ,  ,  , 8| D,  ,  , C|  , 4,  , C| D, 3,11,  |IE,IE,IE,IE| D, 9,  ,10| 7, 1,13,15| D, 2,12,  |"),
	'13-15':   parse_row("|  ,  , 9,  | D,10,  , C| 4, 8,14, C| D, 3,13,  |IE,IE,IE,IE| D,11,  , 2|12,  ,15,  | D, 1,  ,  |"),

	'16-18':   parse_row("|  ,  , 9, T| D,10,  , C| 4, 8,14, C| D,  ,13, 3|IE,IE,IE,IE| D,11,  , 2|12,  ,15,  | D, 1,  ,  |"),
	'19-21':   parse_row("|  ,  ,  , T| D, 8,  , C|14,  , 4, C| D,10,  , 3|IE,IE,IE,IE| D,  ,13,12| 1,15,  , 2| D, 9,11,  |"),
	'22-24':   parse_row("|  ,  ,  , T| D, 8,  , C|14,  , 4, C| D,10,  , 3|IE,IE,IE,IE| D,  ,13,12| 1,15,  , 2| D, 9,11,  |"),
	'25-27':   parse_row("|  ,  ,  , T| D,  , 4, C|15,  ,  , C| D, 8,  , 3|IE,IE,IE,IE| D,12,10, 1|11,14, 2,  | D,13,  ,9 |"),
	'28-30':   parse_row("|  ,  ,  , T| D,  , 4, C|15,  ,  , C| D, 8,  , 3|IE,IE,IE,IE| D,12,10, 1|11,14, 2,  | D,13,  ,9 |"),

	'31-33':   parse_row("| D,  ,  ,  [  , 4, 8,10] D,14,  , T|IE,IE,IE,IE| D,12, 9, C| 1, 3,  , C| D,  ,  ,11| 2,  ,15,13|"),
	'34-36':   parse_row("| D,  ,  ,  [  , 4, 8,10] D,14,  , T|IE,IE,IE,IE| D,12, 9, C| 1, 3,  , C| D,  ,  ,11| 2,  ,15,13|"),
	'37-39':   parse_row("| D,  ,10,  [ 4,  ,  ,15] D,  , 8, T|IE,IE,IE,IE| D,  , 1, C|11, 3, 9, C| D, 2,  ,12|13,  ,  ,14|"),
	'40-42':   parse_row("| D,  ,10,  [ 4,  ,  ,15] D,  , 8, T|IE,IE,IE,IE| D,  , 1, C|11, 3, 9, C| D, 2,  ,12|13,  ,  ,14|"),
	'43-45':   parse_row("| D, 1, 8,  [  ,  ,15,  ] D,  ,  , T|IE,IE,IE,IE| D, 4,  , C|  , 3, 2, C| D, 9,12,14|  ,10,13,11|"),

	'46-48':   parse_row("[  , 1, 8,  ] D,  ,15, T|IE,IE,IE,IE| D,  , C,  | 3, 4, C,  | D,  , 2,  |  , 9,12,14| D,10,13,11|"),
	'49-51':   parse_row("[  ,  , 2,  ] D,  ,10, T|IE,IE,IE,IE| D, 1, C, 8| 3,  , C, 4| D,14,  ,11|13,12,  , 9| D,  ,  ,15|"),
	'52-54':   parse_row("[  ,  , 2,  ] D,  ,10, T|IE,IE,IE,IE| D, 1, C, 8| 3,  , C, 4| D,14,  ,11|13,12,  , 9| D,  ,  ,15|"),
	'55-57':   parse_row("[ 8, 2,  ,  ] D,  ,  , T|IE,IE,IE,IE| D,13, C,  | 3, 9, C,11| D, 1,  ,14| 4,  ,  ,  | D,15,10,  |"),
	'58-60':   parse_row("[ 8, 2,  ,  ] D,  ,  , T|IE,IE,IE,IE| D,13, C,  | 3, 9, C,11| D, 1,  ,14| 4,  ,  ,  | D,15,10,  |"),

	'61-63':   parse_row("| D, 8,  ,  |  ,  ,  ,14| D, 2,10,  |  , 4, C,  | D, 3, C,13|IE,IE,IE,IE| D,11, 9, 1|15,  ,  ,  |"),
	'64-66':   parse_row("| D, 8,  ,  |  ,  ,  ,14| D, 2,10,  |  , 4, C,  | D, 3, C,13|IE,IE,IE,IE| D,11, 9, 1|15,  ,  ,  |"),
	'67-69':   parse_row("| D,10,  ,  |  ,  , 2,  | D, 1,15, 4| 8, 9, C,  | D, 3, C,  |IE,IE,IE,IE| D,13,  ,  |11,14,  ,  |"),
	'70-72':   parse_row("| D,10,  ,  |  ,  , 2,  | D, 1,15, 4| 8, 9, C,  | D, 3, C,  |IE,IE,IE,IE| D,13,  ,  |11,14,  ,  |"),
	'73-75':   parse_row("| D,  ,  ,  |  , 9,14, 2| D,15,  , 8|13,11, C,  | D, 3, C, 1|IE,IE,IE,IE| D, 4,10,  |  ,  ,  ,  |"),

	'76-78':   parse_row("| D,  ,  ,  |  , 9,14, 2| D,15, 3, 8|13,11, C,  | D,  , C, 1|  ,  ,  ,  | D, 4,10,  |IE,IE,IE,IE|"),
	'79-81':   parse_row("| D, 4,  ,  | 8, 2,  ,  | D,  , 3,13|11,  , C, 9| D, 1, C,10|  ,15,14,  | D,  ,  ,  |IE,IE,IE,IE|"),
	'82-84':   parse_row("| D, 4,  ,  | 8, 2,  ,  | D,  , 3,13|11,  , C, 9| D, 1, C,10|  ,15,14,  | D,  ,  ,  |IE,IE,IE,IE|"),
	'85-87':   parse_row("| D,  ,  ,  | 2,  ,  , 4| D,  , 3,  |10,  , C, 1| D,  , C,  |15,13,  , 9| D, 8,  ,  |IE,IE,IE,IE|"),
	'88-90':   parse_row("| D,  ,  ,  | 2,  ,  , 4| D,  , 3,  |10,  , C, 1| D,  , C,  |15,13,  , 9| D, 8,  ,  |IE,IE,IE,IE|"),

	'91-93':   parse_row("| 1,  ,  ,10|  , D, S, C| 2, S, S, C| 4, D, S,  [13,  ,  ,  ] 3, D,15, T|IE,IE,IE,IE| 9, D, 8,  |"),
	'94-96':   parse_row("| 1,  ,  ,10|  , D, S, C| 2, S, S, C| 4, D, S,  [13,  ,  ,  ] 3, D,15, T|IE,IE,IE,IE| 9, D, 8,  |"),
	'97-99':   parse_row("| 2, 9,  ,  |10, D, S, C| 1, S, S, C|  , D, S, 4[  , 8,  , 7] 3, D,  , T|IE,IE,IE,IE|  , D,  ,  |"),
	'100-102': parse_row("| 2, 9,  ,  |10, D, S, C| 1, S, S, C|  , D, S, 4[  , 8,  , 7] 3, D,  , T|IE,IE,IE,IE|  , D,  ,  |"),
	'103-105': parse_row("| 9,  ,  , 2|  , D, S, C|  , S, S, C|  , D, S,10[  ,  , 8,  ] 3, D, 4, T|IE,IE,IE,IE| 1, D, 7,  |"),

	'106-108': parse_row("| 9,  ,  , 2|  , D,  ,  |IE,IE,IE,IE| S, D, 3,10| S, S, 8, C| S, D, 4, C[  ,  ,  ,  ] 1, D, 7, T|"),
	'109-111': parse_row("|10,  ,  , 9|  , D, 1,  |IE,IE,IE,IE| S, D, 3,  | S, S,  , C| S, D,  , C[ 8,  , 7, 4]  , D,  , T|"),
	'112-114': parse_row("|10,  ,  , 9|  , D, 1,  |IE,IE,IE,IE| S, D, 3,  | S, S,  , C| S, D,  , C[ 8,  , 7, 4]  , D,  , T|"),
	'115-117': parse_row("| 4,  ,  ,  |  , D, 9,  |IE,IE,IE,IE| S, D, 3,  | S, S,  , C| S, D, 8, C[  , 7, 1,  ]10, D,  , T|"),
	'118-120': parse_row("| 4,  ,  ,  |  , D, 9,  |IE,IE,IE,IE| S, D, 3,  | S, S,  , C| S, D, 8, C[  , 7, 1,  ]10, D,  , T|"),

	'121-123': parse_row("| S,  , S,  |SA, D,SA,  [  ,10, 1, 9]  , D, 4, T| 8, 7, 3, C|  , D,  , C|IE,IE,IE,IE|  , D,  ,  |"),
	'124-126': parse_row("| S,  , S,  |SA, D,SA,  [  ,10, 1, 9]  , D, 4, T| 8, 7, 3, C|  , D,  , C|IE,IE,IE,IE|  , D,  ,  |"),
	'127-129': parse_row("| S,  , S,  |SA, D,SA,  [  ,  , 9, 1]  , D,  , T| 4,10, 3, C|  , D, 7, C|IE,IE,IE,IE|  , D,  , 8|"),
	'130-132': parse_row("| S,  , S,  |SA, D,SA,  [  ,  , 9, 1]  , D,  , T| 4,10, 3, C|  , D, 7, C|IE,IE,IE,IE|  , D,  , 8|"),
	'133-135': parse_row("| S,  , S,  |SA, D,SA,  [  ,  ,  ,  ] 1, D, 8, T| 7,  , 3, C|  , D,  , C|IE,IE,IE,IE| 4, D, 9,10|"),

	'136-138': parse_row("|  , D,  , S| S,  , C, S| S, D, C, 3[ 1,  , 8,  ] 7, D,  , T|IE,IE,IE,IE|  , D,  ,  | 4,  , 9,10|"),
	'139-141': parse_row("|  , D,  , S| S,  , C, S| S, D, C, 3[ 9,  ,10,  ] 1, D, 4, T|IE,IE,IE,IE|  , D, 8, 7|14,12,  ,  |"),
	'142-144': parse_row("|  , D,  , S| S,  , C, S| S, D, C, 3[ 9,  ,10,  ] 1, D, 4, T|IE,IE,IE,IE|  , D, 8, 7|14,12,  ,  |"),
	'145-147': parse_row("|  , D,  , S| S,  , C, S| S, D, C, 3[  ,  , 1,  ]  , D,10, T|IE,IE,IE,IE| 9, D,  , 8|12, 4,14, 7|"),
	'148-150': parse_row("|  , D,  , S| S,  , C, S| S, D, C, 3[  ,  , 1,  ]  , D,10, T|IE,IE,IE,IE| 9, D,  , 8|12, 4,14, 7|"),

	'151-153': parse_row("|  , D,  , 1|  ,  , C,  |  , D, C, S| 3, S, 9, S|  , D,12, S[ 4, 7,  , 8]10, D,14, T|IE,IE,IE,IE|"),
	'154-156': parse_row("|  , D,  , 1|  ,  , C,  |  , D, C, S| 3, S, 9, S|  , D,12, S[ 4, 7,  , 8]10, D,14, T|IE,IE,IE,IE|"),
	'157-159': parse_row("|  , D, 1,  |  ,  , C, 8|  , D, C, S| 3, S,  , S|10, D, 7, S[ 9,  ,12,  ]14, D, 4, T|IE,IE,IE,IE|"),
	'160-162': parse_row("|  , D, 1,  |  ,  , C, 8|  , D, C, S| 3, S,  , S|10, D, 7, S[ 9,  ,12,  ]14, D, 4, T|IE,IE,IE,IE|"),
	'163-165': parse_row("|  , D,  , 4| 9,  , C, 1|10, D, C, S| 3, S,  , S|12, D,  , S[  , 8,  , 7]  , D,  , T|IE,IE,IE,IE|"),

	'166-168': parse_row("|  , D,  , 4| 9,  , C, 1|10, D, C,  |IE,IE,IE,IE|12, D, S, 3|  , 8, S, 7| S, D, S,  [  ,  ,  ,  ]"),
	'169-171': parse_row("|  , D,  ,  | 1,  , C, 9|  , D, C,  |IE,IE,IE,IE|  , D, S, 3| 7, 4, S,  | S, D, S,10[ 8,11,  ,12]"),
	'172-174': parse_row("|  , D,  ,  | 1,  , C, 9|  , D, C,  |IE,IE,IE,IE|  , D, S, 3| 7, 4, S,  | S, D, S,10[ 8,11,  ,12]"),
	'175-177': parse_row("|  , D,  ,  |  , 1, C,  | 9, D, C,10|IE,IE,IE,IE|11, D, S, 3|12,  , S, 4| S, D, S,  [ 7, 8,  ,  ]"),
	'178-180': parse_row("|  , D,  ,  |  , 1, C,  | 9, D, C,10|IE,IE,IE,IE|11, D, S, 3|12,  , S, 4| S, D, S,  [ 7, 8,  ,  ]")
}
