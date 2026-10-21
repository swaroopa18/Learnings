This module teaches you to translate a customer’s problem into clear technical requirements before selecting a model or API capability.

You will identify:

- Task: What the API must accomplish.
- Inputs and outputs: What information it receives and what result it must produce.
- Context requirements: How much information or conversation history it needs.
- Constraints and risks: Cost, latency, accuracy, privacy, and reliability requirements.
- Validation needs: What must be tested before recommending or building the solution.


## Classify the Task

Before choosing a model or API capability, identify the core task the API must perform. Translate the customer's business need into a specific technical requirement.

### Common API task types

- Generate: Create new content.
- Summarize: Shorten information while preserving key points.
- Classify: Assign labels, categories, priorities, or routes.
- Extract: Pull specific fields from input.
- Reason: Evaluate evidence, rules, or options.
- Transform: Change content format, tone, or structure.
- Retrieve: Use approved sources to provide grounded answers.
- Act through a tool: Interact with an external system to retrieve information or initiate an action.
- Support live or multimodal interaction: Handle voice, audio, images, or real-time exchanges.

### How to classify a workflow

1. Identify the API's primary output or action.
2. Determine the input it receives.
3. Define the output it must return.
4. Explain how the output will be used.
5. Identify secondary tasks if the workflow combines multiple capabilities.

### Example

Weak requirement: “Use AI to improve customer support.”

Strong requirement: “Classify customer-support messages into approved routing categories, assign a priority level, and return a short explanation for auditing.”

Key takeaway: Classify the task before selecting the model. Focus on what the API must deliver, rather than choosing a capability because it sounds impressive. This creates a clear foundation for model selection, testing, and technical handoff.

## Summary: Define Technical Requirements

After classifying the task, define the technical requirements that determine which model or API pattern is suitable. These requirements describe what the API must accept, return, handle, and guarantee.

### Key technical requirements

1. Input and output modality: Identify whether inputs and outputs involve text, JSON, images, audio, files, or other formats.
2. Reasoning depth: Determine whether the task needs simple classification or transformation, or more complex multi-step reasoning.
3. Required context: Establish whether user input is sufficient or whether approved documents, business data, permissions, or live system information are needed.
4. Output structure: Define the required response format, fields, schema, and validation rules.
5. Latency tolerance: Specify how quickly the API must respond and whether streaming or asynchronous processing is acceptable.
6. Throughput and scale: Estimate request volume, concurrency, input sizes, and expected growth.
7. Reliability: Define acceptable errors, retry behavior, fallbacks, monitoring, and human-review requirements.
8. Contract and interface: Document required fields, state management, error handling, and the appropriate API interface.

### Example: Support-routing API

| Requirement | Specification                                                 |
| ----------- | ------------------------------------------------------------- |
| Task        | Classify support messages                                     |
| Input       | Short text message                                            |
| Output      | Structured JSON with label, priority, reason, and review flag |
| Context     | User input and predefined categories                          |
| Reasoning   | Low to moderate                                               |
| Latency     | Low latency preferred                                         |
| Scale       | Thousands of messages daily                                   |
| Reliability | Valid output and controlled categories                        |
| Review      | Escalate ambiguous or high-priority cases                     |

### Key takeaway

Define the requirements before selecting the model or API. This allows the team to compare options based on actual workflow needs, cost, speed, reliability, and implementation constraints.

Before building, validate current API capabilities, supported models, structured-output behavior, pricing, limits, and availability against official OpenAI documentation.

## Summary: Define Risk and Review Requirements

Before recommending a model or API pattern, identify the risks, safety boundaries, and review processes that could affect whether the solution is suitable for deployment.

### Key requirements

1. Sensitive data: Identify personal information, confidential business data, customer records, and other sensitive information the API may process.
2. Human review: Determine which outputs or actions require human approval, especially for high-risk, regulated, or customer-impacting decisions.
3. Safety boundaries: Define what the API must not answer, recommend, disclose, or do.
4. Quality threshold: Establish acceptable accuracy, consistency, and error rates, including which failures require escalation.
5. Validation approach: Specify the evidence needed to verify performance, such as representative test cases, edge cases, schema checks, and latency tests.
6. Data access and permissions: Identify approved data sources, authorized users, and information the API must never expose.
7. Governance and approval: Define who approves data use, tools, actions, and the overall workflow.
8. Observability: Identify the evidence needed to monitor quality and failures, such as misclassification rates, unsupported claims, or tool-call errors.

### Example: Support-routing API

A structured classification pattern may be suitable if testing confirms acceptable routing accuracy, valid outputs, and reliable escalation of high-priority complaints.

However, if routing requires live order information or interpretation of approved company policies, the solution may need additional capabilities and validation.

### Key takeaway

Treat model selection as a testable recommendation, not an assumption. Define risks, access permissions, review requirements, and measurable quality thresholds before implementation. This makes the final recommendation safer, more accountable, and easier for a technical team to validate and maintain.

## Summary: Defining Capability Requirements Before Choosing a Model

A retail customer wants an API to classify thousands of incoming product-support messages daily and route them to the correct team.

The key lesson is to define workflow requirements before choosing a model.

### Requirements overview

- Business goal: Reduce manual triage and improve routing consistency.
- Task: Classify support messages and recommend a routing destination.
- Input: Short text messages.
- Output: Structured fields for routing label, priority, reason, and review flag.
- Modality: Text input and structured text output.
- Reasoning: Low to moderate, with human review for ambiguous cases.
- Context: Predefined categories; no external sources needed initially.
- Performance: High throughput, low latency, and cost efficiency.
- Risk management: Escalate high-priority or uncertain cases for human review.
- Validation: Test representative examples, edge cases, output validity, latency, throughput, and review triggers.

### Recommended initial pattern

Use a structured classification response because the task requires predictable outputs, efficient processing, and consistent routing.

Additional capabilities should be considered only when requirements justify them:

- Retrieval: When decisions depend on approved policies or documents.
- Tool use: When live order status or external system actions are required.
- Approval controls: When automatically updating tickets or taking consequential actions.
- Realtime or speech: When agents need live voice interactions.
- Optimization or specialized patterns: When testing shows that simpler improvements cannot meet quality requirements.

Key takeaway: Choose a model and API pattern based on workflow needs and validation evidence, not on which model appears most advanced.


## Exercise: Shortlist and Compare Model Candidates

The goal is to select two or three suitable models for an internal IT helpdesk triage API, compare them against the same requirements, and recommend a provisional lead.

### 1. Define the workflow requirements

- Input: Short text description of an employee's IT issue.
- Task: Classify the issue and determine urgency.
- Output: Structured fields: `issue_category`, `urgency`, `recommended_queue`, `needs_review`.
- Context: Predefined categories and routing rules; no live data retrieval.
- Interface: An API supporting structured responses.
- Operational needs: Low latency, high throughput, and reasonable cost.
- Safety: Avoid silently misrouting urgent or ambiguous issues.
- Human review: Required for uncertain classifications and high-urgency cases.

### 2. Shortlist current model candidates

Official model documentation checked: 19 October 2026.

[Deep learning Generic color lineal-color icon | Magnific (formerly Freepik)](https://images.openai.com/static-rsc-4/IgwTeJ2DbwNWRy_VB3w2H3Ev7ZutTyXazgvTYNzx3SYxQcLUpB_bDvKV1dVDkDqn4OEqfGYXk9SeoJAdyfOqfSwGD1_QeINebmz7EpQE1EOzdDjLs6oXkHldYtHLxs0kRWXHp0nO_qIkUAful7dAIWGyNRMhYTO5ryVPyXxczMI?purpose=inline)

Candidate A — GPT-6 Luna

Provisional lead

Model ID: `gpt-6-luna`

Designed for focused, high-volume tasks. Its low published token prices make it a strong starting point for routine helpdesk classification, provided it meets the accuracy and review requirements.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://developers.openai.com\&sz=32)

OpenAI API



[叮当次元袋 - 杭州叮当猫科技有限公司](https://images.openai.com/static-rsc-4/KROFt15DUN3v6kjK8HuwG4ba0YQ5yJKRCQ7YFwDzvNvPcOaX9IW3e0Qyfb2RcM-0KfSLCyt8_oVbEDGbXAmH1CyGbapb3yX4I1X3RS7qgT_H46nmL8cKMKwLgFZ2FAjr9HLhGlrOVz-TY903h9ltv3zdqmVF62hdqk9SiqTEBC4?purpose=inline)

Candidate B — GPT-6.1 Sol

Model ID: `gpt-6.1-sol`

A balanced alternative when Luna struggles with ambiguous requests, urgency assessment, or more complex category distinctions. Retain it as the quality-versus-cost comparison.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://developers.openai.com\&sz=32)

OpenAI API



[Free Download Best Microsoft Build 2025 Logo Concepts](https://images.openai.com/static-rsc-4/GUO2yEJ2xCM8axdOcxsnO-i5Hxrnb3CAeEDn4KdpwOqoTOErvRoeNF9n25XrC3fl2-Scjd3rFdgvqsZTZaNN9jO_5SVbN6nrg9k7P_hAazxgf8QBDHp6C5-uAx9QQOxoJVJ72qj7Qtu9MoLBnZ-ZXM3mLQ1EoRHo01CWSxH4Lpo?purpose=inline)

Candidate C — GPT-6 Astra

Model ID: `gpt-6-astra`

The flagship candidate for demanding reasoning tasks. Keep it as a benchmark if simpler models fail on difficult cases, but defer it as the default until testing demonstrates sufficient additional value to justify the higher cost.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://developers.openai.com\&sz=32)

OpenAI API



Official references:

- [OpenAI model catalog](https://developers.openai.com/api/docs/models?utm_source=chatgpt.com)
- [OpenAI API pricing](https://developers.openai.com/api/docs/pricing?tab=suite\&utm_source=chatgpt.com)

### 3. Compare candidates against the same requirements

| Requirement       | GPT-6 Luna                         | GPT-6.1 Sol                     | GPT-6 Astra                     |
| ----------------- | ---------------------------------- | ------------------------------- | ------------------------------- |
| Task fit          | Strong starting candidate          | Strong alternative              | Capable, potentially excessive  |
| Input/output      | Text to structured fields          | Text to structured fields       | Text to structured fields       |
| Reasoning         | Test routine cases                 | Test ambiguous cases            | Benchmark difficult cases       |
| Context           | Short descriptions and fixed rules | Same                            | Same                            |
| Interface         | Evaluate with Responses API        | Same                            | Same                            |
| Latency           | Measure in representative tests    | Measure in representative tests | Measure in representative tests |
| Cost              | Lowest of these three              | Middle                          | Highest                         |
| Safety and review | Same application-level safeguards  | Same safeguards                 | Same safeguards                 |
| Decision          | Lead provisionally                 | Retain as alternative           | Defer unless justified          |

The models support text input and text output. Use the [official model documentation](https://developers.openai.com/api/docs/models?utm_source=chatgpt.com) and [Structured Outputs guide](https://developers.openai.com/api/docs/guides/structured-outputs?utm_source=chatgpt.com) to verify the current interface and schema requirements.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://developers.openai.com\&sz=32)

OpenAI API

+1



### 4. Validation plan

Before making the final recommendation, test all three models against the same labeled helpdesk examples.

- Measure category and urgency accuracy.
- Check that every required output field is present and valid.
- Test ambiguous requests and urgent incidents.
- Verify that `needs_review` is triggered appropriately.
- Measure latency and cost at expected request volumes.
- Confirm current model availability, limits, and pricing in official documentation.

### 5. Provisional recommendation

Start with GPT-6 Luna (`gpt-6-luna`) as the cost-efficient baseline. Retain GPT-6.1 Sol as the alternative if it materially improves classification quality, and use GPT-6 Astra as a higher-capability benchmark for difficult cases.

This is a provisional shortlist, not a validated winner. The final decision depends on representative evaluation results, acceptable error thresholds, and the customer's operational constraints.