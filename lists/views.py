from django.shortcuts import render, redirect
from lists.models import Item, List


def home_page(request):
    return render(request, 'home.html')


def new_list(request):
    list_ = List.objects.create()
    return redirect('/lists/{0}/'.format(list_.pk))


def view_list(request, list_id):
    list_ = List.objects.get(pk=list_id)
    return render(request, 'list.html', {'list': list_})


def add_item(request, list_id):
    list_ = List.objects.get(pk=list_id)
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect('/lists/{0}/'.format(list_.pk))
