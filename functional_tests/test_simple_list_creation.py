from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(FunctionalTest):

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Homer has heard about a cool new online to-do app. He goes
        # to check out its homepage
        self.browser.get(self.live_server_url)

        # He notices the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # He is invited to enter a to-do item straight away
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # He types "Buy Duff" into a text box (Homer loves beer)
        inputbox.send_keys('Buy Duff')

        # When he hits enter, the page updates, and now the page lists
        # "1: Buy Duff" as an item in a to-do list
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy Duff')
       
        # There is still a text box inviting him to add another item. He
        # enters "Drink Duff" (Homer is looking forward to this bit)

        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Drink Duff')
        inputbox.send_keys(Keys.ENTER)

        
        # The page updates again, and now shows both items on his list
        self.wait_for_row_in_list_table('1: Buy Duff')
        self.wait_for_row_in_list_table('2: Drink Duff')

        # Satisfied, he goes back to sleep


    def test_multiple_users_can_start_lists_at_different_urls(self):
        # Homer starts a new todo list
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy Duff')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy Duff')

        # He notices that his list has a unique URL
        homer_list_url = self.browser.current_url
        self.assertRegex(homer_list_url, '/lists/.+')

        # Now a new user, Bart, comes along to the site.

        ## We use a new browser session to make sure that no information
        ## of Homer's is coming through from cookies etc.
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Bart visits the home page. There is no sign of Homer's list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy Duff', page_text)
        self.assertNotIn('Drink Duff', page_text)

        # Bart starts a new list by entering a new item
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Cause mischief')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Cause mischief')

        # Bart gets his own unique URL
        bart_list_url = self.browser.current_url
        self.assertRegex(bart_list_url, '/lists/.+')
        self.assertNotEqual(homer_list_url, bart_list_url)

        # Again, there is no trace of Homer's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy Duff', page_text)
        self.assertIn('Cause mischief', page_text)

        # Satisfied, they both go back to sleep

