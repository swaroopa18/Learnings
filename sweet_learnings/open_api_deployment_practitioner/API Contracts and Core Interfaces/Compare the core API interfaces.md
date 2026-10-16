## Summary: Responses API

The Responses API is the recommended starting point for new projects that require controlled model interactions, structured outputs, tool use, or supported multimodal and agentic workflows. The choice should be based on the workflow’s requirements and validated against current official documentation.

### Key takeaways

- Model interaction: Control how the application interacts with the model.
- Output shape and structured output: Define predictable response fields and review flags.
- Tool behavior: Support workflows that require tools, such as ticket-status lookups, subject to current tool support.
- Multimodal and agentic patterns: Use these capabilities where currently supported and relevant.
- State management: Chain turns using `previous_response_id` without creating a Conversations object. Use the Conversations API when durable conversation state across sessions, devices, or jobs is needed.
- Application responsibility: The API provides the inference interface, while the application manages tool execution, pending work, returned results, and downstream use.

### Example use case

For a support-case summary using GPT-6 Astra, the workflow might require:

1. A structured case summary with defined fields.
2. A review flag to identify cases requiring attention.
3. A potentially slow ticket-status lookup.
4. The ability to accept changed user requirements while work is in progress.

The Responses API may be a suitable starting point, but the application must define how ongoing work, tool results, and changed requirements are handled.

### Documentation to validate before implementation

- Supported tools and tool configurations.
- Structured-output options.
- Streaming and asynchronous behavior.
- SDK examples and implementation patterns.
- Multimodal capabilities.
- Current availability, constraints, and limitations.

### Recommendation for technical pre-sales and partner consultants

In the Core Interface and API Contract Plan, explain why the Responses API fits the workflow rather than simply naming it. Document the required capabilities and outstanding validation points.

Bottom line: Recommend Responses API as a fit for the workflow, distinguish inference from state management and application logic, and validate implementation details against current official documentation before making build commitments.


-------------------------------------------------------------

## Chat Completions API — Explained in Simple Words
Think of the Chat Completions API as an older way for your application to talk to an AI model using messages, similar to a chat conversation.
For example:
- User: What is AI?
- Assistant: AI stands for Artificial Intelligence.
Your application sends messages to the model and receives a response.

### There are 3 important things to understand
1. Chat Completions API — the older, still-supported approach
If a company already has an application using Chat Completions, it can continue using it. The team can maintain the code, fix bugs, or add features without automatically changing the API.
2. Responses API — the recommended choice for new projects
For new applications, OpenAI recommends the Responses API. It supports workflows involving things like tool use, structured outputs, and multi-step interactions.
3. Conversations API — helps maintain conversation continuity
When an application needs to remember the context of a conversation across multiple interactions, the Conversations API can help manage persistent conversation state when used with the Responses API. Alternatively, the application can manage that state itself.

### Real-world example
Imagine a company has a customer support chatbot built using Chat Completions.
Now the company wants a new AI assistant that can:
- Summarize customer conversations in a structured format.
- Use tools to retrieve information.
- Handle follow-up questions over several turns.
What should the solution architect do?
1. Check the existing system: It uses Chat Completions, so compatibility matters.
2. Evaluate the Responses API: It may be a better fit for the new requirements.
3. Decide how to manage conversation history: The application can manage it, or the team can use the Conversations API with Responses.
4. Consider integration risks: Changing the API could affect existing code, tests, data formats, and other systems.
The team should make a decision based on the requirements, not simply copy the old design.

### The key lesson to remember
Existing project = respect compatibility.
New project = evaluate the Responses API first.
Need ongoing conversation context = decide how to manage state, potentially using the Conversations API with Responses.

--------------------------------------------------------------------------------------------------------------------------

# Conversations API — Study Notes

## 1. What is the Conversations API?

The Conversations API helps an AI application **maintain conversation state across multiple interactions**.

It allows a conversation to continue across sessions, devices, or jobs using a persistent conversation object with its own unique ID.

**Example:** A customer reports a payment issue today and asks for an update tomorrow. The system can use the saved conversation context to continue helping.

## 2. How do the APIs differ?

- **Responses API:** Used to send input to the AI and generate responses.
- **Conversations API:** Helps maintain persistent conversation state when used with Responses.
- **Chat Completions API:** An older, still-supported interface for generating chat responses.

**Remember:** Conversations is not a third inference API alongside Responses and Chat Completions.

## 3. What is conversation state?

Conversation state is the information needed to continue a conversation, such as previous messages or relevant context.

Example:
- Day 1: User reports a payment problem.
- Day 2: User asks for an update.
- The system retrieves the relevant context so the user does not have to explain everything again.

## 4. When should we use the Conversations API?

Use it when the workflow needs:
- Follow-up questions about an earlier interaction.
- Continuity across sessions or devices.
- Ongoing customer support cases.
- Multi-step tasks that continue over time.
- Persistent context across jobs or interactions.

## 5. When is it unnecessary?

A single stateless request may be enough when all the information needed to answer is included in that request.

**Rule:** Do not use persistent conversation state unless the workflow requires it.

## 6. Important design considerations

Before implementation, decide:

1. **What is retained?** Messages, summaries, or case details.
2. **Where does state live?** In the Conversations API or your own application.
3. **Who owns it?** Which team or system manages the state.
4. **How long is it retained?** Define the retention period and policy.
5. **What privacy constraints apply?** Protect user information and control access.
6. **How is failure handled?** Plan for missing, unavailable, or mismatched conversation state.
7. **How does it affect testing?** Test follow-ups, context accuracy, and recovery.
8. **How is it documented?** Record state handling, logging, and handoff procedures.

## 7. What is state ownership?

State ownership means deciding which system is responsible for managing and controlling conversation data.

- Application-managed state: Your application stores and retrieves the required context.
- Conversations API-managed state: The conversation object is maintained through OpenAI's API, while your application remains responsible for using the correct conversation ID and managing its own data-handling requirements.

## 8. Benefits and risks

**Benefits**
- Better continuity.
- Fewer repeated questions.
- More convenient multi-turn workflows.

**Risks**
- Privacy and retention concerns.
- Incorrect or missing context.
- Additional testing and operational complexity.

## 9. Solution architect's responsibility

A solution architect must determine whether persistent state is necessary, define what is retained, decide who owns it, and plan for privacy, testing, and failure recovery.

## 10. Quick revision

- Responses API = generates responses.
- Conversations API = helps preserve conversation state.
- Chat Completions API = existing, supported chat interface.
- Stateless request = everything needed is supplied in the request.
- Persistent state = information is maintained for future interactions.
- Conversations API is optional, not a default requirement.

**Golden rule:** Use the Conversations API when persistent continuity is needed, and document how state is stored, managed, protected, and recovered.

### Possible exam question

**Q: What should an architect evaluate before using the Conversations API?**

**Answer:** Whether the workflow requires persistent continuity, what information is retained, where the state lives, who owns it, how long it is retained, which privacy policies apply, and how failures and testing are handled.

-------------------------------------------------------------


# Interface Decision Table — Simple Notes

## 1. Main concept

When building an AI application, you need to make two separate decisions:

1. Inference interface: Which API will generate the AI response?
2. State approach: Does the application need to remember previous interactions?

## 2. Understand the three APIs

| API                  | When to use it                                                            | Remember                                                      |
| -------------------- | ------------------------------------------------------------------------- | ------------------------------------------------------------- |
| Responses API        | Recommended starting point for new projects                               | Generates responses and supports tools and structured outputs |
| Chat Completions API | Maintaining an existing application or meeting compatibility requirements | Still supported                                               |
| Conversations API    | When persistent conversation state is needed with Responses               | Helps maintain context across interactions                    |

## 3. How to choose the right API

Step 1: Understand the workflow

What does the application need to do?

Step 2: Choose the inference interface

Usually Responses for new projects; consider Chat Completions for existing systems and compatibility.

Step 3: Decide on state

Need persistent context? Consider Conversations. Otherwise, a stateless request or application-managed state may be sufficient.

Step 4: Validate before building

Check capabilities, privacy, retention, limitations, testing, and compatibility.

## 4. Questions to ask before making a recommendation

- What does the application need to do?
- Does it require structured output?
- Does it need to use tools?
- Must it remember previous conversations?
- Is there an existing implementation that must remain compatible?
- What product limitations, privacy requirements, or migration risks need to be checked?

## 5. Practical example

A company wants to build a new customer support assistant that summarizes cases, retrieves information using tools, and remembers follow-up questions.

Possible recommendation:

- Inference interface: Responses API.
- State approach: Consider the Conversations API for persistent context across follow-ups.
- Before implementation: Validate required capabilities, state retention, privacy, recovery behavior, and current documentation.

If the company already has a Chat Completions implementation, assess compatibility and migration impact before changing it.

-------------------------------------------------------------

# Exercise: Choose the Right Core API Interface

## 1. Compare the three workflows

| Workflow                      | Inference interface                                                                 | State approach                                                       |
| ----------------------------- | ----------------------------------------------------------------------------------- | -------------------------------------------------------------------- |
| A. Customer-support assistant | Responses API                                                                       | Persistent Conversations object with Responses, if needed            |
| B. Simple stateless summary   | Responses API                                                                       | Stateless                                                            |
| C. Existing FAQ chatbot       | Chat Completions API if compatibility requires it; evaluate Responses for new needs | Existing state approach, or application-managed state if appropriate |

## 2. Rationale for each choice

### A. Customer-support workflow

Requirements: Structured case summaries, approved account context, ticket-status tool use, follow-up questions, and dashboard integration.

- Interface: Responses API, recommended starting point for a new workflow.
- State: Consider the Conversations API if the workflow needs persistent continuity across sessions. Otherwise, application-managed state or chained Responses may be sufficient.
- Validate: Structured output requirements, tool behavior, account-data permissions, conversation retention, dashboard field formats, and compatibility with the existing chatbot.

### B. Simple stateless workflow

Requirements: A user pastes a short support note and receives a concise summary for human review.

- Interface: Responses API as the recommended starting point for a new project.
- State: Stateless, because the request contains everything needed and no follow-up context is required.
- Validate: Output format, summary quality, model suitability, privacy requirements, and current API capabilities.

Why? A persistent conversation object would add unnecessary complexity when there is no need to remember previous interactions.

### C. Existing chat-style FAQ workflow

Requirements: Maintain an existing FAQ bot while reviewing whether a new workflow needs a different interface.

- Interface: Keep Chat Completions if compatibility is important and the current implementation meets requirements. Evaluate Responses for new capabilities or new workflows.
- State: Retain the existing state approach if it meets requirements. Use application-managed state, chained Responses, or persistent Conversations with Responses if the new design calls for it.
- Validate: Existing integrations, tests, message formats, tool requirements, migration effort, operational risks, and current support guidance.

Why? An existing implementation does not automatically need to be migrated just because a newer interface is recommended for new projects.

## 3. What must be checked in current documentation?

For all three workflows, validate:

- Required API capabilities and limitations.
- Structured output and tool support.
- State handling and conversation continuity.
- Privacy, retention, and data-handling requirements.
- SDK examples and integration compatibility.
- Testing, monitoring, and failure recovery.

## 4. Optional stretch question

Q1. Why might a customer still use Chat Completions?

Because their existing application, integrations, tests, and operational processes depend on its message format and behavior. Changing it may introduce cost, risk, and additional work.

Q2. What question should guide migration planning?

“What changes to state management, tools, output formats, integrations, and tests would be required if we moved this workflow to the Responses API?”