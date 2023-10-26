from django.contrib import admin

# Register your models here.

from .models import Categories, Item

admin.site.register(Categories)
admin.site.register(Item)
