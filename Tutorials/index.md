# Tutorial 

Welcome to the Medial EarlySign (MES) tutorials! This guide provides a high-level overview of the end-to-end machine learning workflows for healthcare, from initial setup to model deployment. Each step in this guide links to a more detailed tutorial that will walk you through the specifics.
The tutorials uses command-line tools and Python helpers that interact with the MES infrastructure.

All the software is released under MIT open source licence. Some of the models are also planned to be released while some other will be accesible only through our parteners. 

## Overview

Medial EarlySign (MES) provides three  ways to work with the infrastructure:

1. A Python API that exposes many infrastructure capabilities for accessing and manipulating the data, creating sample files, training, and inference.
2. Standalone applications (executables) that implement infrastructure workflows; these are useful when the Python API does not yet cover a specific feature.
3. When a model is deployed, we will use `AlgoMarker` which is a minimal API with mainly inference capability. Deployment does not require the full training API or a training data repository. Deployed models accepts JSON-formatted patient records and don't need full MES infrastructure. See [Deployment](07.Deployment) for details. The AlgoMarker is very minimal and can be also run in a distroless linux images

## Who is this for?

These tutorials are for data scientists and developers who want to use the MES infrastructure to build and deploy machine learning models. Whether you are new to the MES ecosystem or an experienced user, these guides will help you get the most out of our tools.

## Setup requirements

1. Use the Python integration where possible - see the [Python](../Infrastructure%20Library/Medial%20Tools/Python) section. Note that the Python package does not expose every feature. Some capabilities are still only available as executables, but [extension](../Infrastructure%20Library/Medial%20Tools/Python/Extend%20and%20Develop.md) of the python library is possible. Follow the [Python setup instructions](../Installation/Python%20API%20for%20MES%20Infrastructure.md).

2. If you need the command-line tools, follow the installation guide: [MES Tools to Train and Test Models](../Installation/MES%20Tools%20to%20Train%20and%20Test%20Models.md). Each tool includes a `--help` flag that lists its arguments and options and `--version` flag to output git version it was complied with. Common tools are covered also within this Wiki.

3. To develop your own applications against the infrastructure, see the examples in the [Examples of Simple Applications](../Infrastructure%20Library/Medial%20Tools/index.md#examples-of-simple-applications) section below.

In most cases, Python plus a few tools will be sufficient - it is uncommon need to write new C++ code.

## Tutorials

* [01.Load the data](01.ETL%20Tutorial)
* [02.Access Data](02.Access%20Data)
* [03.Create Samples](03.Create%20Samples)
* [04.Train Model](04.Train%20Model)
* [05.Apply Model](05.Apply%20Model)
* [06.Model Evaluation](06.Model%20Evaluation)
* [07.Deployment](07.Deployment)



## Let's Get Started!

Ready to dive in? Start with the [Load the data](./01.ETL%20Tutorial) guide.