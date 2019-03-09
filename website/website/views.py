from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.urls import reverse

from website.forms import SignUpForm


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
    template_name = 'dashboard.html'

    def get_current_tabs(self):
        return menu_tabs()

    def get_context_data(self, **kwargs):
        context = super(Scan, self).get_context_data(**kwargs)
        return context
