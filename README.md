# Tree menus

Tree menus is a project created for as an examination project for a job interview.

The project focuses on creating tree menus using a custom Django tag, which only
use one query to the database to generate the data.

##
This project will not be updated any further unless there's a good reason for it

## Running the project
Clone project to your computer

	git clone https://github.com/XShaygaND/tree-menus.git

Install required packages

	pip install -r requirements.txt

Create migrations

	python manage.py makemigrations treemenus

Migrate project

	python manage.py migrate
		
Run the server on your localhost

	python manage.py runserver