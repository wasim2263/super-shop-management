# super-shop-management
# Local Installation
clone the repo and go to the project directory
- copy .env.example and make .env
- go to https://djecrety.ir/ or https://miniwebtool.com/django-secret-key-generator/ and generate a key
- assign the key in the .env file to DJANGO_SECRET_KEY
- install pip for python 3
create virtual env for the project and activate it for this project. can follow https://medium.com/@gitudaniel/installing-virtualenvwrapper-for-python3-ad3dfea7c717 
- install dependencies using pip `install -r requirements.txt`
- create migrations: `python manage.py makemigrations`
- run migrations: `python manage.py migrate`
- create superuser: `python manage.py createsuperuser`
- run in local server: `python manage.py runserver`. it will run at `http://127.0.0.1:8000/`

# User manual
- go to http://127.0.0.1:8000/admin/ and log in as admin
- go to users menu and create new user who can be at the billing desk
- add brand and category for the products
- now got to http://127.0.0.1:8000 and start using the project
- can add or edit Product from the product menu
- in Home user can make the sell. use search to search the product and add it by clicking add button.
- clicking on QTY of the item will enable changing the item amount. click enter after entering the selling amount
- fill up the customer form and click purchase to finish the purchase. it will redirect to invoice. 
- click print to print the invoice
 