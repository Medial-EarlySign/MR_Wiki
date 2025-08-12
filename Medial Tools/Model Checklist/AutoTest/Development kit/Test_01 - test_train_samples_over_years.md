# Test_01 - test_train_samples_over_years
## Overview
The goal is to test the samples distribution and some properties of the trained samples.
 
## Inputs:
- WORK_DIR  -output work directory
- TRAIN_SAMPLES_BEFORE_MATCHING - The training samples

## Outputs
The output is located under WORK_DIR/01.test_train_samples_over_years.log

- Prints the distribution of cases/controls in each year in the sample - Do we see something weird here? is it unbalanced? Is there any pattern? 
- Prints the distribution of cases/controls in each month in the samples - Do we see something weird here? is it unbalanced? Is there any pattern? 
- Creates a folder - samples_stats.train
    - stats.txt - contains a table how many "distinct" outcomes a patient has in the samples - prints a histogram of that. If each patient is suppose to be either case/control please check that. Otherwise you can see how many controls turned into cases
    - cases_controls_id_histogram.html: x axis - how many times a patient was repeated in the samples as case/control. y axis - patients count. We can see how many of the patients repeats themselves in the samples. Does that seems OK?
