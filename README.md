# Django rest framework backend for the Quote app
This application serves as a for the React frontend, which is available at:
https://github.com/edwinbulter/quote-web

When launched, the API can be tested in IntelliJ using the file quote_api_test.http, located at
https://github.com/edwinbulter/quote-django/tree/master/api

Implemented features:
- A set of quotes will be requested at ZenQuotes and written in the default python sqlite database if the database is empty
- If ZenQuotes is unavailable, a fallback file with quotes is used to initialize the empty database
- Only unique quotes are written to the database:
  - by looking at the quoteText only, quotes are compared
  - if the new quoteText doesn't appear in the database, it is added
- When requesting a random quote, 'quote ids to exclude' can be sent in the body of the POST request to avoid sending the same quote again when requesting a random quote
- If the list with 'quote ids to exclude' exceeds the number of quotes in the database:
  - a set of quotes is requested at ZenQuotes, added to the database and a random new quote is returned 
  - if ZenQuotes is unable to deliver the quotes, a random quote without looking at the ids to exclude is returned
- Liking of quotes
  - Liked quotes will be written on an event stream
  - Liked quotes will get their likes field incremented

Python project set up:
- install pipx to be able to install (and uninstall if you ever want) django globally in its own virtual environment:
  - pip install --user pipx
- install django with pipx: 
  - pipx install django
- create your project in your project-folder with 
  - django-admin startproject quote_django
- cd quote_django
- setup poetry for dependency resolution and virtual environment:
  - poetry init
- open project in vscode or intellij and open a terminal window
- poetry shell
- poetry add django djangorestframework
- python manage.py startapp api
- python manage.py migrate
- Add 'rest_framework' and 'api' to INSTALLED_APPS in quote_django/settings.py
- python manage.py createsuperuser --username admin --email admin@example.com
