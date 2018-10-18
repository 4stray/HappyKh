[![Build Status](https://travis-ci.com/Formeme/HappyKh.svg?branch=master)](https://travis-ci.com/Formeme/HappyKh)
# HappyKh Project Setup (for unix systems)
## Supported platforms: Linux, MacOS
## Preinstalled Software Requirements
* Install npm locally:
```sh
$ sudo apt-get update
$ sudo apt-get install nodejs
$ sudo apt-get install npm
```
* [Python3.6 or higher](https://www.python.org/downloads/)
* [Git utility](https://git-scm.com/downloads)
### Download HappyKh Project locally
Clone HappyKh project locally using git utility:
```sh
$ git clone https://github.com/Formeme/HappyKh.git
$ cd HappyKh
```

### Local Deployment
##### Django Server Setup
Create Python Virtual Environment with the name of **venv** in the root folder (you can use python3.6+) and apply it:
```sh
$ python3.6 -m venv venv
$ source venv/bin/activate
```

Configure Python Virtual Environment using file **requirements.txt**:
```sh
$ pip install -r happykh/requirements.txt
```

Run Django Development Server:
```sh
$ cd happykh
$ python3 manage.py runserver
```
#

#### Django Server Setup in PyCharm
1. Click the **Edit Configuration** button and create new Django Server
2. Add new **Django Server** using "+" button
3. Add new **Environment Variable** (environment variables are separated by semicolon): 
*DJANGO_SETTINGS_MODULE=happykh.settings*
4. Setup Python interpreter
##### [PyCharm Screenshot for Django Server Setup](https://raw.githubusercontent.com/nikita-sobol/Screenshots/master/pycharm-django-server-setup.png)
#

#### Pytest in PyCharm Configuration
1. Click the **Edit Configuration** button and add **Python test** -> **pytest**
2. Add new **Environment Variable** (environment variables are separated by semicolon): 
3. Setup Python interpreter
*DJANGO_SETTINGS_MODULE=happykh.settings*
4. Edit **Working Direсtory** input field
##### [PyCharm Screenshot for Unittest Setup](https://raw.githubusercontent.com/nikita-sobol/Screenshots/master/pycharm-unittest-setup.png)
#

#### Vue.js Server Setup
In HappyKh root folder go to the **frontend** folder:
```sh
$ cd frontend
$ npm install
```
After **npm** installation run command in order to launch the client server:
```sh
$ npm run serve
```
#
#### Database Setup
Install Postgresql db:
```sh
sudo apt-get install postgresql postgresql-contrib
```
Log into an interactive session:
```sh
sudo -u postgres psql
```
Create database and user **localuser**:
```sh
CREATE DATABASE happykh;
CREATE USER localadmin WITH PASSWORD 'localpassword';
```
Give your database user access rights to the database:
```sh
ALTER ROLE localadmin SET client_encoding TO 'utf8';
ALTER ROLE localadmin SET default_transaction_isolation TO 'read committed';
ALTER ROLE localadmin SET timezone TO 'UTC';
ALTER USER localadmin CREATEDB;
GRANT ALL PRIVILEGES ON DATABASE happykh TO localadmin;
\q
```

### Environment Variables Description
**SENDGRID_API_KEY** - WebAPI key is mandatory for sending email

**EMAIL_HOST_USER** - mailbox which will be used to send email from to other users
#
### Project Styleguides
#### [Frontend Styleguide](https://github.com/Formeme/HappyKh/wiki/Frontend-Styleguide)
#### [Backend Styleguide](https://github.com/Formeme/HappyKh/wiki/Backend-Styleguide)










