### Summary: Design Moderation, Guardrails, and Human Review

API workflows need a guardrail control layer to prevent unsafe, unsupported, malformed, or sensitive outputs from proceeding unchecked.

Key concepts include:

- Moderation checks: Detect harmful or inappropriate content.
- Guardrails: Enforce safety rules, business policies, and restrictions.
- Structured-output checks: Validate that API responses follow the required format and schema.
- Human review: Send uncertain, high-risk, or flagged outputs to a person for approval.
- Escalation rules: Define when and how failed checks or high-risk cases are escalated.

Main objective: Decide where each control runs, what it checks, what result it returns, and how the application responds when a check passes, fails, or requires human review.

### Summary: Add Moderation and Safety Checks

OpenAI moderation models help identify potentially harmful content in supported text and image inputs. However, moderation is only one layer of a complete safety system and cannot replace application-specific rules or human judgment.

Key controls to implement:

- Unsafe or disallowed content: Use moderation checks and safety policies.
- Sensitive or high-impact content: Apply stricter validation and human review where needed.
- Customer-specific policies: Enforce customer rules, authorization, and approved-use constraints.
- Misuse or adversarial inputs: Detect attempts to bypass instructions or manipulate the workflow.
- Output risk: Validate responses before displaying, storing, sending, or acting on them.

Main takeaway: Build a layered safety system using moderation, deterministic guardrails, evaluators, authorization checks, human review, and escalation rules. Define which control owns each decision, test expected behavior, and retest after changes.

## Summary: Add Guardrails

Guardrails are enforceable rules and controls that keep API workflows within approved boundaries. They must be specific enough to implement, test, audit, and review—not just general instructions such as “be safe.”

### Six essential guardrail categories

1. Scope boundary: Define what the API can answer, what it must refuse, and when it should ask for clarification.
2. Source-use boundary: Restrict answers to approved sources, verify citations support claims, and trigger review when evidence is missing.
3. Structured-output boundary: Validate required fields, permitted values, data types, formats, and review indicators.
4. Evidence and uncertainty boundary: Route answers for review when evidence is missing, conflicting, or fails a defined evaluation threshold. Do not rely solely on the model’s self-reported confidence.
5. Tool/action boundary: Define which tools and actions are allowed, restricted, approval-only, or prohibited.
6. Customer-facing boundary: Specify which outputs must be reviewed before being displayed, sent, or used to trigger downstream actions.

### Deployment-ready guardrail format

| Field             | What to define                                                                                   |
| ----------------- | ------------------------------------------------------------------------------------------------ |
| Boundary          | The behavior, source, output, tool, action, or risk being controlled                             |
| Trigger           | The exact condition that activates the guardrail                                                 |
| Check location    | Before generation, after generation, before action, before display, or before downstream routing |
| Expected behavior | Continue, clarify, refuse, retry, block, review, or escalate                                     |
| Evidence captured | Validation results, failure categories, source IDs, review decisions, and release-gate evidence  |
| Owner             | The person or team responsible for remediation, review, escalation, or risk acceptance           |

### Example: Source-support guardrail

If a policy answer has no approved source references, the application should:

- Block final display.
- Mark the answer as requiring review.
- Route it to the policy owner.
- Record the failure reason and control outcome.

Importantly, having citations is not enough. The application must verify that the sources are approved and that their content actually supports the answer.

Main takeaway: A guardrail is effective only when the application enforces it and tests verify that the expected behavior occurs. Defining a rule in JSON alone does not enforce the rule.

## Summary: Designing a Guardrail Control Flow

A guardrail control flow is a sequence of checks that determines whether an API response can be approved, revised, blocked, or sent for human review. Model-generated output must not be trusted until all required validations pass.

### Recommended control flow

1\. Receive user request

2\. Input safety and scope checks

Block disallowed requests or ask for clarification.

3\. Generate response

Stop dependent actions if generation is incomplete or blocked.

4\. Validate structured output

Check schema, required fields, types, and values.

5\. Validate source support

Verify sources are approved and support the claims.

6\. Check action permissions and review triggers

Evaluate high-impact risks and approval requirements.

All checks pass

Approve output and permit authorized next steps.

Review required

Block final release and escalate to a human reviewer.

7\. Record evidence and outcomes

Log validation results, failure reasons, review decisions, and retesting requirements.

### Key implementation rules

- Moderation and scope: Block unsafe or disallowed requests before generation when possible.
- Schema failures: Retry with correction if permitted, or block and route to review. Never release malformed output.
- Source failures: Missing, unapproved, unverifiable, or unsupported sources must trigger the defined failure path.
- Review-field consistency: Preserve an existing `needs_review=true` flag and its valid reason. If the reason is missing or blank, supply an allowed reason for a known trigger; otherwise use `malformed_output` and record the missing explanation.
- Tool and action permissions: Validate authorization and approval requirements before executing actions, not just before displaying the answer.
- Human review: Any required-review path must reach the review process, never the normal approval path.
- Logging and testing: Record failures and outcomes, and test individual triggers and combinations of triggers.

Main takeaway: Guardrails work as a coordinated, enforceable pipeline. The application—not the model alone—must decide whether an output can proceed, requires correction, must be blocked, or needs human approval. The example pseudocode is illustrative; its helper functions must be implemented and tested against the actual deployment architecture.

## Summary: Add Structured-Output Checks

Structured-output checks validate that API responses contain the correct fields, valid values, and consistent review decisions before they move downstream. Valid JSON alone does not guarantee that an answer is safe, supported, or authorized.

### What to validate

1. Required fields: Confirm fields such as `answer`, `source_ids`, `confidence_note`, `needs_review`, and `review_reason` are present.
2. Allowed types and values: Check data types, permitted values, and allowed review-reason categories.
3. Source support: Require valid, approved source references whenever evidence is necessary.
4. Review consistency: Ensure sensitive, uncertain, or high-risk cases cannot bypass required review.
5. Invalid-output handling: Block, retry within defined limits, use an approved fallback, or route to human review.
6. Downstream compatibility: Ensure other systems can interpret the output without ambiguity.

### Example validation rules

| Condition                                  | Expected behavior                                                |
| ------------------------------------------ | ---------------------------------------------------------------- |
| Required field is missing                  | Block output and route to review                                 |
| `review_reason` is not an allowed value    | Reject the field and prevent incorrect routing                   |
| Required source IDs are missing            | Prevent final display and trigger review                         |
| `needs_review` is missing                  | Reject output; never guess the review decision                   |
| High-risk answer has `needs_review: false` | Fail cross-field validation                                      |
| All checks pass                            | Continue only if other safety and authorization checks also pass |

### Key lesson

Structured-output validation must check consistency between fields, not just whether the fields exist.

For example, a response about restricted data that has no source references but sets `needs_review` to `false` must fail validation—even if the JSON is perfectly formatted.

Also, a model-generated confidence note is not proof that an answer is correct. Use approved evidence, deterministic checks, defined evaluation thresholds, and human review where appropriate.

Main takeaway: Never pass an output downstream merely because it matches the expected format. Validate its structure, evidence, permissions, and review requirements before allowing it to proceed.

## Summary: Add Human Review

Human review should be a defined workflow control, not an improvised response to risky output. Every review point must specify when review is required, who is responsible, what evidence is needed, what decisions are allowed, and what happens next.

### When to require human review

- Missing evidence or unsupported answers.
- Low-confidence or uncertain results.
- Sensitive, unsafe, or high-impact requests.
- Customer-facing outputs that require approval.
- Malformed or unreliable API responses.
- Tool calls or actions with real-world consequences.
- Cases where the implementation team cannot independently assess the risk.

### Four essential elements of human review

| Element               | What to define                                                                                                |
| --------------------- | ------------------------------------------------------------------------------------------------------------- |
| Trigger               | The exact condition that requires review.                                                                     |
| Owner and timing      | Who reviews the case and whether approval is needed before a response, action, or release.                    |
| Evidence and decision | What the reviewer sees and whether they can approve, reject, edit, request more evidence, pause, or escalate. |
| Fallback and record   | What happens if review is delayed, unavailable, or denied, and what audit evidence is retained.               |

### Example review workflow

For an API-generated answer that lacks approved source evidence:

1. Detect the missing or unsupported evidence.
2. Block the final answer from being displayed.
3. Send the request, draft response, source status, and review reason to the policy owner.
4. Allow the reviewer to approve, revise, reject, or request additional evidence.
5. Keep the answer on hold until the required review is completed.
6. Record the review status and decision while minimizing sensitive information in logs.

### Key deployment rules

- Fail safely: If required approval is unavailable, delayed, denied, or unresolved, do not proceed with the protected response or action.
- Review before action: Require approval before consequential tool calls, such as sending, deleting, provisioning, or updating records.
- Preserve evidence: Record the trigger, owner, decision, timestamp, and escalation status, while redacting unnecessary sensitive details.
- Test every path: Verify that expected cases reach review and that denied or unresolved cases never reach the normal approval path.

Main takeaway: Human review is effective when it has a clear trigger, accountable owner, sufficient evidence, defined decisions, a safe fallback, and a verifiable audit trail.

## Summary: Connect Controls to Failure Categories

Controls are most effective when each one is linked to a specific workflow risk, a detectable failure condition, an expected response, and a clear release decision.

### Control-mapping framework

| Field                      | Purpose                                                                                                                                           |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| Risk                       | Identify what could go wrong.                                                                                                                     |
| Failure category           | Classify the type of failure.                                                                                                                     |
| Control and check location | Specify the control and when it runs.                                                                                                             |
| Trigger                    | Define the condition that activates the control.                                                                                                  |
| Expected workflow behavior | Specify whether to block, retry, clarify, review, or escalate.                                                                                    |
| Owner and release impact   | Assign responsibility and decide whether release is blocked, remediation is required, conditional release is allowed, or escalation is necessary. |

### Practical examples

| Risk                                     | Failure category                  | Required control and behavior                                                          |
| ---------------------------------------- | --------------------------------- | -------------------------------------------------------------------------------------- |
| Policy answer lacks approved evidence    | Unsupported claim                 | Validate sources after generation; block final display and route to policy review.     |
| API returns malformed output             | Invalid structured output         | Validate schema; block, retry within limits, or route to review.                       |
| Restricted-data guidance bypasses review | Missed review trigger             | Apply a human-review gate before response or action.                                   |
| API proposes an unauthorized action      | Unauthorized tool/action behavior | Check permissions before execution; block unauthorized actions and record the failure. |

### Release-readiness rules

- Block release when a critical safety control or required review gate fails.
- Require remediation when output validation or downstream compatibility is unreliable.
- Allow conditional release only when residual risks are explicitly accepted by an authorized owner and applicable requirements permit it.
- Escalate when risk ownership or the appropriate decision is unclear.

Main takeaway: Every control must connect a risk to an enforceable check, a predictable workflow response, an accountable owner, and a testable release decision. Eval owners should verify both that controls activate when required and that failures cannot bypass the release gate.