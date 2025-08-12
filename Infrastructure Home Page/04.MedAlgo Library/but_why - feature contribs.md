# but_why - feature contribs
feature contributions (AKA but_why) is an attempt to explain a specific prediction of a classifier, by providing an interpretable simple model of simple features.
We saw 3 works in this field:

1. LIME - ([https://arxiv.org/pdf/1602.04938.pdf](https://arxiv.org/pdf/1602.04938.pdf)) - build a complex model, then build a local simple model (Lasso) for the predictions of the complex model. By local they mean - generate samples, and weight them according to their distance from the interesting sample (patient).
2. tree path interpreter - ([https://blog.datadive.net/interpreting-random-forests/](https://blog.datadive.net/interpreting-random-forests/)) - for tree ensembles such as XGB, follow the decision path for the interesting sample (patient), and accumulate the changes in the outcome mean for each feature.
3. SHAP - ([https://arxiv.org/abs/1802.03888](https://arxiv.org/abs/1802.03888)) - an improvement over (2), which promises consistency when the impact of a feature stays the same but the structure of the trees changes. 
[Yaron Kinar](https://www.linkedin.com/in/yaron-kinar-il/) built LinearizeScore - a local c++ version of LIME, which uses real samples (LIME are using artificial samples which are generated assuming feature independence and normality).
we added MedPredictor::calc_feature_contribs, which supports (2) and (3), only for XGB.
In Likely we are doing a somewhat strange hybrid solution: we are building a strong XGB model using all the features, then we build a second XGB model with only part of the features (the ones that make medical sense), and we aim to explain the predictions of the strong model. We then use calc_features_contribs for getting the weak model feature contributions, in (2) mode. 
Note that we currently do not know of a reliable way to quantify which method is better, except in artificial data experiments. Also note that for migrating to yaron's solution, we need the entire repo in memory on our production machine which is currently not feasible. 
 
