# shuBay

A product sales service like eBay where every user can be a vendor.

This project was created as a part of my final project for my DB class.

## About

shuBay comes with the following features:

- Applying for vendor (as user)
- Creating, managing products (as vendor)
- Browsing products
- Adding products to cart
- Purchasing products (creates an order)
- Viewing past orders
- Completing requested orders (as vendor)
- Creating product categories (as admin)
- Managing vendors (as admin)
- Managing vendor applications (as admin)

## Requirements

```
Python v3.7+
Pip for Python 3 (pip3)
```

## Installation

Install all required packages

```
pip3 install -r requirements.txt
```

## Environment Variables

Environment variables must be in a `config.json` file in the root directory of the project with the following values:

```json
{
  "SECRET_KEY": "<RANDOM_CRYPTOGRAPHIC_SECRET>",
  "WTF_CSRF_SECRET_KEY": "<RANDOM_CRYPTOGRAPHIC_SECRET",
  "SQLALCHEMY_DATABASE_URI": "postgresql://user:password@ip:port/shuBay",
  "ADMIN_PASSWORD": "<STRONG_PASSWORD>",
  "SQLALCHEMY_TRACK_MODIFICATIONS": false,
  "SQLALCHEMY_ECHO": false
}
```

While `SQLALCHEMY_TRACK_MODIFICATIONS` should be set to false, you may set `SQLALCHEMY_ECHO` to true if you want to 
see all the queries that being executed by sqlalchemy. Sqlalchemy will log every query executed to the console in SQL
format.

## Initialization

Database tables must be initialized before this application can be used.

```
flask init-db
```

This command also creates a default admin account (with password specific in config) along with some default product
categories.

## Usage

**NOTE**: Before running, please ensure that all values in the config file are filled out. 
Please also ensure that you do not execute `flask run` without setting the environment variables 
(such as `export FLASK_APP=main`).

You may run the application using the following commands, after which the project should be running on 
`http://127.0.0.1:5000`.

Development:

```
export FLASK_APP=main
export FLASK_ENV=development
export FLASK_DEBUG=TRUE
flask run
```

Production:

```
export FLASK_APP=main
export FLASK_ENV=production
flask run
```

## Adding/removing admin accounts

Admins can be manually added/removed by setting the is_admin value of a user to true/false.

This can also be done through the use of some custom flask commands included with the application.

`flask add-admin <email>`

`flask revoke-admin <email>`

## Project Structure:

If you would like to understand the code for this project, please take 5-10 minutes to read this section.

This project's code has 5 main parts:

- Models
- Views
- Controllers
- Forms
- Services

### Models

Models define how a table should be created in a database. They are also used for performing CRUD operations on the DB.

Models can be found under packages (such as users, products, orders, etc.).

### Views

Views are what the user sees (HTML files). Views can be found in the templates folder.

### Controllers

Controllers handle the routing of the website. They handle http requests and execute business logic based on what route
invoked. 

For example, the auth controller has the routes login, logout, register, and change password. 
When a user visits /auth/login, the logic for handling user login is executed through the auth controller's login method.

Controller can be found under packages (such as auth, products, orders, etc.).

## Forms

Forms are created and validated (using python classes) in the backend. They are dynamically created on the front-end
based on all the specified fields that are provided in the class. Certain forms also handle some business logic
such as validating user credentials (see LoginForm in auth/forms.py).

Forms can be found under packages (such as auth, vendor etc.).

## Services

Services is where the core of the website's CRUD operations take place. Services use models to create, read, update, and
delete from the database. 

Services can be found under packages (such as users, vendor, products etc.).

## Todo

- Add flash messages
- Add ER Diagram
- Add project description