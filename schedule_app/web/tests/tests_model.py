from django.contrib.auth import get_user
from django.core.exceptions import ValidationError
from django.test import TestCase

from schedule_app.web.models import Profile, AppUser


class ProfileTest(TestCase):

    def test_create_profile__when_first_name_contain_only_letters__expect_success(self):
        user = AppUser(
            email='test@gmail.com',
            password='DoDo1976'
        )
        user.full_clean()
        user.save()

        profile = Profile(
            first_name='George',
            last_name='Slavchev',
            telephone_number='+359888823142',
            user=user,
        )
        profile.full_clean()
        profile.save()
        self.assertIsNotNone(profile.pk)

    def test_create_profile__when_first_name_contain_a_digit__expect_fail(self):
        user = AppUser(
            email='test@gmail.com',
            password='DoDo1976'
        )
        user.full_clean()
        user.save()

        profile = Profile(
            first_name='George2',
            last_name='Slavchev',
            telephone_number='+359888823142',
            user=user,
        )

        with self.assertRaises(ValidationError) as context:
            profile.full_clean()
            profile.save()
        self.assertIsNotNone(context.exception)

    def test_create_profile__when_first_name_contain_a_dollar_sign__expect_fail(self):
        user = AppUser(
            email='test@gmail.com',
            password='DoDo1976'
        )
        user.full_clean()
        user.save()

        profile = Profile(
            first_name='George$',
            last_name='Slavchev',
            telephone_number='+359888823142',
            user=user,
        )

        with self.assertRaises(ValidationError) as context:
            profile.full_clean()
            profile.save()
        self.assertIsNotNone(context.exception)

    def test_create_profile__when_first_name_contain_a_space__expect_fail(self):
        user = AppUser(
            email='test@gmail.com',
            password='DoDo1976'
        )
        user.full_clean()
        user.save()

        profile = Profile(
            first_name='Geo rge',
            last_name='Slavchev',
            telephone_number='+359888823142',
            user=user,
        )

        # with self.assertRaises(ValidationError) as context:
        #     profile.full_clean()
        #     profile.save()
        # self.assertIsNotNone(context.exception)

        try:
            profile.full_clean()
            profile.save()
            self.fail()
        except ValidationError as ex:
            self.assertIsNotNone(ex)
