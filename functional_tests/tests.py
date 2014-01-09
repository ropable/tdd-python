from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class newVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Open the application home page.
        self.browser.get(self.live_server_url)

        # Check that the page title is correct.
        self.assertIn('To-Do', self.browser.title)

        # Check that any input field is present, with placeholder text.
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'), 'Enter a to-do item')

        # Input a to-do item and press ENTER to submit the form.
        inputbox.send_keys('Buy peacock feathers')
        inputbox.send_keys(Keys.ENTER)

        # Add a short pause after submitting before looking for elements,
        # in order to view the CSRF error before the browser closes.
        #import time
        #time.sleep(2)

        # After hitting ENTER, the page updates and now lists
        # "1. Buy peacock feathers" as an item in a table.
        self.check_for_row_in_list_table('1: Buy peacock feathers')

        # Add a second item.
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)

        self.check_for_row_in_list_table('1: Buy peacock feathers')
        self.check_for_row_in_list_table('2: Use peacock feathers to make a fly')

        self.fail('Finish the test!')
