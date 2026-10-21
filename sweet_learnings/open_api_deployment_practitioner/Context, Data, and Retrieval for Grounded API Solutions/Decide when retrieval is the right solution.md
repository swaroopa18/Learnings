### Summary: Decide When Retrieval Is the Right Solution

Retrieval should be implemented only when a workflow has a genuine need for external or specialized knowledge. Documents should not be connected to an API simply because they are available.

There are three possible decisions:

- Use retrieval: The workflow needs relevant information from documents, knowledge bases, or frequently updated sources.
- Do not use retrieval: The task can be handled reliably using the model’s existing capabilities or a simpler solution.
- Pause and validate: Sources, access permissions, or information quality need to be checked before proceeding.

Why this decision matters: Retrieval affects API contracts, context management, security, evaluation, guardrails, observability, and production readiness.

Key takeaway: Start with the workflow’s actual knowledge requirements, then decide whether retrieval is necessary, appropriate, and safe.


### Summary: Identify the Knowledge Requirement

Before implementing retrieval, clearly define what business knowledge the API needs, why it needs it, and what risks arise if the information is incorrect or outdated.

A strong knowledge requirement connects the workflow, trusted sources, accuracy risks, and decisions or actions affected.

What to identify:

- Workflow step: What task or question requires business knowledge?
- Required knowledge: What policies, records, documents, or rules are needed?
- Source expectation: Which approved source should support the answer?
- Accuracy risk: What happens if the information is generic, incomplete, or outdated?
- Action or decision: What will the user or system do based on the answer?
- Evidence need: Are citations, references, or audit trails required?
- Output boundary: What must the API avoid claiming, inferring, exposing, or summarizing without sufficient evidence?

Example:

Instead of saying, “The assistant needs company policies,” specify that it needs the current employee leave and regional holiday policies to answer leave-related questions accurately and prevent incorrect HR guidance.

Key takeaway: A clear knowledge requirement helps teams decide whether retrieval is necessary and guides security, data handling, evaluation, guardrails, observability, and production-readiness planning. If the knowledge need is unclear, pause before implementing retrieval.


### Summary: Decide Whether Retrieval Is Needed

Retrieval is appropriate when an API needs approved, current, permission-aware, and traceable business knowledge to answer accurately. It should not be added simply because it is a more advanced approach.

Three recommendation options:

1. Retrieval needed: The workflow depends on current policies, internal records, approved documents, or source-based evidence.
2. Retrieval not needed: General reasoning, drafting, classification, or user-provided context is sufficient.
3. Defer pending source validation: Sources are unapproved, outdated, incomplete, poorly owned, or have unresolved access permissions.

Decision flow:

- Does the workflow require knowledge beyond the user’s request?
- Must the answer rely on approved, current, or traceable sources?
- Are the sources reliable, owned, current, and permissioned?
- Does retrieval provide more value than the complexity and risk it introduces?
- Can the grounded output be verified before use?

If sources are not ready or the output cannot be validated safely, pause implementation.

Design implications: The decision affects API contracts and structured outputs, security and permissions, context and state management, tool actions, evaluations and guardrails, observability, latency, cost, and production readiness.

Key takeaway: Choose retrieval only when its benefits justify its complexity. Document the recommendation, source requirements, ownership, access assumptions, risks, and validation tests before implementation.


### Summary: Define Knowledge Access

Knowledge access defines what information the API needs, what it is authorized to use, and what it must not retrieve, expose, summarize, or infer.

A strong retrieval design does not connect every available document. It selects only sources that are relevant, approved, sufficiently current, properly owned, and authorized for the workflow.

Three source-level decisions:

- Include: The source is relevant, approved, current enough, and permissioned for the workflow.
- Exclude: The source is outdated, unapproved, confidential, irrelevant, or outside the user's access rights.
- Validate: Approval, ownership, freshness, completeness, sensitivity, or permissions are unresolved.

Permissions must be validated based on factors such as user role, department, region, customer or tenant, data classification, contractual restrictions, and environment.

What to document in the design plan:

1. Needed source — documents, systems, records, or knowledge bases.
2. Source owner — the accountable team or person.
3. Access boundary — who or what can access the source.
4. Workflow approval — whether the source is approved for use.
5. Sensitivity — confidential, regulated, or customer-specific data concerns.
6. Source decision — include, exclude, or validate.
7. Validation owner — who confirms source readiness and permissions.
8. Output boundary — what the API must not reveal or infer.

Key takeaway: More context does not automatically mean better answers. Restrict retrieval to necessary, approved, and authorized knowledge, and resolve access uncertainties before production use.


### Summary: Real-World Example — Retrieval Fit and Knowledge Access

1\. Life sciences field-team API — Retrieval needed

The API must answer questions using approved, current product guidance and regional requirements, rather than generic model knowledge.

The design should:

- Include approved, current product guidance and validated regional addenda.
- Identify source owners, versions, effective dates, and regional applicability.
- Enforce permissions for field-team users.
- Exclude draft and outdated materials.
- Test for missing, conflicting, or stale information before a pilot.

2\. Text-rewriting API — Retrieval not needed

When users provide all the text required for a shorter summary, retrieval adds unnecessary complexity. A clear prompt and structured-output contract may be sufficient.

3\. Engineering-improvement recommendations — Source-grounded knowledge needed

Recommendations based on a codebase, warehouse data, and internal company knowledge require access to relevant sources, appropriate permissions, and supporting evidence. The example does not establish that a specific retrieval technology was used.

Key takeaway: Retrieval decisions depend on the workflow's knowledge requirements, not simply on whether documents exist. Select approved sources, enforce access boundaries, validate source quality, and ensure outputs are supported by evidence before implementation.


## Exercise: Decide Whether Retrieval Is Needed

| Workflow                     | Recommendation                  | Reason                                                                                                                                                                                    |
| ---------------------------- | ------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| A. Employee policy assistant | Retrieval needed                | Answers depend on current, approved HR policies and region-specific rules. Generic model knowledge may be outdated or incorrect.                                                          |
| B. Support ticket classifier | Retrieval not needed            | The ticket contains all the information needed to assign a fixed category. A prompt and structured-output schema should be sufficient.                                                    |
| C. Regional pricing helper   | Defer pending source validation | Pricing spreadsheets include drafts, unclear ownership, and different regional permissions. Using them before validation could expose restricted information or produce incorrect prices. |

### What to validate or hand off

A. Employee policy assistant

- Identify approved HR policy sources and regional addenda.
- Confirm source owners, effective dates, and employee access permissions.
- Test outdated, conflicting, and unsupported policy answers.
- Require source references where appropriate.

B. Support ticket classifier

- Define the permitted categories and output schema.
- Evaluate classification accuracy across representative tickets.
- Define handling for ambiguous or incomplete messages.

C. Regional pricing helper

- Identify the authoritative pricing source and accountable owner.
- Remove or exclude drafts and outdated spreadsheets.
- Validate regional permissions and access restrictions.
- Confirm effective dates and resolve conflicting prices before piloting retrieval.

### Optional stretch example

Workflow: Internal assistant using an unapproved draft compliance manual

Recommendation: Defer pending source validation.

Reason: The document may contain inaccurate or unapproved guidance. Connecting it to retrieval could produce misleading compliance answers.

Next steps: Obtain approval from the compliance owner, verify the current version, establish access permissions, and test source-grounded answers before use.

Key takeaway: Retrieval is appropriate when a workflow needs trusted external knowledge. Avoid it when the supplied input is sufficient, and defer it when sources or permissions are not ready.