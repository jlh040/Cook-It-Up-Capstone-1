from math import floor
from secret_keys import API_KEY
import requests

def make_additional_calls(resp, list_of_recipe_titles, cuisine_name):
    """Make additional calls if
    number of calls was > 100.
    """
    api_endpoint = 'https://api.spoonacular.com/recipes/complexSearch'
    total_num_of_recipes = resp.json()['totalResults']
    num_of_addtl_calls = floor(total_num_of_recipes / 100)
    offset = 100

    if resp.json()['totalResults'] > 100:
        for num in range(num_of_addtl_calls):
            addtl_resp = requests.get(api_endpoint, params = {
            'cuisine': cuisine_name,
            'apiKey': API_KEY,
            'number': 100,
            'offset': offset
            })
            offset += 100
            list_of_recipe_titles.extend([(obj['id'], obj['title']) for obj in addtl_resp.json()['results']])
        return list_of_recipe_titles
    else:
        return list_of_recipe_titles
