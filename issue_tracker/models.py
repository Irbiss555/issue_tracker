from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.deletion import get_candidate_relations_to_delete

from issue_tracker.validators import MinLengthValidator


class SoftDeletedManager(models.Manager):
    def get_queryset(self):
        return super(SoftDeletedManager, self).get_queryset().filter(is_deleted=False)


class IsDeletedMixin(models.Model):
    is_deleted = models.BooleanField(default=False)
    objects = SoftDeletedManager()

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        delete_candidates = get_candidate_relations_to_delete(self.__class__._meta)
        if delete_candidates:
            for relation in delete_candidates:
                if (
                        relation.on_delete.__name__ == 'CASCADE'
                        and relation.one_to_many
                        and not relation.hidden
                ):
                    for item in getattr(self, relation.related_name).all():
                        item.delete()

        self.save(update_fields=['is_deleted', ])

    class Meta:
        abstract = True


class Project(IsDeletedMixin):
    users = models.ManyToManyField(get_user_model(), related_name='projects', verbose_name='Users')
    title = models.CharField(max_length=100, verbose_name='Title', validators=(MinLengthValidator(3),))
    description = models.TextField(
        max_length=800,
        null=True,
        blank=True,
        verbose_name='Description',
        validators=(MinLengthValidator(3),)
    )
    start_date = models.DateField(verbose_name='Start date')
    end_date = models.DateField(null=True, blank=True, verbose_name='End date')

    def __str__(self):
        return "{}. {}".format(self.pk, self.title)

    class Meta:
        permissions = [('change_project_users', 'Can change users of a project')]


class Issue(IsDeletedMixin):
    project = models.ForeignKey(
        to='issue_tracker.Project',
        related_name='issues',
        on_delete=models.CASCADE,
        verbose_name='Project',
        null=True
    )
    summary = models.CharField(max_length=500, verbose_name='Summary', validators=(MinLengthValidator(3),))
    description = models.TextField(
        max_length=2500,
        null=True,
        blank=True,
        verbose_name='Description',
        validators=(MinLengthValidator(3),)
    )
    status = models.ForeignKey('issue_tracker.Status', on_delete=models.CASCADE, verbose_name='Status')
    type = models.ManyToManyField('issue_tracker.Type', related_name='issues', verbose_name='Type')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated')

    def __str__(self):
        return "{}. {}".format(self.pk, self.summary)


class Status(IsDeletedMixin):
    title = models.CharField(max_length=50, verbose_name='Title')

    def __str__(self):
        return "{}. {}".format(self.pk, self.title)


class Type(IsDeletedMixin):
    title = models.CharField(max_length=100, verbose_name='Title')

    def __str__(self):
        return "{}. {}".format(self.pk, self.title)
