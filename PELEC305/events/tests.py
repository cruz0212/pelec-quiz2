from django.contrib.auth.hashers import check_password
from django.test import TestCase
from django.urls import reverse

from .forms import EventRegistrationForm
from .models import EventRegistration


class EventRegistrationFormTests(TestCase):
    def valid_data(self, **overrides):
        data = {
            'full_name': 'Juan Dela Cruz',
            'email': 'juan@gmail.com',
            'age': 18,
            'password': 'securepass',
        }
        data.update(overrides)
        return data

    def test_valid_registration_is_saved_with_hashed_password(self):
        form = EventRegistrationForm(data=self.valid_data())

        self.assertTrue(form.is_valid())
        registration = form.save()

        self.assertEqual(EventRegistration.objects.count(), 1)
        self.assertNotEqual(registration.password, 'securepass')
        self.assertTrue(check_password('securepass', registration.password))

    def test_full_name_must_be_at_least_five_characters(self):
        form = EventRegistrationForm(data=self.valid_data(full_name='Ana'))

        self.assertFalse(form.is_valid())
        self.assertIn('full_name', form.errors)

    def test_email_must_be_gmail_address(self):
        form = EventRegistrationForm(data=self.valid_data(email='juan@example.com'))

        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_age_must_be_at_least_eighteen(self):
        form = EventRegistrationForm(data=self.valid_data(age=17))

        self.assertFalse(form.is_valid())
        self.assertIn('age', form.errors)

    def test_password_must_be_at_least_eight_characters(self):
        form = EventRegistrationForm(data=self.valid_data(password='short'))

        self.assertFalse(form.is_valid())
        self.assertIn('password', form.errors)

    def test_registration_view_displays_form(self):
        response = self.client.get(reverse('event_register'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<form method="post"')
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_registration_view_saves_valid_data(self):
        response = self.client.post(reverse('event_register'), data=self.valid_data())

        self.assertRedirects(response, reverse('event_register'))
        self.assertEqual(EventRegistration.objects.count(), 1)

    def test_registration_view_shows_validation_errors(self):
        response = self.client.post(
            reverse('event_register'),
            data=self.valid_data(full_name='Ana', email='ana@example.com', age=16),
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(EventRegistration.objects.count(), 0)
        self.assertContains(response, 'Full name must be at least 5 characters.')
        self.assertContains(response, 'Email must end with @gmail.com.')
        self.assertContains(response, 'Ensure this value is greater than or equal to 18.')
