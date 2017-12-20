from django.shortcuts import redirect, render
from django.http import HttpResponse
from lists.models import Item # our class of items!

# Create your views here.
def home_page(request):
  if request.method == 'POST':
    Item.objects.create(text=request.POST['item_text']) # create = new & save
    return redirect('/') # redirect back to homepage

  # write the HTML template page
  items = Item.objects.all()
  return render(request, 'home.html', {'items': items}) # REMEMBER: to pass the items in the render argument to view


