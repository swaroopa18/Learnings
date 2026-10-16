## Define the Request

A request contract defines what the caller sends to the API.

Key elements:

1. Endpoint purpose: What the API should accomplish.
2. Method and route: e.g., `POST /case-summary`.
3. Headers: Content type and request metadata.
4. Authentication: How the caller is verified.
5. Caller type: User, application, or internal service.
6. Required fields: Information that must be provided.
7. Optional fields: Information that may be included.
8. Validation rules: Allowed values and input constraints.
9. Context/state reference: Required conversation or context IDs.
10. Excluded fields: Sensitive or unapproved information.

Example: Support-case summary

- Purpose: Generate an internal support-case summary.
- Caller: Authenticated internal dashboard.
- Method: `POST /case-summary`
- Required fields: `account_id`, `issue_text`, `approved_context_ids`
- Optional fields: `user_question`, `case_priority_hint`
- Validation: Required fields must be valid; context IDs must reference approved sources.
- Excluded: Payment details, credentials, secrets, and unapproved account notes.

Key takeaway: Define clear inputs, validation, authentication, and exclusions. Distinguish the application's endpoint from the OpenAI API interface used behind it.

## Define the Response

A response contract defines what the API returns and how the client should handle it.

Key elements:

1. Success status code or condition.
2. Response body and required structure.
3. Required and optional fields.
4. Source, evidence, and review fields.
5. Next steps for the client or reviewer.
6. Error handling for incomplete, unsafe, or invalid output.

Example response fields:

| Field                     | Type                    | Purpose                                  |
| ------------------------- | ----------------------- | ---------------------------------------- |
| `issue_summary`           | String                  | Summary of the customer issue            |
| `urgency`                 | Enum: low, medium, high | Priority for review                      |
| `recommended_next_action` | String                  | Suggested next step                      |
| `source_ids`              | Array of strings        | Approved supporting sources              |
| `confidence_note`         | String                  | Explains uncertainty                     |
| `needs_human_review`      | Boolean                 | Indicates whether human review is needed |
| `review_reason`           | String or null          | Explains why review is required          |

Important rules:

- Define a schema for predictable output.
- Validate source IDs against approved sources.
- An empty `source_ids` array should trigger review or a defined failure response.
- A confidence note is not a calibrated confidence score.
- Define fallback behavior for refusals, missing context, and invalid output.
- Separate machine-readable fields from human-review information.

Key takeaway: A response contract ensures predictable output, clear error handling, and safe downstream integration.

## Structured-Output Requirements

Definition: Structured-output requirements specify the format, fields, data types, and rules an API response must follow for reliable processing.

### 1. Purpose

Used for:

- Dashboards and reporting
- Routing and workflow automation
- Tool inputs
- Human review
- Downstream system processing

### 2. Key Requirements

- Required fields: Must be present.
- Optional fields: May be omitted if permitted.
- Data types: String, number, Boolean, array, etc.
- Allowed values: Permitted values, e.g., `low`, `medium`, `high`.
- Field meaning: Defines the purpose of each field.
- Invalid-output behavior: Reject, retry, or escalate invalid responses.

### 3. Governance Fields

- `source_ids` – identifies supporting sources.
- `confidence_note` – explains uncertainty.
- `needs_human_review` – indicates whether manual review is needed.
- `review_reason` – explains the need for review.
- `escalation_path` – specifies the next review step.

### 4. Structured Outputs vs. JSON Mode

- Structured Outputs: Enforces adherence to a supported JSON Schema.
- JSON mode: Produces valid JSON but does not guarantee schema compliance; application-side validation is required.

### 5. Validation

- Structural validation: Checks missing fields, incorrect types, malformed JSON, and invalid values.
- Application validation: Checks business rules and relationships between fields.

In strict Structured Outputs, every property must be listed in `required`. Nullable fields can contain `null` but cannot be omitted.

### 6. Error Handling

Reject or retry invalid responses when appropriate. Handle refusals and incomplete responses separately, and escalate cases requiring human review.

Key takeaway: A good structured-output contract defines the schema, validation rules, and failure-handling behavior so API responses are reliable and safe for downstream use.

## Define Error States and Status Codes

Definition: Error states and status codes describe possible API failures, their causes, and the actions required to recover safely.

### 1. Common Error States

- Missing required field
- Invalid data type or allowed value
- Invalid authentication
- Unauthorized access
- Unsupported input or workflow
- Missing context or unavailable source
- Timeout or dependency failure
- Asynchronous failure
- Structured-output failure
- State or conversation-reference mismatch

### 2. What to Define for Each Error

1. Condition: What triggers the error.
2. Status code: HTTP status code or internal failure category.
3. User-safe message: Clear explanation without exposing sensitive details.
4. Next step: Retry, correct input, request access, or escalate for review.

### 3. Common HTTP Status Codes

| Code | Meaning               | Example                           |
| ---- | --------------------- | --------------------------------- |
| 400  | Bad Request           | Invalid input                     |
| 401  | Unauthorized          | Missing or invalid authentication |
| 403  | Forbidden             | Insufficient permission           |
| 404  | Not Found             | Resource does not exist           |
| 408  | Request Timeout       | Request took too long             |
| 422  | Unprocessable Content | Input fails semantic validation   |
| 429  | Too Many Requests     | Rate limit exceeded               |
| 500  | Internal Server Error | Unexpected server failure         |
| 502  | Bad Gateway           | Invalid upstream response         |
| 503  | Service Unavailable   | Dependency unavailable            |
| 504  | Gateway Timeout       | Upstream service timed out        |

### 4. Examples

- Missing field: Message: “The account identifier is missing.” Action: Resubmit with `account_id`.
- Unauthorized access: Message: “You do not have access to this account.” Action: Deny access and log the failure.
- Source unavailable: Message: “Approved source context is unavailable.” Action: Request human review or return a structured failure.
- Structured-output failure: Message: “The response could not be produced in the required format.” Action: Retry safely or escalate for review.

### 5. Important Principles

- Separate authentication, authorization, validation, dependency, and model-output failures.
- Never expose sensitive internal details in user-facing errors.
- Retry only when appropriate; use backoff for transient failures.
- Log errors for debugging and auditing.
- Define recovery actions and escalation paths before implementation.

Key takeaway: A complete API contract specifies not only successful responses but also failure conditions, status codes, safe messages, and recovery behavior.

## Make the API Contract Specific Enough to Test

Definition: An API contract must clearly define inputs, outputs, validation rules, errors, and review behavior so developers can implement and testers can verify it.

### 1. Avoid Vague Requirements

Examples:

- “Send some text.”
- “Return a summary.”
- “Make a recommendation.”
- “Use the right context.”
- “Handle errors gracefully.”

These statements lack clear rules and measurable outcomes.

### 2. Specify the Following

- Request shape: Expected input format.
- Required fields: Fields that must be provided.
- Optional fields: Fields that may be omitted.
- Validation rules: Accepted types, values, and constraints.
- Response fields: Expected output structure.
- Structured outputs: Required schema and field types.
- Error states: Failure conditions and status codes.
- Review behavior: When human review is required.
- Test examples: Valid and invalid requests with expected results.

### 3. Example

Weak contract: “The API should summarize customer issues and suggest what to do next.”

Strong contract: The API accepts `account_id`, `issue_text`, and `approved_context_ids`. It returns `issue_summary`, `source_ids`, `urgency`, `recommended_next_action`, `confidence_note`, `needs_human_review`, and `review_reason`.

If approved context is missing, the API must not invent source-backed claims and must flag human review or return a structured failure.

### 4. Benefits

- Reduces ambiguity and implementation errors.
- Makes testing easier.
- Improves security and reliability.
- Clarifies responsibilities across teams.
- Helps determine whether the API is ready for implementation or needs review.

Key takeaway: A good API contract is specific, measurable, and testable, with clearly defined success and failure behavior.

## Turning a Vague Requirement into an API Contract

Objective: Convert a general business request into clear, testable API specifications.

### 1. Vague Requirement

“The API should summarize customer issues and suggest what the account team should do next.”

Problem: It does not define inputs, outputs, validation, errors, or human-review rules.

### 2. Request Contract

| Field                  | Requirement                        | Purpose                                 |
| ---------------------- | ---------------------------------- | --------------------------------------- |
| `account_id`           | Required                           | Identifies an authorized account        |
| `issue_text`           | Required                           | Contains the issue to summarize         |
| `approved_context_ids` | Required where grounding is needed | References approved information         |
| `user_question`        | Optional                           | Specifies a follow-up question or focus |

### 3. Response Contract

| Field                     | Purpose                           |
| ------------------------- | --------------------------------- |
| `issue_summary`           | Concise issue summary             |
| `source_ids`              | Supporting source references      |
| `urgency`                 | `low`, `medium`, or `high`        |
| `recommended_next_action` | Suggested internal action         |
| `confidence_note`         | Explains uncertainty              |
| `needs_human_review`      | Boolean review flag               |
| `review_reason`           | Explanation for review, or `null` |

All response fields must be present in the strict Structured Outputs schema. If `needs_human_review` is `true`, `review_reason` must contain a nonempty explanation.

### 4. Error States

- Missing `account_id`
- Unauthorized account access
- Missing approved context
- Source unavailable
- Invalid urgency value
- Structured-output failure

Each error should define its trigger, status code where applicable, safe error message, and recovery action.

### 5. Benefits

- Makes implementation and testing easier.
- Clarifies required inputs and outputs.
- Improves dashboard integration.
- Defines when human review is needed.
- Helps identify unresolved customer dependencies.

Key takeaway: A strong API contract transforms a vague business requirement into a specific, testable agreement covering inputs, outputs, validation, errors, and review behavior.

# Exercise: Define a Clear Interface Contract

## 1. Request contract

Endpoint: `POST /v1/customer-issues/summarize`

| Field                  | Type             | Requirement         |
| ---------------------- | ---------------- | ------------------- |
| `account_id`           | String           | Required            |
| `issue_text`           | String           | Required, non-empty |
| `approved_context_ids` | Array of strings | Required            |
| `user_question`        | String or null   | Optional            |

Authentication: Require a valid access token. The caller must have permission to access the specified account.

## 2. Response contract

| Field                     | Type             | Description                     |
| ------------------------- | ---------------- | ------------------------------- |
| `issue_summary`           | String           | Concise issue summary           |
| `source_ids`              | Array of strings | Sources supporting the response |
| `urgency`                 | String           | `low`, `medium`, or `high`      |
| `recommended_next_action` | String           | Suggested next step             |
| `confidence_note`         | String           | Explains uncertainty            |
| `needs_human_review`      | Boolean          | Indicates review requirement    |
| `review_reason`           | String or null   | Reason for review               |

## 3. Schema and structured-output requirements

Use OpenAI Structured Outputs with a supported JSON Schema and strict adherence enabled.

- All properties must be listed in `required`.
- Set `additionalProperties` to `false`.
- Define allowed values for `urgency` using an enum.
- Use explicit types for every field.
- Allow `null` only where specified.
- Validate business rules separately from the schema.

Example validation rule: If `needs_human_review` is `true`, `review_reason` must contain a nonempty explanation.

## 4. Error contract

| Error                       | HTTP status | Expected action                       |
| --------------------------- | ----------- | ------------------------------------- |
| Missing required field      | 400         | Correct and resubmit request          |
| Invalid authentication      | 401         | Authenticate again                    |
| Unauthorized account access | 403         | Deny access and log failure           |
| Approved source unavailable | 503         | Return structured failure or escalate |
| Invalid input value         | 422         | Correct the input                     |
| Structured-output failure   | 500         | Retry safely or route for review      |
| Request timeout             | 504         | Retry according to policy             |

Errors must provide safe messages without exposing sensitive internal details.

## 5. Example successful response

```
{
  "issue_summary": "Customer reports repeated billing discrepancies.",
  "source_ids": ["support-123"],
  "urgency": "high",
  "recommended_next_action": "Verify recent invoices and contact the customer.",
  "confidence_note": "Based on the available support record.",
  "needs_human_review": false,
  "review_reason": null
}
```

## 6. Testing and validation

- Verify missing fields are rejected.
- Verify invalid tokens and unauthorized accounts are denied.
- Verify `urgency` accepts only the permitted values.
- Verify all required response fields are present.
- Verify missing sources trigger the defined review or failure behavior.
- Verify incomplete responses and structured-output failures are handled safely.

## 7. Reflection

This contract makes the API specific enough to implement and test. It defines the request, response, authentication, schema constraints, error handling, and human-review rules needed for dashboard integration.

Optional stretch: Add automated tests for one invalid input, one unauthorized request, and one structured-output failure.