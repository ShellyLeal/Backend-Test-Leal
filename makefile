# VARIABLES 
TEST = ./test/
SOURCE = ./source/

# COMMANDS

requirements: # Install requirements
	pip install -r requirements.txt

run: # Run project
	python manage.py runserver

unittest:
	python manage.py test

