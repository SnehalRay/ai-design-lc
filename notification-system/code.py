'''
Problem: Notification System

User: id, name, notification list, notification type

Notification System

- people can subscribe to it => subscribe method
- send notification (list[user])
|
there will be a system where I have a normal queue
and whoever is in the send notification list, i create a notification object and put them in a queue
this will trigger a new function where everyone from the queue will be sent the queue with a probability of yes or no 50%
This try will happen 3 times if it fails. If it fails, there will be a self.dead_letter_queue which will store the failed messages

-check_failed_notifications: returns the dlq

'''

import random
from enum import Enum

class NotificationType(Enum):
    EMAIL = "email"
    PHONE = "phone"
    PUSH = "push"

class NotificationStatus(Enum):
    RECEIVED = "received"
    NOT_RECEIVED = "not_received"
    PENDING = "pending"


class Notification:
    def __init__(self, user: 'User'):
        self._user = user
        self._status = NotificationStatus.PENDING

    @property
    def user(self):
        return self._user

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value: NotificationStatus):
        self._status = value



class User:
    _id_counter = 0

    def __init__(self, name: str, notification_type: NotificationType):
        User._id_counter += 1
        self._id = User._id_counter
        self._name = name
        self._notification_type = notification_type
        self._notifications = []

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def notification_type(self):
        return self._notification_type

    @property
    def notifications(self):
        return self._notifications

    def add_notification(self, notification: Notification):
        self._notifications.append(notification)


class NotificationSystem:
    def __init__(self):
        self._subscribers: set[int] = set()
        self._dead_letter_queue: list[Notification] = []

    def subscribe(self, user: User):
        self._subscribers.add(user.id)

    def send_notifications(self, users: list[User]):
        queue = []
        for user in users:
            if user.id not in self._subscribers:
                continue
            notification = Notification(user)
            user.add_notification(notification)
            queue.append(notification)
        self._process_queue(queue)

    def check_failed_notifications(self) -> list[Notification]:
        return self._dead_letter_queue

    def _process_queue(self, queue: list[Notification]):
        for notification in queue:
            sent = False
            for _ in range(3):
                if random.random() < 0.5:
                    notification.status = NotificationStatus.RECEIVED
                    sent = True
                    break
            if not sent:
                notification.status = NotificationStatus.NOT_RECEIVED
                self._dead_letter_queue.append(notification)


def main():
    alice = User("Alice", NotificationType.EMAIL)
    bob = User("Bob", NotificationType.PUSH)
    charlie = User("Charlie", NotificationType.PHONE)
    diana = User("Diana", NotificationType.EMAIL)  # will not subscribe

    system = NotificationSystem()
    system.subscribe(alice)
    system.subscribe(bob)
    system.subscribe(charlie)

    all_users = [alice, bob, charlie, diana]

    print("=== Notification Simulation ===\n")
    print(f"Subscribers: Alice, Bob, Charlie")
    print(f"Sending to: Alice, Bob, Charlie, Diana (unsubscribed)\n")
    print("Diana skipped — not subscribed\n")

    system.send_notifications(all_users)

    print("Results:")
    for user in [alice, bob, charlie]:
        if user.notifications:
            status = user.notifications[-1].status.value
            print(f"  {user.name} ({user.notification_type.value.upper()}) -> {status.upper()}")

    failed = system.check_failed_notifications()
    print(f"\nDead Letter Queue ({len(failed)}):")
    for n in failed:
        print(f"  {n.user.name} — {n.status.value.upper()}")


if __name__ == "__main__":
    main()



