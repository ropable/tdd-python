from functional_tests.base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(FunctionalTest):

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Open the application home page.
        self.browser.get(self.server_url)

        # Check that the page title is correct.
        self.assertIn('To-Do', self.browser.title)

        # Check that any input field is present, with placeholder text.
        inputbox = self.get_item_input_box()
        self.assertEqual(inputbox.get_attribute('placeholder'),
                         'Enter a to-do item')

        # Edith inputs a to-do item and presses ENTER to submit the form.
        inputbox.send_keys('Buy peacock feathers')
        inputbox.send_keys(Keys.ENTER)
        # Edit is taken to a new URL, and the page lists:
        # "1. Buy peacock feathers" as an item in a table.
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')
        self.check_for_row_in_list_table('1: Buy peacock feathers')

        # Edith adds a second item.
        inputbox = self.get_item_input_box()
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)
        self.check_for_row_in_list_table('1: Buy peacock feathers')
        self.check_for_row_in_list_table(
            '2: Use peacock feathers to make a fly')

        # A new user, Francis, visits the site. We use a new browser session
        # for this user.
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Visit the home page. There is no sign of Edit's list.
        self.browser.get(self.server_url)

        page_text = self.browser.find_element_by_tag_name('body').text

        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)

        # Francis starts a list new.
        inputbox = self.get_item_input_box()
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)

        # Francis gets redirected to his own unique URL.
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)

        # Again, there is no trace of Edith's list.
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)
