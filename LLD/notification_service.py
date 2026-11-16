from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

@dataclass
class SendResult:
    success: bool
    channel: str
    recipient: str
    error: Optional[str] = None
    
class Channel(ABC):
    @property
    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def get_context(self, user):
        pass

    @abstractmethod
    def send(self, user, message) -> SendResult:
        pass

class Email(Channel):
    name = 'email'
    def get_context(self, user):
        return {
            "name": user.name,
            "email": user.email
        }
    def send(self, user, message):
        recipient = user.email
        try:
            print(f"Sending Email to {recipient}: {message}")
            return SendResult(
                success=True,
                channel=self.name,
                recipient=recipient,
            )
        except Exception as e:
            return SendResult(
                success=False,
                channel=self.name,
                recipient=recipient,
                error=str(e)
            )
class SMS(Channel):
    name = "sms"

    def get_context(self, user):
        return {
            "name": user.name,
            "phone": user.phone_number
        }
    
    def send(self, user, message):
        recipient = user.phone_number

        try:
            # Replace this with actual SMS provider integration
            print(f"Sending SMS to {recipient}: {message}")

            return SendResult(
                success=True,
                channel=self.name,
                recipient=recipient
            )

        except Exception as e:
            return SendResult(
                success=False,
                channel=self.name,
                recipient=recipient,
                error=str(e)
            )

class Slack(Channel):
    name = 'slack'

    def get_context(self, user):
        return {
            "name": user.name,
            "phone": user.phone_number
        }

    def send(self, user, message):
        recipient = user.name

        try:
            print(f"Sending Slack to {recipient}: {message}")

            return SendResult(
                success=True,
                channel=self.name,
                recipient=recipient
            )

        except Exception as e:
            return SendResult(
                success=False,
                channel=self.name,
                recipient=recipient,
                error=str(e)
            )
#----------------#
class MessageTemplate:
    def __init__(self, templates):
        self.templates = templates

    def render(self, channel_name, **context):
        template = self.templates.get(channel_name)

        if template is None:
            raise ValueError(
                f"Template not found for channel: {channel_name}"
            )

        return template.format(**context)

# ---------------USER-----------#

class User:
    def __init__(self, name, email, phone_number, preferred_channels):
        self.name = name
        self.email = email
        self.phone_number = phone_number
        self.preferred_channels = preferred_channels


# -------------Notification Service--------------

class NotificationService:

    def notify(self, user, template):
        results = []

        for channel in user.preferred_channels:

            context = channel.get_context(user)

            message = template.render(
                channel.name,
                **context
            )

            result = channel.send(user, message)
            results.append(result)

        return results


user1 = User('Swaroo', 'anisetti@gmail.com', '+918247554837', [Email(), SMS()])
template = MessageTemplate({
    "email": "Hello {name}, welcome! Your registered email is {email}.",
    "sms": "Hi {name}, welcome!",
    "slack": "{name} just joined our platform!"
})
notification_service = NotificationService()
notification_service.notify(user1, template)