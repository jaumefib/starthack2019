# Generated by Django 2.1.7 on 2019-03-09 12:36

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0007_auto_20190309_1235'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cup',
            name='time1',
            field=models.DateTimeField(default=datetime.datetime(2019, 3, 9, 12, 36, 54, 229541), null=True),
        ),
    ]