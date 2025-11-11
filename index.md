
# Home

## Medial EarlySign - Documentation Overview

Medial EarlySign provides an infrastructure to convert **Electronic Medical Records (EMR)** - a complex, semi-structured time-series dataset into **machine-learning-ready** data and reproducible model pipelines. The library is optimized for sparse time-series EMR data and is designed for low memory usage and fast processing at scale.
Unlike images or free text, EMR data can be stored in complex format. The infrastructure standardize both the storage and the processing of time-series signals. We can think about this infrastructure as "TensorFlow" of medical data machine learning.

Key benefits at a glance:

- **Fast and memory-efficient processing** for large-scale EMR sparse time series where general-purpose libraries (e.g., pandas) are often impractical.
- Shareable, tested pipelines and methods that save engineering time and reduce duplicated effort.
- Built-in safeguards to reduce **data leakage** and time-series-specific overfitting.
- **Production-ready**: easily deployable in Docker or minimal Linux images.

This framework is deployed in production across multiple healthcare sites and played a key role in our award-winning submission to the [CMS AI Health Outcomes Challenge](https://www.cms.gov/priorities/innovation/innovation-models/artificial-intelligence-health-outcomes-challenge).

### Core components

The documentation and tooling are organized around three main areas:

- Data repository layer - MedRepository: an internal, compact format and API for storing and reading EMR signals efficiently.
- MedModel - a full ML pipeline that accepts data from MedRepository or JSON EMR inputs and produces predictions and explainability output. Supports training and inference with existing models.
- Tools - training and evaluation utilities for model performance (bootstrap analysis, fairness checks, explainability) while utilizing the infrastructure of both MedRepository and MedModel into a workflow. See: [Medial Tools](Medial%20Tools)

## Getting started

Choose a starting path:

- Use an existing model:
    - If the model is already deployed, follow: [How To Use Deployed AlgoMarker](Infrastructure%20Library/AlgoMarkers/Howto%20Use%20AlgoMarker.md#how-to-use-the-deployed-algomarker)
    - If the model exists but needs deployment: [AlgoMarker Deployment](Infrastructure%20Library/AlgoMarkers/Howto%20Use%20AlgoMarker.md#how-to-deploy-algomarker)
    - Browse available models: [Models](Models)
- Build a new model or evaluate an existing one: follow the step-by-step guides in [Medial Tools](Medial%20Tools)

## Repositories and resources

- [MR_LIBS](https://github.com/Medial-EarlySign/MR_Libs) - Core infrastructure libraries
- [MR_Tools](https://github.com/Medial-EarlySign/MR_Tools) - Tools and pipelines built on MR_LIBS
- [MR_Scripts](https://github.com/Medial-EarlySign/MR_Scripts) - Helper scripts and utilities