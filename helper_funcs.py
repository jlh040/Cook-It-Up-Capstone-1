from math import floor
from secret_keys import API_KEY
import requests

list_of_cuisines = [
            'African',
            'American',
            'British',
            'Cajun',
            'Caribbean',
            'Chinese',
            'Eastern European',
            'European',
            'French',
            'German',
            'Greek',
            'Indian',
            'Irish',
            'Italian',
            'Japanese',
            'Jewish',
            'Korean',
            'Latin American',
            'Mediterranean',
            'Mexican',
            'Middle Eastern',
            'Nordic',
            'Southern',
            'Spanish',
            'Thai',
            'Vietnamese'
            ]

calorie_choices = [
        (99, 'Less than 100'),
        (199, 'Less than 200'),
        (299, 'Less than 300'),
        (399, 'Less than 400'),
        (499, 'Less than 500'),
        (599, 'Less than 600'),
        (699, 'Less than 700'),
        (799, 'Less than 800'),
        (899, 'Less than 900'),
        (999, 'Less than 1000')
    ]

def make_additional_calls(resp, list_of_recipe_titles, cuisine_name=None, query=None, cals=None):
    """Make additional calls if
    number of recipe results is > 100.
    """
    api_endpoint = 'https://api.spoonacular.com/recipes/complexSearch'
    total_num_of_recipes = resp.json()['totalResults']
    num_of_addtl_calls = floor(total_num_of_recipes / 100)
    offset = 100
    
    if resp.json()['totalResults'] > 100:
        for num in range(num_of_addtl_calls):
            if cuisine_name:
                addtl_resp = make_request_by_cuisine(api_endpoint, cuisine_name, offset)
            elif query:
                addtl_resp = make_request_by_query_and_cals(api_endpoint, query, cals, offset)
            offset += 100
            list_of_recipe_titles.extend([(obj['id'], obj['title']) for obj in addtl_resp.json()['results']])
        return list_of_recipe_titles
    else:
        return list_of_recipe_titles

def make_request_by_query_and_cals(api_endpoint, query, cals, offset):
    """Make a request to the API."""
    resp = requests.get(api_endpoint, params = {
            'query': query,
            'apiKey': API_KEY,
            'number': 100,
            'maxCalories': cals,
            'offset': offset
            })
    return resp

def make_request_by_cuisine(api_endpoint, cuisine_name, offset):
    """Make a request to the API."""
    resp = requests.get(api_endpoint, params = {
            'cuisine': cuisine_name,
            'apiKey': API_KEY,
            'number': 100,
            'offset': offset
            })
    return resp

def get_ingredients_from_recipe(resp):
    """Get a list of ingredients from a recipe."""
    list_of_ingredients = []
    for ingred in resp.json()['extendedIngredients']:
        list_of_ingredients.append(ingred['original'].capitalize())
    
    return list_of_ingredients

def check_for_no_image(form):
    if form.image_url.data == '':
        form.image_url.data = None

