from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import localdate
from .utils import validate_date, spawn_uuid
from django.db.models.signals import post_save
from .tasks import slack_advertisement
from django.dispatch import receiver


class menu(models.Model):
    '''The menu model with its respective
    entries for luch options'''

    optionOne = models.CharField(max_length=40)
    optionTwo = models.CharField(max_length=40)
    optionThree = models.CharField(max_length=40)
    optionFour = models.CharField(max_length=40)
    date = models.DateField(validators=[validate_date])
    uuid = models.UUIDField(default=spawn_uuid, editable=False)


class lunch(models.Model):
    '''The lunch model for employees'''

    MENU = [
        ('Option 1', 'Option 1'),
        ('Option 2', 'Option 2'),
        ('Option 3', 'Option 3'),
        ('Option 4', 'Option 4'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    option = models.CharField(max_length=255, choices=MENU)
    preference = models.CharField(max_length=40, blank=True, null=True)
    date = models.DateField(default=localdate, editable=False)
#=====================================================