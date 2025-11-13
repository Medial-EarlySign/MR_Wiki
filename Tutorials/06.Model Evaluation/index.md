# Model Evaluation

Please refer to our suggested [Checklist](../../Infrastructure%20Library/Medial%20Tools/Model%20Checklist) for model evaluation
Common evaluation tools and workflows used in MES:

1. [bootstrap_app](../../Infrastructure%20Library/Medial%20Tools/bootstrap_app) - bootstrap-based performance analysis with cohort and subgroup filtering. For example, we might want to test performance in different sub-cohorts: time window, age range, etc.
2. Feature importance and post-processing - see [Flow post-processors](../../Infrastructure%20Library/05.PostProcessors%20Practical%20Guide/ButWhy%20Practical%20Guide.md).
3. Explainability - add model explainers as post-processors. See the [Explainers Guide](../../Infrastructure%20Library/05.PostProcessors%20Practical%20Guide/ButWhy%20Practical%20Guide.md#adding-an-explainer-to-an-existing-model) and our patent [US20240161005A1](https://patents.google.com/patent/US20240161005A1) for the MES-specific approach. Recognizing that standard Shapley values struggle with high-dimensional, correlated medical data, we developed a specialized extension. This new method was validated by our clinicians in a blinded study against other explainability techniques and was a key component of our award-winning submission to the [CMS Health AI Outcome Challenge](https://www.cms.gov/priorities/innovation/innovation-models/artificial-intelligence-health-outcomes-challenge). The results are published, but some of the process can be seen in the Research tab of this wiki.
4. Covariate-shift / simulation tools - [Simulator](../../Infrastructure%20Library/Medial%20Tools/Simulator.md).
5. Automated checks - [AutoTest](../../Infrastructure%20Library/Medial%20Tools/Model%20Checklist/AutoTest), a pipeline of tests derived from the Model Checklist.