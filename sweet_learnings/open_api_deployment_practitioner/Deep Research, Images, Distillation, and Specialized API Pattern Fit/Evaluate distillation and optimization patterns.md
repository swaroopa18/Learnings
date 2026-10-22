## Summary: Evaluate Distillation and Optimization Patterns

Distillation and optimization can improve an API solution’s quality, cost, and latency, but they should not be the default solution to every problem.

Before customizing a model, identify the actual root cause. Many issues can be resolved through better system design, including:

- Prompt clarity: Make instructions specific and unambiguous.
- Output contracts: Define the expected format and structure clearly.
- Retrieval quality: Ensure the system retrieves relevant context.
- Tool boundaries: Clarify when and how tools should be used.
- Evaluation coverage: Build sufficient tests to measure performance.
- Model selection: Choose a model that matches the task and required capabilities.
- Data consistency: Ensure input data is reliable and consistent.

### When to consider distillation or optimization

Consider these approaches when you have repeated, measurable quality gaps or demonstrated performance constraints, along with sufficient example data, reliable evaluation methods, and clear operational ownership.

Key takeaway: Diagnose first, measure performance, fix design problems, and use distillation or optimization only when evidence shows they are justified.


## Summary: Start with Simpler Improvements

Before using distillation or advanced optimization, diagnose and improve the existing API workflow first.

### 1. Try simpler improvements first

- Prompt improvement: Clarify instructions and resolve ambiguity.
- Output contract: Define the required response format and fields.
- Retrieval improvement: Improve the relevance and accuracy of retrieved context.
- Tool boundaries: Define when tools should be used and what they should do.
- Eval coverage: Test representative cases and recurring failures.
- Model selection: Revisit the model and its capabilities.
- Data quality: Fix inconsistent or unreliable source data.
- Structured Outputs: Enforce a supported output schema.

### 2. Choose the right design

For workflows such as support-ticket classification, consider two approaches:

- Decisions API + generation: Use Decisions to select a category, then generate a routing note separately. This separates classification from writing.
- Single generation call + Structured Outputs: Generate both the category and note in one call, enforcing the required schema.

Structured Outputs ensures the response follows the schema, but it does not guarantee correct classification or a useful note. Both approaches require clear category definitions and evaluation of category accuracy and note usefulness.

### 3. Follow an evidence-based decision ladder

1. Establish baseline quality, cost, and latency.
2. Identify repeated failure patterns.
3. Apply simpler improvements.
4. Evaluate results against clear criteria.
5. Consider distillation or optimization only if significant gaps remain.
6. Confirm approved training data, operational ownership, and an available training route.

### 4. Important fine-tuning consideration

Fine-tuning availability is changing. According to the provided material, new training jobs are subject to eligibility restrictions, and new job creation for active existing customers is scheduled to end on January 6, 2027. Existing fine-tuned models can continue running until their underlying base models are deprecated.

Verify current organizational eligibility, recent fine-tuned-model usage, base-model lifecycle, and official guidance before proposing fine-tuning or distillation.

Key takeaway: Define, test, and improve the existing workflow before adding the cost and maintenance burden of a specialized approach. Distillation and optimization should be justified by evidence, not assumed to be the first solution.


## Summary: Real-World Example — Avoiding Premature Distillation

A customer-support team uses an API to classify tickets and draft routing notes. Most results are good, but some categories repeatedly produce errors, while high usage increases cost and latency.

The right approach is to diagnose first, then optimize if necessary.

1. Clarify categories: Make ticket labels distinct, clear, and stable.
2. Check context: Ensure the model receives relevant ticket details, policies, and examples.
3. Improve the output contract: Define required fields, confidence signals, reason codes, and fallback behavior.
4. Analyze failure patterns: Identify which categories and edge cases cause errors.
5. Establish evaluation baselines: Measure classification accuracy and routing-note usefulness separately.
6. Measure performance: Track cost, latency, throughput, and reliability.

### Choose improvements based on the cause

| Observed problem                           | First action                          |
| ------------------------------------------ | ------------------------------------- |
| Overlapping categories                     | Refine the taxonomy                   |
| Missing or irrelevant context              | Improve retrieval and source data     |
| Inconsistent response formats              | Use Structured Outputs                |
| Unclear failure patterns                   | Expand evaluations                    |
| Good quality but excessive cost or latency | Evaluate optimization or distillation |

### Decisions API versus a single generation call

- Decisions API + separate note generation: Classify the ticket first, then generate its routing note independently.
- Single generation call + Structured Outputs: Generate both the category and note in one schema-constrained response.

In either design, a correct category does not guarantee a useful routing note. Evaluate both independently.

For ambiguous tickets, unsupported categories, and refusals, define a review or fallback path. Set routing thresholds using labeled examples and the consequences of misclassification rather than arbitrary confidence cutoffs.

Key takeaway: Fix quality problems before optimizing performance. If quality meets its targets but cost or latency remains unacceptable, evaluate optimization or distillation against explicit performance goals and acceptable quality-loss limits, with clear operational ownership.

## Summary: Distillation Fit

Distillation is suitable when an existing workflow works reliably but needs to become faster, cheaper, or easier to scale.

### Key points

1. Validate the existing workflow: Ensure the teacher consistently produces the desired behavior.
2. Define the goal: Identify measurable improvements in cost, latency, throughput, or scalability.
3. Prepare quality examples: Collect reviewed, accurate, and approved teacher outputs.
4. Evaluate the student: Compare teacher and student using the same test cases and held-out evaluation data.
5. Set quality thresholds: Define acceptable quality loss before testing.
6. Assign ownership: Ensure a team can maintain, version, monitor, and retest the solution.
7. Verify feasibility: Confirm that an appropriate training route and organizational eligibility are available.

### Decision rule

- Proceed: Quality requirements are met and efficiency improves sufficiently.
- Revise or reject: The student fails essential behaviors or does not deliver the expected gains.
- Defer: The original workflow, evaluation criteria, training route, or ownership is not ready.

Key takeaway: Distillation should preserve proven behavior while improving a measurable operational constraint. Never make a workflow faster or cheaper at the expense of unacceptable quality loss.

## Summary: Optimization Fit

Optimization is appropriate when a team can identify a specific, measurable problem in an API workflow and verify that changes improve it.

Unlike distillation, which focuses on transferring behavior to a smaller or cheaper approach, optimization can improve many parts of the existing workflow, including prompts, models, retrieval, tools, output schemas, caching, monitoring, and evaluation.

### 1. When is optimization justified?

- Quality gap: Repeated, measurable errors occur.
- Performance constraint: Latency, reliability, throughput, or output consistency fails to meet requirements.
- Cost or scale pressure: The workflow is too expensive at expected usage volumes.
- Known bottleneck: Evidence identifies where improvement is needed.
- Baseline and evaluations: The current and optimized versions can be compared.
- Ownership: A team is responsible for testing, monitoring, and maintenance.

### 2. Define a measurable goal

Avoid vague goals such as “make it faster” or “make it cheaper.”

Example: Reduce average response latency for support-ticket routing while maintaining routing accuracy, valid structured outputs, and an acceptable human-review rate.

### 3. Use observability

Track sufficient operational evidence to understand and compare workflow behavior.

Useful metrics include:

- Request ID and release version
- Model and configuration used
- Latency and token usage or cost
- Success and error categories
- Output-contract validity
- Human-review and fallback rates
- Quality and evaluation results

Logs should be designed to protect sensitive data.

### 4. Compare the baseline with the optimized version

1. Measure the current workflow.
2. Identify the bottleneck.
3. Change the relevant component.
4. Test both versions on equivalent cases.
5. Compare performance and quality against predefined thresholds.
6. Accept the change only if it delivers the intended improvement without unacceptable regressions.

Important: A successful API call does not necessarily mean the output is correct. Evaluation must include incorrect answers, invalid formats, errors, and human-review outcomes.

### Key takeaway

Optimization should be evidence-driven, measurable, and controlled. Define what must improve, establish a baseline, collect reliable metrics, and preserve essential quality requirements. Only adopt changes when evaluation demonstrates that the tradeoff is worthwhile.

## Summary: Choosing the Right Optimization Path

Choose the simplest change that addresses the measured problem, and use evaluations to prove it works.

### 1. Match the problem to the solution

| Problem                 | Try first                                                  | Consider deeper optimization when…                               |
| ----------------------- | ---------------------------------------------------------- | ---------------------------------------------------------------- |
| Inconsistent outputs    | Improve prompts, schemas, examples, and fallback rules     | Clear requirements and evals show simpler fixes are insufficient |
| Weak retrieval          | Improve source quality, chunking, metadata, and filters    | Retrieval is validated, but cost or latency remains a blocker    |
| Unreliable tool use     | Clarify tool boundaries, schemas, and error handling       | Tool behavior is stable but performance still needs improvement  |
| High latency            | Revisit model selection, context size, and workflow steps  | Quality is acceptable but latency still misses the target        |
| High cost               | Reduce unnecessary context, tool calls, and duplicate work | A cheaper approach can preserve acceptable quality               |
| Increasing scale        | Review throughput, caching, fallbacks, and monitoring      | The workflow is stable and changes can be evaluated safely       |
| Overly complex workflow | Simplify architecture, context, and tool usage             | A validated approach can serve as the quality reference          |

### 2. Distinguish model choice from processing mode

- Model comparison: Determines which model best meets quality, cost, and latency requirements.
- Processing-mode comparison: Tests whether a different processing option for the same model improves speed enough to justify its cost.

To isolate processing-mode effects, keep the model, prompt, reasoning settings, test cases, and acceptance criteria fixed. Record cache, transport, and load conditions as well.

### 3. Measure the complete workflow

For a category-plus-note workflow, count success only when both the category and the routing note meet their quality criteria.

Measure total cost and time, including:

- All API calls
- Failed attempts and retries
- Human review
- Classification and note generation

A faster classification step may not improve end-to-end latency if note generation or human review dominates.

Apply the correct pricing to each endpoint. For example, a Decisions classification call and a separate generation call have different billing components. Evaluate the combined cost before claiming savings.

### 4. Follow an evidence-based decision process

1. Identify the specific constraint.
2. Establish baseline metrics.
3. Try the lowest-complexity improvement first.
4. Evaluate quality, latency, cost, and reliability.
5. Consider deeper optimization or distillation if simpler changes are insufficient.
6. Define monitoring, rollback, and operational ownership before deployment.

Key takeaway: Don't simply recommend “optimization.” Specify the problem, the first change to try, the metrics and quality thresholds for acceptance, and who will monitor and maintain the solution.

## Summary: Identify Tradeoffs and Ownership

Distillation and optimization can improve an API workflow, but they may introduce tradeoffs in quality, cost, latency, reliability, and maintainability.

### 1. Evaluate the major tradeoffs

| Area                 | Key question                                                   |
| -------------------- | -------------------------------------------------------------- |
| Quality              | What quality must be preserved, and what loss is unacceptable? |
| Cost                 | What is the target, and how will spending be measured?         |
| Latency              | What response time is required?                                |
| Throughput and scale | What volume or concurrency must the system support?            |
| Reliability          | Could optimization introduce new failure modes?                |
| Maintainability      | Can future teams understand and support the design?            |
| Governance           | What approvals and documentation are required?                 |
| Version management   | How will changes be tracked and rolled back?                   |
| Evaluation           | Which tests prove the change works?                            |
| Ownership            | Who monitors, retests, and maintains the workflow?             |

### 2. Define operational ownership

The responsible team must:

- Monitor quality: Track output correctness and consistency.
- Monitor performance: Measure cost, latency, throughput, and reliability.
- Retest after changes: Re-run evaluations when prompts, models, tools, data, policies, or requirements change.
- Manage versions: Document changes and maintain rollback options.
- Detect failures and drift: Identify recurring errors and declining quality.
- Decide when to act: Update, pause, roll back, or escalate the workflow when necessary.

### 3. Deployment readiness

Before deploying a specialized pattern, establish:

1. Clear quality and performance targets.
2. Defined evaluation criteria and monitoring metrics.
3. A named operational owner.
4. Change approval and version-control procedures.
5. A documented rollback and escalation plan.

Key takeaway: An optimization is not deployment-ready simply because it improves cost or latency. It must meet quality requirements, have acceptable tradeoffs, and include clear ownership for monitoring, maintenance, evaluation, and rollback.