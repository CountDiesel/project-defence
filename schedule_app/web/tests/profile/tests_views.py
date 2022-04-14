import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from schedule_app.web.models import AppUser, Profile, Doctor

UserModel = get_user_model()


class ShowProfileViewTests(TestCase):

    def test_get__without_credentials__expect_404(self):
        response = self.client.get(reverse('show profile'), follow=True)
        self.assertEqual(response.status_code, 404)

    def test_get__expect_correct_template(self):
        self.my_admin = AppUser(email='slavchev.george@gmail.com', is_staff=True)
        self.my_admin.set_password('DoDo1976')
        self.my_admin.save()
        Profile.objects.create(first_name='George', last_name="Slavchev", user_id=self.my_admin.pk)
        self.client.login(email='slavchev.george@gmail.com', password='DoDo1976')
        response = self.client.get(reverse('show profile'), follow=True)
        self.assertTemplateUsed(response, 'profile.html')


class CreateProfileViewTests(TestCase):
    def setUp(self) -> None:
        date = datetime.datetime.now()

        Doctor.objects.create(first_name='Bojidar', last_name='Slavchev', specialty='Test', days='1',
                              manipulation_duration=30, manipulation_per_day=10, first_day_slot=date,
                              picture='doctors/Bojidar-Slavchev_t.png')

    def test_get__expect_correct_template(self):
        user_data = {
            'email': 'test@test.com',
            'password': 'passphrase',
        }
        AppUser.object.create_user(**user_data)
        self.client.login(**user_data)
        response = self.client.get(reverse('create profile'))
        self.assertTemplateUsed(response, 'profile_create.html')

    def test_put__create_profile__when_all_valid__expect_to_create(self):
        user_data = {
            'email': 'test@test.com',
            'password': 'passphrase',
        }
        user = AppUser.object.create_user(**user_data)
        self.client.login(**user_data)
        profile_data = {
            'first_name': 'George',
            'last_name': 'Slavchev',
            'telephone_number': '+359888823142',
            'user': user
        }

        self.client.post(reverse('create profile'), data=profile_data)

        profile = Profile.objects.get()
        self.assertIsNotNone(profile)
        self.assertEqual(profile_data['first_name'], profile.first_name)
        self.assertEqual(profile_data['last_name'], profile.last_name)
        self.assertEqual(profile_data['telephone_number'], profile.telephone_number)
        self.assertEqual(profile_data['user'], profile.user)

    def test_put__create_profile__when_all_valid__expect_to_redirect_to_index(self):
        user_data = {
            'email': 'test@test.com',
            'password': 'passphrase',
        }
        user = AppUser.object.create_user(**user_data)
        self.client.login(**user_data)
        profile_data = {
            'first_name': 'George',
            'last_name': 'Slavchev',
            'telephone_number': '+359888823142',
            'user': user
        }
        response = self.client.post(reverse('create profile'), data=profile_data, follow=True)

        self.assertRedirects(response, reverse('view doctors'))
