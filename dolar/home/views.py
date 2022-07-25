from django.views.generic import ListView, DetailView
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect

from datetime import datetime, timedelta

from django.views.generic import TemplateView

from .models import Cotizacion
from .forms import EditProfileForm, PasswordForm


class SignupView(CreateView):
    form_class = UserCreationForm
    template_name = 'home/signup.html'
    success_url = 'home/'

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('home/')
        return super().get(request, *args, **kwargs)


class ProfileView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    form_class = EditProfileForm
    template_name = 'home/profile.html'
    success_url = '/profile'
    login_url = 'quotes:login'
    success_message = 'Profile settings have been updated'

    def get_object(self):
        return self.request.user


class PasswordView(LoginRequiredMixin, SuccessMessageMixin, PasswordChangeView):
    form_class = PasswordForm
    template_name='home/password.html'
    success_url = '/password'
    success_message = 'Successfully updated password'


class IndexView(LoginRequiredMixin, ListView):
    template_name = 'home/index.html'
    context_object_name = 'latest_quote_list'
    login_url = 'quotes:login'

    def get_latest_ars(self):
        return [
            Cotizacion.objects.order_by('-datetime').filter(name='blue')[:2],
            Cotizacion.objects.order_by('-datetime').filter(name='bna')[:2],
            Cotizacion.objects.order_by('-datetime').filter(name='bbva')[:2],
            Cotizacion.objects.order_by('-datetime').filter(name='santander')[:2],
            Cotizacion.objects.order_by('-datetime').filter(name='patagonia')[:2],
        ]

    def get_latest_cop(self):
        return [
            Cotizacion.objects.order_by('-datetime').filter(currency='cop')[:2],
        ]

    def get_queryset(self):
        """Return the last five published values."""
        return {"ars": self.get_latest_ars(), "cop": self.get_latest_cop()}


class ArchiveView(LoginRequiredMixin, ListView):
    template_name = 'home/archive.html'
    context_object_name = 'quote_list'
    login_url = 'quotes:login'

    def get_last_entries(self, currency, name, days_back=15):
        results = []
        days = 0
        while days < days_back:
            given_date = datetime.now().date() - timedelta(days=days)
            cotiz = Cotizacion.objects.order_by('-datetime').filter(currency=currency).filter(name=name).filter(datetime__date = given_date)
            if len(cotiz) > 0:
                results.append(cotiz[0])
            days += 1
        return results

    # def get_ars(self):
    #     return [
    #         Cotizacion.objects.order_by('-datetime').filter(name='blue')[:50],
    #         Cotizacion.objects.order_by('-datetime').filter(name='bna')[:50],
    #         Cotizacion.objects.order_by('-datetime').filter(name='bbva')[:50],
    #         Cotizacion.objects.order_by('-datetime').filter(name='santander')[:50],
    #         Cotizacion.objects.order_by('-datetime').filter(name='patagonia')[:50],
    #     ]

    def get_ars(self):
        blue = self.get_last_entries('ars', 'blue')
        bna = self.get_last_entries('ars', 'bna')
        bbva = self.get_last_entries('ars', 'bbva')
        santander = self.get_last_entries('ars', 'santander')
        patagonia = self.get_last_entries('ars', 'patagonia')
        return [blue, bna, bbva, santander, patagonia]
        # return [blue]

    def get_cop(self):
        return [
            Cotizacion.objects.order_by('-datetime').filter(currency='cop')[:50],
        ]


    def get_queryset(self):
        """Return the last five published values."""
        return {"ars": self.get_ars(), "cop": self.get_cop()}


class HistoryView(LoginRequiredMixin, ListView):
    template_name = 'home/history.html'
    context_object_name = 'quote_list'
    login_url = 'quotes:login'

    def __init__(self, currency, name):
        self.currency = currency
        self.name = name

    def get_last_entries(self, currency, name, days_back=15):
        results = []
        days = 0
        while days < days_back:
            given_date = datetime.now().date() - timedelta(days=days)
            cotiz = Cotizacion.objects.order_by('-datetime').filter(currency=currency).filter(name=name).filter(datetime__date = given_date)
            if len(cotiz) > 0:
                results.append(cotiz[0])
            days += 1
        return results

    def get_values(self):
        values = self.get_last_entries(self.currency, self.name)
        return values

    def get_queryset(self):
        """Return the last value for earch day."""
        return {"values": self.get_values()}


class BNAHistory(HistoryView):
    def __init__(self, currency='ars', name='bna'):
        super().__init__(currency, name)


class BBVAHistory(HistoryView):
    def __init__(self, currency='ars', name='bbva'):
        super().__init__(currency, name)


class BlueHistory(HistoryView):
    def __init__(self, currency='ars', name='blue'):
        super().__init__(currency, name)


class SantanderHistory(HistoryView):
    def __init__(self, currency='ars', name='santander'):
        super().__init__(currency, name)


class PatagoniaHistory(HistoryView):
    def __init__(self, currency='ars', name='patagonia'):
        super().__init__(currency, name)


class COPHistory(HistoryView):
    def __init__(self, currency='cop', name='generic'):
        super().__init__(currency, name)


class DetailView(LoginRequiredMixin, DetailView):
    model = Cotizacion
    template_name = 'home/detail.html'
    context_object_name = 'quote'
    login_url = 'quotes:login'


class LoginInterfaceView(LoginView):
    template_name = 'home/login.html'


class LogoutInterfaceView(LogoutView):
    template_name = 'home/logout.html'


class WelcomeView(LoginView):
    template_name = 'home/welcome.html'

    def get(self, request, *args, **kwargs):     # overriding this method redirects to indicated website when authenticated
        if self.request.user.is_authenticated:
            return redirect('home/')
        return super().get(request, *args, **kwargs)

