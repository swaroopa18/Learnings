## State and Context

1\. Stateless Requests

- Each request contains all required information.
- Does not depend on previous interactions.
- Easier to test, validate, and repeat.
- Best for simple workflows and when data retention should be minimized.

2\. Stateful Interactions

- Maintains context across multiple interactions.
- Retains information such as previous answers, user preferences, or case details.
- Best for follow-up questions and ongoing workflows.

3\. State Management For stateful systems, define:

- What is stored and where.
- Who owns the state.
- How long it is retained.
- Privacy policies and handling of missing, stale, or mismatched state.

4\. Context Management

- Too little context leads to incomplete responses.
- Too much context increases cost and latency.
- Include only relevant information.

5\. Testing

- Stateless: Verify each request works independently.
- Stateful: Test continuity, missing state, stale state, and mismatched state.
- Track asynchronous tool calls and preserve action history when users revise requests.

Key takeaway: Use stateless requests when possible and stateful interactions when continuity is necessary. Document decisions in the API contract and translate them into tests.

## Tools and Actions

- Tools are external capabilities used to retrieve information, perform calculations, or interact with other systems.
- Examples: checking ticket status, retrieving account details, checking inventory, and updating records.

API Contract should define:

1. Purpose: What the tool does.
2. Input: Required fields or arguments.
3. Output: Expected results.
4. Execution boundary: What the model requests vs. what application code executes.
5. Permissions: Allowed system and data access.
6. Failure handling: How errors or incomplete results are managed.
7. Approval: Whether user approval is required.

Types of tool use:

- Read-only: Retrieves information without changing systems.
- Action-taking: Changes records, sends messages, or creates tasks; requires stronger approval, logging, and verification.

Key takeaway: Determine whether the workflow needs tools. Define tool inputs, outputs, permissions, and failure behavior in the API contract. System-changing actions need clear approval and verification rules.

## Streaming and Async Behavior

1\. Standard Response

- Returns the complete response after processing finishes.
- Best when a complete, validated output is required.

2\. Streaming

- Delivers output progressively as it is generated.
- Useful for long explanations, drafts, and conversational responses.
- The client must handle partial output and final completion.

3\. Asynchronous Behavior

- Allows long-running work to continue without making the client wait.
- The client checks status and retrieves the result later.
- Useful for slow tools, data retrieval, and external systems.

Types of Async Work

- Background response generation: Start generation and retrieve the result later.
- Async tool calling: The application runs a tool while independent work continues. Dependent steps must wait for the tool result.

4\. API Contract Must Define

- How success and completion are identified.
- How progress is tracked.
- Timeout and failure handling.
- Retry behavior.
- What the client should do next.

5\. Important Rules

- Never treat pending work as completed.
- Do not invent missing tool results.
- Track response IDs and tool-call IDs.
- Streaming does not replace final structured-output validation.
- Revised instructions do not undo actions already performed.

Key takeaway: Use standard responses for complete results, streaming for progressive output, and async behavior for long-running tasks. Define completion, failure, timeout, and retry rules in the API contract.

## Structured Outputs

- Structured outputs provide predictable fields for downstream systems, dashboards, routing, and validation.
- OpenAI Structured Outputs: Enforces adherence to a supported JSON schema.
- JSON mode: Ensures valid JSON but does not guarantee schema adherence.

Common fields:

- `issue_type`
- `urgency`
- `recommended_next_action`
- `source_ids`
- `needs_human_review`
- `review_reason`

Define before implementation:

1. Required and optional fields.
2. Field meanings and data types.
3. Allowed values.
4. Invalid or incomplete output handling.
5. Refusal and human-review procedures.

Important points:

- A model-generated confidence note is not a calibrated confidence score.
- Schema adherence does not guarantee factual accuracy.
- Use validation, evaluators, or human review for high-risk decisions.
- Convert schema requirements into automated tests.

Key takeaway: Structured outputs improve reliability and integration by ensuring predictable data fields and clearly defined error-handling rules.

## Idempotency and Retries

- Retries: Repeat a request after a timeout, temporary failure, or service issue.
- Idempotency: Ensures repeating a request does not cause unintended duplicate actions.

Importance:

- Read-only requests usually have low retry risk.
- Write operations, emails, and task creation have higher risk of duplicates.

Best practices:

- Check whether repeating a request is safe.
- Use a unique `request_id` or idempotency key for deduplication where needed.
- Define retry conditions and failure handling in the API contract.
- Test for duplicate records or customer-visible actions.

Key takeaway: Define retry and idempotency rules to prevent unintended duplicate work, especially for actions that modify systems.


## Illustrative Example: Interface Choice

Customer-support workflow requirements:

- Remember the current case.
- Ask clarifying questions when details are missing.
- Call a ticket-status tool.
- Return structured output with `issue_type`, `urgency`, `recommended_next_action`, and `needs_human_review`.

Design considerations:

1. Stateless: Include all required case details and approved context in every request.
2. Stateful: Define what is retained, where it is stored, retention period, ownership, and failure handling.
3. Tool use: Specify tool inputs, expected outputs, permissions, errors, and verification.
4. Structured output: Define required fields and data types before testing.
5. Testing: Validate missing context, unavailable tools, invalid output, and human-review triggers.

Key takeaway: Choose an interface that supports the workflow’s state, tool-use, and structured-output requirements. Document assumptions, errors, dependencies, and tests in the API contract.

## Exercise: Map Interface Implications — Sample Answer

Workflow: Customer-support assistant

| Area              | Interface implication                                                            |
| ----------------- | -------------------------------------------------------------------------------- |
| State             | Retain the current case for follow-up questions.                                 |
| Context           | Include case details and approved context.                                       |
| Tools             | Use a ticket-status lookup tool; define inputs and errors.                       |
| Streaming         | Optional for showing summaries progressively.                                    |
| Async             | Use if ticket lookup takes longer; track pending and completed status.           |
| Structured output | Return `issue_type`, `urgency`, `recommended_next_action`, `needs_human_review`. |
| Retries           | Retry temporary failures under defined rules.                                    |
| Idempotency       | Prevent duplicate actions using a request ID for write operations.               |
| Verification      | Test missing context, tool failures, invalid output, and review triggers.        |

### Additional checks

- Pending work: Do not mark a response or tool call complete until it finishes.
- Tool results: Match each result to its original tool-call ID.
- Revised instructions: Track the revision and its status.
- Failed steering: Report failure; retry only through an explicit application action.
- Privacy: Define where case state is stored and how long it is retained.
- Write-action safety: Confirm retries cannot send duplicate emails or create duplicate tasks.

### Reflection

Interface choices determine how context is maintained, tools are executed, results are delivered, and failures are handled. Document these decisions and convert them into testable API requirements.