from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import unittest

class TestInventory(unittest.TestCase):
    def setUp(self):
        firefox_options = Options()
        firefox_options.add_argument("--headless")
        self.driver = webdriver.Firefox(options=firefox_options)

    def test_inventory(self):
        driver = self.driver
        driver.get("http://10.48.10.217")  # Use the actual host

        # Verify presence of test items
        for i in range(10):
            item_name = f'Item {i}'
            assert item_name in driver.page_source, f"{item_name} not found!"

        print("Inventory test passed!")

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
