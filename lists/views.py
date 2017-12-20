from django.shortcuts import redirect, render
from django.http import HttpResponse
from lists.models import Item, List # our class of items!

# Create your views here.
def home_page(request):
  return render(request, 'home.html') # REMEMBER: to pass the items in the render argument to html template

def view_list(request, list_id):
  list_ = List.objects.get(id=list_id) # getting the list object matching current list_id
  items = Item.objects.filter(list=list_) # filter for those with the current list_object
  return render(request, 'list.html', {'list': list_})

def new_list(request):
  list_ = List.objects.create()
  Item.objects.create(text=request.POST['item_text'], list=list_) # create = new & save
  return redirect(f'/lists/{list_.id}/')

def add_item(request, list_id):
  list_ = List.objects.get(id=list_id)
  Item.objects.create(text=request.POST['item_text'], list=list_)
  return redirect(f'/lists/{list_.id}/')

"""
in def home_page(request):
  # removed because home page no longer dealing with post requests
  if request.method == 'POST':
    Item.objects.create(text=request.POST['item_text']) # create = new & save
    return redirect('/lists/the-only-list-in-the-world/') # redirect back to homepage
"""
