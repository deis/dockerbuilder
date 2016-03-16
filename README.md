# Deis Dockerbuilder v2

[![Build Status](https://travis-ci.org/deis/dockerbuilder.svg?branch=master)](https://travis-ci.org/deis/dockerbuilder)
[![Docker Repository on Quay](https://quay.io/repository/deisci/dockerbuilder/status "Docker Repository on Quay")](https://quay.io/repository/deisci/dockerbuilder)

Deis (pronounced DAY-iss) Workflow is an open source Platform as a Service (PaaS) that adds a developer-friendly layer to any [Kubernetes](http://kubernetes.io) cluster, making it easy to deploy and manage applications on your own servers.

For more information about the Deis Workflow, please visit the main project page at https://github.com/deis/workflow.

## Beta Status

This Deis component is currently in beta status, and we welcome your input! If you have feedback, please [submit an issue][issues]. If you'd like to participate in development, please read the "Development" section below and [submit a pull request][prs].

[issues]: https://github.com/deis/workflow/issues
[prs]: https://github.com/deis/workflow/pulls

# About

The dockerbuilder is the central API for the entire Deis Platform. Below is a non-exhaustive list of things it can do:

* Create a new application
* Delete an application
* Scale an application
* Configure an application
* Create a new user
