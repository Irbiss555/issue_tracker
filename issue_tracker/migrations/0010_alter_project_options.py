# Generated by Django 3.2.11 on 2022-02-25 05:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('issue_tracker', '0009_project_users'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='project',
            options={'permissions': [('change_project_users', 'Can change users of a project')]},
        ),
    ]
