from django.core.management.base import BaseCommand, CommandError
from website import models


class Command(BaseCommand):
    help = 'Updates the logistics moving tables'

    def handle(self, *args, **options):
        for station in models.Station.objects.all():
            cups_to_clean = 0
            for droppOff in models.DropOff.objects.filter(station=station):
                cups_to_clean += models.Cup.objects.filter(dropOff=droppOff, user=None).count()
            if cups_to_clean > 0:
                sellPoints = models.SellPoint.objects.all()
                i = 0
                while i < sellPoints.count() and cups_to_clean > 0:
                    if sellPoints[i].cups_desired - sellPoints[i].cups_current > 0:
                        if cups_to_clean >= sellPoints[i].cups_desired - sellPoints[i].cups_current:
                            sellPoints[i].cups_current = sellPoints[i].cups_desired
                            cups_to_clean -= (sellPoints[i].cups_desired - sellPoints[i].cups_current)
                        else:
                            sellPoints[i].cups_current = sellPoints[i].cups_current + cups_to_clean
                            cups_to_clean = 0
                        sellPoints[i].save()
                    i += 1
        self.stdout.write(self.style.SUCCESS('Done'))
