
import application.views as views
from django.contrib.auth.models import User
from application.models import menu, lunch
from django.test import TestCase
from django.urls import reverse
from application.tasks import slack_advertisement
from django.utils.timezone import localdate


# Create your tests here.
class testCreateMenuView(TestCase):
    '''A class to test create_menu view'''

    @classmethod
    def setUpTestData(cls):

        # Create 10 menus to test the view
        for item in range(10):
            menu.objects.create(
                optionOne = 'potatoes',
                optionTwo = 'chicken', 
                optionThree = 'fish',
                optionFour = 'Vegetables',
                date = '2020-12-%s' %str(item+1)  
            )

        # Create test user
        User.objects.create_user(
            username='justin', 
            email='jlennon@beatles.com', 
            password='user12345'
        )

        # Create test superuser
        User.objects.create_superuser(
            username='nora', 
            email='norita@cornershop.com', 
            password='user12345'
        )

    def test_create_menu_view_url(self):
        print('Method: Tests create_menu authentication url')
        response = self.client.get('/new-menu/')
        self.assertEqual(response.status_code, 302)
    
    def test_unauthorized_users_create_menu_view(self):
        print('Method: Tests access denied for non admin users')
        self.client.login(
            username='justin',
            password='user12345',
        )
        response = self.client.get(reverse(views.create_menu))
        self.assertNotEqual(response.status_code, 200)

    def test_authorized_users_create_menu_view(self):
        print('Method: Tests successfull access for admin users')
        self.client.login(
            username='nora',
            password='user12345',
        )
        response = self.client.get(reverse(views.create_menu))
        self.assertEqual(response.status_code, 200)
    
    def test_create_menu_uses_template(self):
        print('Method: Tests create_menu view has the right template')
        self.client.login(
            username='nora',
            password='user12345',
        )
        response = self.client.get('/new-menu/')
        self.assertTrue(response, 'templates/createMenu.html')


class testMainPageView(TestCase):
    '''A class to test the nora's main page'''

    @classmethod
    def setUpTestData(cls):

        # Create test user
        User.objects.create_user(
            username='justin', 
            email='jlennon@beatles.com', 
            password='user12345'
        )

        # Create test superuser
        User.objects.create_superuser(
            username='nora', 
            email='norita@cornershop.com', 
            password='user12345'
        )
    
    def test_access_template_main_page_view(self):
        print('Method: Tests template and admin users access to main page view')
        self.client.login(
            username='nora',
            password='user12345',
        )
        response_temp = self.client.get('')
        response = self.client.get(reverse(views.main_page))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response_temp, 'templates/index.html')    

    def test_non_admin_users_allowed_main_page_view(self):
        print('Method: Tests denied non admin users to main page view')
        self.client.login(
            username='justin',
            password='user12345',
        )
        response = self.client.get(reverse(views.main_page))
        self.assertEqual(response.status_code, 302)


class testEditMenuView(TestCase):
    '''A class to test the main admin page view'''

    @classmethod
    def setUpTestData(cls):

        # Create 10 menus to test the view
        for item in range(10):
            menu.objects.create(
                optionOne = 'potatoes',
                optionTwo = 'chicken', 
                optionThree = 'fish',
                optionFour = 'Vegetables',
                date = '2020-12-%s' %str(item+1)  
            )

        # Create test user
        User.objects.create_user(
            username='justin', 
            email='jlennon@beatles.com', 
            password='user12345'
        )

        # Create test superuser
        User.objects.create_superuser(
            username='nora', 
            email='norita@cornershop.com', 
            password='user12345'
        )

    def test_non_admin_users_allowed_edit_menu_view(self):
        print('Method: Tests denied non admin users to edit menus ')
        self.client.login(
            username='justin',
            password='user12345',
        )
        # Test denial of access for all menus
        for pk in range(10):
            response = self.client.get('/edit-menu/' + str(pk+1))
            self.assertEqual(response.status_code, 302) 

    def test_allowed_admin_access_edit_menu(self):
        print('Method: Tests allowed access for admin users to edit menus')    
        self.client.login(
            username='nora',
            password='user12345',
        )
        # Test granted access for all menus
        for pk in range(10):
            response = self.client.get('/new-menu/' + str(pk+1))
            self.assertTrue(response.status_code, 200)
