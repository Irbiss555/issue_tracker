# Generated by Django 3.2.11 on 2022-02-07 19:29

from django.db import migrations, models
import issue_tracker.validators


class Migration(migrations.Migration):

    dependencies = [
        ('issue_tracker', '0002_auto_20220125_1131'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, validators=[issue_tracker.validators.MinLengthValidator(3)], verbose_name='Title')),
                ('description', models.TextField(blank=True, max_length=800, null=True, validators=[issue_tracker.validators.MinLengthValidator(8)], verbose_name='Description')),
                ('start_date', models.DateField(verbose_name='Start date')),
                ('end_date', models.DateField(blank=True, null=True, verbose_name='End date')),
            ],
        ),
        migrations.AlterField(
            model_name='issue',
            name='description',
            field=models.TextField(blank=True, max_length=2500, null=True, validators=[issue_tracker.validators.MinLengthValidator(10)], verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='issue',
            name='summary',
            field=models.CharField(max_length=500, validators=[issue_tracker.validators.MaxLengthValidator(20)], verbose_name='Summary'),
        ),
    ]
