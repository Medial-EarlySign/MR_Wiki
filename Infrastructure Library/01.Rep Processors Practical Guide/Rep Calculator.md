# Rep Calculator
Rep processor to calculate things:
 
examples/rep_processor_calc.json
Full parameter list: [https://Medial-EarlySign.github.io/MR_LIBS/classRepCalcSimpleSignals.html](https://Medial-EarlySign.github.io/MR_LIBS/classRepCalcSimpleSignals)
 
The input signals is given with comma separated string in "signals" parameter - for example: ""

- calculator - the calculator type, list of types can be found in next section
- output_signal_type - string type of output signal. For example "T(i),V(f)" to generate signal with 1 time channel of type int and 1 value channel of type float. This is the default
- max_time_search_range  -integer that specify what is the maximal time gap to construct the virtual signal based on all signals. The date of the new signal will be the latest date. 
- signals_time_unit - the time unit to use in max_time_search_range (default Days)
- names - the name of the virtual signal
- time_channel - integer that specify which time channel to use in all input signals (default 0)
- work_channel - integer that specify which value channel to use in all input signals (default 0). (If signal has less channels, will use last channel. not common usage)
- calculator_init_params - additional arguments string based on "calculator" parameter. since it's can be multiple arguments, you need to escape the string with "{}" and put arguments inside of brackets as in the examples.
 
## Calculator type - "calculator" parameters
All "calculator" parameter options can be found in here [https://Medial-EarlySign.github.io/MR_LIBS/classSimpleCalculator.html](https://Medial-EarlySign.github.io/MR_LIBS/classSimpleCalculator.html):

- sum - linear combination of multiple signals    res := b0 + sum_sigma(i=1..N){ factor[i] * input[i]},    where b0 is a bias
    - calculator_init_params - can receive "b0" - to specify constant bias argument + "factors" which is comma separated numbers that correspond each input signal (default is list of ones)
- log - calculates log on signal
- ratio - divides signals, accepts "factor" as final factor after dividing (default 1),.  res := factor * V1^power_mone / V2^power_base
    -  calculator_init_params -  "power_mone", "power_base" which default value is 1, and "factor" which the default is also 1
- multiply -multiply of signals. res := b0 * pie_multiply(i=1..N) {input[i]^powers[i]} 
    -  calculator_init_params "b0" and "powers" which is comma separated numbers that correspond each input signal (default is list of ones)
- kfre -  Implements calculation of 3,4 or 8-variable Kidney Failure Risk Equations (KFRE).
           The code can be found under
                 Libs/Internal/MedProcessTools/MedProcessTools/RepProcess.h
                 Libs/Internal/MedProcessTools/MedProcessTools/RepProcess.cpp
- empty - dummy virtual signal to create empty signal
- exists - res := in_range_val if signal exists otherwise out_range_val
    - calculator_init_params   - "out_range_val", "in_range_val"
- range - A simple Range check that return "in_range_val" if within range and returns "out_range_val" if outside range. Accepts also "min_range", "max_range"
    - calculator_init_params - "in_range_val", "out_range_val", "min_range", "max-range"
- set -  res := "in_range_val" if is in set otherwise "out_range_val"
    - calculator_init_params   - "out_range_val", "in_range_val", "sets" or "sets_file" to specify list of codes of file path to read codes. 
- eGFR - calculates eGFR from Creatinine, Gender, Age, based on CKD_EPI or MDRD equations. 
    - calculator_init_params  - You can pass "mdrd" to control if to use MDRD or CKD_EPI equation. You can also pass "ethnicity". 0 -for white, "1" for black
 
## Examples:
```json
{
                    "rp_type":"calc_signals",
                    "calculator":"ratio",
                    "names":"PaO2_over_FiO2",
                    "signals":"Art_PaO2,FiO2",
                    "max_time_search_range":"180",
                    "signals_time_unit":"Minutes",
                    "calculator_init_params":"{factor=100}",
					"unconditional":"0"
}
{
                    "rp_type":"calc_signals",
                    "calculator":"set",
                    "names":"Ventilation_proc",
                    "signals":"PROCEDURE",
                    "max_time_search_range":"0",
                    "signals_time_unit":"Minutes",
                    "calculator_init_params":"{sets=Invasive_Ventilation,Non-invasive_Ventilation}",
					"unconditional":"0"
},
{
                    "rp_type":"calc_signals",
                    "calculator":"range",
                    "names":"Ventilation_1",
                    "signals":"Peak_Insp_Pressure",
                    "max_time_search_range":"0",
                    "signals_time_unit":"Minutes",
                    "calculator_init_params":"{min_range=0;max_range=1000}",
					"unconditional":"0"
 },
```
 
Run Flow with those signals (print them):
```bash
#Flow with rep_processors: pids arg can be omitted to print all pids
Flow --rep /home/Repositories/MIMIC/Mimic3/mimic3.repository --model_rep_processors $MR_ROOT/Projects/Resources/examples/rep_processor_calc.json --pids_sigs_print --sigs "PaO2_over_FiO2,Art_PaO2,FiO2" --pids 100000027
 
pid     signal_name     description_name        description_value       ...
100000027       PaO2_over_FiO2  Time_ch_0       142142154|21700404-19:54        Val_ch_0        147
100000027       PaO2_over_FiO2  Time_ch_0       142142160|21700404-20:00        Val_ch_0        210
100000027       PaO2_over_FiO2  Time_ch_0       142142997|21700405-09:57        Val_ch_0        134
100000027       PaO2_over_FiO2  Time_ch_0       142143060|21700405-11:00        Val_ch_0        67
100000027       PaO2_over_FiO2  Time_ch_0       142143120|21700405-12:00        Val_ch_0        67
100000027       PaO2_over_FiO2  Time_ch_0       142143134|21700405-12:14        Val_ch_0        57
100000027       PaO2_over_FiO2  Time_ch_0       142143180|21700405-13:00        Val_ch_0        57
100000027       PaO2_over_FiO2  Time_ch_0       142144290|21700406-07:30        Val_ch_0        74
100000027       PaO2_over_FiO2  Time_ch_0       142144335|21700406-08:15        Val_ch_0        80
100000027       PaO2_over_FiO2  Time_ch_0       142146240|21700407-16:00        Val_ch_0        98.5714
100000027       Art_PaO2        Time_ch_0       142142154|21700404-19:54        Time_ch_1       142142154|21700404-19:54        Val_ch_0        147
100000027       Art_PaO2        Time_ch_0       142142599|21700405-03:19        Time_ch_1       142142599|21700405-03:19        Val_ch_0        89
100000027       Art_PaO2        Time_ch_0       142142997|21700405-09:57        Time_ch_1       142142997|21700405-09:57        Val_ch_0        67
100000027       Art_PaO2        Time_ch_0       142143134|21700405-12:14        Time_ch_1       142143134|21700405-12:14        Val_ch_0        57
100000027       Art_PaO2        Time_ch_0       142143846|21700406-00:06        Time_ch_1       142143846|21700406-00:06        Val_ch_0        52
100000027       Art_PaO2        Time_ch_0       142143900|21700406-01:00        Time_ch_1       142143900|21700406-01:00        Val_ch_0        57
100000027       Art_PaO2        Time_ch_0       142144007|21700406-02:47        Time_ch_1       142144007|21700406-02:47        Val_ch_0        63
100000027       Art_PaO2        Time_ch_0       142144148|21700406-05:08        Time_ch_1       142144148|21700406-05:08        Val_ch_0        74
100000027       Art_PaO2        Time_ch_0       142144335|21700406-08:15        Time_ch_1       142144335|21700406-08:15        Val_ch_0        80
100000027       Art_PaO2        Time_ch_0       142145347|21700407-01:07        Time_ch_1       142145347|21700407-01:07        Val_ch_0        86
100000027       Art_PaO2        Time_ch_0       142146228|21700407-15:48        Time_ch_1       142146228|21700407-15:48        Val_ch_0        69
100000027       Art_PaO2        Time_ch_0       142146662|21700407-23:02        Time_ch_1       142146662|21700407-23:02        Val_ch_0        71
100000027       Art_PaO2        Time_ch_0       142147017|21700408-04:57        Time_ch_1       142147017|21700408-04:57        Val_ch_0        89
100000027       Art_PaO2        Time_ch_0       142148289|21700409-02:09        Time_ch_1       142148289|21700409-02:09        Val_ch_0        64
100000027       FiO2    Time_ch_0       142142085|21700404-18:45        Time_ch_1       142142085|21700404-18:45        Val_ch_0        100
100000027       FiO2    Time_ch_0       142142100|21700404-19:00        Time_ch_1       142142100|21700404-19:00        Val_ch_0        100
100000027       FiO2    Time_ch_0       142142148|21700404-19:48        Time_ch_1       142142148|21700404-19:48        Val_ch_0        100
100000027       FiO2    Time_ch_0       142142160|21700404-20:00        Time_ch_1       142142160|21700404-20:00        Val_ch_0        70
100000027       FiO2    Time_ch_0       142142340|21700404-23:00        Time_ch_1       142142340|21700404-23:00        Val_ch_0        50
100000027       FiO2    Time_ch_0       142142400|21700405-00:00        Time_ch_1       142142400|21700405-00:00        Val_ch_0        50
100000027       FiO2    Time_ch_0       142142820|21700405-07:00        Time_ch_1       142142820|21700405-07:00        Val_ch_0        50
100000027       FiO2    Time_ch_0       142142850|21700405-07:30        Time_ch_1       142142850|21700405-07:30        Val_ch_0        50
100000027       FiO2    Time_ch_0       142143060|21700405-11:00        Time_ch_1       142143060|21700405-11:00        Val_ch_0        100
100000027       FiO2    Time_ch_0       142143120|21700405-12:00        Time_ch_1       142143120|21700405-12:00        Val_ch_0        100
100000027       FiO2    Time_ch_0       142143180|21700405-13:00        Time_ch_1       142143180|21700405-13:00        Val_ch_0        100
100000027       FiO2    Time_ch_0       142143360|21700405-16:00        Time_ch_1       142143360|21700405-16:00        Val_ch_0        100
100000027       FiO2    Time_ch_0       142143435|21700405-17:15        Time_ch_1       142143435|21700405-17:15        Val_ch_0        100
100000027       FiO2    Time_ch_0       142144290|21700406-07:30        Time_ch_1       142144290|21700406-07:30        Val_ch_0        100
100000027       FiO2    Time_ch_0       142144560|21700406-12:00        Time_ch_1       142144560|21700406-12:00        Val_ch_0        100
100000027       FiO2    Time_ch_0       142144800|21700406-16:00        Time_ch_1       142144800|21700406-16:00        Val_ch_0        70
100000027       FiO2    Time_ch_0       142146000|21700407-12:00        Time_ch_1       142146000|21700407-12:00        Val_ch_0        70
100000027       FiO2    Time_ch_0       142146240|21700407-16:00        Time_ch_1       142146240|21700407-16:00        Val_ch_0        70
```
