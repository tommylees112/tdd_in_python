from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import time
import unittest

# TO RUN: $ python manage.py test functional_tests

MAX_WAIT = 10

class NewVisitorTest(LiveServerTestCase): #inherit behaviour from django.LiveServerTestCase // unittest.TestCase

  def wait_for_row_in_list_table(self, row_text):
    start_time = time.time()
    while True:
      # if tests pass then we escape the infinite loop
      try:
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])
        return
      # if errors arise then wait 0.5s and retry but EXIT if more than 10s
      except (AssertionError, WebDriverException) as e:
        if time.time() - start_time > MAX_WAIT:
          raise e
        time.sleep(0.5)

  def setUp(self):
    self.browser = webdriver.Firefox()

  def tearDown(self):
    self.browser.quit()

  def check_for_row_in_list_table(self, row_text):
    table = self.browser.find_element_by_id('id_list_table')
    rows = table.find_elements_by_tag_name('tr')
    self.assertIn(row_text, [row.text for row in rows])

  def test_can_start_a_list_and_retrieve_it_later(self):
    # Edith heard about a new online to do app, she goes to check out the homepage
    self.browser.get(self.live_server_url)

    # she notices the header and title mention to-do lists
    self.assertIn('To-Do', self.browser.title)
    header_text = self.browser.find_element_by_tag_name('h1').text # get header text
    self.assertIn('To-Do', header_text) # check it contains to-do

    # she is invited to enter a to-do item right away
    input_box = self.browser.find_element_by_id('id_new_item')
    self.assertEqual(
      input_box.get_attribute('placeholder'),
      'Enter a to-do item'
      )

    # she types "buy peacock feathers" into a text box
    input_box.send_keys('Buy peacock feathers')

    # when she hits enter the page updates and now lists "1: Buy peacock feathers"
    # as an item to do list
    input_box.send_keys(Keys.ENTER)
    self.wait_for_row_in_list_table('1: Buy peacock feathers')

    # there is still a text box inviting her to do another item
    # she types "use peacock feathers to make a fly"
    input_box = self.browser.find_element_by_id('id_new_item')
    input_box.send_keys('Use peacock feathers to make a fly')
    input_box.send_keys(Keys.ENTER)

    # the page updates again, and now shows both items on the list
    self.wait_for_row_in_list_table('1: Buy peacock feathers')
    self.wait_for_row_in_list_table('2: Use peacock feathers to make a fly')

  def test_multiple_users_can_start_lists_at_different_urls(self):
    # edith wonders whether site will remember her list - then she sees the site
    # has generated a unique url for her -- there is some explanatory text
    # edith starts a new to-do list
    self.browser.get(self.live_server_url)
    input_box = self.browser.find_element_by_id('id_new_item')
    input_box.send_keys('Buy peacock feathers')
    input_box.send_keys(Keys.ENTER)
    self.wait_for_row_in_list_table('1: Buy peacock feathers')

    # she notices that her list has a unique URL
    edith_list_url = self.browser.current_url
    self.assertRegex(edith_list_url, '/lists/.+')

    # now a new user, Francis, comes along to the site
    ## we use a new browser session to make sure that no information sent thru
    ## edith's cookies etc.
    self.browser.quit()
    self.browser = webdriver.Firefox()

    # francis visits the home page. There's no sign of Edith's list
    self.browser.get(self.live_server_url)
    page_text = self.browser.find_element_by_tag_name('body').text
    self.assertNotIn('Buy peacock feathers', page_text)
    self.assertNotIn('make a fly', page_text)

    # Francis starts a new list by entering a new item. He is less interesting
    input_box = self.browser.find_element_by_id('id_new_item')
    input_box.send_keys('Buy milk')
    input_box.send_keys(Keys.ENTER)
    self.wait_for_row_in_list_table('1: Buy milk')

    # Francis gets his own URL
    francis_list_url = self.broswer.current_url
    self.assertRegex(francis_list_url, '/lists/.+')
    self.assertNotEqual(francis_list_url, edith_list_url)

    # again there is no trace of Edith's list
    page_text = self.browser.find_element_by_tag_name('body').text
    self.assertNotIn('Buy peacock feathers', page_text)
    self.assertIn('Buy milk', page_text)

    # satisfied they both back to sleep
    # self.fail('Finish the test!')

"""
Selenium methods:
----------------
self.browser.find_element_by_id()
self.browser.find_element_by_tag_name()
self.browser.find_elements_by_tag_name()
input_box.get_attribute('placeholder')
input_box.send_keys(Keys.ENTER)

refactor the any method:
  self.assertTrue(
    any( row.text == '1: Buy peacock feathers' for row in rows ),
    f"New to-do item did not appear in table. Contents were:\n {table.text}" # error message
    )
  self.assertIn('1: Buy peacock feathers', [row.text for row in rows])

remove if want to use the django liveservertestcase
  if __name__ == '__main__':
  #   unittest.main(warnings='ignore')

explicit wait time & explicit assertions
  time.sleep(1) # explicit wait time for page to reload
  self.check_for_row_in_list_table('1: Buy peacock feathers')
  self.check_for_row_in_list_table('2: Use peacock feathers to make a fly')
"""
