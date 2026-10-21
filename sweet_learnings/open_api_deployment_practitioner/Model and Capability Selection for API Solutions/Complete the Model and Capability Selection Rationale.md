The Model and Capability Selection Rationale consolidates the workflow requirements, shortlisted models, comparison results, and stress-test findings into a concise, customer-ready technical recommendation.

It should document:

- Current shortlist: Candidate models and their relevant capabilities.
- Verified sources and date: Evidence supporting model capabilities, pricing, latency, and availability.
- Evaluation evidence: Results from task-specific evaluations and stress tests covering quality, reliability, safety, and validation.
- Final recommendation: The selected model and why it fits the workflow requirements.
- Rejected candidates: Alternatives not selected and the reasons for rejection.
- Trade-offs: Cost, latency, quality, reliability, and implementation complexity.
- Volatile product facts: Pricing, rate limits, model availability, and other details that may change.
- Risks and mitigations: Known limitations, failure modes, safety concerns, and validation requirements.
- Next review area: The assumptions, metrics, or product changes to reassess during the next review.

Outcome: A defensible, evidence-based rationale that explains not just which model was selected, but why it is the best fit for the workflow, what trade-offs were accepted, and what conditions would trigger reconsideration.


## Summary: Model and Capability Selection Rationale

A Model and Capability Selection Rationale is a decision document that explains why a particular model, API capability, or solution pattern is suitable for a specific workflow, based on evidence and requirements.

### Key sections to include

1. Workflow and business value: Define the task, expected outcome, and customer benefit.
2. Inputs, outputs, and capabilities: Specify modalities, required model capabilities, and interface or API contract requirements.
3. Candidate patterns and recommendation: Compare viable approaches, recommend the simplest effective pattern, and explain why alternatives were rejected.
4. Tradeoffs and risks: Assess cost, latency, scale, reliability, safety, review effort, and unresolved assumptions.
5. Validation and next steps: Identify the evidence required before building, piloting, or expanding the solution, and specify the next review area.

### What the comparison record must capture

- Incumbent prompt and version, candidate model IDs, and supported reasoning settings.
- Approved inputs, tool permissions, and compatibility changes.
- Per-run quality scores, review scores, latency, usage and tool costs, retries, and reviewer effort.
- Whether evidence is measured or planned.
- Prompt changes linked to specific failures and regression tests.
- Evidence that would cause the recommendation to be reversed.

### How to make the recommendation

Recommend a candidate only when it meets predefined requirements for task quality, output correctness, safety, review behavior, and latency. Among candidates that pass, compare total cost per successful task, rather than simply comparing model prices.

Reject alternatives based on specific evidence, and revalidate model IDs, supported capabilities, pricing, and limits before implementation.

Core principle: The rationale is a workflow-specific, evidence-based decision—not a universal model ranking, product overview, final architecture, or production deployment plan.

## Summary: Make the Model and Capability Selection Rationale Defensible

A defensible rationale explains why a solution fits the workflow, what evidence supports the choice, what assumptions remain, and what would change the recommendation.

### Core principles

1\. Use the current model catalog. Record exact model IDs, official sources, and verification dates. Treat model availability, capabilities, limits, and pricing as changeable facts—not permanent rankings.

2\. Use durable decision criteria. Evaluate task type, input/output modality, reasoning needs, context requirements, output structure, latency, throughput, cost, reliability, safety, operational risk, and validation evidence.

3\. Separate decision logic from product facts. The workflow requirements should remain stable even when model offerings, API behavior, pricing, or limits change.

4\. Make assumptions explicit. Before build, confirm model and API compatibility, structured-output behavior, modality and tool support, pricing, rate limits, data handling, safety, performance expectations, and review ownership.

5\. Identify the next review area. Route unresolved issues to the appropriate team: security and governance, retrieval readiness, tool and action design, evaluation and guardrails, observability, or production readiness.

6\. Document what would change the recommendation. Define evidence-based conditions for switching patterns or candidates, such as failed quality thresholds, excessive latency, higher cost per successful task, new data sensitivity, or the need for retrieval or live tool access.

### Example of defensible wording

> The current model catalog was checked on [verification date]. The selected candidate met the predefined quality, structured-output, review-trigger, latency, and cost-per-successful-task thresholds in representative workflow tests. The recommendation is conditional on confirming current model availability, API compatibility, pricing, limits, and data-handling requirements before build. If further evaluation shows that a simpler baseline meets the same requirements at lower cost, or that the selected candidate fails under peak load, the recommendation will be revisited.

### Final takeaway

A strong rationale is evidence-based, conditional, maintainable, and open to challenge. It distinguishes stable workflow requirements from volatile product facts, records the evidence behind the selection, and specifies both the next review steps and the conditions that would reverse the decision.

## Summary: Turn model-selection evidence into a customer-ready recommendation

For the retail support workflow, the goal is to reduce manual triage through accurate, consistent, low-latency structured classification while escalating ambiguous or high-priority cases to human reviewers.

### Recommended approach

- Workflow pattern: Structured classification with structured output.
- Required fields: `routing_label`, `priority`, `reason`, and `needs_review`.
- Selection method: Test shortlisted model candidates on the same representative cases and compare quality, schema compliance, review-trigger behavior, latency, and total cost per successful task.
- Human oversight: Route ambiguous, high-priority, and otherwise flagged cases for review.
- Alternative patterns: Defer retrieval, tool use, agentic workflows, and specialized optimization unless the workflow requirements or evaluation evidence justify them.

### What makes the recommendation defensible?

1. Evidence: Use representative evaluation results rather than model reputation or a general ranking.
2. Economics: Compare the total cost of successfully completed tasks, including retries and human-review effort where measurable.
3. Explicit risks: Validate incorrect routing, missed review triggers, invalid output, peak-volume latency, and changing label definitions.
4. Current product facts: Record exact tested model IDs, official documentation sources, verification dates, supported interfaces, pricing, and limits.
5. Reversal criteria: Reconsider the choice if it fails quality or latency thresholds, another candidate delivers better task economics, or requirements change.

### Customer-ready recommendation

> We recommend structured classification with structured output as the baseline for the retail product-support workflow. The specific model candidate should be selected based on representative evaluation evidence demonstrating that it meets the required routing-quality, output-validity, review-trigger, latency, and cost thresholds. Before build, we will confirm the exact model ID, current API compatibility, pricing, limits, and data-handling requirements. We will revisit the selection if evaluation results or operational constraints show that another candidate or capability pattern better meets the customer’s requirements.

Key takeaway: Recommend the simplest pattern that meets the workflow requirements, support the model choice with measurable evidence, and document what would cause the decision to change. The fictional candidate results in the example should not be presented as real model-performance claims.



