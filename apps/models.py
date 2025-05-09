from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django_ckeditor_5.fields import CKEditor5Field
from taggit.managers import TaggableManager
from django.utils.text import slugify
import itertools

# from tinymce.models import HTMLField
# Create your models here.

# class Editor(models.Model):
#     content = HTMLField()  # TinyMCE editor field

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("apps:posts_by_category", args=[self.slug])


class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="posts"
    )
    content = CKEditor5Field('Text', config_name='extends')
    image = models.ImageField(upload_to="post_images/", blank=True, null=True)
    tags = TaggableManager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)[:50]  # optional limit
            slug = base_slug
            for i in itertools.count(1):
                if not Post.objects.filter(slug=slug).exists():
                    break
                slug = f"{base_slug}-{i}"
                if len(slug) > 60:  # avoid overly long slugs
                    slug = slug[:60]
            self.slug = slug
        super().save(*args, **kwargs)


    def get_absolute_url(self):
        return reverse("apps:post_detail", args=[self.slug])

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return f"Comment by {self.author} on {self.post}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)

    def __str__(self):
        return self.user.username
