# recipe-app

A project built using the Python-based Django framework, which is being hosted on Heroku. It allows its users to view a recipe wiki, upload their own recipes, and search for recipes.

## Installation:

1. Install the latest version of [Python](https://www.python.org/downloads/), and check that it's installed afterwards by running ```python --version``` in your terminal/CMD.

2. Install Django - ```pip install django```

3. Navigate to the project folder and create a new superuser by running the following command and following the prompts: ```python manage.py createsuperuser```

4. Run the following command from the project folder to start the server: ```python manage.py runserver```

5. In your browser, navigate to [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## Features:
- Admin panel capable of preforming CRUD operations on database (can be accessed by going to /admin URL and logging in with same credentials as above)
- View all recipes in list
- Click on any recipe to view it's details
- Create new recipes by entering custom information
- Search recipes by sorting based upon difficulty, filtered results returned in the form of different charts
