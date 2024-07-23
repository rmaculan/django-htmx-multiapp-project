from django.shortcuts import render
from blog.models import Post
from marketplace.models import Item

def landing_page(request):
    blog_posts = Post.objects.all()[:5]  # Fetch the latest 5 blog posts
    marketplace_items = Item.objects.all()[:5]  # Fetch the latest 5 marketplace items
    
    return render(request, 'landing_page.html', {
        'blog_posts': blog_posts,
        'marketplace_items': marketplace_items,
    })
