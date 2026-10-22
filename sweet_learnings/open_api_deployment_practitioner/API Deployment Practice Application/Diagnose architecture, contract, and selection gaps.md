### Summary: Diagnose Architecture, Contract, and Selection Gaps

This module focuses on evaluating whether the current Employee Policy API is ready for a safe pilot deployment using the Northstar case evidence.

The review covers three key areas:

1. Architecture fit: Check whether the API architecture meets the business requirements and supports safe, reliable deployment.
2. Contract quality: Assess whether API endpoints, inputs, outputs, error responses, and validation rules are clearly defined and consistent.
3. Selection rationale: Verify that the chosen API design and technology are supported by clear evidence and justified against alternatives.

Goal: Identify design gaps and deployment risks that could affect pilot readiness, then use the findings to support an evidence-based deployment recommendation without redesigning the API from scratch.

### Summary: Northstar API Architecture Evidence

Northstar’s Employee Policy API uses a retrieval-grounded approach to answer employee questions about HR, travel, benefits, and IT policies through the employee portal and mobile app.

- Request fields: `question`, `user_id`, `user_role`, `region`, and `channel`.
- Response fields: `answer`, `source_titles`, `confidence_label`, and `next_step`.
- Architecture fit: The design is reasonable for routine employee self-service because answers are grounded in approved policy documents.
- Key architecture gaps: The contract does not define safe behavior for missing, outdated, region-specific, role-specific, restricted, ambiguous, or unsupported policy content.
- Confidence handling: Northstar must define who assigns `confidence_label`, the evidence behind each value, and the resulting portal or human-review action. It must not be treated as a calibrated model confidence score.
- Pilot scope: The API only answers questions; it does not take actions such as creating HR tickets, updating employee records, or approving expenses.

Key takeaway: The architecture is not necessarily wrong, but its handling of exceptions and uncertainty is insufficiently defined. Northstar should close these gaps before approving a safe pilot deployment.

### Summary: Review Architecture Fit — Northstar

Overall assessment: The Employee Policy API architecture fits the routine employee self-service workflow, but important design gaps must be resolved before pilot exposure.

What fits

- A retrieval-grounded API can provide faster, more consistent answers using approved company policy documents.
- The portal and mobile app can use the same structured request and response.
- Read-only retrieval is appropriate for the first release.
- The backend can coordinate retrieval and answer generation without a managed agent session.
- Action-taking features, such as creating tickets or updating employee records, remain outside the pilot scope.

What must be resolved before the pilot

1. Clear boundaries: Define how restricted, ambiguous, unsupported, and out-of-scope questions are declined or routed to human review.
2. Verified context: Confirm that `user_role` and `region` are trustworthy and determine what happens when either is missing or unreliable.
3. Policy reliability: Define how missing, outdated, conflicting, or region-specific policy content is handled.
4. Confidence and next steps: Establish who assigns `confidence_label`, what evidence supports each value, and which deterministic action follows.
5. Runtime selection: Do not introduce a managed session or agent runtime without a demonstrated workflow benefit and confirmation that data-residency and retention requirements are met.

Recommendation: The architecture pattern is suitable in principle, but pilot readiness is not yet established. Resolve the contract and safety gaps, validate the behavior against risky scenarios, and confirm deployment requirements before approving pilot exposure.

### Summary: Review Contract Quality — Northstar

Overall assessment: The Employee Policy API contract is partially defined but not yet complete enough for enterprise release.

The existing request and response fields provide a useful foundation, but the contract must define how the API behaves in both normal and exceptional situations.

Key contract gaps and improvements

| Gap                    | Recommended improvement                                        |
| ---------------------- | -------------------------------------------------------------- |
| Missing source         | Return a structured `missing_source` reason and safe fallback. |
| Outdated policy        | Include source freshness, version, and approval status.        |
| Region-specific policy | Define regional applicability and conflict handling.           |
| Role-specific policy   | Specify role applicability and access restrictions.            |
| Restricted content     | Define refusal, escalation requirements, and approved routes.  |
| Ambiguous question     | Ask for clarification instead of guessing.                     |
| Unsupported question   | Return a structured reason and user-safe explanation.          |
| Retrieval failure      | Define error states and safe fallback behavior.                |

Additional requirement: Define `confidence_label` as a customer-defined workflow field, including its permitted values, assignment rules, supporting evidence, and resulting actions. It must not be presented as a calibrated model confidence score.

Recommendation: Before pilot deployment, finalize the API contract so implementation, testing, logging, monitoring, and handoff teams can consistently identify successful answers, policy limitations, clarification requests, refusals, and system failures.

The exact schema can be decided by the implementation team. The essential requirement is that every important policy-specific failure case has explicit, testable behavior rather than leaving the API to guess.

### Summary: Review Selection Rationale — Northstar

Overall assessment: A retrieval-grounded text API with structured output and safe fallback behavior is the best-fit pattern for Northstar’s current employee policy self-service workflow.

Why this pattern fits

- Uses approved internal policy documents to ground answers in current business context.
- Returns concise answers, source titles, a customer-defined `confidence_label`, and a next step.
- Supports consistent display and routing in the employee portal and mobile app.
- Can safely handle missing, outdated, restricted, regional, ambiguous, or unsupported policy information once fallback rules are defined.

What remains unresolved

1. Verify source approval, freshness, and policy applicability.
2. Define structured failure responses and escalation behavior.
3. Expand validation to cover high-risk and exceptional cases.
4. Keep future action-taking, such as ticket creation, outside the first pilot until separately approved and designed.
5. Avoid adding realtime, voice, multimodal, visual, research-style, or specialized optimization capabilities without evidence of a business need.

Important distinction: A classification or decision capability may help route requests, but it does not replace a sourced policy explanation. Likewise, `confidence_label` is a Northstar-defined workflow field, not a calibrated model confidence score or a probability produced by a decision capability.

Recommendation: Retain the retrieval-grounded text API pattern for the first pilot, but treat selection as provisional until source governance, contract behavior, and risk-based validation are sufficiently defined. Future ticket creation should be evaluated as a separate tool/action workflow.

