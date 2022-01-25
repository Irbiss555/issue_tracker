# Generated by Django 3.2.11 on 2022-01-25 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('issue_tracker', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='issue',
            name='type',
        ),
        migrations.AddField(
            model_name='issue',
            name='type',
            field=models.ManyToManyField(related_name='issues', to='issue_tracker.Type', verbose_name='Type'),
        ),
    ]
