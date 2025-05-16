from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import unittest

class TestInventory(unittest.TestCase):
    def setUp(self):
        options = Options()
        options.add_argument("--headless")
        self.driver = webdriver.Firefox(options=options)

    def test_inventory_display(self):
        driver = self.driver
        driver.get("http://10.48.10.217")  # Use actual app host

        for i in range(10):
            item_name = f'Item {i}'
            assert item_name in driver.page_source, f"{item_name} not found in page source"

        print("All test inventory items verified.")

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
