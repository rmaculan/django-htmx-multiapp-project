from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .models import Post, Like
from django.views.generic.edit import CreateView
from .forms import PostForm, LikeForm
from django.core.files.storage import default_storage
from PIL import Image
from .models import Post
import logging

logger = logging.getLogger(__name__)



class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'index.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        if form.cleaned_data['thumbnail']:
            # Process the thumbnail here
            # Example: Resizing the image
            try:
                with default_storage.open(
                    form.instance.thumbnail.name, 'rb+') as img_file:
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
            return redirect('blog:index')  # Assuming 'index' redirects to your homepage
    else:
        form = UserCreationForm()
    return render(request, 'blog/register.html', {'form': form})

def login_view(request):
        if request.method == 'POST':
            form = AuthenticationForm(data=request.POST)
            if form.is_valid():
                user = form.get_user()
                login(request, user)
                return redirect('blog:index')
        else:
            form = AuthenticationForm()
        return render(request, 'registration/login.html', {'form': form})

def logout_view(request):
    # Perform any necessary actions here, e.g., logging
    logger.info("Logout view accessed")
    
    # Use Django's built-in logout view
    logout(request)
    
    # Redirect to the home page or another appropriate page after logout
    return redirect('blog:index')

def profile(request):
    return render(request, 'blog/profile.html')

@login_required
def create_blog_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog:index')  # Redirect to the list of blog posts after successful creation
    else:
        form = PostForm()
    return render(request, 'blog/create_blog_post.html', {'form': form})

def read_blog_posts(request):
    blog_posts = Post.objects.all().order_by('-publish_date')
    username = request.session.get('username', 'Anonymous')  # Default to 'Anonymous' if not found
    print(f"Username from session: {username}")
    return render(
        request, 
        'blog/index.html', 
        {'posts': blog_posts,
         'username': username
         })

def read_my_posts(request):
    blog_posts = Post.objects.filter(author=request.user).order_by('-publish_date')
    return render(request, 'blog/my_posts.html', {'posts': blog_posts})

def read_blog_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(request, 'blog/post_detail.html', {'post': post})

def update_blog_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('blog:index')  # Redirect to the index page after successful update
    else:
        form = PostForm(instance=post)  # Ensure you're passing the `post` instance here

    return render(request, 'blog/update_blog_post.html', {'form': form, 'post_id': post_id})

def delete_blog_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    post.delete()
    return redirect('blog:index')

def search_posts(request):
    query = request.GET.get('query')
    blog_posts = Post.objects.filter(title__icontains=query)
    return render(request, 'blog/index.html', {'posts': blog_posts})

def search_posts_by_author(request):
    query = request.GET.get('query')
    blog_posts = Post.objects.filter(author__username__icontains=query)
    return render(request, 'blog/index.html', {'posts': blog_posts})

def like_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        if not request.user.is_authenticated:
            # Redirect to login page if user is not logged in
            return redirect('blog:login')
        elif not post.likes.filter(id=request.user.id).exists():
            # Increment likes count if the user hasn't liked the post yet
            post.likes_count += 1
            post.save()
            # Optionally, create a Like object to keep track of the relationship
            Like.objects.create(user=request.user, post=post)
        return redirect('blog:post_detail', post_id=post.id)
    else:
        # Handle GET requests appropriately
        pass
    return redirect('blog:index')












# region: Commented out code

## The following code is commented out because it is not needed for the tutorial

# def unlike_post(request, post_id):
#     post = get_object_or_404(Post, pk=post_id)
#     post.likes -= 1
#     post.save()
#     return redirect('blog:index')

# def comment_on_post(request, post_id):
#     post = get_object_or_404(Post, pk=post_id)
#     if request.method == 'POST':
#         content = request.POST.get('content')
#         post.comments.create(author=request.user, content=content)
#     return redirect('blog:post_detail', post_id=post_id)

# def update_comment(request, post_id, comment_id):
#     post = get_object_or_404(Post, pk=post_id)
#     comment = get_object_or_404(post.comments, pk=comment_id)
#     if request.method == 'POST':
#         content = request.POST.get('content')
#         comment.content = content
#         comment.save()
#     return redirect('blog:post_detail', post_id=post_id)

# def delete_comment(request, post_id, comment_id):
#     post = get_object_or_404(Post, pk=post_id)
#     comment = get_object_or_404(post.comments, pk=comment_id)
#     comment.delete()
#     return redirect('blog:post_detail', post_id=post_id)

# endregion


