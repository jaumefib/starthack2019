from website import models

for station in models.Station.objects.all():
    cups_to_clean = 0
    for droppOff in models.DropOff.objects.filter(station=station):
        cups_to_clean += models.Cup.objects.filter(dropOff=droppOff, user=None)
    while cups_to_clean > 0:
        for sellPoint in models.SellPoint.objects.all():
            if sellPoint.cups_desired-sellPoint.cups_current > 0:
                if cups_to_clean >= sellPoint.cups_desired-sellPoint.cups_current:
                    sellPoint.cups_current = sellPoint.cups_desired
                    cups_to_clean -= (sellPoint.cups_desired-sellPoint.cups_current)
                else:
                    sellPoint.cups_current = sellPoint.cups_current + cups_to_clean
                    cups_to_clean = 0
                sellPoint.save()
