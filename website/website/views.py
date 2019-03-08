from django.views.generic import TemplateView
from django.urls import reverse


def menu_tabs():
    t = []
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
