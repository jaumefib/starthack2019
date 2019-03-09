from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist

from website import models
from website.forms import SignUpForm

import re

def menu_tabs():
    t = [('Scan', reverse('scan'), False)]
    return t


class TabsView(TemplateView):
    pass


class Dashboard(TabsView):
    template_name = 'dashboard.html'

    def get_current_tabs(self):
        return menu_tabs()

    def get_context_data(self, **kwargs):
        context = super(Dashboard, self).get_context_data(**kwargs)
        balance = self.request.user.balance
        balance = '{0:,.2f}'.format(balance) + "CHF"
        context.update({
            "balance": balance
        })
        return context


class Status(TabsView):
    template_name = 'status.html'

    def get_current_tabs(self):
        return menu_tabs()

    def get_context_data(self, **kwargs):
        context = super(Status, self).get_context_data(**kwargs)
        movements = models.Movement.objects.all()
        stations = models.Station.objects.filter(importance__gte=4)
        stations_values = []
        for station in stations:
            cups_current = 0
            cups_desired = 0
            for sellpoint in models.SellPoint.objects.filter(station=station).all():
                cups_current += sellpoint.cups_current
                cups_desired += sellpoint.cups_desired
            list.append(stations_values, {"name": station.name, "importance": station.importance, "radius": 0.01*pow((6-station.importance), 2.25)*cups_current, "longitude": station.lon, "latitude": station.lat, "cups_current": cups_current, "cups_desired": cups_desired})
        context.update({
            "movements": movements,
            "stations": stations_values
        })
        return context


class SignUp(TabsView):
    template_name = 'signup.html'

    def post(self, request, *args, **kwargs):
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect("dashboard")
        return render(request, 'signup.html', {'form': form})

    def get_current_tabs(self):
        return menu_tabs()

    def get_context_data(self, **kwargs):
        context = super(SignUp, self).get_context_data(**kwargs)
        # userid = kwargs['new_id']
        # user = User.objects.filter(id=userid).first()
        # if not user:
        #    raise Http404
        form = SignUpForm()
        context.update({
            'form': form,
        })
        return context


class Scan(TabsView):
    template_name = 'user_scan.html'

    def post(self, request, *args, **kwargs):
        qrcode = request.POST.get('qr_code')
        username = request.user
        user = models.CustomUser.objects.filter(username=username).first()

        try:
            cup = models.Cup.objects.filter(id=qrcode, user=None)
            if cup:
                cup.first().assign_to_user(user)
                user.increment_balance()
        except:
            pass

        balance = user.balance
        balance = '{0:,.2f}'.format(balance) + "CHF"
        return render(request, 'dashboard.html', {"balance": balance})

    def get_current_tabs(self):
        return menu_tabs()

    def get_context_data(self, **kwargs):
        context = super(Scan, self).get_context_data(**kwargs)
        return context
