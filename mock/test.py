import unittest
from unittest.mock import patch
from code import (
    NotificationPreference,
    Notification,
    PhoneNotification,
    EmailNotification,
    User,
    Event,
)


class TestNotificationPreference(unittest.TestCase):
    def test_values(self):
        self.assertEqual(NotificationPreference.PHONE.value, "phone")
        self.assertEqual(NotificationPreference.EMAIL.value, "email")


class TestPhoneNotification(unittest.TestCase):
    def test_send_returns_true(self):
        n = PhoneNotification("hello", "555-0000")
        self.assertTrue(n.send_notification())

    def test_message_and_phone_stored(self):
        n = PhoneNotification("hello", "555-0000")
        self.assertEqual(n.message, "hello")
        self.assertEqual(n.phone_number, "555-0000")

    def test_send_prints_correct_output(self):
        n = PhoneNotification("sale", "555-1234")
        with patch("builtins.print") as mock_print:
            n.send_notification()
            mock_print.assert_called_once_with(
                "notification: sale sent to phone number 555-1234"
            )


class TestEmailNotification(unittest.TestCase):
    def test_send_returns_true(self):
        n = EmailNotification("hello", "a@b.com")
        self.assertTrue(n.send_notification())

    def test_message_and_email_stored(self):
        n = EmailNotification("hello", "a@b.com")
        self.assertEqual(n.message, "hello")
        self.assertEqual(n.email, "a@b.com")

    def test_send_prints_correct_output(self):
        n = EmailNotification("sale", "a@b.com")
        with patch("builtins.print") as mock_print:
            n.send_notification()
            mock_print.assert_called_once_with(
                "notification: sale sent to email a@b.com"
            )

    def test_notification_is_abstract(self):
        with self.assertRaises(TypeError):
            Notification("msg")


class TestUser(unittest.TestCase):
    def setUp(self):
        self.user = User()

    def test_default_preferences_empty(self):
        self.assertEqual(self.user.communication_preference, set())

    def test_default_notifications_empty(self):
        self.assertEqual(self.user.notifications, [])

    def test_set_communication_preference(self):
        self.user.communication_preference = {NotificationPreference.EMAIL}
        self.assertIn(NotificationPreference.EMAIL, self.user.communication_preference)

    def test_set_notifications(self):
        n = PhoneNotification("msg", "555-0000")
        self.user.notifications = [n]
        self.assertEqual(len(self.user.notifications), 1)

    def test_set_phone_number(self):
        self.user.phone_number = "555-9999"
        self.assertEqual(self.user.phone_number, "555-9999")

    def test_set_email(self):
        self.user.email = "test@test.com"
        self.assertEqual(self.user.email, "test@test.com")

    def test_private_attributes_not_directly_accessible(self):
        with self.assertRaises(AttributeError):
            _ = self.user.__phone_number
        with self.assertRaises(AttributeError):
            _ = self.user.__email


class TestEvent(unittest.TestCase):
    def _make_user(self, prefs, phone="", email=""):
        u = User()
        u.communication_preference = prefs
        u.phone_number = phone
        u.email = email
        return u

    def test_subscribe_adds_user(self):
        event = Event("test")
        user = self._make_user({NotificationPreference.EMAIL}, email="a@b.com")
        event.subscribe_to_event(user)
        # send_notifications should reach the user without error
        event.send_notifications("msg")
        self.assertEqual(len(user.notifications), 1)

    def test_notification_appended_only_once_for_multiple_preferences(self):
        event = Event("test")
        user = self._make_user(
            {NotificationPreference.PHONE, NotificationPreference.EMAIL},
            phone="555-0000",
            email="a@b.com",
        )
        event.subscribe_to_event(user)
        event.send_notifications("msg")
        self.assertEqual(len(user.notifications), 1)

    def test_multiple_subscribers_each_get_one_notification(self):
        event = Event("test")
        u1 = self._make_user({NotificationPreference.EMAIL}, email="u1@b.com")
        u2 = self._make_user({NotificationPreference.PHONE}, phone="555-0002")
        event.subscribe_to_event(u1)
        event.subscribe_to_event(u2)
        event.send_notifications("msg")
        self.assertEqual(len(u1.notifications), 1)
        self.assertEqual(len(u2.notifications), 1)

    def test_dlq_populated_on_send_failure(self):
        event = Event("test")
        user = self._make_user({NotificationPreference.PHONE}, phone="555-0000")
        event.subscribe_to_event(user)
        with patch.object(PhoneNotification, "send_notification", return_value=False):
            event.send_notifications("msg")
        self.assertEqual(len(event.dlq), 1)
        self.assertIs(event.dlq[0][0], user)
        self.assertEqual(event.dlq[0][1], "msg")

    def test_dlq_empty_on_success(self):
        event = Event("test")
        user = self._make_user({NotificationPreference.EMAIL}, email="a@b.com")
        event.subscribe_to_event(user)
        event.send_notifications("msg")
        self.assertEqual(len(event.dlq), 0)

    def test_retry_succeeds_on_second_attempt(self):
        event = Event("test")
        user = self._make_user({NotificationPreference.EMAIL}, email="a@b.com")
        event.subscribe_to_event(user)
        # Fail once, then succeed
        results = [False, True]
        with patch.object(EmailNotification, "send_notification", side_effect=results):
            event.send_notifications("msg")
        self.assertEqual(len(user.notifications), 1)
        self.assertEqual(len(event.dlq), 0)

    def test_no_subscribers_no_error(self):
        event = Event("empty")
        event.send_notifications("msg")
        self.assertEqual(len(event.dlq), 0)

    def test_send_notifications_same_event_twice(self):
        event = Event("test")
        user = self._make_user({NotificationPreference.EMAIL}, email="a@b.com")
        event.subscribe_to_event(user)
        event.send_notifications("first")
        event.send_notifications("second")
        # Each call appends once
        self.assertEqual(len(user.notifications), 2)


if __name__ == "__main__":
    unittest.main()
