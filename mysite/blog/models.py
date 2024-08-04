from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.text import slugify
from django.utils.translation import gettext as _
from django.conf import settings

class BlogCustomUser(AbstractUser):
    # Fields specific to blog app
    ...

    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_("The groups this user belongs to."),
        related_name="blog_customuser_groups",
        related_query_name="blog_customuser",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_("Specific permissions for this user."),
        related_name="blog_customuser_permissions",
        related_query_name="blog_customuser",
    )

class BloggerProfile(models.Model):
    user = models.OneToOneField(
        BlogCustomUser, 
        on_delete=models.CASCADE
        )
    profile_image = models.ImageField(
        upload_to='profiles/',
          blank=True, 
          null=True
          )
    is_seller = models.BooleanField(default=False)
    is_buyer = models.BooleanField(default=False)
    is_blog_author = models.BooleanField(default=False)

class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    status = models.CharField(
        max_length=10, 
        choices=STATUS_CHOICES, 
        default='draft'
        )
    publish_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    on_delete=models.CASCADE
        
    thumbnail = models.ImageField(
        upload_to='thumbnails/', 
        blank=True, 
        null=True
        )  # New field for thumbnail

    def save(
            self, 
            force_insert=False, 
            force_update=False, 
            using=None, 
            update_fields=None
            ):
        self.slug = slugify(self.title)
        if update_fields is not None and "title" in update_fields:
            update_fields = {"slug"}.union(update_fields)
        super().save(
            force_insert=force_insert, 
            force_update=force_update, 
            using=using, 
            update_fields=update_fields
            )

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(
        Post, 
        related_name='comments', 
        on_delete=models.CASCADE
        )
    author = models.ForeignKey(
        BlogCustomUser, 
        on_delete=models.CASCADE
        )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author} on {self.post.title}"
    
class Like(models.Model):
    post = models.ForeignKey(
        Post, 
        related_name='likes', 
        on_delete=models.CASCADE
        )
    user = models.ForeignKey(
        BlogCustomUser, 
        on_delete=models.CASCADE
        )

    class Meta:
        unique_together = ('post', 'user')  # Prevents duplicate likes from the same user

    def __str__(self):
        return f"Like by {self.user} on {self.post.title}"

    

