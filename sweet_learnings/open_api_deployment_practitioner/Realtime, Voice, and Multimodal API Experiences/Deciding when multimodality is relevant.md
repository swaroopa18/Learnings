### Summary: Deciding When Multimodality Is Relevant

Multimodality includes using voice, images, speech, video, or real-time interaction alongside text to improve the user experience.

Before choosing a non-text modality, consider:

- User needs: What is the user trying to accomplish?
- Input and output: What can the user realistically provide, and what output do they need?
- Added value: What would multimodality improve that text alone cannot?
- Risks and limitations: Consider reliability, accessibility, privacy, consent, and fallback options.

Key takeaway: Use multimodality only when it provides meaningful value. If text is sufficient, keep the experience simple. If the benefits or risks are unclear, validate the idea before proceeding.

### Summary: Start with the Workflow Need

Before selecting a modality, clearly define what the API needs to achieve and understand the user's situation.

Ask these seven questions:

1. What is the user trying to do?
2. Where is the user?
3. What input can they provide?
4. What output do they need?
5. How quickly do they need it?
6. What environmental factors affect the interaction?
7. What would fail if the experience stayed text-only?

Key takeaway: Don't choose voice, images, or real-time interaction just because they are available. Choose a modality only when it solves a specific workflow problem.

Examples:

- Back-office analyst → Text for searchable, auditable reviews.
- Warehouse worker wearing gloves → Voice for hands-free input.
- Technician diagnosing equipment → Images to inspect faults.
- Customer needing immediate support → Voice for real-time spoken guidance.

### Summary: When Is a Non-Text Modality Justified?

A non-text modality is justified when it solves a real user problem that text alone cannot handle effectively.

Use non-text modalities when:

- Typing is difficult or hands-free interaction is needed.
- The task depends on spoken language or visual evidence.
- Real-time, low-latency interaction is essential.
- Multiple input or output formats are required.
- Accessibility needs make another modality more effective.

When text is better: Choose text when reviewability, auditability, reliability, privacy, or consent are major concerns, or when text alone meets the user's needs with less risk.

Possible approaches:

- Text-only for simple, searchable workflows.
- Text + images for visual inspection.
- Speech-to-text (STT) for spoken input.
- Text-to-speech (TTS) for spoken output.
- Realtime voice for workflows requiring immediate spoken interaction.

Key takeaway: Choose the simplest modality that meets the workflow need safely. Don't add complexity just to make an experience seem more advanced.


### Summary: Choosing the Right Modality for Travel Disruptions

A travel disruption workflow needs an experience that is fast, context-aware, safe, and actionable because travelers may be moving through an airport under time pressure.

Recommended solution: A mixed-modality experience

- System-to-voice: Deliver urgent spoken updates, such as gate changes or connection alerts.
- Voice-to-action: Let travelers request changes hands-free, such as finding a later hotel check-in.
- Text fallback: Display itinerary details, booking confirmations, policies, and options for easy review.
- Human handoff: Escalate complex, sensitive, or unresolved cases to a human agent.

Key risks to address:

- High latency that delays urgent responses.
- Unresolved voice consent or recording requirements.
- Booking actions executed without explicit confirmation.
- Situations where simpler text interaction would be sufficient.

Key takeaway: Choose modalities based on the traveler's context, urgency, and task—not because voice seems more natural. Launch realtime voice only when its benefits, safety controls, confirmation process, and fallback options are validated.