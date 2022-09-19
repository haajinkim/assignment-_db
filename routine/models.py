from django.db import models
from user.models import User

# Create your models here.
class Routine(models.Model):
    CATEGORY = {("HOMEWORK", "HOMEWORK"), ("MIRACLE", "MIRACLE")}
    account_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=128)
    category = models.CharField(max_length=128, choices=CATEGORY)
    goal = models.CharField(max_length=128)
    is_alarm = models.BooleanField()
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


class RoutineResult(models.Model):
    RESULT = {("NOT", "NOT"), ("TRY", "TRY"), ("DONE", "DONE")}
    routine_id = models.ForeignKey(Routine, on_delete=models.SET_NULL, null=True)
    result = models.CharField(max_length=128, default="NOT", choices=RESULT)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


class RoutineDay(models.Model):
    routine_id = models.ForeignKey(Routine, on_delete=models.SET_NULL, null=True)
    day = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
