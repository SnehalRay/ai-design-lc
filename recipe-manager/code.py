'''
Desgin recipe

Adding recipes
Removing recipes
Searching recipes
Updating recipes
Managing ingredients and steps


Each recipe should have:
recipe id
name
ingredients
steps
cook time
cuisine type

add_recipe()
remove_recipe()
update_recipe()
get_recipe()
search_by_ingredient()
search_by_cuisine()
get_all_recipes()
'''

from typing import List
from collections import defaultdict

class Recipe:
    def __init__(self, recipe_id: int, name: str, ingredients: set[str],
                 steps: list[str], cook_time: int, cuisine_type: str):
        self.__recipe_id = recipe_id
        self.__name = name
        self.__ingredients = set(ingredients)
        self.__steps = steps
        self.__cook_time = cook_time
        self.__cuisine_type = cuisine_type

    @property
    def recipe_id(self) -> int:
        return self.__recipe_id

    @recipe_id.setter
    def recipe_id(self, value: int):
        if not isinstance(value, int) or value <= 0:
            raise ValueError("recipe_id must be a positive integer")
        self.__recipe_id = value

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str):
        if not value or not value.strip():
            raise ValueError("name cannot be empty")
        self.__name = value.strip()

    @property
    def ingredients(self) -> set[str]:
        return set(self.__ingredients)

    @ingredients.setter
    def ingredients(self, value: set[str]):
        if not isinstance(value, (set, frozenset)) or len(value) == 0:
            raise ValueError("ingredients must be a non-empty set")
        self.__ingredients = set(value)

    @property
    def steps(self) -> list[str]:
        return list(self.__steps)

    @steps.setter
    def steps(self, value: list[str]):
        if not isinstance(value, list) or len(value) == 0:
            raise ValueError("steps must be a non-empty list")
        self.__steps = value

    @property
    def cook_time(self) -> int:
        return self.__cook_time

    @cook_time.setter
    def cook_time(self, value: int):
        if not isinstance(value, int) or value <= 0:
            raise ValueError("cook_time must be a positive integer (minutes)")
        self.__cook_time = value

    @property
    def cuisine_type(self) -> str:
        return self.__cuisine_type

    @cuisine_type.setter
    def cuisine_type(self, value: str):
        if not value or not value.strip():
            raise ValueError("cuisine_type cannot be empty")
        self.__cuisine_type = value.strip()

    def __repr__(self) -> str:
        return (f"Recipe(id={self.__recipe_id}, name='{self.__name}', "
                f"cuisine='{self.__cuisine_type}', cook_time={self.__cook_time}min)")


class RecipeManager:

    __counter = 1

    def __init__(self):
        self.recipe = {} #recipe name: recipe object
        self.ingredients = defaultdict(set) #ingredient : set(recipe objects)
        self.cuisine = defaultdict(set) #cuisine: set(recipe object)

    def add_recipe(self, name, cuisine: str, ingredients: List[str], steps: List[str], cook_time:int):
        if name in self.recipe:
            raise ValueError("Recipe already exists")
        recipe_obj = Recipe(RecipeManager.__counter, name, set(ingredients), steps, cook_time, cuisine)
        RecipeManager.__counter += 1
        self.recipe[name] = recipe_obj
        for ingredient in recipe_obj.ingredients:
            self.ingredients[ingredient].add(recipe_obj)
        self.cuisine[cuisine].add(recipe_obj)

    def remove_recipe(self, name):
        if name not in self.recipe:
            return
        recipe_obj = self.recipe[name]
        for ingredient in recipe_obj.ingredients:
            self.ingredients[ingredient].discard(recipe_obj)
        self.cuisine[recipe_obj.cuisine_type].discard(recipe_obj)
        del self.recipe[name]

    def update_recipe(self, name, cuisine: str, ingredients: List[str], steps: List[str], cook_time:int):
        if name not in self.recipe:
            raise ValueError("Recipe not found")
        recipe_obj = self.recipe[name]
        for ingredient in recipe_obj.ingredients:
            self.ingredients[ingredient].discard(recipe_obj)
        self.cuisine[recipe_obj.cuisine_type].discard(recipe_obj)
        recipe_obj.ingredients = set(ingredients)
        recipe_obj.cuisine_type = cuisine
        recipe_obj.steps = steps
        recipe_obj.cook_time = cook_time
        for ingredient in recipe_obj.ingredients:
            self.ingredients[ingredient].add(recipe_obj)
        self.cuisine[cuisine].add(recipe_obj)

    def get_recipe(self, name):
        if name not in self.recipe:
            raise ValueError("Recipe not found")
        return self.recipe[name]

    def search_by_ingredient(self, ingredient: str):
        results = self.ingredients[ingredient]
        for recipe in results:
            print(repr(recipe))
        return results

    def search_by_cuisine(self, cuisine: str):
        results = self.cuisine[cuisine]
        for recipe in results:
            print(repr(recipe))
        return results

    def get_all_recipes(self):
        for recipe in self.recipe.values():
            print(repr(recipe))


recipeManager = RecipeManager()
recipeManager.add_recipe("omlette","spanish",['eggs','spinach','salt','pepper'],['1.ecsvewc','2. cook','3.serve'],10)
recipeManager.add_recipe('cheese','italian',['cheese'],['cheese'],0)
recipeManager.get_all_recipes()
recipeManager.search_by_cuisine('italian')
recipeManager.search_by_ingredient('spanish')
recipeManager.update_recipe("omlette","mexican",['eggs','spinach','salt','pepper'],['1.ecsvewc','2. cook','3.serve'],10)
recipeManager.search_by_ingredient('spanish')
recipeManager.search_by_ingredient('mexican')
recipeManager.remove_recipe('cheese')
recipeManager.get_all_recipes()


