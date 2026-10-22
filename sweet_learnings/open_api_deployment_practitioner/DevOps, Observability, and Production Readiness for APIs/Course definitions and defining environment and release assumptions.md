### Summary

This module introduces key course terminology, including DevOps, and explains how to prepare an API for production by defining environment and release assumptions. It covers where the API runs, how configuration and secrets are managed, data and access boundaries, evidence required before deployment, and the responsibilities for release approval and rollback.

Key takeaway: Clear environment requirements, security boundaries, deployment criteria, and ownership are essential for a safe and reliable API release.

## Summary: Key Definitions

- DevOps: Practices that help teams configure, deploy, monitor, support, and improve software services.
- Observability: Using evidence such as logs, metrics, traces, alerts, and health checks to monitor API performance, usage, errors, and cost.
- Production readiness: Ensuring an API is reliable, secure, documented, observable, supportable, and recoverable before release.
- Release or version identifier: A label that identifies the running API version and its configuration, helping teams track changes and troubleshoot issues.
- Smoke test: A quick post-deployment check to confirm the API is reachable and its basic functionality works.
- Rollback: Returning to a previous known-good version or configuration when a release causes problems.
- Graceful degradation: Providing a limited, safe response when a component fails instead of failing silently or producing unsafe results.
- Incident-response route: A defined process identifying who handles production issues, who is notified, what evidence is reviewed, and who decides the next action.

Key takeaway: Production readiness means more than making an API work. It must be monitored, safely deployed, recoverable, and supported by clear responsibilities and response procedures.



## Summary: How DevOps Shows Up in This Course

DevOps connects software development with operations, helping teams move from building an API to releasing, monitoring, supporting, and improving it responsibly.

The course focuses on four key DevOps questions:

1. Configure: Is the API set up correctly with the right environment, settings, secrets, dependencies, and access permissions?
2. Release: Is the release identified, supported by sufficient evidence, approved by the right people, and reversible through rollback?
3. Observe: Can the team monitor API health, reliability, usage, latency, costs, and quotas?
4. Respond and improve: Can the team detect issues, notify the right owners, resolve problems safely, roll back if necessary, and improve using evidence?

Key takeaway: DevOps is not just about automation or deployment pipelines. It ensures an API can be configured securely, released responsibly, monitored effectively, and continuously improved after deployment.

## Summary: Identify Environment Assumptions

An environment is the place where an API runs. Before production deployment, teams must understand how environments differ and what evidence is required before promoting an API.

### 1. Four API environments

| Environment | Purpose                            | Limitation                                                   |
| ----------- | ---------------------------------- | ------------------------------------------------------------ |
| Local       | Individual development and testing | Does not prove production readiness.                         |
| Development | Team building and integration      | Does not prove production security or release controls.      |
| Staging     | Testing in a production-like setup | Does not guarantee approval, rollback, or support readiness. |
| Production  | Serving real users and systems     | Requires ongoing monitoring and incident response.           |

### 2. Key environment assumptions to document

- Environments and exposure: Which environments are used, and is the API internal or externally accessible?
- Runtime and hosting: Where is the API approved to run?
- Data and access boundaries: Which data sources and permissions apply in each environment? Is production data separated from test data?
- OpenAI project separation: Should staging and production use separate OpenAI projects to isolate usage, access, rate limits, and spending?
- Test data approach: Will testing use synthetic, sanitized, redacted, or production-like data?
- Promotion criteria: What tests, approvals, and evidence are required before moving to the next environment?

### 3. Understand workflow ownership

- Application-owned workflow: The application coordinates API calls and tracks unfinished jobs.
- Agents API managed session: OpenAI maintains session context and manages the agent's work, while the application still tracks its own jobs and checks outcomes.

Important: The Agents API supports US data residency only and is not eligible for Zero Data Retention (ZDR), even with a self-hosted sandbox. If these restrictions conflict with data requirements, rule out this execution approach before release testing.

### 4. Why staging and production differences matter

Staging may use different credentials, sanitized data, smaller retrieval indexes, lower traffic, or different network permissions. These differences can affect how the API behaves after release.

Key takeaway: Before production deployment, document environment differences, hosting, access and data boundaries, workflow ownership, and promotion requirements. Ensure there is evidence that the API has been tested in an environment that closely matches its intended production use.


## Summary: Identify Configuration Needs

Configuration determines how an API behaves in each environment. A production-ready API should avoid hardcoded values and hidden local settings, with clear documentation of environment-specific settings and how they are controlled.

### 1. Key configuration requirements

- Environment variables: Service URLs, feature flags, and other environment-specific settings.
- Secrets separation: Store API keys, tokens, credentials, and certificates using approved secret-management processes. Never expose them in code or shared documents.
- Dependency management: Document required libraries, services, APIs, retrieval stores, tools, and downstream systems.
- Runtime configuration: Define timeouts, retry limits, exponential backoff, jitter, request-size limits, logging, and concurrency.
- Rate limits, quotas, and spending: Set usage limits, spending thresholds, alerts, throttling behavior, and responses to exceeded limits.
- Version assumptions: Track and validate service versions, prompts, schemas, retrieval configurations, and tool definitions.

### 2. Async jobs and active responses

- Async tool calling: Allows supported models to continue independent work while the application executes a tool.
- Background mode: Runs response generation asynchronously. Define worker ownership, permissions, job state, and mapping between application job IDs and the original `call_id`.
- Mid-turn steering: Confirm model and WebSocket compatibility with the Responses API before enabling this feature.
- Data retention: Verify that enabled features comply with the project's approved retention and privacy controls.

### 3. Storage, validation, and ownership

For workflows involving Zero Data Retention (ZDR) and Private Safety Processing (PSP), document:

- Project policy and storage region.
- Validation evidence and storage access.
- Ownership of encryption keys, monitoring, and record lifecycle.
- Retention requirements and responsibility for stored records.

A previously saved Validated status indicates an earlier successful check; refreshing it does not necessarily run validation again. Current access must be verified using appropriate cloud-access and error evidence.

Disconnecting a storage connection does not automatically delete existing records. Their retention and ownership must still be managed.

### Key takeaway

Configuration readiness means documenting everything another qualified team member needs to run the API safely outside a local environment, including settings, secrets, dependencies, runtime behavior, spending controls, asynchronous processing, data retention, and ownership.

Readiness question: Could another qualified team member understand what must be configured for this API to run safely in staging or production?


## Summary: Define the Release Path

A release path explains how an API moves from a controlled environment, such as staging, into production. It ensures that deployment is an evidence-based decision rather than just a technical handoff.

### 1. Key elements of a release path

- Build and release path: How the API is packaged and promoted between environments.
- Smoke tests: Basic checks confirming that the API is reachable and can complete an expected request.
- Deployment approvals: Who approves the release and what evidence they require.
- Release notes: Changes made, known issues, risks, and items to monitor.
- Release owner: Coordinates the release.
- Approval owner: Authorizes the move to the next environment.
- Rollback owner: Restores a previous known-good version if necessary.
- Version identifier: Identifies the exact release being deployed.

### 2. Validate operating paths

For APIs using asynchronous tools, steering, or managed browsers, release testing must cover more than the successful path.

- Verify that delayed results reach the correct request and dependent work waits for required evidence.
- Confirm that steering requests are actually applied; an accepted request may only be queued.
- Test blocked requests, mid-stream errors, and monitoring interventions.
- Ensure no further actions are dispatched after a monitoring block.
- Test browser access denial, disconnection recovery, and session cleanup.
- Verify that sensitive actions require confirmation enforced by the runtime or appropriate access restrictions.

Important: Stopping or steering a workflow does not undo completed actions or automatically cancel tools that have already started.

### 3. Additional release considerations

- Data and session cleanup: Assign owners for deleting sessions and managing stored records. Self-hosted execution may require separate session deletion and compute shutdown.
- Healthcare deployments: Verify the organization's Business Associate Agreement (BAA), covered services, required configuration, and accountable approval. A BAA alone does not establish application compliance.
- Text watermarking: Document the effective configuration and detector test evidence. Watermarking can indicate OpenAI origin but does not prove factual accuracy. If detector access is unavailable, mark the test as untested.

### 4. Make the release decision explicit

Before release, document unresolved risks and how they will be addressed, monitored, accepted, or escalated.

A good release recommendation identifies:

- Target environment and release version.
- Required tests and supporting evidence.
- Approval and rollback owners.
- Outstanding risks or blockers.
- Recommended decision: proceed, remediate, pause, or roll back.

Key takeaway: A release path makes deployment accountable, testable, and reversible. It clearly defines what is being released, what evidence supports readiness, who authorizes the change, and how the team will respond if something goes wrong.


## Summary: Illustrative Example — Preparing an API for Production

A partner team has built an internal account-support API that summarizes customer support tickets, account notes, and recommended next actions. Although it works locally and passes basic staging tests, further evidence is required before a limited pilot can begin.

### 1. Deployment context and configuration

- Run the API in a staging-like pilot environment.
- Restrict access to approved pilot users and authorized customer accounts.
- Use approved systems for customer data and approved secret-management processes.
- Document rate limits based on expected pilot usage.

### 2. Validation and release evidence

- Confirm service availability through a health check.
- Run a smoke test using an approved account record.
- Test safe handling of missing or unauthorized account information.
- Record the release version and document changes and monitoring requirements.

### 3. Open blockers

- The approval owner for promotion to broader use is not confirmed.
- Rollback responsibility is assigned, but rollback has not been tested.
- Cost and usage monitoring for the pilot has not been verified.

### 4. Release recommendation

Pause the pilot decision until rollback readiness and pilot cost visibility are verified. Naming an owner is not enough; evidence must demonstrate that the controls work.

Once these checks pass, document the pilot's approved scope and conditions. Broader deployment must remain blocked until the appropriate approval owner is confirmed.

Key takeaway: Passing staging tests does not automatically mean an API is production-ready. A release decision must be supported by verified evidence, tested recovery procedures, cost visibility, clear ownership, and explicit approval.