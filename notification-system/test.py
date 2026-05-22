import unittest
from unittest.mock import patch
from code import (
    User, Notification, NotificationSystem,
    NotificationType, NotificationStatus
)


class TestUser(unittest.TestCase):
    def test_unique_ids(self):
        u1 = User("Alice", NotificationType.EMAIL)
        u2 = User("Bob", NotificationType.PUSH)
        self.assertNotEqual(u1.id, u2.id)

    def test_notifications_start_empty(self):
        u = User("Alice", NotificationType.EMAIL)
        self.assertEqual(u.notifications, [])

    def test_add_notification(self):
        u = User("Alice", NotificationType.EMAIL)
        n = Notification(u)
        u.add_notification(n)
        self.assertEqual(len(u.notifications), 1)
        self.assertIs(u.notifications[0], n)


class TestNotification(unittest.TestCase):
    def test_default_status_is_pending(self):
        u = User("Alice", NotificationType.EMAIL)
        n = Notification(u)
        self.assertEqual(n.status, NotificationStatus.PENDING)

    def test_status_setter(self):
        u = User("Alice", NotificationType.EMAIL)
        n = Notification(u)
        n.status = NotificationStatus.RECEIVED
        self.assertEqual(n.status, NotificationStatus.RECEIVED)

    def test_user_reference(self):
        u = User("Alice", NotificationType.EMAIL)
        n = Notification(u)
        self.assertIs(n.user, u)


class TestNotificationSystemSubscribe(unittest.TestCase):
    def test_subscribe_adds_user(self):
        u = User("Alice", NotificationType.EMAIL)
        sys = NotificationSystem()
        sys.subscribe(u)
        self.assertIn(u.id, sys._subscribers)

    def test_subscribe_same_user_twice(self):
        u = User("Alice", NotificationType.EMAIL)
        sys = NotificationSystem()
        sys.subscribe(u)
        sys.subscribe(u)
        self.assertEqual(len(sys._subscribers), 1)


class TestNotificationSystemSendNotifications(unittest.TestCase):
    def test_unsubscribed_user_is_skipped(self):
        u = User("Alice", NotificationType.EMAIL)
        sys = NotificationSystem()
        with patch("code.random.random", return_value=0.1):
            sys.send_notifications([u])
        self.assertEqual(len(u.notifications), 0)

    def test_subscribed_user_gets_notification(self):
        u = User("Alice", NotificationType.EMAIL)
        sys = NotificationSystem()
        sys.subscribe(u)
        with patch("code.random.random", return_value=0.1):
            sys.send_notifications([u])
        self.assertEqual(len(u.notifications), 1)

    def test_notification_status_received_on_success(self):
        u = User("Alice", NotificationType.EMAIL)
        sys = NotificationSystem()
        sys.subscribe(u)
        with patch("code.random.random", return_value=0.1):  # < 0.5 => success
            sys.send_notifications([u])
        self.assertEqual(u.notifications[0].status, NotificationStatus.RECEIVED)

    def test_notification_status_not_received_on_all_failures(self):
        u = User("Alice", NotificationType.EMAIL)
        sys = NotificationSystem()
        sys.subscribe(u)
        with patch("code.random.random", return_value=0.9):  # >= 0.5 => always fail
            sys.send_notifications([u])
        self.assertEqual(u.notifications[0].status, NotificationStatus.NOT_RECEIVED)

    def test_mix_of_subscribed_and_unsubscribed(self):
        u1 = User("Alice", NotificationType.EMAIL)
        u2 = User("Bob", NotificationType.PUSH)
        sys = NotificationSystem()
        sys.subscribe(u1)
        with patch("code.random.random", return_value=0.1):
            sys.send_notifications([u1, u2])
        self.assertEqual(len(u1.notifications), 1)
        self.assertEqual(len(u2.notifications), 0)


class TestNotificationSystemDLQ(unittest.TestCase):
    def test_failed_notification_goes_to_dlq(self):
        u = User("Alice", NotificationType.EMAIL)
        sys = NotificationSystem()
        sys.subscribe(u)
        with patch("code.random.random", return_value=0.9):
            sys.send_notifications([u])
        failed = sys.check_failed_notifications()
        self.assertEqual(len(failed), 1)
        self.assertIs(failed[0].user, u)

    def test_successful_notification_not_in_dlq(self):
        u = User("Alice", NotificationType.EMAIL)
        sys = NotificationSystem()
        sys.subscribe(u)
        with patch("code.random.random", return_value=0.1):
            sys.send_notifications([u])
        self.assertEqual(len(sys.check_failed_notifications()), 0)

    def test_dlq_accumulates_across_calls(self):
        u1 = User("Alice", NotificationType.EMAIL)
        u2 = User("Bob", NotificationType.PUSH)
        sys = NotificationSystem()
        sys.subscribe(u1)
        sys.subscribe(u2)
        with patch("code.random.random", return_value=0.9):
            sys.send_notifications([u1])
            sys.send_notifications([u2])
        self.assertEqual(len(sys.check_failed_notifications()), 2)


if __name__ == "__main__":
    unittest.main()
