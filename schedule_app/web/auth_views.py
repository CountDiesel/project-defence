from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views import generic as views
from schedule_app.web.forms import UserRegistrationForm, UserRegistrationStaffForm, UserRegistrationSuperuserForm, \
    UserUpdateSuperuserForm, UserUpdateStaffForm

UserModel = get_user_model()


class UserLoginView(auth_views.LoginView):
    template_name = 'login.html'
    next_page = 'index'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.request.user.is_authenticated:
            context['logged'] = True

            return context
        return context


class UserLogoutView(LoginRequiredMixin, auth_views.LogoutView):
    next_page = 'index'


class UserRegisterView(views.CreateView):
    form_class = UserRegistrationForm

    template_name = 'register.html'

    success_url = reverse_lazy('index')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_staff:
            self.form_class = UserRegistrationStaffForm
        if request.user.is_superuser:
            self.form_class = UserRegistrationSuperuserForm
        return super().dispatch(request, *args, **kwargs)

    # def form_valid(self, *args, **kwargs):
    #     result = super().form_valid(*args, **kwargs)
    #     # login(self.request, self.object)
    #     return result

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.request.user.is_authenticated:
            context['logged'] = True

            return context
        return context


class UserPasswordChangeView(auth_views.PasswordChangeView):
    template_name = 'change_password.html'
    success_url = reverse_lazy('show profile')


class UserPasswordResetView(auth_views.PasswordResetView):
    email_template_name = 'registration/password_reset_email.html'
    template_name = 'registration/password_reset.html'
    subject_template_name = 'registration/password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.request.user.is_authenticated:
            context['logged'] = True

            return context
        return context


class UserPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = "registration/password_reset_done.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.request.user.is_authenticated:
            context['logged'] = True

            return context
        return context


class UserPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = "registration/password_reset_confirm.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.request.user.is_authenticated:
            context['logged'] = True

            return context
        return context


class UserPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = "registration/password_reset_complete.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.request.user.is_authenticated:
            context['logged'] = True

            return context
        return context


class UserEditView(views.UpdateView):
    model = UserModel
    template_name = 'user_update.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            self.form_class = UserUpdateSuperuserForm
        elif request.user.is_staff:
            self.form_class = UserUpdateStaffForm
        else:
            raise PermissionDenied('You do not have permissions to do that!')
        return super().dispatch(request, *args, **kwargs)


class ShowUsersView(LoginRequiredMixin, views.ListView):
    model = UserModel
    template_name = 'user_show.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser and not request.user.is_staff:
            raise PermissionDenied('You do not have permissions to do that!')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if user.is_superuser:
            return queryset
        elif user.is_staff:
            return queryset.filter(is_superuser=False)
        else:
            return queryset.filter(is_superuser=False, is_staff=False)


class UserDeleteView(LoginRequiredMixin, views.DeleteView):
    model = UserModel
    template_name = 'user_delete.html'
    success_url = reverse_lazy('index')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied('You do not have permissions to do that!')
        if not request.user.is_superuser:
            obj = UserModel.object.get(pk=self.kwargs['pk'])
            if obj.is_superuser:
                raise PermissionDenied('You do not have permissions to do that!')
        return super().dispatch(request, *args, **kwargs)
