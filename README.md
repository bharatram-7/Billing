# Restaurant Billing Application

An application with online food ordering facities for customers and for in-store billing.

## Stack
- Python - Django
- Vue.js

## Local Setup Instructions

1. Clone the repo into the desired folder using `git clone https://github.com/bharatram-7/Billing.git`
2. Install the necessary requirements using `pip install -r requirements.txt`
3. From within the directory that contains manage.py file, Run - `python manage.py migrate`
4. To create a super user, run the command `python manage.py createsuperuser` and enter the required details.
You might encounter a "Too many values to unpack error" which is due to the absence of group configurations. You can ignore it. A superuser will still be created.
5. Run - `python manage.py makemigrations rolestest`
6. Run - `python manage.py migrate` to migrate the app
7. To start the server, run `python manage.py runserver`
8. Visit "/djangoadmin/" to access the Django Admin panel and to create Groups and map permissions

## Groups  - Permissions mapping

### Admin:

Create a group named "Admin" with all the permissions listed below: 

1. user - view, add, change, delete

2. item - view, add, change, delete

3. menu - view, add, change, delete

4. cartitem - view, add, change, delete

5. order - view, add, change

6. purchased item - view, add

### Billing Clerk:

Create a group named "Billing Clerk" with the permissions listed below: 

1. menu - view

2. cartitem - view, add, change, delete

3. order - view, add, change

4. purchased item - view, add

### Customers:

Create a group named "Customers" with all the permissions listed below: 

1. menu - view

2. cartitem - view, add, change, delete

3. order - view, add, change

4. purchased item - view, add

###Note: 
Associate "Admin" role to the superuser via djangoadmin --> Users --> Edit. Do not associate more than one role

# REST  APIs

## View all Menus/Create new menu

Access Required: Admin

Endpoint: api/v1/menus

Methods: GET, POST

Parameters:

{

    "name": "Name goes here",
    "active": false
}

## View menu/Update menu

Access Required: Admin

Endpoint: api/v1/menus/[id]

Methods: GET, PUT, DELETE

Parameters for updating a menu:

{

    "name": "Name goes here",
    "active": false
}

## View active menu with items

Access Required: Admin/Billing Clerk/Customers

Endpoint: api/v1/menus/active

Methods: GET

## View all items/Create new item

Access Required: Admin

Endpoint: api/v1/items

Methods: GET, POST

Parameters:

{

    "name": "",
    "description": "",
    "price": null,
    "image": null,
    "menu": null
}

Required fields: name, description, price, menu

1. For passing an image, you should use multipart/form-data as the content type
2. Images should be square in dimensions
3. Image size should be lesser than 900x900
4. Menu id should be passed for the field menu

## View an item/Update an item

Access Required: Admin

Endpoint: api/v1/items

Methods: GET, PUT

Parameters:

{

    "name": "",
    "description": "",
    "price": null,
    "image": null,
    "menu": null
}

Required fields: name, description, price, menu

1. For passing an image, you should use multipart/form-data as the content type
2. Images should be square in dimensions
3. Image size should be lesser than 900x900
4. Menu id should be passed for the field menu

## View cart with items

Access Required: Admin/Billing Clerk/Customers

Endpoint: api/v1/cartitems

Methods: GET

Note: Carts are private and can't be accessed by anybody else except cart owners

## Create cart item:

Access Required: Admin/Billing Clerk/Customers

Endpoint: api/v1/cart

Methods: GET, POST

Parameters:

{

    "item": 3,
    "quantity": 2
}

1. Item ID needs to be passed. 
2. Quantity should be an integer between 1 and 100 inclusive

## Update cart item:

Access Required: Admin/Billing Clerk/Customers

Endpoint: api/v1/cart/[id]

Methods: GET, PUT

Parameters:

{

    "quantity": 2
}

1. Quantity should be an integer between 1 and 100 inclusive


## View all orders

Access Required: 
1. Admin - All orders are returned 
2. Billing Clerk - All orders are returned
3. Customers - His/her orders

Endpoint: api/v1/orders

Methods: GET

Sample response:

[

    {
        "id": 1,
        "user": "user@cafe.co.in",
        "date": "2021-04-06 22:19:57",
        "total": "400.00",
        "status": "D",
        "rating": null
    }
]

## View an order

Access Required: 
1. Admin - All orders are returned 
2. Billing Clerk - All orders are returned
3. Customers - His/her orders

Endpoint: api/v1/orders/[id]

Methods: GET

Sample response: 


{

    "id": 1,
    "user": {
        "id": 3,
        "name": "Walk-in-customer",
        "email": "walkincustomer@cafe.co.in",
        "groups": [
            "Customers"
        ]
    },
    "purchased_items": [
        {
            "id": 1,
            "item": "Gobi Manchurian",
            "quantity": 5,
            "price": "80.00",
            "order": 1
        }
    ],
    "date": "2021-04-06 22:19:57",
    "total": "400.00",
    "status": "D",
    "rating": null
}

## Create order

Access Required: 
1. Admin & Billing Clerk - Create an order in the name of walk in customer
2. Customers - Create an order in his/her name

Endpoint: api/v1/orders/create

Methods: POST

Parameters:

{

    "purchased_items": [
        {
            "item": "Gobi Manchurian",
            "quantity": 5,
            "price": "80.00",
            "order": 1
        }
    ],
    "total": null,
    "status": null
}

1. Order total needs to be sent along with the items. It can have maximum of 2 decimal places
2. If invalid items are found, a 400 response would be returned
3. Status can be "P" or "D" and they stand for Pending and Delivered respectively


## Deliver order

Access Required: Admin/Billing Clerk

Endpoint: api/v1/orders/status

Methods: PUT

Parameters:

{

    "status": "P"
}

1. Status can be "P" or "D" and they stand for Pending and Delivered respectively

## Rate an order

Access Required: Customers

Endpoint: api/v1/orders/rating

Methods: PUT

Parameters:

{

    "rating": 5
}

1. Rating can be from 1 to 5 inclusive

## View all users/Create new user

Access Required: Admin

Endpoint: api/v1/users

Methods: GET, POST

Parameters: 

{

    "name": "",
    "email": "",
    "groups": ["Admin"]
}

1. Groups field can take one of the following values: Admin, Billing Clerk

## View user/Update user/Delete User

Access Required: Admin

Endpoint: api/v1/users/[id]

Methods: GET, PUT, DELETE

Parameters: 

{

    "name": "",
    "email": "",
    "groups": ["Admin"]
}

1. Groups field can take one of the following values: Admin, Billing Clerk
2. An Admin's group cannot be changed by any other admin/self
3. Admin cannot delete self/other admins
