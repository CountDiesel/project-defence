from django.contrib.auth import models as auth_models
from django.contrib.auth import get_user_model
from django.db import models
from multiselectfield import MultiSelectField
from phonenumber_field.modelfields import PhoneNumberField
from schedule_app.web.managers import AppUsersManager
from schedule_app.web.validators import validate_only_letters


class AppUser(auth_models.AbstractBaseUser, auth_models.PermissionsMixin):
    # new model because custom user fields
    email = models.EmailField(
        unique=True,
        null=False,
        blank=False,
    )

    is_staff = models.BooleanField(
        default=False,
    )

    date_joined = models.DateTimeField(
        auto_now_add=True,
    )

    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'

    # password field is from AbstractBaseUser

    object = AppUsersManager()
    # my custom manager in managers.py




UserModel = get_user_model()


class Profile(models.Model):
    # additional User info
    first_name = models.CharField(
        max_length=25,
        validators=(
            validate_only_letters,
        ),
    )

    last_name = models.CharField(
        max_length=25,
        validators=(
            validate_only_letters,
        ),
    )

    telephone_number = PhoneNumberField()

    picture = models.ImageField(
        null=True,
        blank=True,
    )

    user = models.OneToOneField(
        UserModel,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    def __str__(self):
        return f'{self.first_name} {self.last_name} {self.telephone_number}'


class Doctor(models.Model):
    day = (
        ('0', 'Monday'),
        ('1', 'Tuesday'),
        ('2', 'Wednesday'),
        ('3', 'Thursday'),
        ('4', 'Friday'),
    )

    first_name = models.CharField(
        max_length=25,
        validators=(
            validate_only_letters,
        ),
    )

    last_name = models.CharField(
        max_length=25,
        validators=(
            validate_only_letters,
        ),
    )

    specialty = models.CharField(
        max_length=150,
    )

    days = MultiSelectField(
        choices=day,
        max_choices=5,
    )

    manipulation_duration = models.IntegerField()

    manipulation_per_day = models.IntegerField()

    first_day_slot = models.TimeField()

    picture = models.ImageField()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class CalendarEvent(models.Model):
    doctor_id = models.ForeignKey(
        Doctor,
        on_delete=models.SET_NULL,
        null=True,
        # blank=True,
    )

    patient_id = models.ForeignKey(
        UserModel,
        related_name='patient_id',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    created_by = models.ForeignKey(
        UserModel,
        related_name='created_by',
        on_delete=models.SET_NULL,
        null=True,
        # blank=True,
    )

    date = models.DateTimeField()

    description = models.TextField(
        null=True,
        blank=True,
    )

    class Meta:
        unique_together = ('doctor_id', 'date')


class AppPageInfo(models.Model):
    name = models.CharField(
        max_length=25,
    )

    title = models.CharField(
        max_length=250,
        null=True,
        blank=True,
    )

    text = models.TextField(
        null=True,
        blank=True,
    )

    view_status = models.BooleanField()

    image = models.ImageField(
        null=True,
        blank=True,
    )

    def __str__(self):
        return f'{self.name}'
