# Django rest framework backend for the Quote app
This application serves as the API backend for the React frontend, which is available at:
https://github.com/edwinbulter/quote-web

When launched, the API can be tested in IntelliJ using the file quote_api_test.http, located at
https://github.com/edwinbulter/quote-django/tree/master/api

Implemented features:
- A set of quotes will be requested at ZenQuotes and written in the default python sqlite database if the database is empty
- Only unique quotes are written to the database:
  - if the quoteText/author combination doesn't appear in the database, it is added
- When requesting a random quote, 'quote ids to exclude' can be sent in the body of the POST request to avoid sending the same quote again when requesting a random quote
- If the list with 'quote ids to exclude' exceeds the number of quotes in the database:
  - a set of quotes is requested at ZenQuotes, added to the database and a random new quote is returned 
- Liking of quotes
  - Liked quotes will get their likes field incremented
- A list with liked quotes sorted by the number of likes can be requested. 

## Python project set up:
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

## Resolve the CORS issue caused by the frontend being hosted on a different URL than the API it interacts with.
- poetry add django-cors-headers
- add 'corsheaders' to INSTALLED_APPS in settings.py
- add 'corsheaders.middleware.CorsMiddleware' to MIDDLEWARE at the top in settings.py
- add 'django.middleware.common.CommonMiddleware' to MIDDLEWARE below the previous line in settings.py
- add CORS_ALLOW_ALL_ORIGINS = True to settings.py

## Running tests:
- poetry add pytest pytest-django
- in fact tests decorated with @pytest.mark.django_db will use a temporary database. But to be absolutely sure pytest won't use the normal database, the following measures are taken:
  - created the pytest.ini file which refers to test_settings.py
  - in test_settings the database configured for in memory, logging for console only
- to be able to use mocker in the tests:
  - poetry add pytest-mock

## Prepare application for deployment:
- create separate settings files for development, production and test in a settings folder
- remove the original settings.py file
- change the value of DJANGO_SETTINGS_MODULE in manage.py, pytest.ini, asgi.py and wsgi.py and into the specific settings file
- run the unittests and test the development server to check if the right settings files are used
- python manage.py migrate

## Deploy and run quote-django as a systemd service:
- apt install pipx
- pipx install gunicorn
- pipx ensurepath
- Install Poetry for Dependency Management for all users:
  - apt install python3-poetry
    - Clone the project repository:
      - cd /opt
      - git clone https://github.com/edwinbulter/quote-django.git
      - cd quote-django
      - poetry install
      - poetry shell
- Configure gunicorn
  - poetry add gunicorn
  - create a Gunicorn systemd service:
  - cd /etc/systemd/system
  - vi quote-django.service
    ```
    [Unit]
    Description=gunicorn daemon
    After=network.target
    
    [Service]
    User=root  #🙄 
    Group=root #🙄
    WorkingDirectory=/opt/quote-django
    ExecStart=/root/.cache/pypoetry/virtualenvs/quote-django-yHiKOEz2-py3.12/bin/gunicorn --workers 3 --bind unix:/run/gunicorn.sock quote_django.wsgi
    # unix:/run/gunicorn.sock will let Nginx handle the HTTP traffic 
    
    [Install]
    WantedBy=multi-user.target
    ```
  - Reload the systemd daemon and enable Gunicorn
    - sudo systemctl daemon-reload
    - sudo systemctl start quote-django
    - sudo systemctl enable quote-django

- Install and Configure Nginx
  - apt install nginx
  - vi /etc/nginx/sites-available/quote-django
    ```
    server {
        listen 8001;
        server_name localhost 127.0.0.1;
    
        location = /favicon.ico { access_log off; log_not_found off; }
        location /static/ {
            root /opt/quote-django;
        }
    
        location / {
        include proxy_params;
            proxy_pass http://unix:/run/gunicorn.sock;
        }
    }
    ```
  - Create a symbolic link to enable the site
    ```
    ln -s /etc/nginx/sites-available/quote-django /etc/nginx/sites-enabled
    ```
  - Test Nginx configuration:
    ```
    sudo nginx -t
    ```

- restart nginx:
  - sudo systemctl restart nginx
- watch the logging of nginx:
  - journalctl -u nginx
- watch the logging of quote-django:
  - journalctl -u qoute-django
- now test some API requests from intellij or postman on port 8001

## Deploy quote-django in a docker image
- Add the gunicorn dependency
  ```shell
  poetry add gunicorn
  ```
- create requirements.txt 
  ```
  poetry export -f requirements.txt --output requirements.txt --without-hashes
  ```
- create the [Dockerfile](./Dockerfile)
- create the [.dockerignore file](./.dockerignore)
- build the docker image
  ```shell
  docker build -t quote-django .
  ```
- run the docker image
  ```shell
  docker run -p 8002:8002 quote-django
  ```
- now test some API requests from intellij or postman on port 8002

## Create a Jenkins pipeline for building and deploying a docker image
- Create the [Jenkinsfile](./Jenkinsfile)
- Create a Pipeline job in Jenkins:
  - Open Jenkins > New Item > Select Pipeline
  - In the Pipeline configuration:
    - Choose 'Pipeline script from SCM'
    - Select your Git repository and branch
    - Specify the path to your Jenkinsfile
- Run the pipeline by clicking Build Now in the Jenkins dashboard
