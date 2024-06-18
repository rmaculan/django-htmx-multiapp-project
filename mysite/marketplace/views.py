from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.template import loader

from .models import Item, Question

# Create your views here.
def index(request):
    newest_items = Item.objects.order_by('-id')[:5]
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = {
        "newest_items": newest_items,
        "latest_question_list": latest_question_list,
    }
    return render(request, "marketplace/index.html", context)

def item_list(request):
    return HttpResponse("item list." % Item.objects.all())

def item_detail(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    return render(request, "marketplace/items.html", {"item": item})

# def order_detail(request, order_id):
#     return HttpResponse(f"You're looking at order {order_id}.")

# def review_detail(request, review_id):
#     return HttpResponse(f"You're looking at review {review_id}.")

# def cart_detail(request, cart_id):
#     return HttpResponse(f"You're looking at cart {cart_id}.")

# def user_profile(request, user_id):
#     return HttpResponse(f"You're looking at user profile {user_id}.")

def question_detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "marketplace/question_detail.html", {"question": question})

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)

# def search(request):
#     return HttpResponse("You're searching for items.")

# def add_item(request):
#     return HttpResponse("You're adding an item to the marketplace.")

# def add_order(request):
#     return HttpResponse("You're adding an order to the marketplace.")

# def add_review(request):
#     return HttpResponse("You're adding a review to the marketplace.")

