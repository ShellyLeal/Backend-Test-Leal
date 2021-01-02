from django.test import TestCase
from  application.models import menu, lunch
from django.urls import reverse
from django.utils.timezone import localdate
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


# Create your tests here.
class testMenuModel(TestCase):
    '''A class to test the menu model'''

    @classmethod
    def setUpTestData(cls):
        menu.objects.create(
            optionOne = 'potatoes',
            optionTwo = 'chicken', 
            optionThree = 'fish',
            optionFour = 'Vegetables',
            date = '2020-12-23'          
        )
    
    def test_instance_exists(self):
        print('Method: Looks if the created menu instance exists.')
        item = menu.objects.filter(pk=1)
        if item.exists():
            status = True
        else:
            status = False
        self.assertTrue(status)
    
    def test_certain_fields(self):
        print('Method: Check the field has what really must have.')
        item = menu.objects.get(pk=1)
        if item.optionFour == 'chicken':
            status = False
        else:
            status = True
        self.assertTrue(status, False) 
    
    def test_date_is_not_today(self):
        print('Method: Assert if date is not today')
        item = menu.objects.get(pk=1)
        if item.date != localdate():
            status = True
        else:
            status = False
        self.assertTrue(status, False)

    def test_no_past_dates(self):
        print('Method: Check validationError raises for past dates')
        Menu = menu(
            optionOne = 'pork',
            optionTwo = 'lettuce', 
            optionThree = 'apple',
            optionFour = 'honey',
            date = '2020-12-20'        
        )
        self.assertRaises(ValidationError, Menu.full_clean)
    
    def test_no_missing_menu_options(self):
        print('Method: Test if there cannot be missing menu options')
        Menu = menu(
            optionOne = 'pork',
            optionFour = 'honey',
            date = '2020-12-20'        
        )
        self.assertRaises(ValidationError, Menu.full_clean)


class testLunchModel(TestCase):
    '''A class to test the lunch model'''

    @classmethod
    def setUpTestData(cls):
        # Create test user
        test_user = User.objects.create_user(
            username='justin', 
            email='jlennon@beatles.com', 
            password='user12345'
        )
        # Create test lunch request
        lunch.objects.create(
            user = test_user,
            option = 'Option 1',
            preference = 'no salt'
        )

    def test_missing_user(self):
        print('Method: Test if user is missing')
        item = lunch(
            option = 'Option 2',
        )
        self.assertRaises(ValidationError, item.full_clean)
    
    def test_lunch_date(self):
        print('Method: Test if date luch instance is always localdate')
        item = lunch.objects.get(pk=1)
        self.assertEqual(item.date, localdate())
    


    
