### Summary: Build and Evaluate a Current Model Shortlist

Model selection should be a current, evidence-based comparison, not a permanent ranking. Filter candidate models against workflow requirements, including task, modality, inference interface, context and output needs, safety, latency, scalability, and cost.

Evaluate the strongest candidates against defined performance thresholds using relevant evaluations (evals). Select the least complex model that meets all requirements.

Document the final shortlist with:

- Official sources and verification dates.
- Evaluation results and performance evidence.
- Tradeoffs in capability, cost, latency, and complexity.
- Facts and model details that must be revalidated before implementation.

Key takeaway: Choose models based on verified requirements and evaluation evidence, and revalidate critical details before building.

### Summary: Build a Current Model Shortlist

A current model shortlist is a small set of candidate models that satisfy the workflow’s essential requirements and are ready for task-specific evaluation. It is not a list of every available model or a permanent ranking.

Key steps:

1. Consult official guidance: Use the latest Models documentation and model comparison resources.
2. Filter candidates: Assess task and modality support, API compatibility, context and output limits, operational constraints, cost, and evaluation readiness.
3. Exclude or hold unsuitable candidates: Remove models that fail mandatory requirements or whose critical constraints cannot yet be verified.
4. Document every candidate: Record its exact model ID, official source, date checked, configuration, and evidence supporting its inclusion.
5. Revisit regularly: Update the shortlist as model capabilities, pricing, availability, and limits change.

For example, GPT-6 Astra should be considered only when its capabilities and deployment requirements fit the workflow. Its reasoning settings and fine-tuning limitations must also be checked against the use case.

Key takeaway: Shortlist models based on verified requirements, not popularity or assumed superiority. Every candidate must pass essential filters before being compared through representative evaluations.

### Summary: Avoid Model-Selection Shortcuts

Model selection must be based on workflow-specific evidence rather than assumptions, popularity, or price alone.

Common shortcuts to avoid:

- Choosing the newest or most capable model: Extra capability may increase cost, latency, and complexity without improving results.
- Choosing the lowest listed price: Compare total cost per successful task, including retries, failed attempts, extra calls, human review, and operational overhead.
- Relying on general benchmarks: Public benchmarks help identify candidates, but representative workflow evaluations are needed to verify real-world performance.
- Reusing old implementation choices: Recheck current model availability, capabilities, and suitability before recommending an existing choice.
- Comparing under different conditions: Use consistent test cases, prompts, output requirements, and scoring criteria wherever possible.
- Failing to record model identity: Record the exact model ID and configuration to make evaluations reproducible.

Selection principle: Choose the least complex model that meets predefined quality, safety, latency, and cost-effectiveness thresholds.

If no candidate meets the requirements, improve the baseline, reconsider the requirements, or defer the decision rather than making an unsupported recommendation.

## Summary: Compare Shortlisted Models Against the Workflow

Model comparison should be based on the same documented workflow requirements so that another technical team can review and reproduce the decision.

### 1. Separate requirements from preferences

- Must-have requirements: Essential conditions such as modality support, API compatibility, Structured Outputs, availability, and context limits.
- Selection preferences: Factors that distinguish viable candidates, such as latency, cost, additional capability, implementation complexity, and review burden.

Remove candidates that fail a must-have requirement. Preferences should only influence decisions among viable candidates.

### 2. Build a model comparison matrix

Compare each candidate against the same requirements and document whether it meets them, meets them with conditions, or remains unverified. Use the findings to identify tradeoffs and outstanding questions.

### 3. Assign a decision position

- Retain: Meets the documented requirements.
- Retain with conditions: Appears suitable, pending confirmation of specific assumptions.
- Remove: Has a documented conflict with a must-have requirement.
- Defer: Evidence is insufficient to make a responsible decision.

A provisional lead may emerge, but it is still a hypothesis until it passes representative evaluations.

### 4. Make the comparison repeatable

Preserve useful existing prompts, business rules, approved inputs, examples, schemas, and tool permissions. Make only necessary compatibility changes, record every difference, and compare candidates using matched test cases and consistent scoring rules.

Record the exact model ID, API interface, reasoning settings, prompt and schema versions, test-case versions, scoring rules, date, results, latency, and cost. Mark unexecuted tests as planned rather than inventing results.

### 5. Carry forward validation questions

Confirm:

- Can the model meet latency and volume requirements?
- Does it produce valid structured outputs consistently?
- How does it handle ambiguous, incomplete, and high-risk inputs?
- What is the total cost per successful task?
- Are review triggers reliable?
- Are model availability, pricing, limits, and interface behavior current?

Key takeaway: Choose a provisional lead based on documented fit and tradeoffs, then validate it through repeatable, matched evaluations. If a test fails, change one targeted instruction at a time and rerun both the failed case and the broader test set to detect regressions.

## Summary: Illustrative Model Comparison

A retail customer wants to automate routing thousands of incoming product-support messages per day. Each API response must return four fields: `routing_label`, `priority`, `reason`, and `needs_review`.

The team shortlists models using current official guidance and evaluates them against the same test cases and predefined criteria:

- Correct routing across common and edge cases.
- Valid structured output with required fields and allowed values.
- Reliable review triggers for ambiguous or high-priority cases.
- Acceptable latency under representative conditions.
- Sustainable total cost per successful task.

### Illustrative results

| Candidate | Evidence                                                                                                                          | Decision                                                      |
| --------- | --------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------- |
| A         | Meets common-case, schema, and latency criteria but misses too many review triggers.                                              | Do not select unless the gap is resolved.                     |
| B         | Meets quality, schema, review-trigger, and latency thresholds, with the lowest cost per successful task among passing candidates. | Recommend as the baseline.                                    |
| C         | Meets quality criteria but adds latency and cost without materially improving success.                                            | Do not use by default without evidence of additional benefit. |

These results are fictional and demonstrate the decision method, not actual model performance.

### Why Candidate B wins

Candidate B is recommended because it satisfies all predefined requirements while offering the strongest task economics among candidates that pass. It is not assumed to be universally superior.

Before implementation, the team should record the exact tested model ID, official source, verification date, configuration, and evaluation evidence.

### When to reconsider the decision

Reevaluate the recommendation if model capabilities or availability change, new test cases reveal quality or safety gaps, workflow requirements change, or another candidate demonstrates materially better results.

Key takeaway: A defensible model recommendation is a dated, evidence-based decision tied to a specific workflow. It must be updated when requirements, available candidates, or evaluation results change.

# Exercise: Shortlist and Compare Model Candidates

Below is a worked example using the internal IT helpdesk triage workflow. It provides a rationale you can adapt for the exercise, while keeping untested performance claims separate from verified facts.

## 1. Define the workflow and requirements

Workflow: An internal API classifies employee IT support requests and returns a structured routing recommendation. It does not retrieve live data or take action in another system.

Required output fields:

- `issue_category`
- `urgency`
- `recommended_queue`
- `needs_review`

Must-have requirements

1. Support the intended text-input and API interface.
2. Return all required fields in the required schema.
3. Use only approved category, urgency, and queue values.
4. Flag ambiguous, incomplete, conflicting, or high-risk requests for review.
5. Treat refusals, blocked responses, and invalid output as failures—not successful routing decisions.
6. Meet defined latency, volume, and cost thresholds.

Preferences include lower cost, faster responses, simpler implementation, and fewer unnecessary reviews.

## 2. Create the current shortlist

Official OpenAI model guidance checked on 19 October 2026 describes a range of candidates for different capability, speed, and cost needs. The following three are reasonable candidates to investigate, not proven winners.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://developers.openai.com\&sz=32)

OpenAI API

+1



| Candidate and exact model ID | Why include it                                                                       | Evidence still needed                                                                      |
| ---------------------------- | ------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------ |
| GPT-6 Luna — `gpt-6-luna`    | Candidate for focused, high-volume classification where cost and speed matter.       | Routing accuracy, review-trigger reliability, latency and total task cost.                 |
| GPT-6.1 Sol — `gpt-6.1-sol`  | Candidate for balancing capability, speed and cost.                                  | Whether additional capability improves ambiguous-case handling enough to justify its cost. |
| GPT-6 Astra — `gpt-6-astra`  | Higher-capability candidate for comparison if its additional reasoning is justified. | Whether it materially improves difficult cases and meets operational constraints.          |

Official sources:

- [OpenAI Models documentation](https://developers.openai.com/api/docs/models?utm_source=chatgpt.com)
- [Using GPT-6: model selection and migration guidance](https://developers.openai.com/api/docs/guides/latest-model?utm_source=chatgpt.com)

Verification note: The official documentation was checked on the date above. Confirm account access, the exact model IDs available to your API project, supported Structured Outputs configuration, regional or residency requirements, current pricing, and rate limits before finalizing the shortlist. The incumbent model is not specified in the exercise, so its exact ID must be added from the existing implementation rather than guessed.

## 3. Define the matched evaluation

Keep the following constant across all candidates:

- Prompt: Same classification rules, category definitions, urgency definitions, and routing policy.
- Approved inputs: The same versioned set of representative employee requests.
- Output schema: The same four required fields, types, and allowed values.
- Review rules: The same conditions requiring human review.
- Scoring: The same expected outputs, pass criteria, and cost-accounting method.

Include ordinary requests, ambiguous or incomplete requests, conflicting information, urgent security-related reports, and invalid or blocked-response cases.

Example test cases:

| Input                                                                       | Expected behavior                                                                                                  |
| --------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| “I can't connect to the office Wi-Fi.”                                      | Route to the network queue; assign urgency using the agreed policy.                                                |
| “My laptop keeps crashing, and I have a client presentation in 20 minutes.” | Consider time sensitivity and impact; apply the defined urgency rules.                                             |
| “I can't access my account.”                                                | Route only if the available information supports it; flag for review if the category or urgency remains ambiguous. |
| “I think someone stole my credentials.”                                     | Apply the security escalation policy and flag for review as required.                                              |
| Empty, malformed, or blocked input                                          | Mark the run as invalid or blocked; never count it as a successful routing decision.                               |

## 4. Record configuration changes

| Item       | What stays fixed                       | What may need to change                                               |
| ---------- | -------------------------------------- | --------------------------------------------------------------------- |
| Prompt     | Business rules and routing definitions | Only targeted compatibility or clarity changes, documented separately |
| Output     | Four fields and allowed values         | Model-specific Structured Outputs configuration                       |
| Reasoning  | Same intended task difficulty          | Supported reasoning setting for each candidate                        |
| API        | Same intended production interface     | API-specific request parameters if required                           |
| Tools      | No external actions or live retrieval  | No extra tools unless requirements change                             |
| Evaluation | Same cases and scoring                 | Record every configuration difference                                 |

The GPT-6 migration guidance notes that reasoning settings and supported parameters differ across models. For example, GPT-6 Astra and GPT-6.1 Sol do not support `none` reasoning effort, while GPT-6 Luna does. Any required change must be documented and evaluated.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://developers.openai.com\&sz=32)

OpenAI API



## 5. Set decision criteria and record results

Use predefined thresholds before running the evaluation. For example, the team might require at least 95% routing accuracy, 100% schema validity for accepted outputs, 100% detection of designated mandatory-review cases, and compliance with an agreed latency and cost budget. These are illustrative thresholds; the organization must approve appropriate values for its risk level.

## Working evaluation rationale

Use this as a working record. No model performance results have been measured in this exercise.

Evaluation status

Planned — no runs executed

In progress — partial runs completed

Complete — evidence available for all candidates

Provisional lead

GPT-6 Luna (`gpt-6-luna`) — cost-sensitive baseline hypothesis

GPT-6.1 Sol (`gpt-6.1-sol`) — balanced-capability hypothesis

GPT-6 Astra (`gpt-6-astra`) — higher-capability hypothesis

Defer — insufficient evidence to nominate a lead

Evidence still needed

What would reverse the preference?

A candidate fails a mandatory-review or structured-output threshold.

Copy rationale

## 6. Recommendation and reflection

Provisional approach: Start by evaluating GPT-6 Luna as a cost-sensitive baseline hypothesis, compare it with GPT-6.1 Sol, and include GPT-6 Astra if it passes all mandatory filters and the additional capability is worth testing. Include the incumbent under the same conditions if its exact ID and compatibility are verified.

This is a proposed evaluation order, not a measured model ranking.

The recommendation should change if Luna misses required review cases, Sol or Astra materially improves successful task completion at acceptable cost, or any candidate fails a mandatory requirement. If no candidate passes, retain the incumbent if it remains compliant or defer the decision.

Final takeaway: A defensible shortlist records exact model IDs and dated official sources; a defensible recommendation additionally requires matched evaluation evidence. Keep planned tests separate from measured results, and never trade away mandatory safety or review behavior for speed or lower cost.