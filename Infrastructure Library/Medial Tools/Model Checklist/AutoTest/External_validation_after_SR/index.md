# External Validation (After Silent Run)

The purpose of this test is to analysis the performance when we have outcomes avaialable.

This TestKit documents the follow-up tests to run after completing the External Silent Run. Run this kit after performing the [External Silent Run](../External%20Silent%20Run/) to convert the silent-run (no outcomes repository) artifacts into evaluation-ready outputs.
This is to make sure no information leakage is done and separate the execution of the score calculation from the labels. It is also possible to load the labels in the silent run and the silent run will just ignore the labels, if we only recieved data with outcomes.

Note: The External Silent Run produces repository artifacts and the initial sample files used as inputs to the tests described below. Make sure the External Silent Run completed successfully before running this kit.

## Tests included

- [Test 01 - Load Outcome](Test%2001%20-%20Load%20Outcome.md)
    - Purpose: Load outcome/register data into the working repository and prepare the repository structure for downstream tests.
- [Test 02 - Fit Model to Repository](Test%2002%20-%20Fit%20Model%20to%20Repo.md)
    - Purpose: Convert and fit a provided model to the local repository and produce transformed model files (with/without explainability).
- [Test 04 - Relabel & Create Samples](Test%2004%20-%20Relabel%20&%20Create%20Samples.md)
    - Purpose: Create an outcome registry, relabel samples using diagnosis codes, drop excluded samples, and filter to the comparison cohort.
- [Test 05 - Compare Matrices & Feature Analysis](Test%2005%20-%20Compare%20Matrices%20&%20Features.md)
    - Purpose: Compare the current matrix with a reference matrix, produce Shap/ButWhy explainability reports and feature-level visualizations.
- [Test 06 - Matrix Feature Statistics & KLD Analysis](Test%2006%20-%20Test%20Matrix%20Features.md)
    - Purpose: Produce per-feature statistics, plots and KLD metrics for top Shap-identified features comparing the run with the reference.
- [Test 07 - Bootstrap Analysis](Test%2007%20-%20Bootstrap%20Analysis.md)
    - Purpose: Run bootstrap performance estimation (AUC, sensitivity/precision points, ORs, LIFT) and optional comparator bootstraps.
- [Test 08 - Age Of Flagged](Test%2008%20-%20Age%20Of%20Flagged.md)
    - Purpose: Generate age and temporal analyses for flagged patients and compare distributions across cohorts.
- [Test 09 - Features With Missing Values Analysis](Test%2009%20-%20Features%20With%20Missing.md)
    - Purpose: Inspect and visualize missingness patterns for important features and produce stats and KLD measures.
- [Test 10 - Calibration Test](Test%2010%20-%20Calibration.md)
    - Purpose: Run calibration checks and bootstrap-based calibration graphs for score-bin calibration across cohorts and time windows.

## Notes

- Many tests depend on helper utilities, please ensure these are on PATH. [Installation](../../../../../Installation/index.md#environment-setup-script) 

## Quick start

From the TestKit folder, you can run a single test, e.g.:

```bash
./run.specific.sh 4
```

Or run the full kit:

```bash
./run.sh
```