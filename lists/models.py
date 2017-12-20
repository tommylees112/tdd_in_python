from django.db import models

# Create your models here.
# when you change the models they then create migrations for you when you run
# $ python manage.py makemigrations

class List(models.Model):
  pass

class Item(models.Model): # inherit the SAVE feature from the Django helpers
  text = models.TextField(default="")
  list = models.ForeignKey(List, default=None)

