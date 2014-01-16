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
	#                                 +-----------+-----------+-----------+-----------+-----------+-----------+-----------+-----------+
	#                                 +     1     +     2     +     3     +     4     +     5     +     6     +     7     +     8     +
	#                                 +-----------+-----------+-----------+-----------+-----------+-----------+-----------+-----------+
	#                                 |Th  F  M Tu|Th  F  M Tu|Th  F  M Tu|Th  F  M Tu|Th  F  M Tu|Th  F  M Tu|Th  F  M Tu|Th  F  M Tu|
	#                                 |16 17 20 21|23 24 27 28|30 31  3  4| 6  7 10 11|13 14 17 18|20 21 24 25|27 28  3  4| 6  7 10 11|
	#                                 +-----------+-----------+-----------+-----------+-----------+-----------+-----------+-----------+
	'115-117': parse_row("| 4,  ,  ,  |  , D, 9,  |IE,IE,IE,IE| S, D, 3,  | S, S,  , C| S, D, 8, C[  , 7, 1,  ]10, D,  , T|"),
	'118-120': parse_row("| 4,  ,  ,  |  , D, 9,  |IE,IE,IE,IE| S, D, 3,  | S, S,  , C| S, D, 8, C[  , 7, 1,  ]10, D,  , T|"),

	'169-171': parse_row("|  , D,  ,  | 1,  , C, 9| 9, D, C,  |IE,IE,IE,IE|  , D, S, 3| 7, 4, S,  | S, D, S,10[ 8,11,  ,12]"),
	'172-174': parse_row("|  , D,  ,  | 1,  , C, 9| 9, D, C,  |IE,IE,IE,IE|  , D, S, 3| 7, 4, S,  | S, D, S,10[ 8,11,  ,12]"),
	'175-177': parse_row("|  , D,  ,  |  , 1, C,  | 9, D, C,10|IE,IE,IE,IE|11, D, S, 3|12,  , S, 4| S, D, S,  [ 7, 8,  ,  ]"),
	'178-180': parse_row("|  , D,  ,  |  , 1, C,  | 9, D, C,10|IE,IE,IE,IE|11, D, S, 3|12,  , S, 4| S, D, S,  [ 7, 8,  ,  ]")
}
