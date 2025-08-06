# Test 3 & 4 - Compare Score Distribution

**Overview**
One more test comparing the reference and the new dataset, this time from score distribution aspect. 
****
**Parameters (see env.sh)**
All parameters are included in env.sh and described in [External Silent Run](../External%20Silent%20Run).
In particular, this test uses:
- REFERENCE_MATRIX=... full path to reference matrix (feature matrix from model train)
- ALGOMARKER_PATH=... path to the algomarker model directory
****
**What is actually done?**
Statistics comparing two sets of scores:
- Moments
- Cutoffs
- Statistical test (KLD)
Side check - make sure Algomarker scores are the same as expected using our model.
****
**Test Results Review**
Test 3:
- Raw view - Numerical (compare/score_dist.tsv) and Graphical (compare/score_dist.html) histogram of the two distributions.
- Statistical analysis - compare Mean, STD, and PR in cutoff (0.5-5%, every 0.5%), for the two distributions, see compare/compare_score.txt.
- Check test scores - are they the same when we re-run the model?
  - In general it should be exactly the same. Thus, statistics for Test_Run and Test_Run.Original in compare/compare_score.txt should be exactly the same.
  - However, in LGI, due to historical reasons, we would see minor differences.
- Another check for test_scores is presented in the test log - 03.compare_scores.log. It prints Pearson and Spearman correlations between AlgoMarker scores and our infrastructure calculation.
Test 4:
- 04.calc_score_kld.log: Kullback-Leibler Divergence diff, KLD_to_Uniform, entory_p (no detailed description here as it seems that  Test 4 benefit over Test 3 is doubtful).
**How to read the results?**
See example next, left to right/down: Statistical summary, histograms, and 
<img src="/attachments/13926497/13926499.png"/><img src="/attachments/13926497/13926500.png"/><img src="/attachments/13926497/13926501.png"/>
First and simple, Test_Run and Test_Run.Original are very close. That's OK.
However, we see significant differences between the test run (Orange) and the reference (Blue). It looks like the Age distribution can explain the difference, as the new dataset (Green line) is older than the reference (Blue line). However, the importance of Age might limit our ability to recognize other issues.
