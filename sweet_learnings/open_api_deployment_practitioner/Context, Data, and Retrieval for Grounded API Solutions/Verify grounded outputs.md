## Summary: Retrieval Verification Tests

Retrieval tests verify that an API retrieves the correct, approved source content and that the model uses that evidence accurately, safely, and within defined access permissions.

A correct-sounding answer is not enough. The test must establish that the answer is supported by the right evidence, excludes unsupported claims, and handles missing, conflicting, outdated, or restricted information appropriately.

### Key areas to test

1. Retrieval accuracy: Does the API retrieve the expected approved sources?
2. Source traceability: Can each material factual claim be traced to a supporting source?
3. Evidence grounding: Does the model stay within the retrieved context without inventing details?
4. Source quality and freshness: Are conflicting, outdated, or superseded sources handled correctly?
5. Access control: Does retrieval respect user roles and permission boundaries?
6. Missing evidence: Does the API ask for clarification, decline to answer, or escalate when evidence is insufficient?
7. Citation quality: Are source references specific enough for reviewers to verify the answer?
8. Metadata and filters: Do region, product, role, approval status, and effective-date filters work correctly?

### What the design plan should capture

Include a Retrieval Verification Tests section in the Context, Knowledge Access, and Retrieval Design Plan, using these fields:

| Field                    | Purpose                                           |
| ------------------------ | ------------------------------------------------- |
| Test case                | Workflow question or scenario                     |
| Expected source behavior | Approved and excluded sources                     |
| Expected output behavior | Required answer, citations, or no-answer behavior |
| Risk tested              | Failure mode the test is designed to detect       |
| Owner or reviewer        | Person responsible for validation                 |

For every test, also record the user role, source version or date, expected escalation behavior, what the test proves, and what remains unproven.

The key distinction: Retrieval tests establish whether the system retrieves and uses evidence correctly. They do not prove that the complete production system is ready or that a recommendation has achieved its intended business impact. Their purpose is to demonstrate that the retrieval design is sufficiently verified for the next technical review.

## Review Output Behavior — Summary

Output behavior review verifies that the API generates answers that accurately reflect retrieved evidence, respect access controls, communicate uncertainty, and follow the workflow’s review and escalation rules.

Even when retrieval finds the correct source, the model can still misrepresent it, add unsupported details, rely on outdated guidance, or conceal conflicts between sources.

### What to review

- Evidence grounding: The answer is supported by retrieved content and contains no unsupported claims.
- Source references: Citations or source IDs identify the correct source, section, version, or effective date where required.
- Uncertainty handling: The API communicates uncertainty when evidence is incomplete or unreliable.
- Conflict resolution: The API follows defined source-priority rules or flags unresolved disagreements.
- Freshness and approval: Outdated or unapproved sources are not used as authoritative guidance.
- Missing or inaccessible evidence: The API asks for clarification, declines to answer, escalates, or requests human review as appropriate.
- Permission enforcement: Restricted information is not exposed to unauthorized users.
- Partial-evidence handling: The output remains appropriately limited when retrieval is incomplete or low-confidence.

### Common failure modes

| Failure mode                         | Required design response                               |
| ------------------------------------ | ------------------------------------------------------ |
| Unsupported additions                | Test claims against approved source passages.          |
| Wrong-source grounding               | Enforce source-of-truth rules and metadata filters.    |
| Outdated information                 | Apply effective-date and supersession checks.          |
| Overconfidence with missing evidence | Require clarification, refusal, escalation, or review. |
| Weak source references               | Define citation and provenance requirements.           |
| Permission leakage                   | Test access boundaries independently.                  |
| Hidden source conflicts              | Define conflict-resolution or escalation behavior.     |

### What to define in the API design

Specify the required response fields, such as:

- `answer` — the user-facing response.
- `source_ids` — references to supporting sources.
- `source_status` — verified source approval and freshness status.
- `unsupported_claims_detected` — an assessment requiring validation.
- `needs_review` — whether the workflow requires human review.
- `review_reason` — the reason for escalation or review.

These are illustrative fields, not mandatory OpenAI API fields. Model-generated flags must not be treated as proof that a response is safe or factually grounded. Validate important claims against source evidence and enforce permissions and review requirements separately.

### Design-plan deliverables

The output behavior review should establish:

1. Expected answer behavior for each retrieval test case.
2. Required citations, structured fields, and provenance information.
3. Conditions that trigger clarification, refusal, escalation, or human review.
4. Validation checks for unsupported claims, conflicting sources, and restricted content.
5. Evidence that the next technical reviewer should inspect before implementation.

The goal: Demonstrate that the retrieval design produces outputs that are evidence-grounded, traceable, appropriately bounded, and suitable for the workflow’s next technical review—not that every answer is guaranteed correct or that the system is production-ready.


## Summary: Monitor and Improve Retrieval Quality

Retrieval quality monitoring identifies how retrieval can degrade over time and defines the owners, evidence, and feedback loops needed to keep it accurate, current, and reviewable.

Retrieval quality is not static. Source updates, stale metadata, permission changes, new workflows, and evolving user questions can make an initially sound retrieval design unreliable.

### What to monitor

| Review area            | Evidence to capture                                                            |
| ---------------------- | ------------------------------------------------------------------------------ |
| Retrieval failures     | Questions returning incorrect, missing, or low-quality sources                 |
| User feedback          | Reports of missing, outdated, mismatched, or unclear content                   |
| Wrong-source retrieval | Semantically similar sources that are not authoritative                        |
| Unsupported claims     | Answers containing details not supported by retrieved evidence                 |
| Source references      | Missing, vague, or incorrect citations                                         |
| Permission boundaries  | Unclear access rules or potential unauthorized disclosure                      |
| Source maintenance     | Sources requiring approval, updates, replacement, or archiving                 |
| Metadata quality       | Missing or incorrect region, product, role, approval, or effective-date fields |

### When to improve the retrieval design

Review and consider corrective action when:

- Repeated questions retrieve the wrong sources.
- High-risk workflows return outdated or insufficient evidence.
- Permission tests fail or access assumptions become unclear.
- Source owners confirm changes to approved content.
- Metadata no longer reflects workflow requirements.
- Reviewers repeatedly identify unsupported claims.
- Common workflow questions cannot be answered safely.

### What the design plan should hand off

1. Source ownership: Who maintains, approves, updates, and retires source content?
2. Retrieval ownership: Who reviews retrieval quality and coordinates corrective changes?
3. Review evidence: Which failed queries, source mismatches, user feedback, and test results must be examined?
4. Escalation criteria: Which failures require correction, retesting, or human review?
5. Retesting requirements: Which tests must be repeated after changes to sources, metadata, permissions, filters, or retrieval logic?

### Expected outcome

The design plan should establish a practical feedback loop:

Collect evidence → Review failures → Identify the cause → Update sources or retrieval rules → Retest → Record the outcome.

Keep the scope focused on design readiness rather than full production monitoring. The aim is to make future retrieval problems detectable, assign responsibility for resolving them, and ensure changes are validated rather than assumed to work.

Key takeaway: Retrieval is not a one-time configuration. Sustained quality requires clear ownership, reliable source maintenance, reviewable evidence, and defined retesting criteria.

## Real-world example: Grounded output verification

The life sciences example demonstrates an important principle: an answer can cite a legitimate source and still be unsafe to use.

The two failures have different root causes and require separate tests.

| Issue                      | Root cause                                                   | Verification and corrective action                                                       |
| -------------------------- | ------------------------------------------------------------ | ---------------------------------------------------------------------------------------- |
| Unsupported detail         | The model added a claim not supported by the cited document. | Compare material claims against retrieved passages and require evidence-bounded answers. |
| Outdated regional addendum | Retrieval filters checked region but not effective date.     | Add effective-date, approval-status, and supersession checks; retest source selection.   |

### Additional verification requirements

- Source references: Confirm that citations identify the evidence supporting each material claim.
- Metadata filters: Test product, region, effective date, approval status, and other applicable filters.
- Permission boundaries: Verify that field-team members retrieve only content authorized for their roles and contexts.
- Missing evidence: Require clarification, a no-answer response, or escalation when approved guidance is insufficient.
- Conflicting guidance: Apply documented source-priority rules or escalate unresolved conflicts.
- Ownership: Ask source owners to confirm which addenda are current and permission owners to validate access rules.

### Recommended decision

Do not recommend the retrieval design for the next stage until the identified high-risk failures have been corrected and the relevant tests pass.

The verification record should document the test cases, expected sources, observed outputs, evidence supporting the results, responsible reviewers, and remaining limitations.

Key takeaway: Grounded-output verification must validate four things independently: source selection, evidence-supported claims, output behavior, and access and escalation rules. A citation alone is not proof of correctness, and passing these tests establishes design readiness—not guaranteed production safety or business impact.


# Exercise: Define Retrieval Verification Tests

The goal is to verify that the warranty API retrieves the right approved sources, generates evidence-grounded answers, and respects access and escalation rules before the design is recommended.

## 1. Retrieval verification test plan

| Test case                          | Expected retrieval behavior                                                                                         | Expected output behavior                                                                                                                 | Risk tested                                                           | Owner/reviewer                                                |
| ---------------------------------- | ------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------- | ------------------------------------------------------------- |
| 1. Approved warranty question      | Retrieve the current, approved warranty policy matching the product category, region, and effective date.           | Provide an accurate answer with a specific source reference; limit claims to the policy evidence.                                        | Incorrect source selection or unsupported claims.                     | Warranty policy owner and retrieval engineer                  |
| 2. Missing regional source         | Identify that no approved regional addendum is available for the requested region and date.                         | Explain that the regional rule cannot be verified; request clarification or escalate to human review. Do not guess.                      | Incorrect coverage advice based on incomplete evidence.               | Regional policy owner and support operations lead             |
| 3. Archived deck appears in search | Exclude archived or superseded decks from authoritative results unless explicitly approved for historical research. | Use the current policy or state that sufficient current evidence is unavailable.                                                         | Outdated or superseded warranty guidance.                             | Knowledge management owner                                    |
| 4. Internal-only support article   | Enforce access and content-use rules for internal-only material and the intended audience.                          | Provide only content authorized for the workflow; do not expose internal-only details in customer-facing drafts.                         | Permission leakage or disclosure of confidential information.         | Security/access-control owner and support compliance reviewer |
| 5. Conflicting warranty guidance   | Retrieve the relevant sources and identify conflicting policy statements. Apply documented source-priority rules.   | Follow the approved priority rule or flag the disagreement for human review. Do not blend conflicting guidance into a definitive answer. | Incorrect warranty decisions and inconsistent customer communication. | Warranty policy owner and compliance reviewer                 |

## 2. Optional stretch tests

| Test case                 | Expected retrieval behavior                                                                                                     | Expected output behavior                                                                                                        | Risk tested                                                  |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------ |
| 6. Source relevance       | Return sources matching the product, warranty question, region, and applicable dates—not merely documents with similar wording. | Answer the specific question using relevant evidence, or explain that the available sources do not resolve it.                  | Semantically similar but irrelevant sources.                 |
| 7. Unsupported-claim risk | Retrieve the correct approved policy and supporting passages.                                                                   | Ensure each material warranty claim is supported by the retrieved evidence; remove unsupported details or flag them for review. | Hallucinated coverage conditions, exclusions, or exceptions. |

## 3. Additional checks for every test

For each case, record:

- Source version and effective date: Which approved policy or addendum should apply?
- Access boundary: What is the user's role, and is the output intended for internal or customer-facing use?
- Expected source references: Which document, section, or record should support the answer?
- Missing-evidence behavior: Should the API clarify, decline to answer, or escalate?
- What the test proves: For example, that archived guidance is excluded under the tested conditions.
- What remains unproven: For example, whether all regional policies and permission combinations behave correctly.

## 4. Recommendation before the next technical review

The retrieval design should not be recommended until the high-risk test cases have defined expected behavior and the relevant tests pass. In particular, confirm that:

1. Only applicable, approved warranty sources are treated as authoritative.
2. Region, product category, effective date, and approval status are handled correctly.
3. Internal-only content cannot leak into customer-facing drafts.
4. Missing evidence and conflicting guidance trigger the appropriate review behavior.
5. Material claims can be traced to supporting source passages.

Reflection: The API should not be judged solely on whether its answers sound correct. The verification plan must establish that it selected the right evidence, used that evidence faithfully, and handled uncertainty and permissions safely. Passing these tests supports the next technical review; it does not prove complete production readiness.