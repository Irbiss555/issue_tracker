from django.contrib.auth import login
from django.contrib.auth.models import User
from django.shortcuts import redirect, resolve_url
from django.urls import reverse
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView

from accounts.forms import MyUserCreationForm
from django.conf import settings


class RegisterView(CreateView):
    model = User
    template_name = 'registration/user_create.html'
    form_class = MyUserCreationForm

    def get_context_data(self, **kwargs):
        context = super(RegisterView, self).get_context_data(**kwargs)
        context['register_page'] = 'True'
        return context

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.get_success_url())

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if not next_url:
            next_url = self.request.POST.get('next')
        if not next_url:
            next_url = reverse('issue_tracker:project_list')
        return next_url


class LoginUserView(LoginView):
    redirect_authenticated_user = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['login_page'] = 'True'
        return context

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        print(next_url)
        if not next_url:
            next_url = self.request.POST.get('next')
        print(next_url)
        print(resolve_url(settings.LOGIN_REDIRECT_URL))
        return next_url or resolve_url(settings.LOGIN_REDIRECT_URL)
