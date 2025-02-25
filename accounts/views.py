from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import CustomUserCreationForm
from django.contrib.auth import logout
from django.shortcuts import redirect


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


def logout_view(request):
    logout(request)
    return redirect('home')


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

