# Welcome to Medial EarlySign's Open Source Platform

**A note on our journey:** Medial EarlySign was a company that developed a proprietary platform for machine learning on electronic medical records. Following the company's liquidation, the decision was made to release the core software as an open-source project to allow the community to benefit from and build upon this technology.

Our platform is designed to transform complex, semi-structured Electronic Medical Records (EMR) into **machine-learning-ready** data and reproducible model pipelines. The framework is optimized for the unique challenges of sparse, time-series EMR data, delivering **low memory usage** and **high-speed processing** at scale.

It was conceived as a "TensorFlow" for machine learning on medical data.

All software is now open-sourced under the MIT license. Some of the models developed by Medial EarlySign that are currently in production are available exclusively through our partners.

The framework was battle-tested in production across multiple healthcare sites and was a key component of an **award-winning** submission to the [CMS AI Health Outcomes Challenge](https://www.cms.gov/priorities/innovation/innovation-models/artificial-intelligence-health-outcomes-challenge).

## Why Use This Platform?

*   **High-Performance Processing:** Engineered for large-scale, sparse EMR time-series data where general-purpose libraries like pandas fall short.
*   **Reusable Pipelines:** Save valuable engineering time by providing shareable, tested pipelines and methods.
*   **Built-in Safeguards:** Mitigate common pitfalls like data leakage and time-series-specific overfitting.
*   **Production-Ready:** Designed for easy deployment using Docker or minimal distroless Linux images.

## Core Components

The platform is built on three key pillars:

*   **MedRepository:** A compact, efficient data repository and API for storing and accessing EMR signals. Querying categorical signals like perscriptions and diagnosis in an easy and efficient API. 
*   **MedModel:** An end-to-end machine learning pipeline that takes data from MedRepository or JSON EMR inputs to produce predictions and explainability outputs. It supports both training and inference.
*   **Medial Tools:** A suite of utilities for training, evaluation, and workflow management, including bootstrap analysis, fairness checks, and explainability.

## Getting Started

*   **Build a new model:** Follow the step-by-step [Tutorials](Tutorials/) to build a model from scratch.
*   **Use an existing model:** Browse the collection of [Models](Models) or learn how to deploy a model with [AlgoMarker Deployment](Tutorials/07.Deployment).

## Resources

*   **[MR_LIBS](https://github.com/Medial-EarlySign/MR_Libs):** The core infrastructure libraries.
*   **[MR_Tools](https://github.com/Medial-EarlySign/MR_Tools):** Tools and pipelines built on top of MR_LIBS.
*   **[MR_Scripts](https://github.com/Medial-EarlySign/MR_Scripts):** A collection of helper scripts and utilities.

Explore the documentation to understand the architecture and tools.