from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views import generic as views
from django.contrib.auth.mixins import LoginRequiredMixin

from schedule_app.web.models import AppPageInfo


class PageInfoView(LoginRequiredMixin, views.ListView):
    model = AppPageInfo
    template_name = 'app_page_info_view.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            raise PermissionDenied('You do not have permissions to do that!')
        return super().dispatch(request, *args, **kwargs)


class CreatePageInfoView(LoginRequiredMixin, views.CreateView):
    model = AppPageInfo
    template_name = 'app_page_info_create.html'
    fields = '__all__'
    success_url = reverse_lazy('index')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            raise PermissionDenied('You do not have permissions to do that!')
        return super().dispatch(request, *args, **kwargs)


class EditPageInfoView(LoginRequiredMixin, views.UpdateView):
    model = AppPageInfo
    template_name = 'app_page_info_edit.html'
    fields = '__all__'
    success_url = reverse_lazy('index')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            raise PermissionDenied('You do not have permissions to do that!')
        return super().dispatch(request, *args, **kwargs)


class DeletePageInfoView(LoginRequiredMixin, views.DeleteView):
    model = AppPageInfo
    template_name = 'app_page_info_delete.html'
    success_url = reverse_lazy('index')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            raise PermissionDenied('You do not have permissions to do that!')
        return super().dispatch(request, *args, **kwargs)
