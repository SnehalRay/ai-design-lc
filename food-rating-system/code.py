'''
Food rating system should support
adding the food
food has cuisine
rating the food based on the name
change the rating of the food
'''

from enum import Enum
from sortedcontainers import SortedList


class RatingType(Enum):
    POOR = 1
    BAD = 2
    OK = 3
    GOOD = 4
    EXCELLENT = 5


class Food:
    def __init__(self, name: str, cuisine: str, rating: RatingType):
        self._name = name
        self._cuisine = cuisine
        self._rating = rating

    @property
    def name(self) -> str:
        return self._name

    @property
    def cuisine(self) -> str:
        return self._cuisine

    @property
    def rating(self) -> RatingType:
        return self._rating

    @rating.setter
    def rating(self, rating: RatingType):
        self._rating = rating

class RatingSystem:

    def __init__(self):
        self.food_map: dict[str, Food] = {}
        self.cuisine_score: dict[str, int] = {}
        self.cuisine_count: dict[str, int] = {}
        self.cuisine_sorted: SortedList = SortedList()  # (-avg, cuisine_name)

    def _avg(self, cuisine: str) -> float:
        return self.cuisine_score[cuisine] / self.cuisine_count[cuisine]

    def adding_food(self, name: str, cuisine: str, rating: RatingType) -> bool:
        if name in self.food_map:
            return False
        if cuisine in self.cuisine_score:
            self.cuisine_sorted.discard((-self._avg(cuisine), cuisine))
        self.food_map[name] = Food(name, cuisine, rating)
        self.cuisine_score[cuisine] = self.cuisine_score.get(cuisine, 0) + rating.value
        self.cuisine_count[cuisine] = self.cuisine_count.get(cuisine, 0) + 1
        self.cuisine_sorted.add((-self._avg(cuisine), cuisine))
        return True

    def change_rating(self, name: str, rating: RatingType) -> bool:
        if name not in self.food_map:
            return False
        food = self.food_map[name]
        cuisine = food.cuisine
        self.cuisine_sorted.discard((-self._avg(cuisine), cuisine))
        self.cuisine_score[cuisine] += rating.value - food.rating.value
        food.rating = rating
        self.cuisine_sorted.add((-self._avg(cuisine), cuisine))
        return True

    def best_cuisine_rating(self) -> str:
        if not self.cuisine_sorted:
            return ""
        return self.cuisine_sorted[0][1]
    
rating = RatingType
system = RatingSystem()
print(system.adding_food('biryani','indian',rating.POOR))
print(system.adding_food('butter chicken','indian',rating.GOOD))
print(system.adding_food('pasta','italian',rating.GOOD))
print(system.change_rating('biryani',rating.EXCELLENT))
print(system.best_cuisine_rating())

