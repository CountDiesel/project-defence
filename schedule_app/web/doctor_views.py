import calendar
from calendar import _nextmonth, _prevmonth
from dateutil import parser
from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from datetime import datetime, timedelta
from django.views import generic as views
from schedule_app.web.calendar import MyNewCalendar
from schedule_app.web.forms import DoctorSelectForm
from schedule_app.web.models import Doctor, CalendarEvent


class DoctorPreviewView(LoginRequiredMixin, views.ListView):
    model = Doctor
    template_name = 'doctor_preview.html'


def selected_doctor(request, pk):
    doctor = Doctor.objects.get(pk=pk)
    c = []
    for x in range(len(doctor.days)):
        c.append(int(doctor.days[x]))
    cal = MyNewCalendar(firstweekday=0)
    date = datetime.now()
    new_date = date
    week = cal.monthdays2calendar(date.year, date.month)
    month_name = calendar.month_name[date.month]
    if request.GET.get('next'):
        new_date = parser.parse(request.GET.get('next'))
        month = _nextmonth(new_date.year, new_date.month)
        week = cal.monthdays2calendar(month[0], month[1])
        month_name = calendar.month_name[month[1]]
        new_date = date.replace(month=month[1], year=month[0])
    elif request.GET.get('prev'):
        new_date = parser.parse(request.GET.get('prev'))
        month = _prevmonth(new_date.year, new_date.month)
        week = cal.monthdays2calendar(month[0], month[1])
        month_name = calendar.month_name[month[1]]
        new_date = date.replace(month=month[1], year=month[0])

    context = {
        'new_date': new_date,
        'doc': doctor,
        'days': c,
        'date': date,
        'month_name': month_name,
        'month': week,
    }
    return render(request, 'doctor_selected.html', context)


class DoctorDayView(LoginRequiredMixin, views.TemplateView):
    template_name = "doc_day.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        doc = Doctor.objects.get(pk=self.request.GET.get('doc_id'))
        slot = datetime.combine(parser.parse(self.request.GET.get('day')), doc.first_day_slot)
        # slot = doc.first_day_slot
        day = [slot]
        # day = [slot.time()]
        time_change = timedelta(minutes=doc.manipulation_duration)
        for x in range(doc.manipulation_per_day):
            slot += time_change
            day.append(slot)
            # day.append(slot.time())
        day_date = parser.parse(self.request.GET.get('day'))
        context['time'] = datetime.now()
        context['doc'] = doc
        context['date'] = day_date
        context['slots'] = day
        context['is_staff'] = self.request.user.is_staff
        occupied_slots = CalendarEvent.objects.filter(doctor_id=self.request.GET.get('doc_id'),
                                                      date__year=day_date.year, date__month=day_date.month,
                                                      date__day=day_date.day)
        occupied_slots = [x.date.time() for x in occupied_slots]
        context['occupied_slots'] = occupied_slots
        return context


class DoctorScheduleView(LoginRequiredMixin, views.TemplateView):

    template_name = 'doctor_schedule.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        doc = Doctor.objects.get(pk=self.request.GET.get('doc'))
        day_date = parser.parse(self.request.GET.get('slot'))
        events = CalendarEvent.objects.filter(doctor_id=doc.pk, date__year=day_date.year, date__month=day_date.month,
                                              date__day=day_date.day)
        slot = datetime.combine(parser.parse(self.request.GET.get('slot')), doc.first_day_slot)
        day = [slot]
        time_change = timedelta(minutes=doc.manipulation_duration)
        for x in range(doc.manipulation_per_day):
            slot += time_change
            day.append(slot)
        d = []
        for slot in day:
            patient_id = 'None'
            for e in events:
                if e.date == slot:
                    patient_id = e.patient_id
                    break
            d.append((slot, patient_id))

        day_date = parser.parse(self.request.GET.get('slot'))
        context['doc'] = doc
        context['date'] = day_date
        context['slots'] = d
        context['events'] = events
        return context


class CreateDoctorView(LoginRequiredMixin, views.CreateView):
    model = Doctor
    template_name = 'doctor_create.html'
    success_url = reverse_lazy('index')
    fields = '__all__'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class EditDoctorView(LoginRequiredMixin, views.UpdateView):
    template_name = 'doctor_update.html'
    model = Doctor
    success_url = reverse_lazy('index')
    fields = '__all__'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied('You do not have permissions to do that!')
        return super().dispatch(request, *args, **kwargs)


def doctor_select_day(request):
    if request.method == 'POST':
        form = DoctorSelectForm(request.POST)
        request.session['doc_id'] = form.data['doctor']
        request.session['date'] = form.data['date']
        return redirect('doctor select day')
    else:
        form = DoctorSelectForm()
    context = {
        'form': form,
    }
    return render(request, 'doctor_selected_day.html', context)


class DoctorSelectView(LoginRequiredMixin, views.ListView):
    template_name = 'doctor_list.html'
    model = CalendarEvent

    def get_queryset(self):
        doc_id = self.request.session.pop('doc_id', False)
        date = parser.parse(self.request.session.pop('date', False))

        result = CalendarEvent.objects.filter(doctor_id=int(doc_id), date__year=date.year, date__month=date.month, date__day=date.day)
        return result

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)




