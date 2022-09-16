from django.db import models
from user.models import User

# Create your models here.
class Routine(models.Model):
    CATEGORY = {
        ('HOMEWORK','HOMEWORK'),
        ('MIRACLE','MIRACLE')
    }
    account_id = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    category = models.CharField(max_length=128,choices=CATEGORY)
    goal = models.CharField(max_length=128)
    is_alarm = models.BooleanField()
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_At = models.DateTimeField(auto_now=True,blank=True)
    
class RoutineResult(models.Model):
    RESULT = {
        ('안함','NOT'),
        ('시도','TRY'),
        ('완료','DONE')
    }
    routine_id = models.ForeignKey(Routine, on_delete=models.CASCADE)
    result = models.CharField(max_length=128)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_At = models.DateTimeField(auto_now=True,blank=True)

class RoutineDay(models.Model):
    routine_id = models.ForeignKey(Routine, on_delete=models.CASCADE)
    day = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_At = models.DateTimeField(auto_now=True,blank=True)