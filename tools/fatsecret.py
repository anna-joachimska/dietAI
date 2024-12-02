import requests
from requests.auth import HTTPBasicAuth
import os
from langchain_core.tools import tool
from typing import List, Dict

def get_access_token():
    client_id = os.environ["FATSECRET_CLIENT_ID"]
    client_secret = os.environ["FATSECRET_CLIENT_SECRET"]

    url = "https://oauth.fatsecret.com/connect/token"

    auth = HTTPBasicAuth(client_id, client_secret)

    data = {
        "grant_type": "client_credentials",
        "scope": "basic"
    }

    token_response = requests.post(url, auth=auth, data=data)

    if token_response.status_code == 200:
        return token_response.json()["access_token"]
    else:
        return None


def get_recipe_by_id(recipe_id, recipe_name, access_token):
    url = "https://platform.fatsecret.com/rest/server.api"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    data = {
        "method": "recipe.get",
        "recipe_id": recipe_id,
        "format": "json"
    }
    response = requests.post(url, headers=headers, data=data)

    return {
        "recipe_id": recipe_id,
        "recipe_name": recipe_name,
        "details": response.json()
    }

def get_recipe(calories, dish_name, recipe_type):
    """
    recipe_type: Breakfast, Lunch, Main Dish
    """
    access_token = get_access_token()

    url = "https://platform.fatsecret.com/rest/server.api"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    data = {
        "method": "recipes.search",
        "recipe_types": recipe_type,
        "search_expression": dish_name,
        "calories.from": calories - 300,
        "calories.to": calories + 100,
        "format": "json",
        "mas_results": 1
    }

    response = requests.post(url, headers=headers, data=data)
    print(response.json()["recipes"]["recipe"]["recipe_id"])
    recipe_id = response.json()["recipes"]["recipe"]["recipe_id"]
    recipe_name = response.json()["recipes"]["recipe"]["recipe_name"]

    full_recipe = get_recipe_by_id(recipe_id, recipe_name, access_token)

    return full_recipe


# @tool
# def get_recipes(meal_details: List[Dict]) -> List[Dict]:
#     """
#     Get recipes for breakfast, lunch and dinner
#     Args:
#         meal_details (List[Dict]): list of dictionaries, where each dict contains calories,
#         dish_name and recipe_type (Breakfast, Lunch or Main Dish)
#     Returns:
#          A list of dicts where each dict contains details about each recipe
#     """
#     recipes = []
#     for meal in meal_details:
#         recipe = get_recipe(meal["calories"], meal["dish_name"], meal["recipe_type"])
#         recipes.append(recipe)
#
#     return recipes

@tool
def get_breakfast_recipe(calories: int, dish_name: str ) -> dict:
    """
    Get a breakfast recipe with given number of calories
    Args:
        calories (int): the number of calories
        dish_name (str): the name of the dish
    Returns:
         A dictionary containing the recipe, direction, ingredients and nutritional information
    """

    recipe = get_recipe(calories, dish_name, "Breakfast")

    return recipe

@tool
def get_lunch_recipe(calories: int, dish_name: str ) -> dict:
    """
    Get a lunch recipe with given number of calories
    Args:
        calories (int): the number of calories
        dish_name (str): the name of the dish
    Returns:
         A dictionary containing the recipe, direction, ingredients and nutritional information
    """

    recipe = get_recipe(calories, dish_name, "Lunch")

    return recipe

@tool
def get_main_dish_recipe(calories: int, dish_name: str ) -> dict:
    """
    Get a main dish recipe with given number of calories
    Args:
        calories (int): the number of calories
        dish_name (str): the name of the dish
    Returns:
         A dictionary containing the recipe, direction, ingredients and nutritional information
    """

    recipe = get_recipe(calories, dish_name, "Main Dish")

    return recipe