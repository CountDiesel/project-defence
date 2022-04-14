from django.contrib.auth import get_user, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.views import generic as views
from schedule_app.web.models import Profile, CalendarEvent


class ShowProfileView(LoginRequiredMixin, views.TemplateView):
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.get(pk=self.request.user.pk)
        context['profile'] = profile
        events = CalendarEvent.objects.filter(patient_id=self.request.user.pk)
        context['events'] = events
        return context


class CreateProfileView(LoginRequiredMixin, views.CreateView):
    model = Profile
    template_name = 'profile_create.html'
    success_url = reverse_lazy('index')
    fields = ('first_name', 'last_name', 'telephone_number', 'picture')

    def form_valid(self, form):
        profile = form.save(commit=False)
        profile.pk = get_user(request=self.request).pk
        return super(CreateProfileView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not Profile.objects.filter(pk=self.request.user.pk):
            context['logged'] = True
        return context


class EditProfileView(LoginRequiredMixin, views.UpdateView):
    model = Profile
    template_name = 'profile_update.html'
    success_url = reverse_lazy('show profile')
    fields = ('first_name', 'last_name', 'telephone_number', 'picture')

    def get_object(self, queryset=None):
        current_user = get_user(request=self.request)
        if queryset is None:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, user_id=current_user.pk)


class DeleteProfileView(LoginRequiredMixin, views.DeleteView):
    model = Profile
    template_name = 'profile_delete.html'
    success_url = reverse_lazy('show profile')

    def get_object(self, queryset=None):
        current_user = get_user(request=self.request)
        if queryset is None:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, user_id=current_user.pk)
