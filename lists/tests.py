# from IPython.core.debugger import Tracer
from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from lists.views import home_page
from lists.models import Item

# Create your tests here.
class HomePageTest(TestCase):

  def test_home_page_returns_correct_html(self):
    response = self.client.get('/') #pass the url we want to test
    self.assertTemplateUsed(response, 'home.html') # is the recieved html the home.html?

class ItemModelTest(TestCase):

  def test_saving_and_retrieving_items(self):
    # create a first item in the database
    first_item = Item()
    first_item.text = 'The first (ever) list item'
    first_item.save()

    # create a second item in the database
    second_item = Item()
    second_item.text = 'Item the second'
    second_item.save()

    # return the list of saved items
    saved_items = Item.objects.all()
    self.assertEqual(saved_items.count(), 2)

    # make sure the database read items == the saved items from earlier
    first_saved_item = saved_items[0]
    second_saved_item = saved_items[1]
    self.assertEqual(first_saved_item.text, 'The first (ever) list item')
    self.assertEqual(second_saved_item.text, 'Item the second')

class ListViewTest(TestCase):

  def test_uses_list_template(self):
    response = self.client.get('/lists/the-only-list-in-the-world/')
    self.assertTemplateUsed(response, 'list.html')

  def test_displays_all_items(self):
    Item.objects.create(text='itemey 1')
    Item.objects.create(text='itemey 2')

    response = self.client.get('/lists/the-only-list-in-the-world/')

    self.assertContains(response, 'itemey 1') # helper method for dealing with the bytes of response (convert to utf-8 automatically)
    self.assertContains(response, 'itemey 2')

class NewListTest(TestCase):

  def test_can_save_a_POST_request(self):
    # post Item to database and check that contains the right text
    self.client.post('/lists/new', data = {'item_text': 'A new list item'})
    self.assertEqual(Item.objects.count(), 1)
    new_item = Item.objects.first()
    self.assertEqual(new_item.text, 'A new list item')

  def test_redirects_after_POST(self):
    response = self.client.post('/lists/new', data={'item_text': 'A new list item'})
    self.assertRedirects(response, '/lists/the-only-list-in-the-world/')

"""
class marginalia():
# way of looking without Django test client

  def test_root_url_resolves_to_home_page(self):
    found = resolve('/')
    self.assertEqual(found.func, home_page)

  def test_home_page_returns_correct_html(self):
    request = HttpRequest()
    response = home_page(request)
    html = response.content.decode('utf8')
    expected_html = render_to_string('home.html')
    self.assertTrue(html.startswith('<html>'))
    self.assertIn('<title>To-Do lists</title>', html)
    self.assertTrue(html.strip().endswith('</html>'))
    self.assertEqual(html, expected_html)


# check a response has the content rendered by a template
    self.assertIn('A new list item', response.content.decode())
    self.assertTemplateUsed(response, 'home.html')

# old test for check if it displays all values in list

  def test_displays_all_list_items(self):
    # set up the test
    Item.objects.create(text='itemey 1')
    Item.objects.create(text='itemey 2')

    # print("ITEMS:\n====\n" ,[item.text for item in Item.objects.all()])

    # call the test
    response = self.client.get('/')

    # assertions (things to check)
    # print("\n--------\n", response.content.decode())
    self.assertIn('itemey 1', response.content.decode())
    self.assertIn('itemey 2', response.content.decode())

# before learning django method assertRedirects()
  def test_redirects_after_POST(self):
    # test that redirected to list specific page after posted new item
    response = self.client.post('/lists/new', data = {'item_text': 'A new list item'}) #without slash @ end = ACTION
    self.assertEqual(response.status_code, 302)
    self.assertEqual(response['location'], '/lists/the-only-list-in-the-world/')

# remove from home_page class because home no longer doing these actions

  def test_only_saves_items_when_necessary(self):
    self.client.get('/')
    self.assertEqual(Item.objects.count(), 0)

  def test_redirects_after_POST(self):
    response = self.client.post('/', data={'item_text': 'A new list item'})
    # HTTP redirect = 302 pointing browser to new location
    self.assertEqual(response.status_code, 302)
    self.assertEqual(response['location'], '/lists/the-only-list-in-the-world/')

  # create a POST request to database then redirect to home page
  def test_can_save_a_POST_request(self):
    self.client.post('/', data={'item_text': 'A new list item'}) # create the new item

    self.assertEqual(Item.objects.count(), 1) # check that item saved to database
    new_item = Item.objects.first() # get the first item
    self.assertEqual(new_item.text, 'A new list item')


"""
