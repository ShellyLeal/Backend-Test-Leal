# Backend-Test-Leal
Implementation of a management system to coordinate the meal delivery for Cornershop employees.

![Owner Page](https://github.com/ShellyLeal/Backend-Test-Leal/blob/progress/docs/ownerpage.JPG)


Trello Updates on the project steps (please be free to read about the step Future Implementations and colaborate): https://trello.com/b/u1iDFoU7/meal-management


# Preparing the Django environment
To clone the project, use the following command:

    $ git clone https://github.com/ShellyLeal/Backend-Test-Leal.git

Please create a virtual environment before working on the project. Here are the instructions for doing so: https://docs.python.org/pt-br/3/library/venv.html

Also remember to install the requirements by running the following command:

    $ pip install -r requirements.txt
    
Now you have to set the URL mora.cornershop.io. 
Make an entry in hosts file, located in:

        C:\Windows\System32\drivers\etc\hosts
        
and update the file with the following line:

        127.0.0.1		noracornershop.io:8000

# Preparing the Slack environment

You will need to create a Slack group for receiving the restaurant's update about the daily menu.
Here's what mine looks like:

![Slack Demo](https://github.com/ShellyLeal/Backend-Test-Leal/blob/progress/docs/slackdemo.JPG)


After creating the group and the proper channel, you need to create a Slack API. Here are the instructions for doing so: https://api.slack.com/apps

After that, register the authentication code for the app. Here are the instructions for doing so: https://api.slack.com/legacy/oauth

With the channel name and the OAuth Code, change the following fields in the file settings.py of this project.

    # Here is where you insert the Slack API token
    OAUTH_TOKEN = 'INSERT YOUR TOKEN HERE' 

    # Here is where you place the Slack channel name
    SLACK_CHANNEL = '#restaurante'


To test administrator tools (the restaurant owner), feel free to clone the project and use the following command:

    python manage.py createsuperuser

For deleting the superuser, use the following commands inside the virtual environment:
    
    python manage.py shell
    from django.contrib.auth.models import User
    User.objects.get(username="NameHere", is_superuser=True).delete()
  
But remember, I recommended you to create users inside the testing environment, which can be done by using the available Unit Tests by the end of this tutorial.

There are two mock members to represent the clients of the restaurant. Here are their following IDs and passwords:

      # Company Worker called Justin
      username: justin
      password: user12345
      # Company Worker called Sarah
      username: sarah
      password: sarah123


# Unit Testing Instructions
You can run the tests with the following command: 

    python manage.py test
    
The ideal is to get the following results, if the tests results are positive:
![UnitTests](https://github.com/ShellyLeal/Backend-Test-Leal/blob/progress/docs/unittest.JPG)




