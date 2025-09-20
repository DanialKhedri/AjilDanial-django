from django.shortcuts import render
from django.views.generic import FormView
from django.contrib.auth import login, logout
from django.shortcuts import redirect
from .forms import SignUpForm, LoginForm
# Create your views here.


# ویوی ثبت‌نام
class SignUpView(FormView):
    template_name = 'signup.html'
    form_class = SignUpForm
    success_url = '/'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)

# ویوی ورود
class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = '/'

    def form_valid(self, form):
        login(self.request, form.user)
        return super().form_valid(form)

# ویوی خروج
from django.views import View

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('/')
