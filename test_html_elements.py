from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import unittest
import time

class TestBooks(unittest.TestCase):
    def setUp(self):
        options = Options()
        options.add_argument("--headless")
        self.driver = webdriver.Firefox(options=options)

    def test_books_display(self):
        driver = self.driver
        driver.get("http://10.48.10.181")
        time.sleep(2)
        self.assertIn("Book", driver.page_source)

        book_rows = driver.find_elements(By.XPATH, "//table//tr")
        self.assertGreater(len(book_rows), 1, "No books found in the table")

    def test_add_book(self):
        driver = self.driver
        driver.get("http://10.48.10.217")
        time.sleep(2)

        title_input = driver.find_element(By.NAME, "title")
        title_input.send_keys("Test Book")

        submit_button = driver.find_element(By.XPATH, "//input[@type='submit']")
        submit_button.click()
        time.sleep(2)

        self.assertIn("Test Book", driver.page_source)

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
