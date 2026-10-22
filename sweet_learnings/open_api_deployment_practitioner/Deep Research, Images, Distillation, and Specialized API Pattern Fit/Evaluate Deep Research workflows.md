Summary: Evaluating Deep Research Workflows

Deep Research is a specialized Responses-based workflow suited to complex tasks that require gathering information from multiple sources, comparing evidence, resolving conflicting findings, and synthesizing results into a reviewable output.

Evaluation should focus on:

- Workflow fit: Determine whether the task needs in-depth research rather than a quick response.
- Source and tool selection: Choose reliable, relevant sources and appropriate tools.
- Prompt completeness: Clearly define the research question, scope, constraints, expected output, and evidence requirements.
- Background execution: Assess whether the workflow can run asynchronously for longer research tasks.
- Validation: Verify facts, citations, source quality, and consistency of findings.
- Review ownership: Establish who is responsible for reviewing and approving the final output.
- Current guidance verification: Confirm that model capabilities, tool instructions, and workflow guidance are up to date immediately before publication or customer recommendation.

Key takeaway: Deep Research is valuable when a task requires evidence-based synthesis and human review. A reliable workflow combines clear instructions, appropriate tools, source validation, explicit review responsibility, and verification of current guidance before the results are shared.

## Summary: Key Definitions

- Standard API pattern: A common approach, such as model generation, structured outputs, retrieval, tool use, or agentic workflows, that does not require specialized optimization.
- Specialized API pattern: A targeted approach used when standard patterns are insufficient, including Deep Research, image workflows, distillation, and optimization.
- Deep Research workflow: A Responses API-based workflow for multi-step research, source gathering, evidence comparison, synthesis, traceability, and human review.
- Image understanding (vision): Analyzes existing images to extract information, interpret visuals, or identify issues.
- Image generation or editing: Creates new images or modifies existing ones.
- Combined visual workflow: Connects image understanding and image generation/editing as separate steps within one larger process.
- Validation burden: The additional evidence and checks needed before recommending a specialized approach, including quality, safety, rights, cost, and maintenance.
- Standard-pattern alternative: A simpler, lower-complexity solution to consider before adopting a specialized workflow.

Key takeaway: Start with the simplest suitable API pattern. Recommend a specialized workflow only when it provides clear value and its additional validation requirements can be met.

## Summary: Understanding the Responses-Based Deep Research Surface

Deep Research is implemented as a Responses API workflow in which an application submits a complete research task, uses approved data sources and tools, and receives an output with visible evidence or citations for human review.

### Key source and tool decisions

- Web search: Validate source authority, relevance, freshness, and citations.
- File search: Ensure internal documents are approved, current, complete, and permission-protected.
- Remote MCP servers: Check server trust, approval, data sharing, and tool-call safety.
- Code interpreter: Use for calculations and data analysis when needed; validate results and reproducibility.

The workflow must use at least one approved research source: web search, file search over approved vector stores, or source-access tools through an approved remote MCP server. Code interpreter is optional when supported and useful.

### Background execution and data handling

- Plan for potentially long-running tasks using background mode, polling or webhooks, completion notifications, timeouts, and cost and latency limits.
- Zero Data Retention (ZDR): The course notes that background requests may temporarily store response data on disk for approximately 10 minutes, even with `store=false`.
- If customer data-handling requirements prohibit this temporary storage, leave background mode off and verify current data-handling guidance.

### Key takeaway

Before implementing or recommending Deep Research, validate the current model and tool compatibility, approved data sources, evidence visibility, background execution behavior, and data-retention requirements. Historical examples should not be treated as current implementation guidance.

## Summary: Identify Deep Research Workflow Needs

Deep Research is most useful when a task requires multi-source research, evidence comparison, synthesis, and a reviewable output. Simple questions that can be answered from one approved source are often better handled by a retrieval-grounded response.

### Key fit signals

- Multi-source investigation: Gather information from multiple approved sources.
- Evidence comparison: Identify conflicting claims, gaps, and uncertainty.
- Current information: Research changing information using approved web sources.
- Internal knowledge: Synthesize approved policies, files, and knowledge bases.
- Private-system access: Use trusted, approved remote MCP servers where appropriate.
- Data analysis: Use code interpreter for calculations and structured-data analysis when needed.
- Long-running tasks: Plan background execution, polling or webhooks, timeouts, and notifications.
- Reviewable output: Provide traceable evidence, explain uncertainty, and assign human review responsibility.

### Examples of suitable workflows

- Weekly market and risk briefings
- Regulatory and policy-change summaries
- Competitive research
- Technical literature reviews
- Vendor risk assessments
- Multi-source customer account research

### How to evaluate fit

Define the workflow in one sentence:

> The user needs to synthesize [source types] using [approved tools] to produce [output] for [decision or action]. A standard pattern may be insufficient because [reason].

Key takeaway: Recommend Deep Research only when the task genuinely requires research-style synthesis and a simpler approach is insufficient. Validate source permissions, evidence quality, tool compatibility, execution requirements, and human review before implementation.

## Summary: Identify Risks in Deep Research Workflows

Deep Research can produce polished, authoritative-looking answers that conceal weak evidence, uncertainty, or errors. The main risk is that users may trust the synthesis before its sources and conclusions have been reviewed.

### Common risks

- Source quality and freshness: Sources may be outdated, incomplete, or unreliable.
- Unsupported or overconfident claims: Conclusions may exceed what the evidence supports.
- Source conflicts: Contradictory evidence may be overlooked or improperly resolved.
- Unapproved sources: The workflow may rely on sources not authorized by the customer or domain owner.
- Traceability gaps: Claims cannot be linked to supporting evidence.
- Review ownership gaps: No qualified person is accountable for approving important findings.
- Permission issues: Sensitive information may be accessed or exposed to unauthorized users.

### How to reduce these risks

1. Use approved, authoritative, and current sources.
2. Make citations and evidence visible for review.
3. Explicitly flag uncertainty, missing evidence, and conflicting claims.
4. Enforce source permissions and access boundaries.
5. Assign qualified reviewers before high-impact decisions or distribution.
6. Validate tool behavior and source access before deployment.

Example: If two sources disagree about a regulatory deadline, the workflow should flag the disagreement, show the relevant evidence, and escalate it to a qualified reviewer rather than confidently choosing one date.

Key takeaway: A safe Deep Research workflow makes evidence, uncertainty, source boundaries, permissions, and review responsibilities explicit. A polished answer is not necessarily a verified answer.

## Summary: Define Validation Needs

Validation ensures a Deep Research workflow is reliable, traceable, and safe for customer use. A well-written synthesis alone is not proof of accuracy.

### Three key validation questions

| Question                                 | What to verify                                                                                   |
| ---------------------------------------- | ------------------------------------------------------------------------------------------------ |
| Are sources trustworthy and allowed?     | Sources are approved, current, relevant, and accessible to the user.                             |
| Is the synthesis accurate and traceable? | Important claims have supporting evidence, and conflicts or gaps are visible.                    |
| Is the review process safe?              | Reviewers are assigned, escalation rules are defined, and incomplete evidence is handled safely. |

### What to include in a validation plan

- Source readiness: Confirm approved sources, freshness, relevance, and access permissions.
- Evidence expectations: Define which claims require citations or reviewer-visible evidence.
- Output structure: Specify a consistent format for reviewing research findings.
- Uncertainty handling: Establish how to handle missing, weak, outdated, or conflicting evidence.
- Review ownership: Assign responsibility for approving, correcting, or escalating results.
- Capability validation: Verify implementation choices against current official documentation and approved product guidance.

### Define safe failure behavior

The workflow should be able to state:

- “The available sources are insufficient to support this conclusion.”
- “The sources conflict on this point. Human review is required.”
- “This claim needs evidence before it can be included.”
- “This output is a draft for analyst review, not a final recommendation.”

Key takeaway: A strong validation plan proves that the workflow uses approved sources, produces evidence-backed findings, exposes uncertainty, and routes high-impact decisions to qualified reviewers. Knowing when not to answer is an essential safety feature.

## Summary: Deep Research Deployment Example

The uploaded file presents a pseudocode-only planning sketch for a Responses API-based Deep Research workflow. It demonstrates how to prepare research tasks, validate sources and tools, manage execution, check evidence, and require human review.&#x20;

### Key controls

1. Prepare the research task: Check for missing requirements and ask clarifying questions before proceeding.
2. Approve sources and tools: Use authorized web search, approved internal vector stores, and code interpreter when needed. Enable remote MCP servers only after trust, data sharing, and approval requirements are verified.
3. Enforce permissions: Ensure users and workflows can access only authorized source content.
4. Manage long-running tasks: Define background execution, polling or webhooks, and tool-call budgets for cost and latency.
5. Require evidence: Return source references, tool traces, conflicts, open questions, and a structured research brief.
6. Assign human review: Verify evidence, permissions, and conflicting findings before distributing the output.&#x20;

   Pasted text.txt



### Workflow statuses

| Status                | Action                                                  |
| --------------------- | ------------------------------------------------------- |
| `needs_clarification` | Request missing research constraints.                   |
| `pause_or_escalate`   | Resolve source or tool approval risks.                  |
| `needs_review`        | Flag evidence-related risks for review.                 |
| `ready_for_review`    | Send the draft to a reviewer; it is not final approval. |



Pasted text.txt

Pasted text.txt



### Important limitations

- The sketch is not runnable SDK code.
- Its role and permission rules are illustrative, not authenticated access checks.
- Model and tool compatibility must be verified against current official documentation.
- Background requests in ZDR projects may still involve temporary disk storage for approximately 10 minutes, even with `store=false`. If this conflicts with customer requirements, disable background mode.&#x20;

  Pasted text.txt

  Pasted text.txt

Key takeaway: A production Deep Research workflow must enforce source permissions, use approved tools, manage long-running execution, expose evidence and risks, and fail safely when controls or evidence are insufficient. Research outputs remain drafts until reviewed by a qualified person.

## Summary: Real-World Example — Evaluating a Deep Research Workflow

A financial services customer wants to create a weekly risk briefing by synthesizing regulatory updates, market commentary, internal policy documents, and competitor disclosures.

### Why Deep Research may be appropriate

The workflow requires:

- Gathering information from multiple approved sources.
- Comparing external and internal information.
- Identifying uncertainty, conflicting evidence, and unsupported claims.
- Producing a structured, traceable briefing for human review.
- Supporting analysts’ decisions without automating final risk actions.

A standard retrieval-grounded response may be sufficient for questions based on one internal policy source. Deep Research may be better suited to complex, multi-source synthesis.

### Requirements before recommending it

1. Confirm approved source access and permission boundaries.
2. Validate source authority and freshness.
3. Require evidence references and traceability.
4. Define the briefing format and human review ownership.
5. Establish escalation rules for missing or conflicting evidence.
6. Verify current official documentation for model compatibility, supported tools, availability, limits, and data handling.

### Recommended approach

Proceed with a limited prototype using approved public sources, approved internal vector stores, structured evidence references, appropriate tool-call limits, and analyst review. Use background execution only when compatible with the customer's data-handling requirements.

Do not automate final risk decisions. Verify current official guidance immediately before implementation, publication, or customer recommendation.

Key takeaway: Deep Research is a plausible solution when multi-source investigation and traceable evidence are essential, but the recommendation must be conditional on validation, permissions, and human oversight.