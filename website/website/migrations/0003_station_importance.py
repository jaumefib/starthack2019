# Generated by Django 2.1.7 on 2019-03-09 04:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_customuser_balance'),
    ]

    operations = [
        migrations.AddField(
            model_name='station',
            name='importance',
            field=models.IntegerField(default=0),
        ),
    ]
