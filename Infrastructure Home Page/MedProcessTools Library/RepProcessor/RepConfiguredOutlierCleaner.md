# RepConfiguredOutlierCleaner
**RepConfiguredOutlierCleaner is a subClass of basicOutlierCleaner.**
**It implements the learn method to define the borders on a signal values, and inherit apply from its parent so that  values that lie outside those values are removed. As the basic cleaner also has a trimming threshold these thresoholds are set to +-1e98, so no values are trimmed.**
**This cleaner gets in its parameters a name of a csv file that details the way each signal is treated.**
**Another parameter is clean_method which is either "learned", "confirmed" or "logical". **
**"learned" means that the borders are determined by calculation of distribution as described in the configuration file for this signal.**
**"confirmed" means that learning was done already on part of THIN and bounds  were set and confirmed by the author (Coby).**
**"logical" means that the thresholds are predetermined to the thresholds given in the configuration file. Those thresholds were set by understanding the nature of the signal (for example signal must be positive or percentage must not exceed 100).**
**note: even when confirmed or learned are chosen, values that are outside the logical bounds are removed first.**
**Format of the configuration file:**
**name,logicalL,logicalH,low bound,low dist,high bound,high dist**
**name:name of signal.**
**logicalL: Lower bound for the logical option**
**logicalH: Higher bound for the logical option**
**low bound: The lower bound that was calculated for the confirmed option ( may be set to none- meaning stay with the logical bound).**
**low dist: The probability distribution used in confirmed or should be used in learned for calculation of lower bound. May be norm, lognorm or manual ( that means do not use learned. Value was chosen manually for confirmed mode.**
**high bound: see low bound above.**
**high dist : see low dist above.**

### Include file is - H:/MR/Libs/Internal/MedUtils/MedProcessTools/RepProcess.h
### RepBasicOutlierCleaner
- **Description: ** A child class of RepBasicOutlierCleaner
- **Inherits from: **RepBasicOutlierCleaner
- **Generate new dynamic-version: **No
- **Members:**
    - string confFileName;   The file that holds the cleaning parameters for each signal.
    -  string cleanMethod;    // "logical" "confirmed" or "learned" as explained above.
    -  map<string,confRecord> outlierParams;         holds the parameter that were read from confFile.
- **Implemented methods:   **
    - *Constructors :*
        - *inheritted*
    - *void init_defaults() *: init cleaning parameters to default values
    - *virtual int init(map<string, string>& mapper) *: init cleaning parameters according to map
    - *int Learn(MedPidRepository& rep, vector<int>& ids, vector<RepProcessor *>& prev_processor) *: Learn the thresholds for removal of values according to the description above.
    - apply  is inheritted from basic cleaner.

 
 
