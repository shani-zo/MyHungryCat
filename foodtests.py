import os
import unittest
import datetime

from HealthMonitor import HealthMonitor, FEEDING_INTERVAL, HEALTH_CHECK_INTERVAL
from food_storage import upload, download, get_last_added_food
from food import CatFood
from tools import run_periodically, is_image_file
from feeding_cache import get_feeding_data, update_feeding_data, FEEDING_CACHE_FILE_PATH


class FoodStorageTests(unittest.TestCase):
    def feed(self):
        upload('resources\\fish1.jpg')

    def test_get_last_food_added(self):
        self.feed()
        _, last_feeding_time = CatFood.get_last_added_cat_food()
        self.assertLess((datetime.datetime.now() - last_feeding_time).total_seconds(), 60)

    def test_download(self):
        key, _ = get_last_added_food()
        save_path = download(key)
        self.assertTrue(os.path.exists(save_path))


class FeedingCacheTests(unittest.TestCase):
    def test_get_feeding_data(self):
        if os.path.exists(FEEDING_CACHE_FILE_PATH):
            os.remove(FEEDING_CACHE_FILE_PATH)
        self.assertRaises((OSError, IOError), get_feeding_data)
        with open(FEEDING_CACHE_FILE_PATH, 'w') as f:
            f.write("test")
        self.assertEqual(get_feeding_data(), 'test')

    def test_update_feeding_data(self):
        update_feeding_data('test1')
        with open(FEEDING_CACHE_FILE_PATH, 'r') as f:
            self.assertEqual(f.read(), 'test1')
        update_feeding_data('test2')
        with open(FEEDING_CACHE_FILE_PATH, 'r') as f:
            self.assertEqual(f.read(), 'test2')


class ToolsCase(unittest.TestCase):
    def test_is_image_file(self):
        image_path = 'resources\\fish1.jpg'
        non_image_path = __file__
        self.assertTrue(is_image_file(image_path))
        self.assertFalse(is_image_file(non_image_path))

    def test_run_periodically(self):
        count = 0

        # def change_counter():
        #     count += 1
        # run_periodically(change_counter, 0.1)


if __name__ == '__main__':
    unittest.main()
