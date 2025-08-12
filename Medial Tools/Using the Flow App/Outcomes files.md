# Outcomes files
Outcome files are meant to be a formal definition for outcome groups of patients used in learning and testing.
An outcome has the following types

- binary - the outcome is 0 or 1 (we always use 0 for controls and 1 for the outcome itself)
- categorical - the outcome is in the range 0...(ncateg-1).
- regression - a continous outcome.
 
Each outcome is a list of rows, in each row we have:

- patient id
- date/time: the sampling date for the outcome (typically before the raw date)
- outcome value
- length: length of the outcome in time (from the time point and on, or a certain number of days after it, 0 means from this point and on)
- raw date: the actual date of the outcome
 
## Formal definition of an outcome file
An outcome file is a tab delimited text file with the following lines:
NAME <name for outcome: to be used in printings>
DESC <description: description lines for this outcome>
TYPE <one of: binary , multi , regression> : binary - is a 0/1 outcome, multi - is a multicategory outcome in the range 0...(ncateg-1) , regression is a continous outcome
NCATEG <number of categories> : needed when TYPE multi is used. Defining the number of categories in the outcome.
EVENT <pid> <date/time - of sample> <outcome value> <length - of outcome> <raw date - actual outcome date>
IGNORE <pid> : pids to always ignore when learning and testing this outcome: this is needed more in pre outcome stages in which we still need to filter and select matched controls for our outcome.
 
 
 
 
