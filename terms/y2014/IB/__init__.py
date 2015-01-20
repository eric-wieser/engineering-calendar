from timetable import TimeSlot, LabInfo

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
		'EIETL',
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

	LabInfo('[]',
		'Structural Design Workshop',
		'Inglis Instrument Shop',
		TimeSlot.full_week_of(TimeSlot.afternoon_long)),

	LabInfo('M',
		'Microprocessors',
		'EIETL',
		[TimeSlot.morning, TimeSlot.afternoon_short]),

	LabInfo('MA',
		'Microprocessors',
		'EIETL',
		[TimeSlot.morning])
]
