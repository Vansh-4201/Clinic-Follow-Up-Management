from django.test import TestCase

# Create your tests here.

from django.contrib.auth.models import User
from django.urls import reverse

from .models import Clinic, UserProfile, FollowUp, PublicViewLog


#1

class ClinicModelTest(TestCase):
    def test_clinic_code_is_generated_and_unique(self):
        c1 = Clinic.objects.create(name="Clinic One")
        c2 = Clinic.objects.create(name="Clinic Two")

        self.assertIsNotNone(c1.clinic_code)
        self.assertIsNotNone(c2.clinic_code)
        self.assertNotEqual(c1.clinic_code, c2.clinic_code)


#2

class FollowUpModelTest(TestCase):
    def setUp(self):
        self.clinic = Clinic.objects.create(name="Clinic")
        self.user = User.objects.create_user(username="user", password="pass")
        UserProfile.objects.create(user=self.user, clinic=self.clinic)

    def test_public_token_is_generated_and_unique(self):
        f1 = FollowUp.objects.create(
            clinic=self.clinic,
            created_by=self.user,
            patient_name="A",
            phone="9999999999",
            due_date="2026-02-10",
        )
        f2 = FollowUp.objects.create(
            clinic=self.clinic,
            created_by=self.user,
            patient_name="B",
            phone="8888888888",
            due_date="2026-02-11",
        )

        self.assertNotEqual(f1.public_token, f2.public_token)

#3

class DashboardAuthTest(TestCase):
    def test_dashboard_requires_login(self):
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 302)  # redirect to login

#4

class AuthorizationTest(TestCase):
    def setUp(self):
        self.clinic_a = Clinic.objects.create(name="Clinic A")
        self.clinic_b = Clinic.objects.create(name="Clinic B")

        self.user_a = User.objects.create_user(username="a", password="pass")
        self.user_b = User.objects.create_user(username="b", password="pass")

        UserProfile.objects.create(user=self.user_a, clinic=self.clinic_a)
        UserProfile.objects.create(user=self.user_b, clinic=self.clinic_b)

        self.followup = FollowUp.objects.create(
            clinic=self.clinic_a,
            created_by=self.user_a,
            patient_name="Test",
            phone="9999999999",
            due_date="2026-02-10",
        )

    def test_user_cannot_edit_other_clinic_followup(self):
        self.client.login(username="b", password="pass")
        response = self.client.get(
            reverse("edit_followup", args=[self.followup.id])
        )
        self.assertEqual(response.status_code, 404)

#5

class PublicViewLogTest(TestCase):
    def setUp(self):
        self.clinic = Clinic.objects.create(name="Clinic")
        self.user = User.objects.create_user(username="user", password="pass")
        UserProfile.objects.create(user=self.user, clinic=self.clinic)

        self.followup = FollowUp.objects.create(
            clinic=self.clinic,
            created_by=self.user,
            patient_name="Public",
            phone="9999999999",
            due_date="2026-02-10",
        )

    def test_public_page_creates_view_log(self):
        url = reverse("public_followup", args=[self.followup.public_token])
        self.client.get(url)

        self.assertEqual(PublicViewLog.objects.count(), 1)
