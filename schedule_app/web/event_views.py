import datetime
from dateutil import parser
from django.contrib.auth import get_user
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied, ValidationError
from django.db import IntegrityError
from django.http import HttpResponse, Http404
from django.urls import reverse_lazy
from schedule_app.web.helpers import check_selected_slot_is_valid
from schedule_app.web.models import CalendarEvent, Doctor
from django.views import generic as views


class CreateCalendarEventView(LoginRequiredMixin, views.CreateView):
    model = CalendarEvent
    template_name = 'calendar_event_create.html'
    success_url = reverse_lazy('index')
    # fields = ()
    fields = ('patient_id','description')

    def form_valid(self, form):
        event = form.save(commit=False)
        current_user = get_user(request=self.request)
        doc = Doctor.objects.get(pk=self.request.GET.get('doc'))
        date = self.request.GET.get('slot')
        if not event.patient_id:
            event.patient_id = current_user
        event.created_by = current_user
        event.doctor_id = doc
        event.date = parser.parse(date)
        if not check_selected_slot_is_valid(event):
            raise Http404("You're trying to reserve time slot outside doctor's schedule!")
        try:
            return super(CreateCalendarEventView, self).form_valid(form)
        except IntegrityError:
            raise Http404("ERROR: Record with that time already exist!")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        doc = Doctor.objects.get(pk=self.request.GET.get('doc'))
        context['doc'] = doc
        date = parser.parse(self.request.GET.get('slot'))
        context['slot'] = date
        context['date'] = datetime.datetime.now()
        return context


class DeleteEventView(LoginRequiredMixin, views.DeleteView):
    model = CalendarEvent
    template_name = 'event_delete.html'
    success_url = reverse_lazy('show profile')

    def dispatch(self, request, *args, **kwargs):
        event = CalendarEvent.objects.get(pk=self.kwargs['pk'])
        if event.created_by.pk != request.user.pk and not request.user.is_staff:
            raise PermissionDenied('You do not have permissions to do that!')
        return super().dispatch(request, *args, **kwargs)


class EditEventView(LoginRequiredMixin, views.UpdateView):
    model = CalendarEvent
    template_name = 'event_edit.html'
    fields = ('description', )
    success_url = reverse_lazy('index')

    def dispatch(self, request, *args, **kwargs):
        event = CalendarEvent.objects.get(pk=self.kwargs['pk'])
        if event.created_by.pk != request.user.pk and not request.user.is_staff:
            raise PermissionDenied('You do not have permissions to do that!')
        return super().dispatch(request, *args, **kwargs)



