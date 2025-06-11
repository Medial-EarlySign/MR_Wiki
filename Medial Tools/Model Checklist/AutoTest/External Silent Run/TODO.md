# TODO

env file - remove FILTER_LAST_DATE, we don't want to support it = we want to assume data has no duplications
General - prepare focused output, with just the important features
General - printing the missing value rate for each feature/important feature. There is a "mask" of imputations in MedFeatures, we want to print this matrix also in (TestModelExternal), than we can count the stats of missing values or plot the graphs without imputations.
Test 1 - improve ETL to mark with WARNING any evidence for possible concern
Test 1 - parse output file to get all signal value distribution effort in one dataframe, see code in wiki 
General - arranged output from test by directory (all output from test 'n' are in 'directory n')
Test 2 - parse compare_rep.txt with the code from the wiki, or save as tsv from the start
Test 2 - improve the logic to mark feature status in table 21, or simply drop the table and keep just t22
Test 2 - add t-test
Test 2 - table 22, what is AUC, and why do we need it?
Test 2 - bring to feature importance columns, the value from the reference
Test 3 - bug in calculation of correlation between Test_Run and Test_Run.Original
Test 3 - consider checking score distribution differences (also?) after matching on Age
Test 5 - print also Male ratio for the whole population
Test 6 - coverage calculation and missing values (as reference comes after imputation, and currently we report test before imputation)
Test 7 - check KLD computation
Test 9 - add a reference
 
 
Rerun on THIN with LungFlag
