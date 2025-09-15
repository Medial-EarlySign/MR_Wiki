# Test 5 - Sex Ratio

**Overview**
Here we compare score distribution to check sex fairness, and similarity to reference  
****
**Parameters (see env.sh)**
All parameters are included in env.sh and described in [External Silent Run](../External%20Silent%20Run).
In particular, this test uses:

- SCORE_MIN_RANGE, SCORE_MAX_RANGE - range of score to inspect, will jump with 0.01 between scores
- Assumes test 02 completed and we have "$WORK_DIR/compare/rep_propensity_non_norm.matrix","$WORK_DIR/compare/rep_propensity.matrix", "$WORK_DIR/compare/test.preds", "$WORK_DIR/compare/reference.preds" Alon - we have not discussed those in test 2, what are they and are they important to mention at all?
****
**What is actually done?**
Compare results (reference vs new dataset) by sex and positive rate.
 
**How to read the results?**
The following is example of results for Test 5 (see 05.sex_ratio.log)
For each score cutoff in range, we see:

- The flagged males ratio in this cohort VS reference. . For instance, we can see here:
    - Male ratio going down when cutoff goes up, both for reference and test.
    - However, the values are higher for the tested dataset, probably because of overall bigger share for males (need to verify).
- Positivity rate, same as we saw in Test 3.
<img src="../../../../attachments/13926532/13926530.png"/>
