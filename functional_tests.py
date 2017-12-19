from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):

  def setUp(self):
    self.browser = webdriver.Firefox()

  def tearDown(self):
    self.browser.quit()

  def test_can_start_a_list_and_retrieve_it_later(self):
    # Harry heard about a new online to do app, she goes to check out the homepage
    self.browser.get('http://localhost:8000')

    # he wnotices the header and title mention to-do lists
    self.assertIn('To-Do', self.browser.title)
    self.fail('Finish the test!')

    # he is invited to enter a to-do item right away
    # he types "buy peacock feathers" into a text box

    # when he hits enter the page updates and now lists "1: Buy peacock feathers"
    # as an item to do list

    # there is still a text box inviting him to do another item
    # he types "use peacock feathers to make a fly"

    # the page updates again, and now shows both items on the list

    # edith wonders whether site will remember her list - then she sees the site
    # has generated a unique url for her -- there is some explanatory text

    # she visits that url - her to do list is still there

    # satisfied she goes back to sleep

if __name__ == '__main__':
  unittest.main(warnings='ignore')
