from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Post

@login_required
def create_blog_post(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        Post.objects.create(title=title, content=content, author=request.user)
        return redirect('blog_post_list')  # Assuming you have a URL pattern named 'blog_post_list'

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