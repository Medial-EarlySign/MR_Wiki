# MedRegistry
[Code documentation](https://Medial-EarlySign.github.io/MR_LIBS/classMedRegistry)
Methods in MedRegistry:

- reading the object: *read_text_file* or* read_from_file* to read in text format or in binary format.
- writing the object: write*_text_file* or* write_from_file* to writein text format or in binary format.
- [create_registry](https://Medial-EarlySign.github.io/MR_LIBS/classMedRegistry.html#a7e4937c56e85b3246f5a3922fa00a145) - an option to create registry records by implementing private function ** to fetch each patient registry records
- [calc_signal_stats](https://Medial-EarlySign.github.io/MR_LIBS/classMedRegistry.html#abc3c0e37860a50d7b3386bc683314803) - a method to create contingency table with other signal splited by gender and age groups.
- [create_incidence_file ](https://Medial-EarlySign.github.io/MR_LIBS/classMedRegistry.html#a71f5c339661ac0ed97ffb2a1612c3ff9)- a method to calc the incidence (also with kaplan meier) 
 
A class that holds all registry records on all patients using MedRegistryRecord. very similar to MedCohort, but a more generic class to hold multiple periods for outcome on same patients.
for example pregnancy, influenza, kidney stones, sofa scores... 
Each record consist of those fields in [MedRegistryRecord](https://Medial-EarlySign.github.io/MR_LIBS/classMedRegistryRecord):
<table><tbody>
<tr>
<th>Parameter name</th>
<th>description</th>
</tr>
<tr>
<td>pid</td>
<td>patient id</td>
</tr>
<tr>
<td>start_date</td>
<td>the start date of the outcome </td>
</tr>
<tr>
<td>end_date</td>
<td>the end date of the outcome</td>
</tr>
<tr>
<td> registry_value</td>
<td><p> the registry value. 0 for controls, 1 for cases or other value in more complex cases.</p><p>For example in diabetes it may mark the states from 0-2. 0 - no diabetes, 1- pre, 2- diabetes.</p><p>for each period we create record, or value for SOFA Score</p></td>
</tr>
</tbody></table>
 
**Example records for cancer from MedCohort:**
A patient who is in the cohort from 01.01.2000 till 01.01.2016 and got cancer in 01.01.2012 will be presented by 2 MedRegistryRecords.
one period for control outcome period and one period for the case period:

1. control period: start_date=01.01.2000, end_date=01.01.2012, registry_value=0
2. case period: start_date=01.01.2012, end_date=01.01.2016, registry_value=1
a patient who is always control will create 1 record with the start,end dates of the control period
 
It has several ways to be initialized:

1. by reading from disk - binary format or text format
2. by creating registry using create_registry method. need to implement get_registry_records to handle single patient records.the class have also the ability to create contingency table with other signal:for each Gender,Age_bin - the 4 stats number of the registry with the appearances or not appearances of the signal value
