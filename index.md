# Home

![Pepy Total Downloads](https://img.shields.io/pepy/dt/medpython)
![PyPI - License](https://img.shields.io/pypi/l/medpython)
![GitHub contributors](https://img.shields.io/github/contributors-anon/Medial-EarlySign/MR_LIBS)
![GitHub commit activity](https://img.shields.io/github/commit-activity/t/Medial-EarlySign/MR_LIBS)

[![GitHub Repo](https://img.shields.io/badge/github-repo-blue?logo=github)](https://github.com/Medial-EarlySign/MR_LIBS)
![GitHub Repo stars](https://img.shields.io/github/stars/Medial-EarlySign/MR_WIKI)

**A note on our journey:** Medial EarlySign was a company that developed a proprietary platform for machine learning on electronic medical records. Following the company's liquidation, the decision was made to release the core software as an **open-source** project to allow the community to benefit from and build upon this technology. Please feel free to [reach me out](#community-and-contributions) in any case of an issue. I'm voluntarily holding this, so please be patients.

Our platform is designed to transform complex, semi-structured Electronic Medical Records (EMR) into **machine-learning-ready** data and reproducible model pipelines. The framework is optimized for the unique challenges of sparse, time-series EMR data, delivering **low memory usage** and **high-speed processing** at scale.

The framework was battle-tested in production across multiple healthcare sites and was a key component of an **award-winning** submission to the [CMS AI Health Outcomes Challenge](https://www.cms.gov/priorities/innovation/innovation-models/artificial-intelligence-health-outcomes-challenge).

## From Raw Data to Insight in Three Simple Steps

Our platform streamlines the development and deployment of clinical predictive models, transforming raw patient data into actionable insights. For live predictions (inference), you can use raw JSON data directly, bypassing the need for an optimized data store.

<img src="images/MES_Arch.png">

This structured approach ensures that data is processed efficiently, models are built systematically, and the results are both accurate and interpretable.

### The Workflow

**1. Start with Raw Patient Data**

Begin with your data in a simple JSON format.

```json
{
  "patient_id": "1",
  "data": {
    "signals": [
      {
        "code": "Hemoglobin",
        "unit": "g/dL",
        "data": [
          { "timestamp": [20240806], "value": ["14.1"] },
          { "timestamp": [20250806], "value": ["14.5"] }
        ]
      },
      ...
    ]
  }
}
```

**2. Define Your ML Pipeline**

Configure your entire machine learning workflow from preprocessing and feature engineering to the final model using a single [JSON configuration file](Infrastructure%20Library/MedModel%20json%20format.md). This approach ensures your experiments are reproducible and easy to version.

**3. Get Explainable Predictions**

Train your model using the Python SDK and generate predictions with clear, interpretable explanations. [Example output](Tutorials/07.Deployment/index.md#how-to-use-the-deployed-algomarker).

This is an illustration of the final output in a visual format (Our infrastructure returns the data to create this):

<img src="images/Explainability.png">

For more details, refer to the [Tutorials](Tutorials).

## Quick Installation

You can quickly install the package using **pip**:

```bash
pip install medpython
```
For detailed system requirements and compilation instructions, please see the [Installation Guide](Installation/index.md).

## Why Use This Platform?

*   **High-Performance Processing:** Engineered for large-scale, sparse EMR time-series data where general-purpose libraries like pandas fall short.
*   **Reusable Pipelines:** Save valuable engineering time by providing shareable, tested pipelines and methods.
*   **Built-in Safeguards:** Mitigate common pitfalls like data leakage and time-series-specific overfitting.
*   **Production-Ready:** Designed for easy deployment using Docker or minimal distroless Linux images.
*   **Innovative Algorithms:** Access to outperforming algorithms for processing medical data, explainability, fairness, and more.

## Core Components

The platform is built on three key pillars:

*   **MedRepository:** A compact, efficient data repository and API for storing and accessing EMR signals.
*   **MedModel:** An end-to-end machine learning pipeline for training and inference, producing predictions and explainability outputs.
*   **Medial Tools:** A suite of utilities for training, evaluation, and workflow management.

## Getting Started

*   **Build your first model:** Follow our [Complete Example: From Data to Model](Tutorials/08.A_Complete_Example.md) to learn the end-to-end process.
*   **Explore other tutorials:** Dive into specific topics with our step-by-step [Tutorials](Tutorials/).
*   **Use an existing model:** Browse the collection of [Models](Models) or learn how to deploy a model with [AlgoMarker Deployment](Tutorials/07.Deployment/).

## Community and Contributions

This is an open-source project, and we welcome contributions from the community.

*   **Report issues or ask questions:** Please use our [Github Discussions](https://github.com/Medial-EarlySign/MR_LIBS/discussions).
*   **Contribute to the code:** Check out our repositories:
    *   [MR_LIBS](https://github.com/Medial-EarlySign/MR_Libs): The core infrastructure libraries.
    *   [MR_Tools](https://github.com/Medial-EarlySign/MR_Tools): Tools and pipelines built on top of MR_LIBS.
    *   [MR_Scripts](https://github.com/Medial-EarlySign/MR_Scripts): A collection of helper scripts and utilities.

All software is open-sourced under the MIT license.
