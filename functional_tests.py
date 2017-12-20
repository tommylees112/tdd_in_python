from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest

class NewVisitorTest(unittest.TestCase): #inherit behaviour from unittest.TestCase

  def setUp(self):
    self.browser = webdriver.Firefox()

  def tearDown(self):
    self.browser.quit()

  def test_can_start_a_list_and_retrieve_it_later(self):
    # Harry heard about a new online to do app, she goes to check out the homepage
    self.browser.get('http://localhost:8000')

    # he notices the header and title mention to-do lists
    self.assertIn('To-Do', self.browser.title)
    header_text = self.browser.find_element_by_tag_name('h1').text # get header text
    self.assertIn('To-Do', header_text) # check it contains to-do

    # he is invited to enter a to-do item right away
    input_box = self.browser.find_element_by_id('id_new_item')
    self.assertEqual(
      input_box.get_attribute('placeholder'),
      'Enter a to-do item'
      )

    # he types "buy peacock feathers" into a text box
    input_box.send_keys('Buy peacock feathers')

    # when he hits enter the page updates and now lists "1: Buy peacock feathers"
    # as an item to do list
    input_box.send_keys(Keys.ENTER)
    time.sleep(1) # explicit wait time for page to reload

    table = self.browser.find_element_by_id('id_list_table')
    rows = table.find_elements_by_tag_name('tr')

    self.assertIn('1: Buy peacock feathers', [row.text for row in rows])

    # there is still a text box inviting him to do another item
    # he types "use peacock feathers to make a fly"
    input_box = self.browser.find_element_by_id('id_new_item')
    input_box.send_keys('Use peacock feathers to make a fly')
    input_box.send_keys('ENTER')
    time.sleep(1)

    # the page updates again, and now shows both items on the list
    table = self.browser.find_element_by_id('id_list_table')
    rows = table.find_elements_by_tag_name('tr')
    self.assertIn('1: Buy peacock feathers', [row.text for row in rows])
    self.assertIn('2: Use peacock feathers to make a fly',
                  [row.text for row in rows])

    # edith wonders whether site will remember her list - then she sees the site
    # has generated a unique url for her -- there is some explanatory text

    # she visits that url - her to do list is still there

    # satisfied she goes back to sleep
    self.fail('Finish the test!')

if __name__ == '__main__':
  unittest.main(warnings='ignore')

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

"""
