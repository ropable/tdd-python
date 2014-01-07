from selenium import webdriver
import unittest


class newVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_open_homepage(self):
        # Open the application home page.
        self.browser.get('http://localhost:8000')

        # Check that the page title is correct.
        self.assertIn('To-Do', self.browser.title)


if __name__ == '__main__':
    unittest.main(warnings='ignore')
