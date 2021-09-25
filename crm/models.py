from django.contrib.auth.models import User
from django.contrib.postgres.fields import *
from django.db import models
from django.urls import reverse


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='user', related_query_name='user', on_delete=models.CASCADE,
                                primary_key=True)
    avatar = models.ImageField(upload_to='media/user_avatars/', blank=True,
                               null=True, default='media/user_avatars/default.jpg')
    user_type = models.IntegerField(null=False)  # 0 is emp, 1 is client
    user_position = models.CharField(max_length=40)

    managers = ArrayField(models.IntegerField(null=True, blank=True), null=True, default=[])
    subordinates = ArrayField(models.IntegerField(null=True, blank=True), null=True, default=[])

    tasks = ArrayField(models.IntegerField(null=True, blank=True), null=True, default=[])
    events = ArrayField(models.IntegerField(null=True, blank=True), null=True, default=[])

    def get_absolute_url(self):
        return reverse("profile", kwargs={"user_id": self.user_id})


class Task(models.Model):
    task_type = models.IntegerField(null=False)
    task_status = models.IntegerField(null=False, default=0)


class Competence(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    indicator_names = ArrayField(models.CharField(max_length=100), null=True, default=[])
    indicator_values = ArrayField(models.IntegerField(null=True, blank=True), null=True, default=[])


class Question(models.Model):
    competence = models.ForeignKey(Competence, related_name='competence', related_query_name='competence',
                                   on_delete=models.CASCADE)


class GradeTemplate(models.Model):
    name = models.CharField(max_length=100, default='')
    type = models.IntegerField(null=False)
    questions = models.ManyToManyField(Question())
