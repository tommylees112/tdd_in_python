from django.shortcuts import redirect, render
from django.http import HttpResponse
from lists.models import Item # our class of items!

# Create your views here.
def home_page(request):
  if request.method == 'POST':
    Item.objects.create(text=request.POST['item_text']) # create = new & save
    return redirect('/lists/the-only-list-in-the-world/') # redirect back to homepage
  return render(request, 'home.html') # REMEMBER: to pass the items in the render argument to html template

def view_list(request):
  items = Item.objects.all()
  return render(request, 'list.html', {'items': items})


