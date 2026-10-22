## Summary: Define Eval Criteria and Test Cases

Evals (evaluations) help teams verify that an API workflow behaves as expected instead of relying only on a reasonable-looking prompt.

Key objectives:

- Define evaluation criteria: Establish measurable standards for expected API behavior.
- Create test cases: Cover normal, risky, malformed, unsupported, and review-triggering scenarios.
- Capture evidence: Record API outputs, tool calls, actions, errors, and approval behavior.
- Categorize failures: Identify where and why the workflow fails.
- Set release criteria: Define which failures are acceptable and which must block release.

What to test: Use earlier assumptions about context, retrieval, tools, actions, and approvals to ensure the eval set covers the full workflow.

Main takeaway: The goal is to gather evidence that the API is reliable, safe, and consistent before release—not merely to confirm that the prompt appears correct.

## Summary: Define Success Criteria

Success criteria specify the measurable requirements an API must meet for a workflow to be considered acceptable. They allow reviewers to compare actual API behavior against expected results.

Key areas to define:

1. Expected API behavior: The API answers, asks for clarification, refuses, escalates, or returns a structured failure at the appropriate time.
2. Output quality and format: Responses meet quality standards and follow the required structure.
3. Evidence requirements: Responses include necessary source references, confidence notes, and review fields.
4. Failure and boundary behavior: The API avoids unsupported claims, unsafe responses, unauthorized actions, and out-of-scope recommendations.
5. Human-review triggers: The API identifies cases requiring human judgment or approval.
6. Acceptance thresholds: Establish clear pass/fail rules for release, pilot, remediation, or escalation.

Key takeaway: Success criteria must be specific, measurable, and testable—not vague statements like “the answer is good.”

Example: For supported policy questions, the API must return an answer with at least one approved source ID, a confidence note, `needs_review: false`, and no unsupported claims.

## Summary: Create Test Cases

Test cases validate whether an API behaves correctly across realistic situations, not just ideal scenarios. Each case should make the expected behavior observable and provide evidence for release decisions.

### Four test case categories

- Normal cases: Verify the API successfully handles supported requests using approved sources.
- Boundary cases: Test missing context, unsupported requests, permission limits, and sensitive topics.
- Failure cases: Check handling of tool failures, malformed outputs, missing evidence, adversarial inputs, and unsupported claims.
- Review cases: Ensure clarification, refusal, escalation, or human review occurs when required.

### What every test case should include

1. Test identification: Test ID, input, and workflow condition.
2. Expected behavior: Answer, clarify, refuse, escalate, or return a structured failure.
3. Evaluation rules: Required output fields, pass/fail criteria, and failure category.
4. Evidence capture: API response, source IDs, confidence notes, tool results, approval events, review handoff, and final application status.

### Example test cases

| Test | Scenario                                   | Expected behavior                                                         |
| ---- | ------------------------------------------ | ------------------------------------------------------------------------- |
| T01  | Supported policy question                  | Answer using approved sources.                                            |
| T02  | User requests unauthorized admin access    | Refuse or direct to the approved access process.                          |
| T03  | Contractor requests restricted data access | Trigger human review.                                                     |
| T04  | No supporting source available             | Return a structured failure or review state.                              |
| T05  | Malformed output                           | Fail validation and retry, block, or use a safe fallback.                 |
| T06  | Policy lookup tool unavailable             | Report failure without inventing sources or eligibility.                  |
| T07  | Response blocked before completion         | Stop dependent actions and preserve the incomplete task state for review. |

### Release validation

A test passes only when the response and the underlying workflow behavior meet the defined requirements. Reviewers must inspect actual tool calls, tool results, permissions, approval events, and handoffs—not just the final answer.

For sensitive access requests, for example, the API should return `answer: null`, set `needs_review: true`, provide a `review_reason`, and trigger the appropriate review workflow. Missing any required control should be treated as a blocking failure when it creates a safety or authorization risk.

Key takeaway: A strong eval set proves that the API handles normal requests reliably, respects boundaries, fails safely, and escalates appropriately. Every test should have clear expected results, measurable pass/fail rules, captured evidence, and defined release impact.


## Summary: Define Failure Categories

Failure categories provide a consistent way to classify API evaluation failures, assess their risk, and decide whether to fix, escalate, or block release.

### Key failure categories

1. Unsupported claim: The API provides an answer without approved supporting evidence.
2. Unsafe or disallowed response: The API fulfills a request it should refuse or handle safely.
3. Incorrect clarification behavior: The API guesses instead of requesting required missing information.
4. Incorrect refusal behavior: The API refuses a valid, supported request without justification.
5. Invalid structured output: The response contains missing fields, incorrect types, invalid enum values, or malformed data.
6. Missed human-review trigger: The API fails to flag sensitive, low-confidence, unsupported, or high-impact cases.
7. Incorrect or unauthorized tool/action behavior: The API uses an unapproved tool, exceeds permissions, or fails without a safe fallback.
8. Customer-facing output before required review: The API produces consequential output before mandatory review or approval.

### Map failures to release decisions

| Failure severity | Example                                                                             | Typical decision                          |
| ---------------- | ----------------------------------------------------------------------------------- | ----------------------------------------- |
| Low              | Minor spelling or formatting issue                                                  | Fix later or permit a limited pilot       |
| Medium           | Incorrect clarification or recoverable validation failure                           | Remediate and retest                      |
| High             | Unsupported policy claim or repeated tool failure                                   | Escalate; potentially block release       |
| Critical         | Missed review trigger, unauthorized action, or consequential output before approval | Block release until resolved and retested |

Severity depends on the workflow's risk and impact; not every instance of a category has the same severity.

Key takeaway: Classify failures consistently, assign severity based on risk, and link each category to a clear remediation and release decision. Safety, authorization, and mandatory-review failures should generally be treated as release blockers.