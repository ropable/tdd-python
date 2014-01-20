from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from lists.models import Item, List


def home_page(request):
    return render(request, 'home.html')


def new_list(request):
    list_ = List.objects.create()
    try:
        Item.objects.create(text=request.POST['item_text'], list=list_)
    except ValidationError:
        error_text = "You can't have an empty list item"
        return render(request, 'home.html', {'error': error_text})
    return redirect('/lists/{0}/'.format(list_.pk))


def view_list(request, list_id):
    list_ = List.objects.get(pk=list_id)
    if request.method == 'POST':
        Item.objects.create(text=request.POST['item_text'], list=list_)
        return redirect('/lists/{0}/'.format(list_.pk))
    return render(request, 'list.html', {'list': list_})
