# 1. Define the customer problem, boundary, and constraints

# Example
# API Solution Architecture Brief: Financial Services Pre-Call Briefing

### 1. Customer problem and outcome
Relationship managers spend too much time preparing for client meetings because relevant information is scattered across CRM notes, support history, internal research, and previous meeting summaries. The goal is to provide a concise, accurate briefing that reduces preparation time and helps relationship managers conduct more informed client conversations.

### 2. Workflow moment and user or system actor
The workflow begins when a relationship manager opens a client account before a scheduled meeting. The internal application retrieves authorized account information and invokes the API to generate a structured pre-call briefing.

### 3. What the API solution should do
The API should summarize approved account information into a structured briefing that highlights client context, recent interactions, outstanding issues, and relevant discussion points. It should identify source information where possible and clearly flag missing, outdated, or uncertain details for human review.

### 4. What the API solution should not do
The solution should not make investment recommendations, infer unsupported financial information, modify CRM records, send customer-facing communications, or execute transactions. It should not access information beyond the requesting user's permissions or present generated content as verified fact without appropriate validation.

### 5. What must remain human-owned
The relationship manager must review the briefing, verify important details, decide which discussion points are appropriate, and make all client-facing decisions. Any financial advice, investment recommendation, or consequential action must follow the organization's existing approval and compliance processes.

### 6. Constraints or validation questions before build
Confirm which data sources are approved, how user permissions and sensitive client information will be protected, and what retention, audit logging, and compliance requirements apply. Validate acceptable response time, output format, factual accuracy, source attribution, and the human review process before selecting the model or implementation pattern.

# 2. Map integration needs and select the API architecture pattern

Once the customer problem and solution boundary are clear, the next step is to identify where the API fits into the customer’s existing workflow and systems.

Q. 1. Which application or workflow will call the API?
Q. 2. Which systems, tools, or data sources must the API access?
Q. 3. Which user channel or system channel will receive the output?
Q. 4. Which downstream systems may rely on the response?
Q. 5. Which approval or handoff step is needed before action is taken?


A sketch helps answer:
What might the caller need to send?
What context might the API need?
What structured fields might the workflow require?
What review flags or status values may be needed?
What remains unresolved before implementation?


# Common API architecture patterns


## Example
## Choose the First Architecture Pattern

**Integration path:** The account workspace calls the API and supplies approved account context. The API generates a structured internal briefing and returns it to the workspace for relationship manager review.

**Selected architecture pattern:** Structured output pattern.

**Rationale:** Structured output provides a predictable format with defined fields, making the briefing easier to review, validate, and integrate into the account workspace, provided all required approved context is supplied by the application.

**Out of scope for the first version:** Tool/action workflows. The initial version will not update CRM records, create tasks, send customer-facing messages, or take actions in other systems. Retrieval can be considered later if the application cannot provide the necessary approved context, subject to source-access and freshness validation.


# 3. Add governance, evaluation, and observability assumptions

Governance means the rules, ownership, approvals, and controls that help the organization use the API safely and responsibly.

Q. What data can the API access?
Q. What systems can it call?
Q. Which actions require approval?
Q. Who reviews outputs before they affect users, customers, or systems?

### 1. Evaluation Assumptions

**1. Behavior to test**
- Generates structured briefings from approved account context.
- Avoids unsupported claims and flags missing information.
- Respects source permissions and workflow boundaries.

**2. Acceptable output**
A concise internal briefing with account summary, meeting context, preparation questions, source notes, and review flags.

**3. Unacceptable output**
Incorrect account data, unsupported claims, unauthorized data exposure, unapproved sources, or unauthorized actions.

**4. Human-review triggers**
Missing or conflicting context, permission issues, sensitive topics, uncertainty, or out-of-scope requests.

**5. Evals before launch**
Factual accuracy, missing-context handling, access permissions, sensitive-data protection, refusal behavior, and structured-output validity.

### 2. Observability Assumptions

**1. Activity to monitor**
API requests, request status, context availability, output validation, review flags, errors, and latency.

**2. Failures to track**
Missing inputs, permission failures, unavailable sources, malformed output, timeouts, and reviewer-reported errors.

**3. Reviewers**
Technical lead, solution architect, product owner, security and compliance reviewers, and system owner.

**4. Evidence before rollout**
Evaluation results, security review, source approval, prototype feedback, error logs, and reliability metrics.

**Principle:** Launch only when output quality, access controls, human review, and monitoring are sufficiently validated.

## Key takeaway
For any API workflow, ask four readiness questions before moving forward: 

Governance - What can the API access, and who approves it?
Evaluation - What behavior must be tested?
Observability - What must be visible after use?
Production readiness - What must be true before broader exposure?


## Readiness Assumptions for First Pilot

- **Governance:** Use only approved account data that the relationship manager is authorized to access.
- **Evaluation:** Verify briefing accuracy, structured output, missing-context flags, and avoidance of unsupported recommendations.
- **Observability:** Monitor API status, source availability, errors, review flags, and latency.
- **Production readiness:** Confirm human-review ownership, fallback behavior, access controls, logging rules, and support procedures before expanding the pilot.


# 4. Complete the API Solution Architecture Brief



