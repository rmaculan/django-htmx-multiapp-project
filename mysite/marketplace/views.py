from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate

from .models import Item, Question

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # Redirect to a success page.
            return redirect('marketplace:index')  # Assuming 'index' redirects to your homepage
    else:
        form = UserCreationForm()
    return render(request, 'marketplace/register.html', {'form': form})

def login_view(request):
        if request.method == 'POST':
            form = AuthenticationForm(data=request.POST)
            if form.is_valid():
                user = form.get_user()
                login(request, user)
                return redirect('marketplace:index')
        else:
            form = AuthenticationForm()
        return render(request, 'marketplace/login.html', {'form': form})

def custom_login_view(request):
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                # Return an error response if authentication failed
                return HttpResponse("Invalid login credentials.")
        else:
            # Render the login form
            return render(request, 'login.html')

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

