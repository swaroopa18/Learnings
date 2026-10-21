This module teaches how to map data movement and classify data sensitivity in an API workflow. It covers identifying what data enters, is processed, stored, logged, and sent out of the system.

It also emphasizes data minimization—collecting, accessing, storing, returning, and logging only the information necessary to reduce security risks and determine appropriate access controls, approvals, and retention requirements.

### Summary: Key Definitions

This section introduces essential concepts for reviewing API workflow security:

- Data movement: Tracks how data enters, moves through, is transformed, stored, logged, and exits a workflow.
- Data classification: Categorizes data by sensitivity and required protection.
- Sensitive data: Confidential, personal, regulated, customer-specific, or security-related information requiring extra safeguards.
- Data/system owner: The person or team accountable for data use, permissions, and approvals.
- Logged data: Information recorded for troubleshooting, monitoring, auditing, or support.
- Data minimization: Collecting, processing, storing, returning, and logging only the data necessary for the workflow.
- Abuse monitoring logs: OpenAI platform logs used to enforce policies and mitigate harmful use. By default, they may include customer content and metadata and are retained for up to 30 days, subject to exceptions.
- Application state: Customer data retained by API features to maintain or complete a workflow. Retention depends on the endpoint, settings, and object lifecycle.
- OpenAI data retention controls: Approved controls such as Modified Abuse Monitoring and Zero Data Retention, subject to eligibility and configuration. Zero Data Retention does not mean every feature is stateless.

Key takeaway: Map the complete data flow, classify sensitive information, minimize unnecessary data, identify accountable owners, and verify current OpenAI retention guidance. Make the information clear enough for security, privacy, platform, and system owners to review before implementation.

### Summary: Identify Data Movement

Security reviews should map the entire API workflow, not just the model call. Describe each step from data input to processing, storage, logging, and output.

For every step, identify:

- Data inputs: What data enters, where it comes from, and who or what sends it.
- Processing and outputs: What is transformed and what the API generates.
- Storage and logging: What is retained temporarily or persistently and what is recorded in logs.
- Data transfers: Which internal systems or external environments receive the data.
- Ownership and access: Who owns each source and destination, and what permissions are assumed.

Key takeaway: Be specific and testable. Document exactly what data is used, returned, stored, and logged. Minimize sensitive information in logs, avoid unnecessary data exposure, and identify the permissions and safeguards that must be validated before launch.


### Summary: Classify Data Sensitivity

After mapping data movement, classify all data the API receives, processes, stores, logs, or sends according to its sensitivity.

Common categories include:

- Public data: Approved for public access.
- Internal data: Intended for internal business use.
- Customer-confidential data: Customer records, communications, documents, and account details.
- Personal or regulated data: Information subject to privacy, regulatory, contractual, or industry-specific requirements.
- Secrets and credentials: API keys, passwords, tokens, certificates, and private keys that could enable unauthorized access.
- Customer- or jurisdiction-specific data: Information requiring classification by the appropriate customer or organizational stakeholders.

Key takeaway: Never guess when classification is uncertain. Mark unclear fields as unresolved and consult the appropriate security, privacy, legal, compliance, or system owner. Until confirmed, apply the highest reasonably applicable sensitivity level.

Remember that even routine support requests may contain personal details, payment information, health-related context, or confidential internal notes.


### Summary: Apply Data Minimization

Data minimization reduces security risks by ensuring an API workflow collects, sends, stores, returns, and logs only the data necessary for its task.

Key practices include:

- Collect only required fields and exclude unnecessary sensitive information.
- Mask, redact, or omit sensitive values where appropriate.
- Use subsets of records or identifiers instead of full records whenever possible.
- Minimize logging and retain only essential outputs or metadata.
- Prevent generated responses from revealing unnecessary customer details or internal information.
- Identify unresolved data-handling questions before launch.

Protect logs and understand retention:

- Logs can expose sensitive prompts, customer data, credentials, and generated outputs.
- OpenAI API data is not used to train or improve models unless the organization explicitly opts in to sharing it.
- Abuse monitoring logs may contain prompts, responses, and metadata and are retained for up to 30 days by default, subject to documented exceptions.
- Application state may be stored separately, depending on the API endpoint, capability, settings, and object lifecycle.
- Modified Abuse Monitoring and Zero Data Retention require eligibility and approved configuration. Do not assume they are enabled or that every endpoint is covered.

Key takeaway: Minimize both inputs and outputs, protect logs, distinguish abuse monitoring from application-state retention, and verify current [OpenAI data controls](https://developers.openai.com/api/docs/guides/your-data?utm_source=chatgpt.com) before implementation.


### Summary: Review Pattern — Data Boundary

A data-boundary review identifies exactly what data an API workflow handles, how sensitive it is, what should be minimized, and what still needs confirmation.

Focus on four questions:

1. What data does the API touch? Identify specific fields, records, attachments, generated outputs, logs, and system destinations rather than using vague labels like “support data.”
2. What is the highest likely sensitivity? Apply the highest reasonably applicable classification until an accountable owner confirms it.
3. What should be minimized? Exclude, mask, redact, summarize, or replace unnecessary data with identifiers. Pay special attention to free-text fields, internal notes, attachments, credentials, and generated outputs.
4. What remains unresolved? Identify who must confirm classification, source approval, retention, logging policies, and permitted data use.

Key takeaway: A strong data-boundary statement is specific, concise, and testable. It makes potential data risks visible and identifies the right owner to validate unresolved questions before launch.


## Recommended Exercise: Spot the Data Boundary

1\. Data touched:

The API receives `ticket_id`, `requester_role`, `product_area`, `subject`, `description`, `priority`, `region`, and `internal_notes` from the helpdesk. It generates an internal summary, category, risk flag, and recommended next action. The summary and category are stored in the ticket record, while the full request and response bodies are currently logged. Data is also sent to the OpenAI Responses API.

2\. Highest likely sensitivity:

Customer-confidential, personal, or potentially regulated data. Ticket descriptions and internal notes may contain personal details, account information, payment details, or other sensitive content. The classification remains unconfirmed and must not be assumed.

3\. Data that should be excluded, masked, redacted, or minimized:

- Stop logging full request and response bodies by default.
- Exclude or redact sensitive details, credentials, personal information, and unnecessary internal notes.
- Send only the ticket fields required for triage.
- Log minimal operational metadata, such as request ID, timestamp, status code, latency, and error category.
- Limit stored and generated outputs to the information staff need for triage.

4\. Unresolved data owner or classification question:

The helpdesk/system owner and customer security or privacy reviewers must confirm what production tickets may contain, the permitted purpose of processing, the classification of ticket fields, and applicable access, logging, and retention requirements.

5\. OpenAI platform storage or retention fact to verify:

Verify the current default abuse-monitoring retention behavior, including whether prompts, responses, and derived metadata are retained for up to 30 days, subject to documented exceptions. Separately, confirm whether the selected Responses API configuration stores application state and how long that state persists.

6\. OpenAI organization/project control or endpoint limitation to confirm:

Confirm whether Modified Abuse Monitoring or Zero Data Retention is approved, enabled, and available for the organization or project. Verify whether response storage is enabled and whether the selected endpoint and capabilities are eligible for the intended retention controls. Do not assume Zero Data Retention makes every endpoint stateless.

### Key takeaway

The most immediate issue is full request and response body logging, which can expose sensitive ticket content unnecessarily. Before the pilot expands, minimize the data sent and stored, establish the correct classification with accountable owners, and verify the actual OpenAI retention settings and endpoint behavior against the current [OpenAI data controls documentation](https://developers.openai.com/api/docs/guides/your-data?utm_source=chatgpt.com).


