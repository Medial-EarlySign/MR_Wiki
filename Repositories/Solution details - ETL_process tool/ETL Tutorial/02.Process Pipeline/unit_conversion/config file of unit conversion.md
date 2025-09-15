# Example config/output file of unit conversion
Based on Taiwan Conversions (almost all signals has single unit). transformed all units to lowercase to merge same units before calling this function.
The file was created Automatically and only the row "Ca" was edited => mmol/l.
Rows without edits will be kept "as is", no unit conversion and in most cases that's OK.

- signal is the "source" signal in Taiwan - already did the mapping before with a different file. when "to_signal" is empty will keep the same name as "signal"
- count - how common this signal
- unit - the unit with this signal
- unitcount - How common is the signal+unit combination. If single unit, it will be equal to count. Will sum up to count when taking all rows for the same signal
- to_signal -  when "to_signal" is empty will keep the same name as "signal"
- to_unit - was taken from global+local signals file definitions configuration (just for convenient, not in use). Each signal definition has units
- multiple_by, additive_b0 - the linear transformation. Default is 1 for multiple_by and 0 for additive_b0 if not given (dioing nothing be default to multiple by 1 and add 0)
- value_0 - example values

**Example of top 20 rows:**
```
signal	count	unit	unitCount	to_signal	to_unit	multiple_by	additive_b0	value_0
Glucose	201128	mg/dl	201128		mg/dL			[107.0, 319.0, 127.0, 140.0, 91.0]
Hemoglobin	145250	g/dl	145216		g/dL			[10.2, 13.2, 11.5, 14.5, 13.2]
Hemoglobin	145250	%	34		g/dL			[13.8, 15.1, 19.9, 12.4, 17.8]
Hematocrit	144843	%	144840		%			[27.6, 30.0, 26.3, 48.2, 27.4]
Hematocrit	144843	%pcv	3		%			[27.0, 27.0, 26.0, 26.0, 21.0]
Creatinine	139001	mg/dl	139001		mg/dL			[1.3, 1.0, 0.9, 0.7, 1.0]
MCV	135235	fl	135235		fL			[88.6, 89.8, 92.6, 86.1, 99.2]
Platelets	135159	k/?gl	135091		10*9/L			[189.0, 330.0, 409.0, 39.0, 297.0]
Platelets	135159	10^3/ul	68		10*9/L			[100.0, 36.0, 134.0, 31.0, 25.0]
WBC	134959	k/?gl	134893		10*9/L			[5.13, 12.84, 4.39, 4.8, 1.83]
WBC	134959	10^3/ul	66		10*9/L			[49.22, 0.14, 1.3, 37.49, 0.24]
RBC	134620	m/?gl	134558		10*12/L			[4.41, 4.2, 5.32, 4.32, 3.16]
RBC	134620	10^6/ul	62		10*12/L			[4.03, 4.03, 3.04, 2.79, 2.46]
MCHC-M	134404	g/dl	134404		g/dL			[32.5, 32.5, 32.6, 33.6, 34.7]
MCH	134065	pg	134065		pg			[29.0, 29.2, 31.2, 28.4, 23.3]
RDW	129021	%	129021		%			[15.9, 15.5, 12.2, 17.2, 15.0]
ALT	122626	u/l	122626		U/L			[92.0, 20.0, 58.0, 21.0, 21.0]
eGFR	90973	ml/min/1.73 m^2	90973					[108.8, 57.5, 130.8, 91.5, 106.7]
....
Ca	35375	mmol/l	35349		mg/dL	4.01		[2.2, 2.13, 2.3, 1.84, 2.25]
Ca	35375	mg/dl	26		mg/dL			[9.6, 10.9, 9.8, 10.3, 9.9]
```

In this example, the `Ca` signal with the `mmol/l` unit was given a conversion factor of `4.01`. This factor is used to transform the values from `mmol/l` to the target unit of `mg/dL`. You can see this in the example values: the original values are around 2, while data from `mg/dL` unit has values around 10. For all other signals in the example, the units were consistent and did not require any conversion, so the conversion fields were left blank.
 
Full file:
 
[map_units_stats.cfg](../../../../../attachments/13403029/13403028.cfg)
