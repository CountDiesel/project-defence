from django.urls import path

from schedule_app.web.app_page_info_views import CreatePageInfoView, EditPageInfoView, PageInfoView, DeletePageInfoView
from schedule_app.web.event_views import CreateCalendarEventView, DeleteEventView, EditEventView
from schedule_app.web.auth_views import UserLoginView, UserLogoutView, UserRegisterView, UserPasswordChangeView, \
    UserPasswordResetView, UserEditView, ShowUsersView, UserDeleteView, UserPasswordResetDoneView, \
    UserPasswordResetConfirmView, UserPasswordResetCompleteView
from schedule_app.web.doctor_views import DoctorPreviewView, selected_doctor, DoctorDayView, DoctorScheduleView, CreateDoctorView, \
    EditDoctorView, DoctorSelectView, doctor_select_day
from schedule_app.web.profile_views import EditProfileView, CreateProfileView, DeleteProfileView, ShowProfileView
from schedule_app.web.views import HomeView

urlpatterns = (
    path('', HomeView.as_view(), name='index'),
    path('profile/show/', ShowProfileView.as_view(), name='show profile'),
    path('profile/edit/', EditProfileView.as_view(), name='edit profile'),
    path('profile/create/', CreateProfileView.as_view(), name='create profile'),
    path('profile/delete/', DeleteProfileView.as_view(), name='delete profile'),

    path('login/', UserLoginView.as_view(), name='login user'),
    path('logout/', UserLogoutView.as_view(), name='logout user'),
    path('register/', UserRegisterView.as_view(), name='register user'),
    path('change-password/', UserPasswordChangeView.as_view(), name='change password'),
    path('reset-password/', UserPasswordResetView.as_view(), name='reset password'),
    path("password_reset/done/", UserPasswordResetDoneView.as_view(), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", UserPasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("reset/done/", UserPasswordResetCompleteView.as_view(), name="password_reset_complete"),
    path('update/<int:pk>/', UserEditView.as_view(), name='edit user'),
    path('delete/<int:pk>/', UserDeleteView.as_view(), name='delete user'),
    path('show-users/', ShowUsersView.as_view(), name='show users'),

    path('event/create/', CreateCalendarEventView.as_view(), name='create event'),
    path('event/delete/<int:pk>/', DeleteEventView.as_view(), name='delete event'),
    path('event/edit/<int:pk>/', EditEventView.as_view(), name='edit event'),

    path('doctor/', DoctorPreviewView.as_view(), name='view doctors'),
    path('doctor/<int:pk>/', selected_doctor, name='doctor selected'),
    path('doctor/create/', CreateDoctorView.as_view(), name='create doctor'),
    path('doctor/update/<int:pk>/', EditDoctorView.as_view(), name='update doctor'),
    path('doctor/schedule/', DoctorDayView.as_view(), name='selected day'),
    path('doctor/schedule/print/', DoctorScheduleView.as_view(), name='doctor schedule'),
    path('doctor/select/', doctor_select_day, name='doctor select'),
    path('doctor/select-day/', DoctorSelectView.as_view(), name='doctor select day'),

    path('page-info/', PageInfoView.as_view(), name='page info view'),
    path('page-info/create/', CreatePageInfoView.as_view(), name='page info create'),
    path('page-info/update/<int:pk>/', EditPageInfoView.as_view(), name='page info update'),
    path('page-info/delete/<int:pk>/', DeletePageInfoView.as_view(), name='page info delete'),
)
