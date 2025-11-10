# MedPlot
To create general graph please use **createHtmlGraph** function in MedPlot. to create ROC graphs use plotAUC function.
 
plotAUC** Input: **

- vector of all models predictions vector(each record is prediction vector result of specific model)
- vector of the labels
- vector of the models\predictors names (same size as the first vector)
- output direcotry for writing graphs
- optional - indexes is a mask for selecting rows and may be omitted to select all
 
plotAUC **Output**:** **
the function outputs the following graphs:

- ROC graph curve
- PPV graph curve - for each false positive rate - it's PPV value for each model
- False Positive rate as function of model score - you may see each model scores VS it's false positive rate
- Label distribution of cases and controls 
For Each Graph you may search for specific working point in the search button - fill in X value (false positive rate) and it will find you the Y value (Sensitivity or PPV depends on the graph)
 
Example Run:
 
```c++
vector<float> preds; //from MedModel scores
vector<float> age_baseline; //the age_baseline for each sample
vector<float> labels;
plotAUC({age_baseline, preds}, labels, {"Age_Baseline" ,"MedModel"}, "~/Auc_Example_Folder")
```
 
 
 
