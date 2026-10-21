### Summary: Add Risk, Cost, and Validation Logic

The goal is to make the model recommendation commercially viable, technically reliable, and evidence-based before committing to implementation.

Key areas to stress-test:

- Cost: Estimate expected usage costs and identify assumptions about volume, token consumption, and budget.
- Scale: Assess whether the model can handle growing workloads and user demand.
- Latency: Check whether response times meet workflow requirements.
- Reliability: Identify risks such as inconsistent outputs, failures, and downtime.
- Safety: Consider risks related to inaccurate outputs, harmful responses, privacy, and sensitive data.
- Validation: Identify the tests and evidence needed to confirm the model performs well on real-world tasks.

Expected outcome: A defensible recommendation that clearly distinguishes:

1. Known facts — supported by available evidence.
2. Assumptions — conditions expected to hold true.
3. Validation needs — questions requiring testing or further evidence.
4. Decision triggers — findings that would change the model selection or recommendation.

The focus is not on building detailed pricing models, benchmarks, evaluation suites, security architectures, or monitoring plans. It is on identifying the critical risks and evidence needed to make an informed decision.

## Summary: Cost and Scale Assumptions

A model recommendation must consider the total cost per successful task, not just the model’s API price.

### Key factors to estimate

- Request volume: Expected daily/monthly requests, peak demand, seasonality, and future growth.
- Input and output length: Token usage, retrieved context, and the length of generated responses.
- Processing requirements: Reasoning settings, retrieval, tools, multimodal inputs, and real-time needs.
- Reliability and rework: Failed attempts, permitted retries, reviewer time, and correction effort.
- Performance: Latency, throughput, and success rates at expected scale.
- Routing strategy: Use simpler, cheaper processing for routine cases and more capable models only when justified by task complexity or risk.

### Worked cost comparison

| Candidate | Total cost | Successful tasks | Cost per successful task |
| --------- | ---------- | ---------------- | ------------------------ |
| A         | $18        | 90               | $0.20                    |
| B         | $24        | 96               | $0.25                    |
| C         | $36        | 96               | $0.375                   |

These figures are fictional. Although Candidate A is cheapest per successful task, it fails a required review criterion. Candidate B is the preferred option among the candidates meeting the stated quality thresholds, because it achieves the same success count as C at a lower cost.

Include all attempt costs, applicable cached usage, tool charges, review effort, correction costs, and permitted retries. A blocked response is not a successful task and must not trigger an automatic retry simply to improve the success rate.

### Spend controls and validation

Before implementation, confirm:

- Current official model pricing, availability, and rate limits.
- Expected volume, peak throughput, and usage growth.
- Representative task success rates and total cost per successful task.
- Configured spend controls, their enforcement scope, and safe fallback behavior.

Important: Spend alerts notify teams but do not stop API traffic. Explicit hard limits can stop affected requests, but enforcement may not be instantaneous.

### Expected outcome

Document what is known, what is assumed, what must be validated, and what would change the recommendation. Treat cost and scale estimates as dated planning inputs, not fixed commitments.

The guiding principle: choose the least complex, cost-effective approach that meets the required quality, safety, and reliability thresholds at the expected scale.

## Summary: Latency and Reliability Assumptions

Latency is how long a user or downstream system waits for a response. Reliability is whether the workflow consistently returns usable results and fails safely when it cannot.

### Key assumptions to define

- Response time: Set latency targets based on the workflow, such as fast support routing versus slower background document processing.
- Processing mode: Decide whether the workflow needs synchronous responses, streaming, or asynchronous completion.
- Timeouts and retries: Define acceptable timeouts and safe retry behavior. Avoid repeated retries when they could duplicate actions or increase costs.
- Output validity: Ensure structured outputs contain all required fields and use approved values.
- Failure handling: Define when to retry, repair, reject, fall back to a simpler path, or escalate to human review.
- Safety and uncertainty: Ambiguous or high-risk cases should trigger review rather than produce unsupported answers or execute unauthorized actions.

### Example recommendation

A support-routing API should return valid structured results quickly enough for the intake workflow. If peak traffic increases latency or output validity falls below the required threshold, the design may need a fallback, asynchronous processing, human review, or a simpler processing path.

### What to validate before implementation

Track the signals that matter:

- Response latency and timeout rate.
- Structured-output validity.
- Retry rate and failure categories.
- Human-review triggers and fallback usage.
- Performance under expected peak traffic.

Expected outcome: Document the latency targets, reliability requirements, assumptions, and failure-handling behavior that need validation.

The selection rationale should identify these requirements without attempting to design the full production monitoring system.

## Summary: Safety and Validation Assumptions

Safety and validation assumptions help ensure a model recommendation is evidence-based rather than overconfident. Validation here means identifying what must be verified before implementation or wider use, not designing a complete evaluation or security program.

### 1. Identify likely failure modes

- Structured classification: Incorrect routing, invalid labels, missed review triggers, or unusable output formats.
- Retrieval-supported workflows: Outdated or unapproved sources, unsupported claims, conflicting information, or unauthorized data access.
- Tool-enabled workflows: Incorrect tool calls, malformed arguments, unauthorized actions, or mishandled tool errors.

Also consider sensitive data, unusual inputs, seasonal changes, and adversarial examples.

### 2. Define validation evidence

Before trusting the recommendation, identify the evidence needed:

- Representative success cases, edge cases, and known failures.
- Structured-output and task-quality checks.
- Human review of ambiguous or high-risk outputs.
- Comparison with a simpler baseline.
- Latency and throughput checks.
- Verification of model capabilities, API behavior, limits, pricing, and availability against official OpenAI documentation.

### 3. Account for security and data sensitivity

If the workflow handles confidential records, sensitive customer information, regulated data, or internal-only sources, identify the security, privacy, access-control, and governance reviews required. Do not claim production readiness before these questions are resolved.

### 4. Define human-review requirements

Human review should be considered when outputs affect sensitive decisions, customer-facing communications, regulated workflows, high-risk recommendations, or actions requiring approval.

### Expected outcome

Document:

1. Known risks: How the workflow could fail.
2. Validation requirements: What evidence is needed before proceeding.
3. Unresolved questions: What requires security, technical, or product review.
4. Decision criteria: What findings would change or block the recommendation.

Key takeaway: Recommend a model or workflow pattern conditionally, based on evidence. Confirm product facts against authorized official documentation, and leave detailed evaluation, guardrail, moderation, and production-monitoring design to the appropriate implementation work.

## Summary: Stress-Testing Cost, Latency, Safety, and Validation

The example shows why choosing the most capable model for every request is not automatically the best solution. A high-volume retail support-routing API must balance quality, cost, speed, reliability, and safety.

### Key lessons

- Cost: Estimate total cost per successful task, including retries, review, and correction effort.
- Output length: Return concise structured fields instead of lengthy explanations when downstream systems do not need them.
- Latency and scale: Validate response times and throughput under seasonal peak traffic.
- Reliability: Ensure required fields such as `routing_label`, `priority`, `reason`, and `needs_review` are valid.
- Safety: Route ambiguous or high-priority complaints to human review when required.
- Validation: Compare the shortlisted candidate against a simpler baseline using representative messages and edge cases.
- Fallback: Define safe behavior for timeouts, invalid outputs, and API failures.

### Stronger recommendation

Start with the least complex shortlisted candidate that meets predefined quality, safety, schema-validity, and latency thresholds. Reserve a more capable model for ambiguous or high-risk cases only if testing demonstrates a meaningful improvement that justifies its additional cost and latency.

Key takeaway: A defensible model recommendation is based on measured task-level performance and clearly documented assumptions—not model capability alone. Validate the evidence before committing to implementation, and define what results would change the recommendation.


# Exercise: Stress-Test an IT Helpdesk Selection Rationale

## 1. Cost and scale

- Volume: Validate average daily requests, peak-hour traffic, seasonal spikes, and expected growth.
- Input/output length: Helpdesk requests are assumed to be short. Test whether concise structured outputs are sufficient instead of long explanations.
- Successful task: One request is counted as successful only when it returns a valid support queue, priority, concise reason, and review flag that meet the agreed quality criteria.
- Total cost: Include input/output tokens, cached usage where applicable, reasoning settings, tool charges, failed attempts, permitted retries, human review, and correction effort.
- Retries: Retry only eligible transient failures within a defined limit. Blocked responses should stop and go to the appropriate review path rather than being automatically retried.
- Spend controls: Alerts notify the team but do not stop API traffic. Explicitly configured hard spend limits can stop affected requests, although enforcement may not be instantaneous.

## 2. Latency

Validate the maximum acceptable response time for support agents and test under peak traffic.

- Determine whether synchronous responses are fast enough.
- Set timeout and retry limits.
- Check whether streaming provides meaningful benefit for short structured outputs.
- Define fallback behavior when the model or API is slow or unavailable.

## 3. Reliability

Validate that every successful response contains:

- `routing_label` — a queue from the approved list.
- `priority` — an allowed priority value.
- `reason` — a concise, reviewable explanation.
- `needs_review` — a valid review indicator.

Test malformed or incomplete outputs, timeouts, API errors, and unavailable dependencies. Invalid results must be repaired, retried when safe, rejected, or escalated according to the workflow contract.

## 4. Safety and human review

Send requests for human review when they involve:

- Ambiguous requests that could belong to multiple queues.
- High-priority incidents or potential security breaches.
- Sensitive employee information.
- Low-confidence or unsupported classifications.
- Invalid output or repeated processing failures.

Blocked requests must remain stopped until the appropriate review or resolution occurs.

## 5. Pattern fit

The initial recommendation is unnecessarily complex in three ways:

- Most advanced model for every request: Start with a simpler shortlisted candidate and use a more capable model only for difficult cases if testing proves the benefit.
- Long explanations for every decision: Return short structured fields that downstream systems can consume.
- Retrieval added for possible future needs: Omit retrieval in the first version if requests can be routed using the message and stable instructions alone. Add it only if validated requirements depend on current internal policy documents.

Keep the initial reasoning settings, tool use, and retry behavior as simple as possible while meeting quality and safety requirements.

## 6. Product validation

Before implementation, verify against current official OpenAI documentation:

- Model availability, capabilities, and supported input types.
- API compatibility and structured-output support.
- Context limits, reasoning settings, and applicable rate limits.
- Current input, output, and cached-token prices.
- Tool availability and any additional usage charges.
- Relevant data-handling and safety requirements.

## 7. Tradeoffs and decision criteria

| Area        | Assumption to validate                             | What could change the recommendation?               |
| ----------- | -------------------------------------------------- | --------------------------------------------------- |
| Quality     | The simpler candidate meets routing thresholds.    | Persistent misrouting or missed critical incidents. |
| Latency     | Responses meet intake workflow expectations.       | Peak latency exceeds the agreed limit.              |
| Cost        | Total cost per successful task fits the budget.    | Review and correction costs erase the savings.      |
| Reliability | Required fields remain valid under realistic load. | Frequent invalid outputs or failures.               |
| Safety      | High-risk and ambiguous cases reach review.        | Critical cases bypass required review.              |

Fallback strategy: Use the simpler validated path for routine requests. If the primary model fails or exceeds its timeout, route the request to a safe queue or human review rather than inventing a classification. Do not automatically retry blocked work.

Recommendation: Begin with a simple structured-classification baseline, short outputs, bounded retries, and explicit review handling. Add more capable models, retrieval, or tools only when representative testing demonstrates that they materially improve successful-task quality enough to justify the added cost, latency, and complexity. Treat volume, pricing, throughput, and capability assumptions as items to validate before build—not as confirmed facts.