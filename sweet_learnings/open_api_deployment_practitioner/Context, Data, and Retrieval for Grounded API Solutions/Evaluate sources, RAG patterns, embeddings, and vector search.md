### Summary: Evaluate Sources, RAG Patterns, Embeddings, and Vector Search

This module focuses on evaluating whether data sources are ready to be used in a Retrieval-Augmented Generation (RAG) system before implementation.

Key evaluation criteria include:

- Ownership: Identify who owns and manages each source.
- Approval status: Ensure content is approved and authorized for use.
- Freshness: Check whether information is current and regularly updated.
- Completeness: Verify that documents and records contain sufficient, accurate information.
- Permissions: Confirm that access controls and data privacy requirements are respected.
- Maintenance: Determine how sources will be monitored, updated, and maintained.

Expected outcome: Decide which sources to include, exclude, or validate before implementation, and document any assumptions, risks, or unresolved issues that require review.

Key takeaway: Evaluating source quality, reliability, access permissions, and maintenance requirements before implementation helps ensure that a RAG system retrieves trustworthy and relevant information.

## Summary: Review Candidate Sources

Candidate sources are documents, knowledge bases, structured records, support articles, policies, historical examples, or operational systems that may provide information for a Retrieval-Augmented Generation (RAG) workflow.

A candidate source is not automatically an approved source. Each source must be evaluated against the workflow’s knowledge needs before it can be used.

### Key review criteria

- Relevance: Does the source support the workflow’s answer, decision, or step?
- Authority and approval: Is it an official, approved source?
- Ownership: Who maintains it and approves its use?
- Freshness and completeness: Is the information current and sufficient?
- Sensitivity and permissions: Does it contain restricted data, and is access authorized?
- Maintenance: How often should the source be reviewed or updated?

### Source selection decisions

- Include: Relevant, approved, reliable, sufficiently current, owned, and properly permissioned sources.
- Exclude: Irrelevant, outdated, unofficial, unapproved, or unauthorized sources.
- Validate: Potentially useful sources with unresolved questions about ownership, approval, freshness, completeness, sensitivity, or permissions.

### What to document

Maintain a source inventory containing:

| Field            | Purpose                                 |
| ---------------- | --------------------------------------- |
| Source and type  | Identify the source                     |
| Workflow use     | Explain its purpose                     |
| Owner            | Identify the responsible person or team |
| Approval status  | Record authorization                    |
| Decision         | Include, exclude, or validate           |
| Reason           | Document the rationale                  |
| Validation owner | Assign follow-up responsibility         |

Key takeaway: Source review must begin with the workflow’s knowledge needs. Documenting decisions, exclusions, and unresolved questions makes the RAG design transparent and easier for technical, security, and business teams to review before implementation.


## Summary: Assess Source Readiness

Source readiness determines whether a candidate source is safe, reliable, and suitable for grounding an API workflow using Retrieval-Augmented Generation (RAG).

Relevance alone is not enough. A source may contain useful information but still be unsuitable because it is outdated, unapproved, incomplete, sensitive, or inaccessible to the intended user.

### Key readiness criteria

- Owner: Who is accountable for the source?
- Approval status: Is it officially approved for the intended audience and workflow?
- Freshness: Is the content current enough for the workflow?
- Completeness: Does it cover expected questions, edge cases, and regional differences?
- Permissions: Can the user, service, role, or tenant access it?
- Format: Can the content be reliably searched and interpreted?
- Sensitivity: Does it contain confidential, personal, regulated, or restricted information?
- Source-of-truth status: Is it authoritative or merely a copy or summary?
- Update cadence: How frequently is it maintained and refreshed?
- Conflict handling: Which source takes precedence when information disagrees, and who resolves the conflict?

### Source readiness decisions

| Decision            | Meaning                                                             | Next step                                      |
| ------------------- | ------------------------------------------------------------------- | ---------------------------------------------- |
| Ready to include    | Relevant, approved, reliable, current, and accessible               | Include in retrieval planning                  |
| Exclude             | Unapproved, irrelevant, outdated, overly sensitive, or unauthorized | Document the reason                            |
| Validate before use | Potentially useful but has unresolved issues                        | Assign an owner and identify required evidence |

### Risks of weak source readiness

Poor source evaluation can cause the API to:

- Retrieve outdated or draft guidance.
- Combine conflicting information without clarification.
- Expose data to unauthorized users.
- Produce confident answers from incomplete information.
- Cite sources that are relevant but not authoritative.
- Generate answers that cannot be properly reviewed or defended.

### What to document in the design plan

Record each source’s owner, approval status, freshness, completeness, permissions, sensitivity, authoritative status, update cadence, readiness decision, and unresolved validation questions.

Key takeaway: Retrieval improves grounding only when the underlying sources are trustworthy and authorized. When readiness is uncertain, defer use until the appropriate source owner, system owner, security team, privacy team, or customer stakeholder validates it.


## Summary: Explain RAG Patterns

Retrieval-Augmented Generation (RAG) is a design pattern in which an API retrieves relevant information from approved sources and provides it as context to a language model to generate grounded responses.

### 1. How RAG works

1. Receive a request: A user or system sends a query.
2. Identify relevant content: Determine which source information may answer the query.
3. Retrieve evidence: Find relevant content from approved sources.
4. Provide context: Pass the retrieved content to the model.
5. Generate an answer: The model uses the retrieved evidence to formulate a response.
6. Return the result: Provide the answer along with source references, structured fields, or review flags when required.

### 2. Common RAG patterns

| Pattern                       | When to use                                                                          |
| ----------------------------- | ------------------------------------------------------------------------------------ |
| Single-source grounding       | One authoritative source provides the required information.                          |
| Multi-source grounding        | The workflow needs information from multiple approved sources.                       |
| Retrieval + structured output | Responses must follow a predictable schema for integration, routing, or review.      |
| Retrieval + human review      | Responses affect customers, sensitive workflows, policies, or operational decisions. |
| Deferred retrieval            | Source quality, approval, access, or maintenance is not yet ready.                   |

### 3. Important design considerations

- Output structure: Define whether the API returns free text, structured fields, source references, or review flags.
- Access control: Ensure retrieval respects user and system permissions.
- Source maintenance: Establish ownership, approval processes, and update schedules.
- Conflict handling: Define how the system handles contradictory or outdated sources.
- Validation: Test missing evidence, incorrect retrieval, unsupported claims, and permission boundaries.
- Handoff: Document source decisions, assumptions, risks, and validation responsibilities.

### 4. When not to use RAG

RAG may be unnecessary or unsuitable when:

- The user already provides all the required content.
- The task involves simple classification, transformation, or formatting.
- Sources are unapproved, outdated, or inaccessible under the required permissions.
- Source conflicts cannot be resolved.
- Retrieval adds cost, latency, and maintenance without meaningful benefit.

### Key takeaway

RAG helps ground model responses in relevant evidence, but it does not guarantee correctness. Choose a RAG pattern based on the workflow’s actual needs, source readiness, access requirements, and validation criteria. If simpler approaches are sufficient, avoid adding unnecessary retrieval complexity.


## Summary: Explain Embeddings and Vector Search

Embeddings are numerical representations of text or other content that capture aspects of its meaning. Vector search uses these representations to find content that is semantically similar to a user's query, even when the wording differs.

For example, a user searches for “field guidance,” while an approved document uses “representative talking points.” Semantic search may identify the relevant document despite the different wording.

### Why embeddings and vector search matter

They are useful when:

- Users ask questions in natural language.
- Queries use different vocabulary from source documents.
- The source collection is large.
- Support articles, policies, or procedures express similar concepts in different ways.
- Exact keyword matching is insufficient.

### Key risks and limitations

Embeddings and vector search find potentially relevant content, but they do not guarantee:

- Authority: The result comes from an official source.
- Freshness: The information is up to date.
- Completeness: The retrieved content fully answers the question.
- Permission compliance: The user is authorized to access it.
- Accuracy: The generated answer is fully supported by the retrieved evidence.

Other risks include outdated matches, irrelevant passages, missing metadata filters, and confident answers based on incomplete evidence.

### What to validate before implementation

1. Are results drawn only from approved sources?
2. Are retrieved passages relevant and sufficiently complete?
3. Are outdated or superseded sources filtered out?
4. Are user permissions enforced?
5. Are metadata filters applied correctly for product, region, role, and effective date?
6. Can reviewers verify the source references?
7. Does the API avoid unsupported claims when evidence is weak or missing?

### What to document in the design plan

| Item             | What to capture                                                   |
| ---------------- | ----------------------------------------------------------------- |
| Purpose          | Why semantic retrieval is needed                                  |
| Source scope     | Which approved sources are eligible                               |
| Limitations      | What embeddings cannot prove                                      |
| Metadata filters | Approval status, region, product, date, and permissions           |
| Validation       | Relevance, source quality, access control, and unsupported claims |

Key takeaway: Embeddings represent meaning, and vector search finds semantically similar content. They can improve retrieval when wording differs, but they do not establish whether a source is trustworthy or authorized. Always combine semantic retrieval with source-readiness checks, metadata filtering, access controls, and validation.


## Summary: Real-World Example — Retrieval Pattern and Source Readiness

A life sciences customer wants an API to answer field-team questions using approved product guidance, regional policy addenda, and internal support articles. Some documents are approved and current, while others are drafts or outdated.

### 1. Source readiness decisions

| Candidate source                  | Decision            | Reason                                                              |
| --------------------------------- | ------------------- | ------------------------------------------------------------------- |
| Current approved product guidance | Validate            | Confirm owner, version, audience, and permissions before inclusion. |
| Regional policy addenda           | Include or validate | Confirm approval, freshness, region, and effective date.            |
| Internal support articles         | Validate            | Verify authority, audience, and approval status.                    |
| Draft field training deck         | Exclude             | Draft content is not approved for grounding answers.                |
| Outdated training deck            | Exclude             | Outdated guidance may produce incorrect answers.                    |

### 2. Recommended RAG approach

Use retrieval to ground field-team answers in approved, current product guidance and validated regional addenda. However, defer implementation until critical source-readiness and permission questions are resolved.

Apply metadata filters for:

- Product
- Region
- Approval status
- Effective date
- User or field-team permissions

### 3. Why embeddings and vector search help

They can find relevant passages even when field-team questions use different wording from official documents. However, semantic similarity does not prove that a source is approved, current, complete, or authorized for access.

### 4. What to test before implementation

- Missing or incomplete source content
- Conflicting regional and product guidance
- Outdated or superseded documents
- Unsupported claims in generated answers
- Permission boundaries for different field-team roles
- Correct metadata filtering and source references

Key takeaway: A defensible retrieval design combines the right RAG pattern with source-readiness checks, metadata filtering, access controls, and verification tests. Exclude unapproved or outdated materials, validate uncertain sources, and proceed only when critical risks have been addressed.


## Exercise solution: Evaluate Retrieval Pattern and Source Readiness

### 1. Recommended decision

## Defer pending source readiness

The customer’s warranty workflow is a good candidate for RAG because answers depend on approved policies, product categories, regions, and effective dates. However, key source ownership, versioning, and data-sensitivity issues must be resolved before implementation.

### 2. Evaluate candidate sources

| Candidate source             | Decision | Reason                                                                                                                                                |
| ---------------------------- | -------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| Current warranty policy      | Include  | Approved for support use, has accountable owners, and is updated quarterly. Track policy version and effective date.                                  |
| Regional warranty addendum   | Validate | Confirm ownership, approval, regional applicability, and missing effective dates before use.                                                          |
| Product support articles     | Validate | Separate internal-only from customer-facing content and confirm approval for the intended workflow.                                                   |
| Archived warranty deck       | Exclude  | Two years old and still appearing in search results; exclude it from retrieval to prevent outdated answers.                                           |
| Agent notes from prior cases | Exclude  | Contain customer-specific details and inconsistent handling. Reconsider only if appropriately anonymized, approved, and validated for a specific use. |

### 3. Metadata and permission filters

The retrieval system should apply these filters before passing content to the model.

| Filter                           | Purpose                                                                  |
| -------------------------------- | ------------------------------------------------------------------------ |
| `product_category`               | Retrieve guidance for the correct product.                               |
| `region`                         | Apply the correct regional warranty rules.                               |
| `approval_status`                | Include only approved content.                                           |
| `effective_date`                 | Exclude policies not yet effective or no longer valid.                   |
| `audience`                       | Prevent internal-only guidance from appearing in customer-facing drafts. |
| `user_role` / access permissions | Ensure agents retrieve only content they are authorized to access.       |
| `source_version`                 | Avoid retrieving superseded policy versions.                             |

### 4. Validation owners and open questions

- Legal and Support Ops: Confirm the current warranty policy is authoritative and define precedence when policies conflict.
- Regional policy owner: Confirm ownership, approval, and missing effective dates for regional addenda.
- Knowledge-base owner: Classify support articles by audience and approval status.
- Security and Privacy: Review permissions and determine whether historical case notes may be used safely.
- Implementation team: Test filtering, source references, conflicting rules, missing evidence, and outdated documents.

### 5. Optional stretch: Freshness and permissions

- Freshness rule: Retrieve only the currently approved and effective policy version. Revalidate sources when their review date expires or a new version is published.
- Permission rule: Enforce role- and audience-based access controls in the retrieval layer before content reaches the model. Do not rely on the model alone to protect restricted information.

### 6. Final RAG recommendation

Use a retrieval-plus-structured-output pattern with agent review once critical source-readiness issues are resolved. Responses could contain the answer, policy references, product category, region, effective date, and a `needs_review` flag.

Test regional conflicts, missing effective dates, expired policies, unauthorized content, and unsupported claims before launch.

Reflection: RAG is appropriate because warranty answers depend on changing, authoritative source content. But retrieval should not begin with every document available. The safest approach is to include approved policy sources, validate uncertain sources, exclude unreliable content, and enforce access controls before implementation.