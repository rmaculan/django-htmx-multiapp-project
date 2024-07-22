from django.contrib import admin

# Register your models here.
from .models import Item, CategoryModel, Order, Review, UserProfile, Cart, Question

admin.site.register([Item, CategoryModel, Order, Review, UserProfile, Cart, Question])