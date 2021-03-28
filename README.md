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

To be included