# Cookie / recipe-app

A project built using the Python-based Django framework, which is being hosted on Heroku. It allows its users to view a list of recipes, upload their own recipes after registering, search and filter for recipes, and display different analytics about the filtered recipes.

![Cookie home page](https://i.imgur.com/mniIWwT.png)

## Installation:

1. Install the latest version of [Python](https://www.python.org/downloads/), and check that it's installed afterwards by running ```python --version``` in your terminal/CMD.

2. Install Django - ```pip install django```

3. Navigate to the project folder and create a new superuser by running the following command and following the prompts: ```python manage.py createsuperuser```

4. Run the following command from the project folder to start the server: ```python manage.py runserver```

5. In your browser, navigate to [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## Features:
- Modern and responsive UI
- View list of different recipes
- Search for and filter for recipes by name, cooking time range, difficulty, and ingredients
- Ability to register and submit own recipes to the site
- Click on a recipe to view all details about it including ingredients and cooking instructions
- View data analytics about filtered recipes in the form of tables and different charts

## Tech Stack
- Python
- Django
- HTML/CSS w/ Bootstrap
- JavaScript / jQuery
- Heroku
