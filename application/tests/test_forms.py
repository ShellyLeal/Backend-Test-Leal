from django.test import TestCase
from application.forms import menuForm, lunchForm
from  application.models import menu, lunch
from django.utils.timezone import localdate
from django.contrib.auth.models import User


# Create your tests here.
class testMenuForm(TestCase):
    '''A class to test the menu form'''

    def test_menuForm_datefield_helpText(self):
        print('Method: Tests help text for datefield')
        form = menuForm()
        self.assertEqual(form.Meta.help_texts['date'], 'Format YYYY-MM-DD')
    
    def test_menuForm_model(self):
        print('Method: Test if form\'s model is menu')
        form = menuForm()
        self.assertEqual(form.Meta.model, menu)

    def test_dateformat_menuForm(self):
        print('Method: Tests date format for menuForm')
        data = {
            'Option 1': 'cheese',
            'Option 2': 'pizza',
            'Option 3': 'hamburger',
            'Option 4': 'pizza',
            'Date': '20/10/05',
        }
        form = menuForm(data=data)
        self.assertFalse(form.is_valid())

    def test_no_past_dates(self):
        print('Method: Tests invalid form when date is a past date')
        data = {
            'Option 1': 'cheese',
            'Option 2': 'pizza',
            'Option 3': 'hamburger',
            'Option 4': 'pizza',
            'Date': '2020-10-05',
        }
        form = menuForm(data=data)
        self.assertFalse(form.is_valid())

    def test_menuForm_excluded_fields(self):
        print('Method: Tests excluded field for menu form')
        data = {
            'Option 1': 'cheese',
            'Option 2': 'pizza',
            'Option 3': 'hamburger',
            'Option 4': 'pizza',
            'Date': localdate(),
            'uuid': 2622252,
        }
        form = menuForm(data=data)
        self.assertFalse(form.is_valid())


class testLunchForm(TestCase):
    '''A class to test the lunch form'''

    def test_lunchForm_excluded_field(self):
        print('Method: Tests excluded field for lunch form')
        test_user = User.objects.create_user(
            username='justin', 
            email='jlennon@beatles.com', 
            password='user12345'
        )
        data = {
            'user': test_user,
            'Option': 'cheese',
            'preference': 'pizza',
        }
        form = lunchForm(data=data)
        self.assertFalse(form.is_valid())
    
    def test_lunchForm_required_User(self):
        print('Method: Tests required user to fill lunch form')
        data = {
            'Option': 'cheese',
            'preference': 'pizza',
        }      
        form = lunchForm(data=data)
        self.assertFalse(form.is_valid()) 

    def test_lunchForm_Model(self):
        print('Method: Tests the right model for lunch form')
        form = lunchForm()
        self.assertEqual(form.Meta.model, lunch)
