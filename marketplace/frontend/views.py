from django.shortcuts import render,redirect
from item.models import Categories, Item
from .forms import SignupForm


# Create your views here.
def index(request):
    items = Item.objects.filter(is_sold=False)
    categories = Categories.objects.all()
    return render(
        request, "frontend/index.html", {"categories": categories, "items": items}
    )


def contact(request):
    return render(request, "frontend/contact.html")


def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)

        if form.is_valid:
            form.save()
            return redirect('/login/')
    form = SignupForm()
    return render(request, "frontend/signup.html", {"form": form})
