from django.shortcuts import render, redirect
from .models import menu, lunch
from .forms import menuForm, lunchForm
from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils.timezone import localtime, localdate
from .tasks import slack_advertisement
from .utils import sudo_check


@login_required
@user_passes_test(sudo_check)       
def create_menu(request):
    '''A view that renders a form to create a menu
    for a specific date.
	   Also create two mock users to test the employees 
	acces to the menu. The ideal is to keep these lines commented
	and use the unittests. 
    '''
    if not User.objects.filter(username = 'justin').exists():
       User.objects.create_user(
         username='justin', 
         email='jlo@cornershop.com', 
         password='user12345'
       )
    if not User.objects.filter(username = 'sarah').exists():
       User.objects.create_user(
         username='sarah',
         email='sleal@cornershop.com', 
         password='sarah123'
       )

    new_form = menuForm()
    if request.method == 'POST':
        form = menuForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data.get('date')
            if menu.objects.filter(date=date).exists():
                note = 'This date is already in use'
                return render(
                    request,
                    'createMenu.html',
                    {
                        'menuform':form,
                        'note':note
                    }
                )  
            form.save()
            if date == localdate():
                item = menu.objects.filter(date=date)
                UUID = item[0].uuid
                slack_advertisement(UUID)
            note = 'A new menu has been created'
            return render(
                request,
                'createMenu.html',
                {   
                    'menuform': None,
                    'note': note,
                }
            )             
        else:
            note = 'Date cannot be in the past'
            return render(
                request,
                'createMenu.html',
                {
                    'menuform': form,
                    'note': note,
                }
            )  
    else:
        return render(
            request, 
            'createMenu.html', 
            {
                'menuform' : new_form,
            }
        )


@login_required
@user_passes_test(sudo_check)
def main_page(request):
    '''Nora's main page.
    '''

    date = localtime()
    return render(
        request, 
        'index.html', 
        {
            'date': date,
        }
    )
    

@login_required
def request_lunch(request):
    '''A view to let employees to order
    their meail before 11 AM CLT if the menu
	is already available for that day.
    '''
	# Call today's date as reference
    date = localdate()

    # Check if today's menu is available
    item = menu.objects.filter(date=date)
    if item.exists() and localtime().hour < settings.LIMIT_HOUR:
        
         #Check if employee already requested once a day
        instance = lunch.objects.filter(
            user=request.user,
            date=date,
        )
        if instance.exists():
            return render(
                request,
                'requestMenu.html',
                {
                    'note': 'We\'re preparing your meal!'
                }
            )
        user = lunch(user=request.user)
        new_form = lunchForm()
        if request.method == 'POST':
            form = lunchForm(request.POST, instance=user)
            if form.is_valid():
                form.save()
                note = (
                    'Your today\'s meal has been saved!'
                )
        else:
            note = 'So what are you gonna eat?'
            return render(
                request, 
                'requestMenu.html',
                {
                    'requestMealForm': new_form,
                    'note': note,
                    'todays_menu': item,     
                }
            )
    else:
        note = 'Today\'s menu is not available'
    return render(
        request, 
        'requestMenu.html',
        {
            'requestMealForm': None,
            'note': note,     
        }
    )


@login_required
@user_passes_test(sudo_check)
def list_menu(request):
    '''Show  the list of all the available menus.
    '''    
    menu_dict = {}
    for item in menu.objects.all():
        menu_dict[item.pk] = {
            'date': item.date,
        }
    return render(
        request,
        'listMenu.html',
        {
            'menu_list': menu_dict,
        }
    )


@login_required
@user_passes_test(sudo_check)
def edit_menu(request, id):
    '''A method to allow Nora to edit the Menu.
    '''
    # Fill the form with current data
    note = ''
    pk = menu.objects.get(id=id)
    edit_form = menuForm(instance=pk)
    if request.method == 'POST':
        form = menuForm(request.POST, instance=pk)
        if form.is_valid():
            note = 'The menu has been updated' 
            form.save()
            edit_form = form
            return render(
                request, 
                'editMenu.html', 
                {
                    'form': None,
                    'note': note,
                }
            )
        else:
            note = 'Date cannot be in the past'
            return render(
                request, 
                'editMenu.html', 
                {
                    'form': form,
                    'note': note,
                }
            )
    return render(
        request, 
        'editMenu.html', 
        {
            'form': edit_form,
            'note': note,
        }
    )


def delete_menu(request, id):
    '''A method for superusers to delete their
    linked menus in case they won't 
    need them.

    :param request: the request object callout
    :param id: the object's primary key
    :return: redirects 
    '''
    form = menu.objects.get(id=id)
    form.delete()
    return redirect(to='list')

def delete_orders(request, id):
    '''A method for superusers to delete their
    linked menus in case they won't 
    need them.

    :param request: the request object callout
    :param id: the object's primary key
    :return: redirects 
    '''
    form = lunch.objects.get(id=id)
    form.delete()
    return redirect(to='list')	

@login_required
@user_passes_test(sudo_check)
def list_requests(request):
    '''A view that renders the list of requested
    lunches for 'today'.
    
    :param request: the request callout object
    :return: the rendered HTML list of requests
    '''
    orders = {}
    instant = localdate()
    for item in lunch.objects.filter(date=instant):
        orders[item.pk] = {
            'option': item.option,
            'user': item.user.username,
        }
    return render(
        request,
        'listRequests.html',
        {
           'requests_list': orders,
           'date': instant,
        }
    )


def check_details(request, id):
    '''It shows the details of the orders.
    '''
    item = lunch.objects.filter(id=id)
    return render(
        request,
        'checkDetails.html',
        {
            'lunch': item,
            'pk': id,
        }
    )


def show_menu(request, uuid):
    '''The main website view for the employees.
    '''
    date = localdate()
    Menu = menu.objects.filter(date=date)
    return render(
        request,
        'showMenu.html',
        {
            'lunch': Menu,
        }
    )

