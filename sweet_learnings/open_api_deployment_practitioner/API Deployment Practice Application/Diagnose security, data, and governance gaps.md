## Summary: Diagnose Security, Data, and Governance Gaps

For Northstar, a successful staging API test does not automatically mean the system is ready for enterprise release. The deployment must demonstrate that it can provide accurate answers from approved sources while protecting sensitive data and meeting governance requirements.

Key areas to assess:

1. Security: Verify authentication, role-based access control, authorization, secrets management, and protection against unauthorized data access.
2. Data handling: Confirm data classification, encryption in transit and at rest, PII protection, retention policies, logging controls, and compliance with applicable requirements.
3. Retrieval readiness: Ensure the API retrieves information from approved, current, authoritative sources and respects document-level permissions and user access rights.
4. Governance: Establish clear ownership, audit trails, human review and escalation paths, incident response procedures, and approval responsibilities.
5. Release readiness: Document unresolved risks, validate controls through testing, and obtain the necessary security, data, and business approvals before production deployment.

Key takeaway: Northstar should be released only when its security controls, data-handling practices, retrieval permissions, and governance processes are validated and approved—not merely because the API works in staging.

## Northstar: Security, Data, and Governance Gap Analysis

Release recommendation: Do not approve an unconditional pilot release yet. The evidence identifies unresolved security, logging, retrieval, and governance controls that could expose employee data or produce answers from unapproved sources.

### Key gaps and required actions

| Area                   | Gap identified                                                               | Required action                                                                                               |
| ---------------------- | ---------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| Security               | API trusts caller-supplied `user_role` and `region`.                         | Verify identity and permissions server-side; derive role and region from trusted sources.                     |
| Data protection        | Logs capture questions, user IDs, retrieved snippets, and generated answers. | Define masking, data minimization, retention, access controls, and exclusions for sensitive questions.        |
| Retrieval              | Sources have different approval statuses and regional coverage.              | Enforce source allowlists and region-specific retrieval rules. Exclude unresolved or unapproved content.      |
| Restricted content     | Employee Relations Investigation Procedure is restricted.                    | Block it from employee self-service retrieval unless explicitly approved and appropriately access-controlled. |
| Governance             | Release, security, source, logging, and support owners are not all named.    | Assign accountable owners and obtain documented signoffs before release.                                      |
| Monitoring and support | Operational support and incident ownership are unclear.                      | Define auditability, incident escalation, monitoring, and support responsibilities.                           |

### Source readiness assessment

| Source                                     | Status                                       | Release treatment                                                           |
| ------------------------------------------ | -------------------------------------------- | --------------------------------------------------------------------------- |
| HR Employee Handbook v4.1                  | Approved and current                         | Allow for the pilot                                                         |
| IT Acceptable Use Policy v2.8              | Approved and current                         | Allow for the pilot                                                         |
| Travel and Expense Policy v3.2             | US/Canada approved; UK update pending        | Restrict by region; exclude UK-specific claims until approved               |
| Benefits Enrollment Guide 2026             | US approved; Canada under review; UK unclear | Allow approved US content only; hold Canada and UK content pending approval |
| Employee Relations Investigation Procedure | Restricted                                   | Exclude from self-service retrieval unless authorized                       |

### Priority release gates

1. Identity and authorization: Prevent callers from impersonating roles or changing regional access by manipulating request fields.
2. Logging and privacy: Approve a documented logging policy covering sensitive data, access, retention, masking, and deletion.
3. Retrieval controls: Test that only approved, current, region-appropriate documents can influence answers.
4. Governance signoff: Name the release approver, security reviewer, source owners, logging reviewer, and operational support owner.
5. Validation: Run negative tests for unauthorized access, restricted-source retrieval, regional mismatches, and sensitive-data leakage.

### Final decision

Northstar may continue in controlled staging while these gaps are addressed. A limited pilot should proceed only after critical controls are implemented, tested, and formally approved. Internal-only deployment is not sufficient evidence of safety.

Core lesson: The API must answer using the right sources, for the right users, with safe data handling and clear accountability—not merely return a technically valid response.

## Northstar: Review Data and Access

Recommendation: Northstar should not move to pilot until employee identity and permissions are verified, retrieval is restricted to approved sources, and logging and escalation controls are documented and tested.

### 1. Map data across the workflow

| Data category   | Needed for the workflow                                                              | Required control                                                                                   |
| --------------- | ------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------- |
| Input data      | Employee identity, verified role and region, question, and necessary channel context | Verify identity and authorization server-side; minimize unnecessary fields                         |
| Retrieved data  | Current, approved policy documents applicable to the employee                        | Enforce source allowlists, regional rules, and document-level permissions                          |
| Output data     | Answer, source titles, confidence, and next step                                     | Identify applicable sources, communicate uncertainty, and escalate unresolved or restricted topics |
| Logged data     | Minimum operational metadata needed for monitoring and troubleshooting               | Mask or exclude sensitive content, restrict access, and define retention and deletion              |
| Access data     | Trusted employee identity and entitlements                                           | Do not rely on caller-supplied role or region; validate authorization on every relevant request    |
| Escalation data | Information needed to route an unresolved question to the right support team         | Name owners and define handling for sensitive topics, unsafe answers, and employee complaints      |

### 2. Separate necessary data from data to minimize

- Keep where necessary: Verified employee identity, authorized role and region, the question, approved policy content, and minimal diagnostic metadata.
- Verify before use: Role, region, policy permissions, and source approval status.
- Mask or minimize: Employee identifiers, sensitive question text, retrieved snippets, and generated answers in logs.
- Exclude by default: Restricted HR investigation materials and unapproved regional policies.
- Route for review: Questions that require confidential HR handling, have no approved source, or cannot be answered reliably.

### 3. Key access and governance risks

The employee portal's authentication does not automatically prove that the API has correctly authorized the employee. Northstar must independently establish trusted identity, role, region, and source permissions.

Similarly, a proposed Zero Data Retention (ZDR) arrangement with Private Safety Processing (PSP) would not automatically resolve application logging risks. Eligibility, configuration, storage responsibilities, key access, and retention need verification, while Northstar's own logs require a separate approved policy.

### 4. Evidence required before pilot

- Server-side identity, role, and region verification tested.
- Approved-source and regional retrieval restrictions validated.
- Restricted-source exclusion tested.
- Logging policy approved, including masking, access, retention, and deletion.
- Output behavior defined for uncertain, unsupported, or restricted questions.
- Security, source, logging, release, and support owners formally identified.

Final takeaway: Collect only the data needed to answer the employee's question, retrieve only authorized policy content, return appropriately qualified guidance, and retain only the minimum approved operational evidence. Internal-only access and successful API responses are not sufficient release controls.

## Summary: Review Security Controls — Northstar

Northstar should not proceed to an unconditional pilot release until its security, source governance, and data-handling controls are validated.

Key findings:

1. Identity and access: Verify employee identity, role, and region server-side. Do not trust caller-supplied values without validation.
2. Source governance: Retrieve only approved, current, permission-appropriate policy documents.
3. Regional restrictions: Use travel and expense policies only for the US and Canada. Restrict benefits guidance to approved US content until other regional versions are approved.
4. Restricted content: Exclude the Employee Relations Investigation Procedure from employee self-service unless HR Legal approves a permission-gated process.
5. Logging and privacy: Define masking, sensitive-data exclusions, log access permissions, retention, and deletion.
6. Governance and escalation: Assign accountable owners for security approval, source approval, logging, release decisions, and employee support.

Final recommendation: Keep the pilot conditional until critical controls are implemented, tested, and formally approved. If a policy source is missing, outdated, unapproved, or regionally unclear, the API should decline to provide unsupported guidance and escalate to an appropriate human support team.

Key takeaway: A working API is not necessarily a safe API. Northstar must demonstrate that it provides the right information to authorized employees while protecting sensitive data and maintaining clear accountability.

## Summary: Review Governance and Escalation — Northstar

Recommendation: Keep the pilot conditional until critical security controls, accountable owners, and escalation procedures are confirmed.

### Key governance requirements

1. Authentication and authorization: Security and platform owners must confirm that the API verifies employee identity, role, region, and permissions.
2. Permission-aware retrieval: Source owners and security reviewers must ensure that employees receive only approved, current, authorized policy content.
3. Restricted topics: HR Legal and privacy reviewers must define how sensitive employee relations, disciplinary, grievance, health, and accommodation questions are excluded, permission-gated, or escalated.
4. Logging and retention: Assign an owner to approve masking, log access, retention, deletion, and sensitive-data exclusions.
5. Secrets and configuration: Validate production configuration and access controls independently of successful staging tests.
6. Tool and action boundaries: Keep ticket creation, HR record changes, external messages, and other consequential actions outside the first pilot.
7. Release and support ownership: Name the release approver, source owners, logging reviewer, incident responder, and employee support and escalation owners.

### Future integrations and automation

Potential extensions, event-driven workflows, connected sites, and hosted-browser automation require separate security and governance reviews. They must respect permissions, obtain required approvals, prevent duplicate or repeated actions, and use explicitly authorized data connections. Future ticket creation requires a separate release decision.

### Final release decision

Northstar must demonstrate that it can:

- Verify users and enforce permissions.
- Retrieve only approved and region-appropriate sources.
- Protect sensitive employee data in application logs.
- Escalate restricted or unsupported questions to accountable human owners.
- Obtain documented security, source, logging, and release approvals.

Key takeaway: The central risk is the combination of untrusted user context, insufficient source permissions, and unresolved logging controls. Until these gaps are addressed, a successful API response is not sufficient evidence for pilot approval.