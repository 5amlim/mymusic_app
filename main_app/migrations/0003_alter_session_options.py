# Generated by Django 4.1.4 on 2022-12-20 04:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_session'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='session',
            options={'ordering': ['-date']},
        ),
    ]