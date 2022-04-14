import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from schedule_app.web.models import AppUser, Profile, Doctor, CalendarEvent

UserModel = get_user_model()


class DeleteEventViewTests(TestCase):
    # def setUp(self) -> None:
    #     self.my_admin = AppUser(email='slavchev.george@gmail.com', is_staff=False)
    #     self.my_admin.set_password('DoDo1976')
    #     self.my_admin.save()

    def test_get__without_credentials__expect_403(self):
        self.my_admin = AppUser(email='slavchev.george@gmail.com', is_staff=False)
        self.my_admin.set_password('DoDo1976')
        self.my_admin.save()
        Profile.objects.create(first_name='George', last_name="Slavchev", user_id=self.my_admin.pk)
        date = datetime.datetime.now()
        doc = Doctor.objects.create(first_name='Bojidar', last_name='Slavchev', specialty='Test', days='1',
                                    manipulation_duration=30, manipulation_per_day=10, first_day_slot=date)
        CalendarEvent.objects.create(doctor_id=doc, patient_id=self.my_admin, created_by=self.my_admin,
                                     date=date)
        user_data = {
            'email': 'test@test.com',
            'password': 'passphrase',
        }
        AppUser.object.create_user(**user_data)
        self.client.login(**user_data)

        response = self.client.get(reverse('delete event', args='1'), follow=True)
        self.assertEqual(response.status_code, 403)

    def test_get__without_credentials_but_staff__expect_correct_template(self):
        self.my_admin = AppUser(email='slavchev.george@gmail.com', is_staff=True)
        self.my_admin.set_password('DoDo1976')
        self.my_admin.save()
        Profile.objects.create(first_name='George', last_name="Slavchev", user_id=self.my_admin.pk)
        date = datetime.datetime.now()

        doc = Doctor.objects.create(first_name='Bojidar', last_name='Slavchev', specialty='Test', days='1',
                                    manipulation_duration=30, manipulation_per_day=10, first_day_slot=date,
                                    picture='doctors/Bojidar-Slavchev_t.png')
        user_data = {
            'email': 'test@test.com',
            'password': 'passphrase',
        }
        user = AppUser.object.create_user(**user_data)
        CalendarEvent.objects.create(doctor_id=doc, patient_id=user, created_by=user,
                                     date=date)
        self.client.login(**user_data)
        response = self.client.get(reverse('delete event', args='1'), follow=True)
        self.assertTemplateUsed(response, 'event_delete.html')

    def test_get__with_credentials_is_staff__expect_200(self):
        self.my_admin = AppUser(email='slavchev.george@gmail.com', is_staff=True)
        self.my_admin.set_password('DoDo1976')
        self.my_admin.save()
        Profile.objects.create(first_name='George', last_name="Slavchev", user_id=self.my_admin.pk)
        date = datetime.datetime.now()
        user_data = {
            'email': 'test@test.com',
            'password': 'passphrase',
        }
        user = AppUser.object.create_user(**user_data)
        doc = Doctor.objects.create(first_name='Bojidar', last_name='Slavchev', specialty='Test', days='1',
                                    manipulation_duration=30, manipulation_per_day=10, first_day_slot=date)

        CalendarEvent.objects.create(doctor_id=doc, patient_id=user, created_by=user,
                                     date=date)

        self.client.login(**user_data)

        response = self.client.get(reverse('delete event', args='1'), follow=True)
        self.assertEqual(response.status_code, 200)


class CreateCalendarEventViewTests(TestCase):
    def test_get_001(self):
        pass
