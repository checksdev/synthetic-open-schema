# Synthetic Open Schema

Welcome to the Synthetic Open Schema by Checks.dev! This repository hosts an open-source, versioned YAML-based schema designed for defining and managing synthetic monitors. We are currently in version `v1beta1`, aimed at providing a unified and flexible format for various types of synthetic checks including HTTP, TCP, SSL, and scripted browser scenarios.

## Rationale

The Synthetic Open Schema was created to address the need for a standardized, open, and flexible way to define synthetic monitoring checks. By using a common schema, developers and operators can easily share, understand, and manage their monitoring configurations across different platforms and tools. This schema is designed to be:

- **Extensible**: Easily add new types of checks and extend existing ones.
- **Human-readable**: Use YAML format for simplicity and clarity.
- **Versioned**: Ensure backward compatibility and smooth transitions with versioned schema definitions.
- **Integrated**: Seamlessly integrate with Git for version control and CI/CD pipelines.

## Key Features

- **Versioned Schema**: Currently in `v1beta1`, ensuring stability and evolution with community feedback.
- **Unified Format**: Simplifies defining and managing synthetic monitors across different platforms.
- **Flexible Configurations**: Supports various types of checks with YAML configurations.
- **Scheduling Options**: Define checks with intervals using frequency settings or cron expressions.
- **Customizable Assertions**: Specify conditions for pass/fail criteria in your checks.
- **Notifications**: Integrate with email, Slack, or webhook notifications for alerting.
- **Multi-Region Support**: Run checks across multiple geographic locations or customer-owned agents.
- **GitOps Friendly**: Seamless integration with Git for version control and automated deployments.
- **Infrastructure as Code (IaC)**: Manage and provision your monitoring infrastructure using code, ensuring consistency and reproducibility.

## Infrastructure as Code (IaC)

By adopting the Synthetic Open Schema, you can leverage Infrastructure as Code (IaC) principles for your synthetic monitoring setup. This approach allows you to:

- **Version Control**: Keep your monitoring configurations in Git, providing a history of changes and facilitating collaboration.
- **Automation**: Integrate with CI/CD pipelines to automatically deploy and update synthetic monitors as part of your deployment processes.
- **Consistency**: Ensure that your monitoring setup is consistent across different environments by defining it in code.
- **Reproducibility**: Easily reproduce your monitoring setup in new environments or after a disaster recovery scenario by applying the same codebase.

## Getting Started

1. **Clone the Repository**

   ```bash
   git clone https://github.com/checksdev/synthetic-open-schema.git
   cd synthetic-open-schema
   ```

2. **Explore Examples**

   Dive into the [`examples`](examples) directory to find YAML configurations for different types of synthetic checks:

   - [`http-check.yaml`](examples/http-check.yaml): Example HTTP endpoint monitoring configuration.
   - [`tcp-check.yaml`](examples/tcp-check.yaml): Example TCP service monitoring configuration.
   - [`ssl-check.yaml`](examples/ssl-check.yaml): Example SSL certificate monitoring configuration.
   - [`browser-check.yaml`](examples/browser-check.yaml): Example scripted browser scenario configuration.
   - [`dns-check.yaml`](examples/dns-check.yaml): Example DNS resolution monitoring configuration.


## Examples

### HttpCheck

```yaml
apiVersion: checks.dev/v1beta1
kind: HttpCheck
metadata:
  name: example-http-check
  labels:
    environment: production
spec:
  url: https://api.example.com/health
  method: GET
  headers:
    Authorization: Bearer your_access_token_here
  timeout: 5s
  interval: 1m
  retries: 3
  checks:
    - type: statusCode
      operator: equals
      value: 200
    - type: body
      operator: contains
      value: "OK"
    - type: duration
      operator: lessThan
      value: 500ms
    - type: header
      operator: equals
      value: "Content-Type: application/json"

  locations:
    - us-east-1
    - eu-west-2

```


## Schema Structure

The `schemas/` directory contains the JSON schema definitions for all api versions:

- `v1beta1.json`: JSON schema for HTTP v1beta1 version.

## Contribute

We welcome contributions from the community! Check out the [CONTRIBUTING.md](CONTRIBUTING.md) file for guidelines on how to contribute to the Synthetic Open Schema project.

## License

This project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for details.
