'''
Notification System

user -> subscribe to diff event types

user -> diff type of notifications

event can be sent to different users only once


users:
    preferred way of communication -> []
    notifications: []

Abstract class
notification class:
    self.message = ""

    abstract method: send notification

2 types:
send through phone
send through email


Event class:
    attribute: type of event it is hosting
    adding event
    send notifications

'''

from enum import Enum
from abc import ABC, abstractmethod

class NotificationPreference(Enum):
    PHONE = "phone"
    EMAIL = "email"


class Notification(ABC):
    def __init__(self, message: str):
        self.message = message

    @abstractmethod
    def send_notification(self):
        pass


class PhoneNotification(Notification):
    def __init__(self, message: str, phone_number: str):
        super().__init__(message)
        self.phone_number = phone_number

    def send_notification(self) -> bool:
        print(f"notification: {self.message} sent to phone number {self.phone_number}")
        return True


class EmailNotification(Notification):
    def __init__(self, message: str, email: str):
        super().__init__(message)
        self.email = email

    def send_notification(self) -> bool:
        print(f"notification: {self.message} sent to email {self.email}")
        return True


class User:
    def __init__(self):
        self.__communication_preference = set()
        self.__notifications = []
        self.__phone_number = ""
        self.__email = ""

    @property
    def communication_preference(self):
        return self.__communication_preference

    @communication_preference.setter
    def communication_preference(self, preferences: set):
        self.__communication_preference = preferences

    @property
    def notifications(self):
        return self.__notifications

    @notifications.setter
    def notifications(self, notifications: list):
        self.__notifications = notifications

    @property
    def phone_number(self):
        return self.__phone_number

    @phone_number.setter
    def phone_number(self, phone_number: str):
        self.__phone_number = phone_number

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, email: str):
        self.__email = email



class Event:
    def __init__(self, name: str):
        self.name = name
        self.__subscribers = {} #
        self.dlq = [] 


    def subscribe_to_event(self, user: User):
        self.__subscribers[id(user)] = user

    def send_notifications(self, message: str) -> bool:
        for user in self.__subscribers.values():
            notification_appended = False
            for pref in user.communication_preference:
                if pref == NotificationPreference.PHONE:
                    notification = PhoneNotification(message, user.phone_number)
                elif pref == NotificationPreference.EMAIL:
                    notification = EmailNotification(message, user.email)

                success = False
                for _ in range(3):
                    if notification.send_notification():
                        success = True
                        break

                if success:
                    if not notification_appended:
                        user.notifications.append(notification)
                        notification_appended = True
                else:
                    self.dlq.append((user, message))


if __name__ == "__main__":
    # User 1: prefers both phone and email
    alice = User()
    alice.phone_number = "555-0101"
    alice.email = "alice@example.com"
    alice.communication_preference = {NotificationPreference.PHONE, NotificationPreference.EMAIL}

    # User 2: prefers email only
    bob = User()
    bob.email = "bob@example.com"
    bob.communication_preference = {NotificationPreference.EMAIL}

    # User 3: prefers phone only
    carol = User()
    carol.phone_number = "555-0303"
    carol.communication_preference = {NotificationPreference.PHONE}

    event = Event("Summer Sale")

    event.subscribe_to_event(alice)
    event.subscribe_to_event(bob)
    event.subscribe_to_event(carol)

    print(f"--- Sending notifications for: {event.name} ---")
    event.send_notifications("50% off all items this weekend!")

    print(f"\n--- Results ---")
    print(f"Alice notifications received: {len(alice.notifications)}")
    print(f"Bob notifications received:   {len(bob.notifications)}")
    print(f"Carol notifications received: {len(carol.notifications)}")
    print(f"DLQ size: {len(event.dlq)}")