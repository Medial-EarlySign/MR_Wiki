# Medial EarlySign Tutorials

Welcome to the Medial EarlySign (MES) tutorials! This guide will walk you through our end-to-end machine learning platform for healthcare. From initial setup to model deployment, you'll learn how to leverage our powerful tools to build and deploy impactful models.

All our software is open-source under the MIT license. While some models will be released publicly, others will be available exclusively through our partners.

## How It Works

MES offers three primary ways to interact with the platform:

1.  **Python API:** A comprehensive library for accessing data, creating samples, training models, and running inference. This is the recommended starting point.
2.  **Command-Line Tools:** Standalone executables for specific workflows, especially for features not yet available in the Python API.
3.  **AlgoMarker:** A minimal, lightweight API designed for model deployment. It accepts JSON-formatted patient records and runs inference without requiring the full training infrastructure. It's so lightweight it can even run in distroless Linux containers.

## Who Are These Tutorials For?

These tutorials are designed for data scientists and developers who want to build and deploy machine learning models using the MES platform. Whether you're a new or experienced user, these guides will help you master our tools.

## Getting Started: Setup

1.  **Python API (Recommended):** Start with our Python integration. It provides a convenient way to access most of the platform's features. Follow the [Python setup instructions](../Installation/Python%20API%20for%20MES%20Infrastructure.md) to get started. While the Python package is extensive, you can [extend it](../Infrastructure%20Library/Medial%20Tools/Python/Extend%20and%20Develop.md) to add custom functionality.

2.  **Command-Line Tools:** If you need features not yet available in the Python API, install our command-line tools. Follow the [installation guide](../Installation/MES%20Tools%20to%20Train%20and%20Test%20Models.md). Each tool includes a `--help` flag for usage instructions and a `--version` flag to check its version.

3.  **Custom Applications:** To build your own applications on top of our infrastructure, check out the [examples of simple applications](../Infrastructure%20Library/Medial%20Tools/index.md#examples-of-simple-applications).

In most cases, the Python API combined with a few command-line tools will be all you need. Writing new C++ code is rarely necessary.

## The Tutorials

This series of tutorials will guide you through the entire machine learning workflow:

*   **[01. Load the Data](01.ETL%20Tutorial):** Start here to learn how to load your data into the MES platform.
*   **[02. Access Data](02.Access%20Data):** Learn how to access and manipulate your data.
*   **[03. Create Samples](03.Create%20Samples):** Prepare your data for model training.
*   **[04. Train Model](04.Train%20Model):** Train your machine learning model.
*   **[05. Apply Model](05.Apply%20Model):** Use your trained model to make predictions.
*   **[06. Model Evaluation](06.Model%20Evaluation):** Evaluate the performance of your model.
*   **[07. Deployment](07.Deployment):** Deploy your model for use in a production environment.

## Let's Get Started!

Ready to begin? Head over to the first tutorial: **[01. Load the Data](./01.ETL%20Tutorial)**.
