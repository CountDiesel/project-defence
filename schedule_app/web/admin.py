from django.contrib import admin

from schedule_app.web.models import Profile, AppUser, Doctor, CalendarEvent


@admin.register(AppUser)
class AppUserAdmin(admin.ModelAdmin):
    list_display = ('email',)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name')


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name')


@admin.register(CalendarEvent)
class CalendarEventAdmin(admin.ModelAdmin):
    list_display = ('date', 'doctor_id')
