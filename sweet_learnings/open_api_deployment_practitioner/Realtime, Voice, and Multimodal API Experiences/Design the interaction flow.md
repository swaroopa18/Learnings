### Summary: Designing the Interaction Flow

After selecting a modality (text, voice, image, or multimodal), map the complete user experience from start to finish. Define:

1. Start: How the interaction begins.
2. User input: What the user provides, such as speech, text, or images.
3. System response: How the system interprets the input and responds.
4. Clarification: How it handles unclear audio, missing context, or poor-quality images.
5. User control: How users can interrupt, correct, or confirm actions.
6. Fallback and escalation: What happens when the system cannot complete the task, including alternative methods or human handoff.
7. End: How the interaction completes safely and successfully.

Key takeaway: An interaction flow is a design and readiness plan that anticipates different scenarios, handles errors, preserves user control, and ensures a smooth, reliable experience from beginning to end.


## Interaction Flow: Multimodal Field Support

Goal: Help a field technician diagnose equipment damage using voice input and an uploaded image.

1\. Start

Technician opens the mobile assistant and requests troubleshooting help.

2\. Capture input

Technician describes the symptoms by voice and uploads a photo of the equipment panel.

3\. Validate context

System checks audio clarity, image quality, machine model, and available approved troubleshooting information.

4A. Clarify

If information is missing, ask a specific follow-up question.

4B. Respond

If context is sufficient, provide troubleshooting steps in voice and text.

5\. Confirm before action

System presents a draft service ticket and asks the technician to approve it before submission.

6A. Complete

Submit the confirmed ticket and show its status.

6B. Fallback / handoff

Switch to text, request another photo, retry audio, or escalate to human support.

### Key readiness requirements

- User control: Allow the technician to interrupt, correct details, retake photos, or cancel.
- Confirmation: Never submit a service ticket without explicit approval.
- Fallback: Handle unclear speech, poor image quality, missing information, and system timeouts.
- Escalation: Route unresolved or safety-critical issues to qualified human support.
- Completion: Confirm the actual outcome rather than assuming that a response or tool call succeeded.

Success criterion: The technician receives reliable, context-aware guidance and retains control over consequential actions, with a clear recovery path whenever the system cannot proceed.


## Define User Control

User control ensures that users can pause, stop, resume, correct, confirm, or switch channels at any point in a realtime or multimodal interaction.

For the field-support workflow, the application should provide these controls:

| Control          | Expected behavior                                                                                        |
| ---------------- | -------------------------------------------------------------------------------------------------------- |
| Pause            | Stop audio capture and spoken output, and suspend ongoing interaction where possible.                    |
| Resume           | Restart the session only when the user explicitly resumes.                                               |
| Stop / Cancel    | Stop recording and playback, cancel pending work where possible, and prevent new actions from starting.  |
| Correct          | Let the technician correct a misunderstood symptom or machine detail before the system continues.        |
| Replace input    | Allow the technician to retake or remove an unclear equipment photo.                                     |
| Switch channel   | Allow switching from voice to text when the environment is noisy or audio fails.                         |
| Confirm / Reject | Require explicit approval before submitting a service ticket or performing another consequential action. |

### Implementation rules

1. Check control commands before processing ordinary input.
2. Enforce paused and stopped states so the interaction cannot continue accidentally.
3. Connect controls to actual recording, playback, and pending-action cancellation mechanisms.
4. Provide visible status feedback so the user knows whether the system is listening, paused, or stopped.
5. Handle interruptions by discarding unplayed audio and keeping conversation history consistent with what the user actually heard.
6. Treat model-response cancellation and tool-action cancellation separately; canceling a response does not automatically undo or stop an external action.
7. When microphone capture is paused, provide a button or another channel for resuming, since the system cannot hear spoken commands.

Success criterion: Users remain in control throughout the interaction, understand the current state, and can correct mistakes or stop unintended actions before they cause consequences.


### Summary: Define Fallback Paths

Fallback paths define what the system should do when a voice or multimodal interaction cannot continue reliably or safely.

- Poor audio: Ask the user to repeat or switch to text.
- Transcription errors: Confirm what the system understood and allow corrections.
- Unclear images: Request a clearer photo or a text description.
- Missing context: Ask clarifying questions before proceeding.
- High latency or technical failures: Provide a status update, retry, or switch channels.
- Safety-critical requests: Stop automated guidance and escalate to qualified human support.
- Sensitive actions: Require appropriate confirmation or human review.
- Tool failures: Verify the outcome before reporting success or retrying an action.

Key takeaway: Every likely failure should have a defined response, a clear next step for the user, and a safe recovery or escalation route.

### Summary: Safe Travel-Support Interaction Flow

An airline disruption assistant should guide travelers through flight delays or cancellations using voice, uploaded itinerary images, and rebooking options.

- Start: Explain the assistant’s capabilities and that booking changes require confirmation.
- Capture input: Collect travel details through voice or an itinerary screenshot.
- Clarify: Resolve unclear images, misheard details, or missing information before proceeding.
- Respond: Present eligible rebooking options or direct the traveler to an agent.
- Confirm: Obtain explicit approval before changing a reservation.
- Fallback and escalation: Switch to text, retry, or route complex cases to a human agent.
- Stop: Halt new booking actions and verify the status of pending changes before reporting the outcome.

Key takeaway: A safe interaction flow preserves user control, verifies important details, prevents unauthorized booking changes, and defines clear fallback and escalation paths.