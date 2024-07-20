from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django import forms
from .models import Item, CategoryModel, Question
import logging
from django.views.generic.edit import CreateView
from .forms import ItemPostForm
from django.core.files.storage import default_storage
from PIL import Image

logger = logging.getLogger(__name__)

class ItemPostView(CreateView):
    model = Item
    form_class = ItemPostForm
    template_name = 'marketplace/item_form.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        if form.cleaned_data['image']:
            # Process the image here
            # Example: Resizing the image
            try:
                with default_storage.open(form.instance.image.name, 'rb+') as img_file:
                    img = Image.open(img_file)
                    img = img.resize((300, 300))  # Example resize
                    img.save(img_file)
            except IOError:
                pass  # Handle error
        return response
    


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

def logout_view(request):
    logout(request)
    return redirect('marketplace:index')
        
def user_profile(request):
    user = request.user
    return render(request, 'marketplace/user_profile.html', {'user': user})

def index(request):
    newest_items = Item.objects.order_by('-id')[:5]
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = {
        "newest_items": newest_items,
        "latest_question_list": latest_question_list,
    }
    return render(request, "marketplace/index.html", context)

# Create
@login_required
def create_item(request):
    if request.method == 'POST':
        
        name = request.POST['name']
        description = request.POST['description']
        price = request.POST['price']
        quantity = request.POST.get('quantity', 1)  # Default to 1 if not provided
        image = request.FILES.get('image')

        logger.debug(f'Received files: {request.FILES}')

        # Convert category name to CategoryModel instance
        category_name = request.POST['category']
        category, created = CategoryModel.objects.get_or_create(name=category_name)

        # Use the currently logged-in user as the seller
        seller = request.user

        Item.objects.create(
            name=name, 
            description=description, 
            price=price, 
            quantity=quantity, 
            condition=request.POST['condition'],
            image=image,
            category=category,  # Now correctly assigns the CategoryModel instance
            seller=seller  # Assign the currently logged-in user as the seller
        )
        return redirect('marketplace:index')
    else:
        form = ItemPostForm()
        categories = CategoryModel.objects.all()  # Fetch all categories for selection
        return render(request, 'marketplace/item_form.html', {'form': form, 'categories': categories})

# Read
def item_list(request):
    items = Item.objects.all().order_by('-id')
    return render(request, 'marketplace/index.html', {'items': items})

def item_detail(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    return render(request, 'marketplace/item_detail.html', {'item': item})

def search_items(request):
    query = request.GET.get('query')
    items = Item.objects.filter(title__icontains=query)
    return render(request, 'marketplace/search_results.html', {'items': items})

@login_required
def update_item(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    if request.method == 'POST':
        item.image = request.FILES.get('image', item.image)
        item.name = request.POST['name']
        item.description = request.POST['description']
        item.condition = request.POST['condition']
        item.quantity = request.POST['quantity']
        item.price = request.POST['price']
        item.save()
        return redirect('marketplace:item_detail', item_id=item.id)
    else:
        return render(request, 'marketplace/item_form.html', {'item': item})

# Delete
@login_required
def delete_item(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    if request.method == 'POST':
        item.delete()
        return redirect('marketplace:item_list')
    else:
        return render(request, 'marketplace/item_confirm_delete.html', {'item': item})

# Similar CRUD operations for Question model
@login_required
def create_question(request):
    if request.method == 'POST':
        question_text = request.POST['question_text']
        Question.objects.create(question_text=question_text, asker=request.user)
        return redirect('marketplace:question_list')
    else:
        return render(request, 'marketplace/question_form.html', {})

def question_list(request):
    questions = Question.objects.all().order_by('-id')
    return render(request, 'marketplace/question_list.html', {'questions': questions})

def question_detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'marketplace/question_detail.html', {'question': question})

@login_required
def update_question(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == 'POST':
        question.question_text = request.POST['question_text']
        question.save()
        return redirect('marketplace:question_detail', question_id=question.id)
    else:
        return render(request, 'marketplace/question_form.html', {'question': question})

@login_required
def delete_question(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == 'POST':
        question.delete()
        return redirect('marketplace:question_list')
    else:
        return render(request, 'marketplace/question_confirm_delete.html', {'question': question})
