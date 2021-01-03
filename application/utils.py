'''Helper functions along the project'''
import uuid
from django.utils.timezone import localdate
from django.core.exceptions import ValidationError


def spawn_uuid():
    '''Generates a random
    UUID key'''
    return uuid.uuid4().hex


def validate_date(date):
    '''A help function that 
    checks if a date is a past
    date since 'today'. Raises
    a ValidationError if it happens.

    :param date: the date
    '''
    if date < localdate():
        raise ValidationError(
            ('Wrong'), code='invalid'
        )


def sudo_check(user):
    '''A function to checkout if an user 
    has 'superuser' privileges

    :param user: the current authenticated user
    :return: boolean
    '''
    if user.is_active and user.is_superuser:
        return True
    else:
        return False
