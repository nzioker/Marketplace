from django.shortcuts import render, get_object_or_404,redirect
from .models import Item, Categories
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .forms import NewItemForm, EditItemForm


# Create your views here.
def items(request):
    query = request.GET.get('query', '')
    category_id = request.GET.get('category_id', 0)
    categories = Categories.objects.all()
    all_items = Item.objects.filter(is_sold=False)

    if category_id:
        items = all_items.filter(category_id=category_id)
    if query:
        items = all_items.filter(Q(name__icontains=query) | Q(description__icontains=query))

    return render(request, "item/items.html", {"all_items":all_items, "query":query, "categories":categories, "category_id":int(category_id)})


def details(request, pk):
    item = get_object_or_404(Item, pk=pk)
    same_category = Item.objects.filter(category=item.category, is_sold=False).exclude(
        pk=pk
    )[0:3]

    return render(
        request, "item/detail.html", {"item": item, "same_category": same_category}
    )

@login_required
def newItem(request):
    if request.method == 'POST':
        form = NewItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = request.user
            item.save()
            return redirect("item:details", pk=item.id)
    else:
        form = NewItemForm()

    return render(
        request, "item/form.html", {"form": form, "title":"New Item"}
    )

@login_required
def editItem(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)
    if request.method == 'POST':
        form = EditItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save
            return redirect("item:details", pk=item.id)
    else:
        form = EditItemForm(instance=item)

    return render(
        request, "item/form.html", {"form": form, "title":"Edit Item"}
    )

@login_required
def delete(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)
    item.delete()

    return redirect("dashboard:index")