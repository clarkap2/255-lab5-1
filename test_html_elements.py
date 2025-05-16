from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import unittest
import time

class TestShoppingList(unittest.TestCase):
    def setUp(self):
        options = Options()
        options.add_argument("--headless")
        self.driver = webdriver.Firefox(options=options)

    def test_shopping_page_loads(self):
        driver = self.driver
        driver.get("http://10.48.10.181")
        time.sleep(3)
        self.assertIn("Shopping List", driver.page_source)

    def test_add_shopping_item(self):
        driver = self.driver
        driver.get("http://10.48.10.181")
        time.sleep(3)

        name_input = driver.find_element(By.NAME, "name")
        quantity_input = driver.find_element(By.NAME, "quantity")

        name_input.send_keys("Milk")
        quantity_input.clear()
        quantity_input.send_keys("2")

        driver.find_element(By.XPATH, "//input[@type='submit']").click()
        time.sleep(2)

        self.assertIn("Milk", driver.page_source)

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
