from django.db import models

# Create your models here.
from issue_tracker.validators import MinLengthValidator, MaxLengthValidator


class Project(models.Model):
    title = models.CharField(max_length=100, verbose_name='Title', validators=(MinLengthValidator(3),))
    description = models.TextField(
        max_length=800,
        null=True,
        blank=True,
        verbose_name='Description',
        validators=(MinLengthValidator(8),)
    )
    start_date = models.DateField(verbose_name='Start date')
    end_date = models.DateField(null=True, blank=True, verbose_name='End date')

    def __str__(self):
        return "{}. {}".format(self.pk, self.title)


class Issue(models.Model):
    summary = models.CharField(max_length=500, verbose_name='Summary', validators=(MaxLengthValidator(20),))
    description = models.TextField(
        max_length=2500,
        null=True,
        blank=True,
        verbose_name='Description',
        validators=(MinLengthValidator(10),)
    )
    status = models.ForeignKey('issue_tracker.Status', on_delete=models.CASCADE, verbose_name='Status')
    type = models.ManyToManyField('issue_tracker.Type', related_name='issues', verbose_name='Type')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated')

    def __str__(self):
        return "{}. {}".format(self.pk, self.summary)


class Status(models.Model):
    title = models.CharField(max_length=50, verbose_name='Title')

    def __str__(self):
        return "{}. {}".format(self.pk, self.title)


class Type(models.Model):
    title = models.CharField(max_length=100, verbose_name='Title')

    def __str__(self):
        return "{}. {}".format(self.pk, self.title)
