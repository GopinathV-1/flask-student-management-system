# Flask Toy Project

A simple CRUD project using the flask framework

This repo consists of a source code of a python script and SQLAlchemy to make an interactive student management system
using **Flask** framework

## How is it done?

You might be wondering that how the application performs many operations like creation, deletion, and update of assignments. Well, it was not that complicated as you may think. All these were achieved with the help of Database operation. 

We all know that computers can store and retrieve data easily, so in order to do this operation, we used the Database. We have used queries to pick and formulate the data in a specific structure from Database.We used SQLAlchemy to interact Database using Python. This repo consists of a basic example of how to do that.


## Getting start

To get started with the code on this repo, you need to either *clone* or *download* this repo into your machine just as shown below;

```bash
git clone git@gitlab.com:mountblue/cohort-16-python/gopinath_v/flask-toy-project.git
```

## Dependencies

Before running the application, you need to have some packages preinstalled. So I have provided all the required packages and their versions in requirements.txt file by running the below command you will be able to install all the packages.

```bash
$ pip install -r requirements.txt
```

## Running the App

#### Part 1 providing information to .env file.

To run this, you need to provide the environment values in .env file.

#### open the terminal

## step1

### SECRET_KEY generation

```bash
$ python3
>>> import secrets
>>> secrets.token_hex(16)
```
Provide **email id and password** in .env file. 

### Move to project directory
```bash
$-> cd flask-toy-project
```

### Create Database
```bash
$ sudo -u postgres psql
```

```bash
postgres=# \i create_db.sql
```

```bash
postgres=# \q
```

### Install the virtualenv package
```bash
$ pip install virtualenv
```
### Create the virtual environment
To create a virtual environment, you must specify a path. You may provide any name in the place of <mypython>:
```bash
$ virtualenv <mypython>
```
  
### Activate the virtual environment
```bash
$ source mypython/bin/activate
```

Now you can load the requirements.txt.

#### Part 2 Running the app in Python server

```bash
$ cd flask-toy-project-> python3 run.py

```
Now you can access the app on your local server

### Deactivate the virtual environment
if you have followed step1, use this command to get out of virtualenv
```bash
$ deactivate

```
### Delete Database
```bash
$ sudo -u postgres psql
```

```bash
postgres=# \i delete_db.sql
```

```bash
postgres=# \q
```