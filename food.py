import os

import imageClassification
from exceptions import InvalidFood
from food_storage import get_last_added_food, download
from tools import is_image_file


class Food:
    def __init__(self, food, timestamp):
        if not is_image_file(food):
            raise InvalidFood("Food must be image file")
        self.image = food
        self.timestamp = timestamp


class CatFood(Food):
    ALLOWED_FOOD_TYPES = ['fish']

    def __init__(self, food, timestamp):
        super(CatFood, self).__init__(food, timestamp)
        labels = imageClassification.classify_image(self.image)
        if not set(labels).issubset(self.ALLOWED_FOOD_TYPES):
            raise InvalidFood("This food is not good for cats!")

    @staticmethod
    def get_last_added_cat_food():
        last_added_food_key, last_added_food_modified_date = get_last_added_food()
        image_path = download(last_added_food_key)
        return CatFood(image_path, last_added_food_modified_date)
