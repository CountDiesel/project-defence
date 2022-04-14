from django.views import generic as views
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from schedule_app.web.models import Doctor, Profile, AppPageInfo

UserModel = get_user_model()


class HomeView(views.ListView):
    model = Doctor
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_info'] = AppPageInfo.objects.all()
        if not self.request.user.is_authenticated:
            context['logged'] = True
            return context
        return context

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and not Profile.objects.filter(pk=self.request.user.pk):
            return redirect('create profile')
        # if request.user.is_authenticated:
        #     return redirect('view doctors')
        return super().dispatch(request, *args, **kwargs)

