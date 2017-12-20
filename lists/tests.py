from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from lists.views import home_page

# Create your tests here.
class HomePageTest(TestCase):

  def test_home_page_returns_correct_html(self):
    response = self.client.get('/') #pass the url we want to test
    self.assertTemplateUsed(response, 'home.html') # is the recieved html the home.html?

    # self.assertEqual(response, 'home.html') # purposefully failing test

  def test_can_save_a_POST_request(self):
    response = self.client.post('/', data={'item_text': 'A new list item'})
    self.assertIn('A new list item', response.content.decode())
    self.assertTemplateUsed(response, 'home.html')



"""
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
"""
