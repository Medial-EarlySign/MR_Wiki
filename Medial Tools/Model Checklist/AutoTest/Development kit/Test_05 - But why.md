
# Test 05: But Why

## Purpose
Provide explanations for model predictions using Shapley values, helping users understand which features drive decisions and how feature values influence outcomes.

## Required Inputs
From `configs/env.sh`:

- `WORK_DIR`: Output directory for results
- `MODEL_PATH`: Path to the model
- `REPOSITORY_PATH`: Path to the data repository
- `TEST_SAMPLES`: Path to the test samples

## How to Run
From your TestKit folder, execute:
```bash
./run.specific.sh 5
```
Or include as part of the full suite:
```bash
./run.sh
```

## What This Test Does
- Calculates Shapley values for individual predictions
- Aggregates feature importance statistics
- Generates visual explanations for both global and local feature effects

## Output Location
Results are saved under `$WORK_DIR/ButWhy`:
- `Global.html`: Global signal importance in the model
- `Global.ungrouped.html`: Global feature importance (ungrouped)
- `single_features/`: Directory containing analysis for each important feature
    - For each feature:
        - Stratification plots showing how feature values affect model response
        - Mean outcome for each feature value (probability of being a case)
        - Mean score for each feature value (should align with outcome graph)
        - Mean and confidence interval of Shapley value for each feature value (may differ from outcome in some cases)

## How to Interpret Results
- Use global plots to identify the most influential features
- Review single feature analyses to understand how feature values impact predictions and Shapley values
- Look for expected patterns (e.g., U-shaped risk curves for age in Flu Complications) and ensure the model's logic is reasonable

