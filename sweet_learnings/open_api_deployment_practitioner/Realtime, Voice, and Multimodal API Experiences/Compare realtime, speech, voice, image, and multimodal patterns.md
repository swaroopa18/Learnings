## Summary: Comparing Realtime, Speech, Voice, Image, and Multimodal Patterns

Different modality patterns solve different user needs. Choose the pattern based on the workflow, user experience, reliability, and risk—not simply because it is more advanced.

- Realtime interaction: Enables low-latency, natural conversations with immediate responses, often using audio and video.
- Speech-to-text: Converts spoken language into text for transcription, search, note-taking, or command processing.
- Text-to-speech: Converts written text into spoken audio for accessibility, narration, and voice assistants.
- Voice-to-action: Interprets spoken commands and triggers tasks, such as setting reminders or controlling applications.
- Systems-to-voice: Turns structured system information or events into spoken updates, alerts, or instructions.
- Voice-to-voice: Accepts spoken input and responds with generated speech, supporting conversational assistants.
- Image input: Analyzes images to identify objects, read documents, answer visual questions, or interpret scenes.
- Image output: Generates or edits images for design, illustration, product concepts, and visual communication.
- Multimodal patterns: Combine text, audio, images, or video to handle workflows that require multiple types of information.

### Key decision factors

When choosing a pattern, identify:

1. Primary modality: The main way the user provides information or receives results.
2. Supporting modality: Additional formats that improve the experience.
3. Fallback option: An alternative, such as text input when voice is unavailable.
4. Risk tradeoffs: Potential errors, latency, privacy concerns, accessibility barriers, and unintended actions.

Key takeaway: Match the modality to the task. Use speech-to-text when capturing words matters, voice-to-action when completing tasks matters, image input when visual understanding matters, and multimodal interaction when combining several information types is essential.

## Summary: Modalities Overview

This module introduces the main interaction patterns used in realtime, speech, voice, image, and multimodal API experiences.

- Realtime interaction: Supports fast, back-and-forth communication where timing and interruptions matter.
- Speech-to-text (STT): Converts spoken words into text for easier input, transcription, and processing.
- Text-to-speech (TTS): Converts text into audio for accessibility, hands-free use, and listening.
- Voice patterns: Use speech for actions, system announcements, or natural spoken conversations.
- Image input: Lets users provide images for visual analysis, interpretation, and reasoning.
- Image output: Generates or transforms images for design, creative work, and visual communication.
- Multimodal patterns: Combine multiple modalities, such as speech, text, images, and audio, when one modality alone is insufficient.

### Key design considerations

Consider latency, accuracy, accessibility, privacy, consent, user control, fallback options, and human review, depending on the pattern.

Key takeaway: Choose the simplest modality that meets the user's workflow needs safely. Patterns can overlap, so combine them deliberately rather than adding complexity without a clear benefit.

## Summary: Realtime Interaction

Realtime interaction is best for experiences that require fast, natural back-and-forth communication, where timing, clarification, and immediate responses are essential.

### Key design considerations

- Turn-taking: Handle pauses, interruptions, and overlapping speech naturally.
- Latency: Respond quickly enough to maintain conversational flow.
- Tool-use delays: Keep users informed while the system retrieves information or performs an action.
- Corrections: Allow users to correct misheard words, numbers, names, or instructions.
- Fallback: Switch to text or another reliable channel if realtime interaction fails.

### Examples

- Customer support: Acknowledge the user while checking account information.
- Field assistance: Pause, repeat instructions, or adapt as a technician works.
- Voice assistants: Answer follow-up questions and handle interruptions naturally.

Key takeaway: Realtime is more than fast responses; it requires managing the entire interaction flow. Use it when low latency matters. For tasks where users can wait and need structured, reviewable answers, text-based or asynchronous workflows may be simpler and more reliable.

## Summary: Speech-to-Text (STT)

Speech-to-text (STT) converts spoken input into written text. It is most useful when the primary goal is to capture, document, or process speech rather than maintain a spoken conversation.

### Common use cases

- Transcribing customer calls.
- Capturing spoken notes from mobile workers.
- Creating meeting notes and live captions.
- Allowing hands-free dictation.

### Key considerations before choosing STT

1. Audio quality: Is the speech clear, with minimal background noise?
2. Language and accents: Can the system recognize the required languages, accents, and specialized terminology?
3. Error correction: Can users review, edit, and confirm the transcript?
4. Privacy and consent: Are recording permissions, data retention, and privacy requirements addressed?
5. Transcript handling: Should the text be stored, summarized, reviewed, or deleted?
6. Low confidence: What happens when speech is unclear or the transcript is incomplete?

Key takeaway: A transcript is reviewable, but it is not automatically accurate. For important information such as names, dates, quantities, customer records, or commitments, provide a way to verify and correct errors before acting on the transcript.

## Summary: Text-to-Speech (TTS)

Text-to-speech (TTS) converts written text into spoken audio. It is useful when users need spoken guidance, accessibility support, hands-free information, or voice responses.

### Common use cases

- Technicians listening to troubleshooting instructions while working.
- Travelers receiving spoken updates while moving.
- Users with visual accessibility needs listening to content.
- Customers hearing brief status updates during support interactions.

### Key considerations

1. Environment: Is listening practical and safe for the user?
2. Playback controls: Can users pause, replay, slow down, or switch to text?
3. Response length: Is the spoken content concise and easy to follow?
4. Text alternative: Is a readable transcript available?
5. Voice and tone: Does the delivery suit the task and audience?
6. Content review: Does sensitive or important information need verification before being spoken?
7. Transparency: Are users clearly informed when the voice is AI-generated?

Key takeaway: TTS is a way to deliver information through audio, not necessarily a complete voice agent. Keep spoken responses clear and concise, and provide text alternatives for critical details such as prices, dates, policies, and confirmation numbers.

## Summary: Voice-to-Action, Systems-to-Voice, and Voice-to-Voice

Voice patterns are useful when spoken interaction is central to the user's workflow. Before choosing a pattern, first choose the voice architecture that determines how audio is processed.

### 1. Voice architectures

- Speech-to-speech Realtime: Processes live audio input and output directly. Best for natural, low-latency conversations, interruptions, turn-taking, and realtime tool use.
- Chained voice pipeline: Sequences speech-to-text, a text-based agent, and text-to-speech. Best when transcripts, intermediate text, approvals, and deterministic checks are important.
- GPT-Live with a backend agent: Allows conversation to continue while a separate workflow performs lookups or tasks.

Two delegation options are available:

- Client delegation: The application controls backend context, routing, permissions, and review of results.
- Responses delegation: GPT-Live passes conversation context to a supported hosted model workflow through the Responses API.

Your application remains responsible for custom functions, permissions, task state, and business records. Interrupting speech does not automatically cancel backend work, so cancellation and outdated results must be handled explicitly.

For Realtime connections, generally use WebRTC for browser/mobile audio, WebSocket for server-managed audio streams, and SIP for telephony, subject to current model support.

### 2. Three voice interaction patterns

| Pattern          | Purpose                                                  | Example                                                            |
| ---------------- | -------------------------------------------------------- | ------------------------------------------------------------------ |
| Voice-to-action  | Users speak commands to complete or prepare tasks.       | Scheduling an appointment or checking account status.              |
| Systems-to-voice | Systems turn information into spoken guidance or alerts. | Travel updates, equipment warnings, or accessibility instructions. |
| Voice-to-voice   | Users speak naturally and receive spoken responses.      | Live translation or a conversational voice assistant.              |

### 3. Essential safeguards

- Disclose clearly that the voice is AI-generated.
- Tell users when information is being checked or a tool is being used.
- Require confirmation before sensitive or irreversible actions.
- Allow users to pause, stop, correct, or switch to text.
- Escalate unsafe, sensitive, or unresolved conversations to human support.
- Verify task completion separately from whether the user heard a confirmation.

Key takeaway: Choose the architecture based on audio-processing needs, then choose the interaction pattern based on the user's goal. Prioritize user control, reliable task execution, and safety over conversational sophistication. Verify current model capabilities, connection methods, and API support before implementation.

## Summary: Image Input

Image input allows a system to interpret visual evidence and use it to answer questions or support a workflow.

### Common use cases

- Inspecting damaged products, equipment, or rooms.
- Analyzing screenshots of software errors.
- Reading documents, forms, labels, serial numbers, and receipts.
- Providing visual context for fieldwork or insurance claims.

### Key considerations

1. Image quality: Is the image clear, well-lit, and complete?
2. Unclear images: Can the system ask the user for a clearer image or additional context?
3. Privacy: Does the image contain sensitive or confidential information?
4. Permission: Is the user authorized to upload and share the image?
5. Clarification: Should the system ask follow-up questions before interpreting uncertain details?
6. Human review: Which findings must be verified before action is taken?

Image input can improve understanding, but the model may misinterpret details or miss context that is not visible. Treat images as evidence, not definitive proof, especially for high-risk decisions.

GPT-Live integration: When combining images with GPT-Live, send images to a vision-capable backend, then return the findings as text for GPT-Live to use in the conversation. The Live audio frontend does not accept images directly.

Key takeaway: Use image input when visual information is essential, and provide ways to clarify uncertain results and verify important decisions.

## Summary: Image Output

Image output creates or transforms visual content. It is useful when a workflow benefits from visual communication, creative exploration, or visual guidance.

### Common use cases

- Generating design drafts from voice or text instructions.
- Creating visual guides that show users where to click.
- Producing illustrations for training or support.
- Refining images through iterative user feedback.

### Key considerations

1. Necessity: Would text, a diagram, or a checklist be sufficient?
2. Review: Does the image require brand, legal, accessibility, or human approval?
3. Rights: Are copyright and approved-use requirements clear?
4. Accessibility: Is a non-visual alternative available?
5. Safety and accuracy: Could the image mislead users or be mistaken for an official document?
6. Intended use: Is it for internal brainstorming, customer-facing communication, training, or operational guidance?

Key takeaway: Image output should solve a real communication or design need, not simply enhance a workflow. Start with the simplest effective format, and apply appropriate review before using generated visuals in consequential or customer-facing contexts.

## Summary: Multimodal Patterns

Multimodal patterns combine two or more input or output types—such as voice, text, images, and tool use—to make a workflow more effective.

### Common patterns

| Pattern                                        | Example                                                                        | Main benefit                                          |
| ---------------------------------------------- | ------------------------------------------------------------------------------ | ----------------------------------------------------- |
| Voice input + text output                      | Dictate a sales update and receive a CRM-ready summary                         | Fast capture, easy review                             |
| Voice + image input                            | Technician describes photographed equipment damage                             | Combines visual evidence with context                 |
| Image input + spoken guidance                  | Warehouse worker receives spoken instructions after showing a damaged package  | Hands-free support                                    |
| Text input + image output                      | Generate marketing mockups from a campaign idea                                | Explore visual concepts quickly                       |
| Realtime voice + tools + written confirmation  | Discuss travel changes, check options, then confirm in writing                 | Conversation plus verified actions and an audit trail |
| Image + speech transcript + structured summary | Compile insurance damage photos and dictated observations into a claim summary | Supports consistent case handling                     |

### Six things to define before deployment

1. Primary modality: Which modality drives the main workflow?
2. Supporting modality: Which additional modality provides context, evidence, accessibility, or speed?
3. Switch point: When should the user move between modalities?
4. Failure path: What happens if one modality fails?
5. Confirmation point: What must be confirmed before an action is taken?
6. Review path: What information should a human or downstream system be able to inspect?

### Example: Retail returns

A store associate photographs a damaged product, verbally records observations, and receives a written refund or exchange summary to review before the decision is finalized.

Each modality has a distinct role:

- Image: Captures visible damage.
- Voice: Adds context and observations.
- Written summary: Records the proposed decision for review.

Key takeaway: Use multiple modalities only when each adds clear value. Define how they work together, what happens when one fails, and where confirmation and human review are required.