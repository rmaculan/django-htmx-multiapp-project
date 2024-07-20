from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Post
from django.views.generic.edit import CreateView
from .forms import PostForm
from django.core.files.storage import default_storage
from PIL import Image

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

@login_required
def create_blog_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('index')  # Redirect to the list of blog posts after successful creation
    else:
        form = PostForm()
    return render(request, 'blog/create_blog_post.html', {'form': form})

def read_blog_posts(request):
    blog_posts = Post.objects.all().order_by('-publish_date')
    return render(request, 'blog/index.html', {'posts': blog_posts})

def read_blog_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(request, 'blog/post_detail.html', {'post': post})

# @login_required
# def update_blog_post(request, post_id):
#     post = get_object_or_404(Post, pk=post_id)
#     if request.method == 'POST':
#         post.thumbnail = request.FILES.get('thumbnail')
#         post.title = request.POST['title']
#         post.content = request.POST['content']
#         post.save()
#         return redirect('blog_post_detail', post_id=post.id)  # Redirect back to the post detail view
#     else:
#         return render(request, 'blog/post_edit.html', {'post': post})

# @login_required
# def delete_blog_post(request, post_id):
#     post = get_object_or_404(Post, pk=post_id)
#     if request.method == 'POST':
#         post.delete()
#         return redirect('blog_post_list')  # Redirect back to the list of blog posts
#     else:
#         return render(request, 'blog/post_confirm_delete.html', {'post': post})