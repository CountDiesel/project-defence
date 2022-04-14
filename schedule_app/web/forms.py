from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from schedule_app.web.models import Profile, Doctor


UserModel = get_user_model()


class ShowProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'telephone_number', 'picture')
        widgets = {
            'first_name': forms.TextInput(
                attrs={
                    'readonly': True,
                },
            ),
            'last_name': forms.TextInput(
                attrs={
                    'readonly': True,
                },
            ),
            'telephone_number': forms.TextInput(
                attrs={
                    'readonly': True,
                },
            ),
            'picture': forms.TextInput(
                attrs={
                    'readonly': True,
                },
            ),
        }


class UserRegistrationForm(UserCreationForm):

    class Meta:
        model = UserModel
        fields = ('email',)


class UserRegistrationStaffForm(UserCreationForm):

    class Meta:
        model = UserModel
        fields = ('email', 'password1', 'password2', 'is_staff')


class UserRegistrationSuperuserForm(UserCreationForm):

    class Meta:
        model = UserModel
        fields = ('email', 'password1', 'password2', 'is_superuser', 'is_staff')
        # fields = '__all__'


class UserUpdateSuperuserForm(UserCreationForm):

    class Meta:
        model = UserModel
        fields = ('is_staff', 'is_superuser', )


class UserUpdateStaffForm(UserCreationForm):

    class Meta:
        model = UserModel
        fields = ('is_staff', )


class DoctorSelectForm(forms.Form):
    doctor = forms.ModelChoiceField(
        queryset=Doctor.objects.all(),
    )

    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
    )
