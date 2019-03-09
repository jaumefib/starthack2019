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

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")
        if request.user.role == 3:
            return redirect("status")
        elif request.user.role == 4:
            return redirect("scan")
        return render(request, "dashboard.html", self.get_context_data())

    def get_current_tabs(self):
        return menu_tabs()

    def get_context_data(self, **kwargs):
        context = super(Dashboard, self).get_context_data(**kwargs)

        balance = 0.0
        total_cups = 0
        desired_cups = 0
        identified = self.request.user.is_authenticated
        cups = models.Cup.objects.none()

        if identified:
            username = self.request.user
            usuari = models.CustomUser.objects.filter(username=username).first()
            balance = usuari.balance
            balance = '{0:,.2f}'.format(balance) + "CHF"
            cups = models.Cup.objects.filter(user=self.request.user, dropOff=None).order_by('-time2', '-time3')

            if self.request.user.role == 2:
                total_cups = usuari.sellPoint.cups_current
                desired_cups = usuari.sellPoint.cups_desired

        context.update({
            "balance": balance,
            "cups": cups,
            "identified": identified,
            "total_cups": total_cups,
            "desired_cups": desired_cups,
            "message": ""
        })
        return context


class Status(TabsView):
    template_name = 'status.html'

    def get_current_tabs(self):
        return menu_tabs()

    def get_context_data(self, **kwargs):
        context = super(Status, self).get_context_data(**kwargs)
        movements = models.Movement.objects.all()
        stations = models.Station.objects.all()
        stations_values_current = []
        stations_values_desired = []
        for station in stations:
            cups_current = 0
            cups_desired = 0
            for sellpoint in models.SellPoint.objects.filter(station=station).all():
                cups_current += sellpoint.cups_current
                cups_desired += sellpoint.cups_desired
            list.append(stations_values_current, {"name": station.name, "importance": station.importance, "radius": 0.01*pow((6-station.importance), 2.25)*cups_current, "longitude": station.lon, "latitude": station.lat, "cups_current": cups_current, "cups_desired": cups_desired})
            list.append(stations_values_desired, {"name": station.name, "importance": station.importance,
                                              "radius": 0.01 * pow((6 - station.importance), 2.25) * cups_desired,
                                              "longitude": station.lon, "latitude": station.lat,
                                              "cups_current": cups_current, "cups_desired": cups_desired})
        context.update({
            "movements": movements,
            "stations_current": stations_values_current,
            "stations_desired": stations_values_desired
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
            if user.role == 4:
                cup = models.Cup.objects.filter(id=qrcode)
                cup.first().return_to_dropoff(user.dropOff)
                cup.dropOff.increment_current()
            else:
                cup = models.Cup.objects.filter(id=qrcode, user=None)
                if cup:
                    if user.role == 2:
                        cup.first().sell_cup()
                        cup.sellPoint.decrement_current()
                    else:
                        cup.first().assign_to_user(user)
                        user.increment_balance()
        except:
            pass

        if user.role == 1:
            return redirect("dashboard")
        else:
            return redirect("scan")

    def get_current_tabs(self):
        return menu_tabs()

    def get_context_data(self, **kwargs):
        context = super(Scan, self).get_context_data(**kwargs)
        return context
