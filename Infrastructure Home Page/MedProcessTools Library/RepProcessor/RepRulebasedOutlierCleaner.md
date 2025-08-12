# RepRulebasedOutlierCleaner
**RepRulebasedOutlier cleaner is a subclass of RepProcessor and MedValueCleaner.**
**This cleaner applies the following rules drawn from Coby's imagination:**
1. **BMI=Weight/Height^2*1e4**
2. **MCH=Hemoglobin/RBC*10**
3. **MCV=Hematocrit/RBC*10**
4. **MCHC-M=MCH/MCV*100**
5. **Eosinophils#+Monocytes#+Basophils#+Lymphocytes#+Neutrophils#<=WBC**
6. **MPV=Platelets_Hematocrit/Platelets**
7. **UrineAlbumin<=UrineTotalProtein**
8. **UrineAlbumin_over_Creatinine=UrineAlbumin/UrineCreatinine**
9. **LDL+HDL<=Cholesterol**
10. **NonHDLCholesterol+HDL=Cholesterol**
11. **HDL_over_nonHDL=HDL/NonHDLCholesterol**
12. **HDL_over_Cholesterol=HDL/Cholesterol**
13. **HDL_over_LDL=HDL/LDL**
14. **HDL_over_LDL=1/LDL_over_HDL**
15. **Cholesterol_over_HDL=Cholesterol/HDL**
16. **-----canceled rule 16**
17. **Cholesterol_over_HDL=1/HDL_over_Cholestrol**
18. **LDL_over_HDL=LDL/HDL**
19. **Albumin<=Protein_Total**
20. **FreeT4<=T4*1000**
21. **NRBC<=RBC**
22. **CHADS2<=CHADS2_VASC**
**All rules are checked to within 10% tolerance (#define TOLERANCE (0.1))**
**Rules are checked only if all signals needed for rule implementation exist for the same date.**
**If a rule is checked for a certain date and found to be false (outside the tolerance), all values  of the signals that are included in the rule will be removed for that date.**
**The cleaner has 2 additional parameters:**
**consideredRules: a string of comma separated integers stating the rules you want to apply to the data. If 0 is included in the list, all rules will be applied. If the string is empty (default), no rule will be applied so the cleaner will actualy do nothing.**
**addRequiredSignals: When set to "0" only rules that all the participating signals are in the list of this cleaner will be applied.**
**                                  When set to "1" any rule that includes even one of the named signals will be applied. Signals that are in the rule and are not in the list will be loaded by the cleaner.**
**                                  : the additional signals that are loaded by this cleaner because  addRequiredSignals was set to "1", may not go through the preprocessing by cleaners that preceed this cleaner, if they are not in the signals list for that cleaner.**
**,**
- **Description: ** A child class of RepProcessor used for point-wise cleaning of outliers according to predefined rules
- **Inherits from:** [SampleFilter](../SampleFilter) [RepProcessor](../RepProcessor)
- **Generate new dynamic-version: **No
- **Members:**
- vector <string> signalNames;                                      Names of signals that should be cleaned
- vector <int> signalIds;                                                 Ids of signals to clean
- int time_channel = 0;
- int val_channel = 0;
- MedDictionarySections myDict;                                    keeping it will enable us to get ids at apply stage
- bool addRequiredSignals=false;                                   a flag stating if we want to load signals that are not in the cleaned signal list (see explanation above)
- vector<int> consideredRules;                                       only rules in this list will be considered in this cleaner (see explanation above)

- **Implemented methods:   **
    - *Constructors :*
        - *RepRuleBasedOutlierCleaner() *
    - *void init_defaults() *: init cleaning parameters to default values
    - *int init(void *processor_params) *: init cleaning parameters according to input params
    - *virtual int init(map<string, string>& mapper) *: init cleaning parameters according to map
    - *void set_signal_ids(MedDictionarySections& dict) *: set signalId (actually keep the dictionary for further use in apply).
    - *int apply(PidDynamicRec& rec, vector<int>& time_points) *: apply outliers-cleaning to signal in dynamic-rec at time-points 
