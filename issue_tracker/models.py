from django.db import models

# Create your models here.


class Issue(models.Model):
    summary = models.CharField(max_length=500, verbose_name='Summary')
    description = models.TextField(max_length=2500, null=True, blank=True, verbose_name='Description')
    status = models.ForeignKey('issue_tracker.Status', on_delete=models.CASCADE, verbose_name='Status')
    type = models.ForeignKey('issue_tracker.Type', on_delete=models.CASCADE, verbose_name='Type')
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
