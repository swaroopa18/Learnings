Prompt design defines how an API should behave, including what it should do, avoid, when to clarify, refuse, provide safe alternatives, or escalate for review.

A strong prompt should specify:

- Purpose: The expected task and outcome.
- Output structure: Required fields, formats, and constraints.
- Evidence: Information needed to support responses.
- Safety rules: When to refuse or safely complete requests.
- Escalation: When human review is necessary.
- Evaluation criteria: Clear success and failure conditions for testing before launch.

Key takeaway: Clear, testable prompt requirements make API behavior reliable, safe, and easier to evaluate before deployment.

## Summary: Key Validation Concepts

- Eval: A structured test to check whether the API behaves as expected using test cases, expected and actual results, pass/fail evidence, and identified gaps.
- Moderation and application safety checks: Detect harmful content and apply additional application-specific rules for authorization, approved sources, sensitive contexts, and human review.
- Guardrail: A rule or control that keeps API behavior within approved boundaries, including when to answer, clarify, refuse, or escalate.
- Structured-output validation: Ensures API responses follow the required schema, field rules, and review indicators. Structured Outputs can enforce supported JSON Schemas, while JSON mode alone guarantees only valid JSON.
- Human review: A person or accountable team checks an output or decision before it is used or acted upon.
- Release gate: A checkpoint that determines whether the API is ready to launch, needs fixes, requires conditions, or should be paused.
- Retest trigger: Any significant change to the prompt, model, sources, tools, schema, moderation, guardrails, or review thresholds that requires validation again.

Key takeaway: Reliable API deployment requires clear tests, safety controls, valid structured outputs, human oversight when needed, defined release criteria, and retesting after significant changes.

## Summary: Define Prompt Purpose

A prompt purpose clearly defines what an API should do, what it should produce, and how it should behave in uncertain or unsafe situations.

A strong prompt purpose answers four questions:

1. Workflow role: What task does the API support, and what outcome should it achieve?
2. Expected output: What should it return, and in what format or structure?
3. Behavior boundary: What must the API avoid claiming, recommending, exposing, or executing?
4. Safe failure behavior: When should it answer, clarify, refuse, provide a safe alternative, escalate, or request human review?

### Example

Weak prompt: “Answer employee policy questions.”

Strong prompt: “Answer employee policy questions using only approved sources. Return a structured response with the answer, source IDs, confidence note, review flag, and review reason. Ask for clarification when information is incomplete. Refuse unsafe or out-of-scope requests and trigger human review for sensitive, unsupported, or low-confidence answers.”

### What makes the stronger prompt better?

- Defines approved evidence sources.
- Specifies required output fields.
- Prevents guessing when information is incomplete.
- Establishes safety boundaries.
- Defines when human review is required.

Key takeaway: A clear prompt purpose makes API behavior measurable and testable. It provides the foundation for creating evaluation cases, identifying failures, and deciding whether the API is ready for release.

## Summary: Define Expected Behavior

Expected behavior defines how an API should respond to different situations, making its behavior measurable and testable.

There are five main response paths:

1. Answer: Provide a supported answer when the request is in scope, evidence is available, and the required output format can be met.
2. Clarify: Ask for missing or ambiguous information instead of guessing.
3. Refuse or safe-complete: Decline unsafe or out-of-scope requests and offer a safe alternative when appropriate.
4. Escalate: Route sensitive, high-risk, unsupported, or review-required cases to the appropriate human reviewer with supporting evidence.
5. Return structured failure: Provide a predefined failure status when evidence, permissions, formatting, or tools prevent successful completion.

### Important validation principles

- Test whether the API follows the correct response path, not just whether its answer sounds good.
- Require evidence from approved sources and the correct structured fields.
- Separate what the API may explain from what it is permitted to do. For example, it may explain employee access policies but must not grant access without authorization.
- Never allow the API to invent evidence, conceal failed lookups, or bypass required reviews.

Key takeaway: Define expected behavior for normal, incomplete, unsafe, unsupported, and failed requests before deployment. This creates clear evaluation criteria and helps determine whether the API is safe and ready to launch.

## Summary: Define Structured-Output Expectations

Structured outputs make API responses consistent, machine-readable, and easier to validate, integrate, and route through downstream systems. They are a reliability and integration control, not just a formatting preference.

### Five things to define

1. Required response fields: Specify which fields must always be returned, such as `answer`, `source_ids`, `needs_review`, and `review_reason`.
2. Field rules: Define each field’s data type, allowed values, format, and meaning.
3. Evidence and review fields: Include source references, uncertainty notes, review status, and reasons for escalation.
4. Downstream system needs: Ensure fields meet the requirements of applications, databases, tools, ticketing systems, and review workflows.
5. Invalid-output behavior: Define how to handle malformed or truncated JSON, missing fields, unsupported values, refusals, and failed validation.

### Example: Successful response

```
{
  "answer": "Access requires manager approval.",
  "source_ids": ["policy_access_004"],
  "confidence_note": "Supported by an approved policy source.",
  "needs_review": false,
  "review_reason": null
}
```

### Example: Unsupported response requiring review

```
{
  "answer": null,
  "source_ids": [],
  "confidence_note": "No approved source supports the answer.",
  "needs_review": true,
  "review_reason": "missing_source_support"
}
```

The second response tells downstream systems not to treat the answer as final and to route the case for review.

### Important distinctions

- Structured Outputs: Can enforce a supported JSON Schema.
- JSON mode: Ensures valid JSON, but does not guarantee compliance with a specific schema.
- Application validation: Still needs to check safety, permissions, required fields, application state, and review outcomes.
- Confidence notes: Are explanatory text, not calibrated confidence scores. Low-confidence triggers should rely on defined evidence rules, validated evaluators, or human review.

Key takeaway: Define the required schema, evidence fields, review signals, and failure-handling rules before deployment so every response can be reliably validated and safely processed by downstream systems.

## Summary: Define Prompt Failure Examples

Prompt failure examples identify behaviors that must be caught during validation before an API is released. They turn vague risks into concrete, testable evaluation cases.

### Common failure examples

1. Unsupported or overconfident answers: Claims are made without required evidence or approved sources.
2. Unsafe or out-of-scope responses: The API provides prohibited information or exceeds its approved role.
3. Invalid structured output: Required fields are missing, data types are incorrect, or the response violates the schema.
4. Incorrect clarification or refusal: The API guesses when information is missing or fails to refuse an unsafe request.
5. Missed escalation: Sensitive, high-risk, or unsupported cases are not routed for human review.
6. Unauthorized tool actions: The API performs actions without permission or executes the wrong action.
7. Premature customer-facing answers: A response is shown or acted upon before required human review.

### Example

A policy-support API answers a sensitive employment question without source IDs and fails to set `needs_review` to `true`.

Why this is a failure: The API skipped required evidence and review procedures, even if its answer sounds reasonable.

Key takeaway: Every identified failure should become an evaluation test with a defined input, expected behavior, actual result, and pass/fail criteria. This helps teams detect unsafe, unsupported, or unreliable behavior before release.

## Summary: Real-World Example — Prompt Behavior and Structured Outputs

An enterprise IT team builds an API to answer employee questions about internal software access using only approved IT access policies.

### Required output fields

- `answer` — The supported answer to the employee.
- `source_ids` — IDs of approved policy sources used.
- `confidence_note` — An explanation of the available evidence or uncertainty.
- `needs_review` — A Boolean indicating whether human review is required.
- `review_reason` — The reason for review, or `null` if no review is needed.

### Expected API behavior

1. Answer: Provide an answer when approved sources support it.
2. Clarify: Ask for missing details, such as the tool, department, role, or business reason.
3. Refuse: Decline requests to bypass access controls or violate policy.
4. Escalate: Trigger human review for sensitive datasets, unclear eligibility, missing evidence, or access-provisioning requests.
5. Return structured output: Include all required fields so downstream systems can validate and process the response.

### Key takeaway

A well-designed prompt defines both what the API should say and what actions it must take in different situations. These rules make the workflow testable, improve reliability and safety, and help determine whether the API is ready for deployment.