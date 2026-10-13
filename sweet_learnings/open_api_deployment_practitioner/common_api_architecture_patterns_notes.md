# Notes: Common API Architecture Patterns

## 1. What is an API architecture pattern?

An **API architecture pattern** describes how an AI system interacts
with an application, data source, external tool, or user to complete a
workflow.

The goal is to choose the **simplest architecture that meets the
business requirements safely and reliably**.

At this stage, focus on: - What the workflow needs to accomplish. - What
information the system needs. - Whether it needs external data or
actions. - What output it must produce. - What validation, approvals,
and handoffs are required.

Do not select a model or capability yet. Instead, document the
requirements that will guide that decision later.

## 2. The seven common API architecture patterns

### 1. Simple model call

The application sends instructions and input to the model and receives a
response.

**Best for:** Simple, self-contained tasks.

**Examples:** Summarization, rewriting, classification, drafting, and
reasoning over supplied content.

**Requirements:** Input context, instructions, response format, error
handling, and human review where needed.

### 2. Structured output

The response follows a predefined schema, such as JSON with required
fields.

**Best for:** Downstream processing.

**Examples:** Extracting invoice details, categorizing support tickets,
or generating review decisions.

**Requirements:** Required fields, data types, allowed values,
validation rules, and handling for missing or invalid fields.

### 3. Retrieval-grounded response

The application retrieves relevant information from approved sources and
supplies it as context for the response.

**Best for:** Internal or source-specific knowledge.

**Examples:** Answering questions about company policies, product
documentation, or employee procedures.

**Requirements:** Approved sources, access permissions, information
freshness, evidence or citations, and behavior when relevant information
is unavailable.

### 4. Tool or action workflow

The system interacts with another service to retrieve information,
perform calculations, check live status, or execute an action.

**Best for:** External systems and real-world actions.

**Examples:** Checking order status, calculating a quote, creating a
support ticket, or updating a record.

**Requirements:** Approved tools, permitted operations, input
validation, execution boundaries, approval gates, and audit logs.

### 5. Agentic workflow

The system plans and coordinates multiple steps, potentially using
multiple tools and maintaining state.

**Best for:** Complex, multi-step work.

**Examples:** Investigating a complicated support case across systems or
coordinating a multi-stage business process.

**Requirements:** Defined goals, permitted actions, workflow state, step
sequencing, approval points, escalation, and recovery or handoff
procedures.

### 6. Realtime, voice, or multimodal workflow

The system processes or produces audio, images, video, or other
modalities, potentially in a low-latency interactive experience.

**Best for:** Experiences requiring media or live interaction.

**Examples:** Voice assistants, visual inspection, spoken customer
support, or live interpretation of images.

**Requirements:** Input/output modalities, latency expectations,
consent, media quality, privacy, retention, and fallback behavior.

### 7. Hybrid pattern

Combines two or more patterns when one alone cannot meet the
requirements.

**Best for:** Workflows with multiple genuine needs.

**Examples:** Retrieving company policy, producing structured results,
and creating a case after approval.

**Requirements:** A clear reason for each component, coordination
between components, failure handling, validation, and operational
ownership.

## 3. Quick comparison table

  -----------------------------------------------------------------------
  Pattern                 Main value              Key design decision
  ----------------------- ----------------------- -----------------------
  Simple model call       Generates or transforms Input and response
                          content                 handling

  Structured output       Makes results           Schema and validation
                          machine-readable        

  Retrieval-grounded      Uses approved knowledge Sources, permissions,
                                                  freshness

  Tool/action             Reads or changes        Access boundaries and
                          external systems        approvals

  Agentic                 Coordinates multiple    State, sequencing,
                          steps                   escalation

  Realtime/multimodal     Supports media and live Latency, consent,
                          interaction             fallback

  Hybrid                  Combines necessary      Coordination and added
                          patterns                complexity
  -----------------------------------------------------------------------

## 4. How to choose the right pattern

Use these questions in order.

1.  **Is all the required information already available in the
    request?**
    -   Yes: Start with a simple model call.
    -   No: Determine whether the workflow needs retrieval or an
        external system.
2.  **Must the response follow a fixed format?**
    -   Yes: Add structured output if downstream processing requires it.
3.  **Does the workflow require approved knowledge or live system
    access?**
    -   Approved knowledge: Consider retrieval-grounded responses.
    -   Live data or actions: Consider a tool/action workflow.
4.  **Must the system plan and coordinate multiple steps?**
    -   Yes: Consider an agentic workflow only if simpler, bounded steps
        are insufficient.
5.  **Does the experience genuinely require audio, images, or
    low-latency interaction?**
    -   Yes: Consider a realtime or multimodal pattern.
6.  **Are multiple patterns necessary?**
    -   Combine them only when each pattern solves a distinct
        requirement that the others cannot adequately address.

**Note:** These patterns are not mutually exclusive. For example, a
workflow may retrieve approved information, return a structured
response, and use a bounded tool call. That is a hybrid design.

## 5. What to document at the architecture stage

For each workflow, record the following requirements without committing
to a specific model or implementation.

  -----------------------------------------------------------------------
  Area                                Questions to answer
  ----------------------------------- -----------------------------------
  Business objective                  What problem does the workflow
                                      solve?

  Inputs                              What information does the
                                      application or user provide?

  Knowledge                           Are approved internal sources
                                      required?

  External systems                    Must the workflow read data or
                                      perform actions?

  Output                              Is free text sufficient, or are
                                      fixed fields required?

  Validation                          What must be checked before the
                                      result is accepted or used?

  Risk and approval                   Could an incorrect response or
                                      action cause harm? Is human
                                      approval required?

  Interaction                         Is standard text sufficient, or is
                                      realtime/media interaction
                                      essential?

  Failure handling                    What happens when data, tools, or
                                      validation are unavailable?

  Handoff                             Who or what receives the result
                                      next?
  -----------------------------------------------------------------------

These requirements will later inform model and capability selection,
detailed retrieval design, tool contracts, orchestration, and production
monitoring.

## 6. Example: Applying the patterns

Imagine a customer support workflow that answers policy questions and
may create support tickets.

1.  **Customer asks a question.**
2.  **Retrieve approved support policies.**
3.  **Generate a structured answer with supporting sources.**
4.  **Determine whether a ticket is needed.**
    -   If no, return the answer.
    -   If yes, validate the proposed action and obtain required
        approval.
5.  **Create the ticket through an approved support system.**

The initial architecture could be a **hybrid pattern** consisting of
retrieval-grounded responses, structured output, and a bounded
tool/action workflow.

A full agentic workflow may not be necessary if the steps and decision
rules are predictable. The ticket creation action should have an
explicit authorization boundary, and any required human approval should
occur before execution.

## 7. Use the Minimum Useful Pattern
Choose the simplest API architecture that responsibly meets the workflow requirements. Do not add capabilities just because they are available.
- Simple model call / structured output: When the input provides the needed context; use structured output when predictable fields are required.
- Retrieval: When approved internal information is needed but is not already provided.
- Tool/action: When live data, calculations, or system actions are required.
- Agentic workflow: When complex multi-step coordination, state, and approvals are necessary.
- Realtime/multimodal: When voice, images, audio, or low-latency interaction is essential.
- Hybrid: When multiple patterns are genuinely needed to meet the requirements.

## 8. Use these four parts:
1. Workflow need: Why is this pattern appropriate for the task?
2. What it enables: What specific capability or outcome does it support?
3. What it does not solve: What limitations, risks, or decisions remain unresolved?
4. Open validation question: What must be confirmed before building?

Example
We recommend a structured output pattern because relationship managers need consistent, reviewable client briefings. This enables the application to display predictable fields, such as account summaries, recent issues, and preparation questions. It does not resolve source approval, access permissions, or compliance requirements. Before build, validate whether the application can supply all approved account context directly or whether retrieval is required.
