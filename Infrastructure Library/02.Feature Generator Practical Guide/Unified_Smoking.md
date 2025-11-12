# Unified Smoking
The smoking feature process all raw smoking information signal into unified features. 


## Input signals

* `Smoking_Status` - categorical Smoking Status: Current, Never, Former, Unknown, Never_or_Former
* `Smoking_Intensity` - How many cigarettes per day patient reports smoking in reported date. (optional signal, will use it only if exists)
* `Smoking_Duration` - How many years the patient reported smoking in the reported date. (optional signal, will use it only if exists)
* `Pack_Years` - Calculation of cigarettes packs per day multiply by year (Smoking_Duration * Smoking_Intensity/20). (optional signal, will use it only if exists)
* `Smoking_Quit_Date` - If patient stopped smoking, the date reported stopped smoking. (optional signal, will use it only if exists)

All input signals has 1 time channel of reported date and value channel with the value.

## Method

1. The Smoking feature generator creates a patient timeline of smoking information based on all available input signals. 
For example, no `Smoking_Status` was provided in certain date but `Smoking_Intensity` was reported so the patient is marked as `Current_Smoker` within that time.
    * The smoking generator breaks the timeline based on the input signals. For example. Patient inputs were:
    ```
    20180101 - Reported Current Smoker
    20210101 - Report Former smoker with Quit date of 20200101
    20210301 - Reported Current smoker again
    20250101 - Reported Former Smoker without quit date
    ```
    The feature generator will create a time line with:
    ```
    Assuming age 20 => 20200101 : Was Smoker
    20200101 => 20200701 (middle between 20200101 to 20210301): Was Former smoker
    20210101 => 20230201 (middle between 20210301 to 20250101) : Was Smoker
    20230201 => today: Former Smoker
    ```
    In a case we don't have any reported smoking date, first smoking indication is "Former smoker" it uses a simple linear model (based on age reported former smoker) to estimate "exact" quit date.

## Available features (Outputs)

- One-hot smoking status: Current_Smoker, Ex_Smoker, Never_Smoker, Unknown_Smoker.
- `Smoking_Intensity`: The average (median) daily smoking amount reported up to the time of prediction.
- `Pack_years`: A measure of cumulative tobacco exposure, calculated either from reported pack-years or by multiplying Smoking Years by the Smoking Intensity.
- `Smok_Days_Since_Quitting`: measures the number of days that have passed since the patient stopped smoking.
    * **Current Smokers** are assigned **0 days**.
    * **Never Smokers** are assigned **patient age** in days
    * The exact quit date is given in the input signal `Smoking_Quit_Date`
    * If the exact quit date is missing, we estimate it using one of two methods:
        - **Midpoint Estimate**: If the patient's record shows they switched from being a "Current Smoker" to an "Ex-Smoker," we assume they quit exactly halfway between those two reporting dates.
        - **Model Estimate**: If there's no clear reporting window to use, a linear model (trained on typical quit ages) is applied to estimate the most likely quit date based on the age when the patient reported quitting.
- `Smoking_Years`: The estimated total duration the patient has smoked, derived from a complete timeline of their smoking statuses (including the quit date calculation).

Please specify the requested feature output in the field `smoking_features` 