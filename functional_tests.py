from selenium import webdriver
from selenium.webdriver.common.keys import Keys
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

        # Check that any input field is present, with placeholder text.
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'), 'Enter a to-do item')

        # Input a to-do item.
        inputbox.send_keys('Buy peacock feathers')

        # After hitting ENTER, the page updates and now lists
        # "1. Buy peacock feathers" as an item in a table.
        inputbox.send_keys(Keys.ENTER)
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertTrue(
            any(row.text == '1.Buy peacock feathers' for row in rows),
            'New to-do item did not appear in table'
        )

        self.fail('Finish the test!')

if __name__ == '__main__':
    unittest.main(warnings='ignore')
