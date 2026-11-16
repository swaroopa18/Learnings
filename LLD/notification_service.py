from abc import ABC, abstractmethod
from dataclasses import dataclass
import time
import random
import random
from typing import Optional

@dataclass
class SendResult:
    success: bool
    channel: str
    recipient: str
    error: Optional[str] = None
    
class Channel(ABC):
    def __init__(self, max_retries=3, sleep=time.sleep):
        self._max_retries = max_retries
        self._sleep = sleep  
    BASE_DELAY = 1
    MAX_DELAY = 10
    @property
    @abstractmethod
    def name(self):
        pass

    def send(self, user, message) -> SendResult:
        recipient = self.get_recipient(user)

        for attempt in range(1, self._max_retries + 1):
            try:
                self._deliver(recipient, message)

                return SendResult(
                    True,
                    self.name,
                    recipient
                )

            except Exception as e:
                if attempt == self._max_retries:
                    return SendResult(
                        False,
                        self.name,
                        recipient,
                        str(e)
                    )
                max_delay = min(
                    self.MAX_DELAY,
                    self.BASE_DELAY * (2 ** (attempt - 1))
                )
                delay = random.uniform(0, max_delay)
                print(
                    f"{self.name} failed. "
                    f"Retrying in {delay:.2f} seconds..."
                )

                self._sleep(delay)

        raise RuntimeError("Unexpected retry state")

    @abstractmethod
    def get_context(self, user):
        pass

    @abstractmethod
    def get_recipient(self, user) -> str:
        pass

    @abstractmethod
    def _deliver(self, recipient: str, message: str) -> None:
        pass

class Email(Channel):
    name = 'email'
    def get_recipient(self, user):
        return user.email
    def get_context(self, user):
        return {
            "name": user.name,
            "email": user.email
        }
    def _deliver(self, recipient, message):
        print(f"Sending Email to {recipient}: {message}")
class SMS(Channel):
    name = "sms"

    def get_recipient(self, user):
        return user.phone_number

    def get_context(self, user):
        return {
            "name": user.name,
            "phone": user.phone_number
        }
    
    def _deliver(self, recipient, message):
        print(f"Sending SMS to {recipient}: {message}")

class Slack(Channel):
    name = "slack"

    def get_recipient(self, user):
        return user.slack_id

    def get_context(self, user):
        return {
            "name": user.name
        }

    def _deliver(self, recipient, message):
        print(f"Sending Slack message to {recipient}: {message}")

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