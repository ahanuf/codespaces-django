from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.db import models
from .models import Post, Category, Comment, Profile
from .forms import PostForm, CommentForm

####
def categories(request):
    return {
        "categories": Category.objects.all()
    }
    


# Create your views here.
def post_list(request):
    posts = Post.objects.filter(published=True).order_by("-created_at")
    categories = Category.objects.all()
    context = {"posts": posts, "categories": categories}
    return render(request, "apps/post_list.html", context)


def post_by_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(category=category, published=True)
    context = {"posts": posts, "filter_title": f"category:{category.name}"}
    return render(request, "apps/post_list.html", context)


def post_by_tag(request, tag_slug):
    posts = Post.objects.filter(tags__slug=tag_slug, published=True)
    context = {"posts": posts, "filter_title": f"Tag {tag_slug}"}
    return render(request, "apps/post_list.html", context)


def search_posts(request):
    query = request.GET.get("q", "")
    posts = (
        Post.objects.filter(published=True)
        .filter(models.Q(title__icontains=query) | models.Q(content__icontains=query))
        .distinct()
    )
    context = {
        "posts": posts,
        "query": query,
        "filter_title": f'Search results for " {query} "',
    }
    return render(request, "apps/post_list.html", context)


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, published=True)
    comments = post.comments.filter(approved=True)  # type: ignore

    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect("account_login")
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            messages.success(request, "Your comment is awaiting moderation")
            return redirect(post.get_absolute_url())
    else:
        form = CommentForm()

    context = {"post": post, "comments": comments, "form": form}
    return render(request, "apps/post_detail.html", context)


@login_required
def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()
            messages.success(request, "Post created successfully.")
            return redirect(post.get_absolute_url())

    else:
        form = PostForm()

    return render(request, "apps/post_form.html", {"form": form, "title": "create post"})


@login_required
def post_edit(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.user != post.author:
        return HttpResponseForbidden("I don't think so")

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, " Post updated successfully.")
            return redirect(post.get_absolute_url())
    else:
        form = PostForm(instance=post)

    return render(request, "apps/post_form.html", {"form": form, "title": "Edit Post"})


@login_required
def post_delete(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.user != post.author:
        return HttpResponseForbidden("not allowed.")

    if request.method == "POST":
        post.delete()
        messages.success(request, "post deleted successfully.")
        return redirect("apps:post_list")
    return render(request, "apps/post_confirm_delete.html", {"post": post})


def profile_detail(request, username):
    # Get the user or return a 404 if not found
    user = get_object_or_404(User, username=username)
    # Get or create the profile for this user
    profile, created = Profile.objects.get_or_create(user=user)
    return render(request, "apps/profile_detail.html", {"profile": profile})


def custom_login_redirect(request):
    username = request.user.username
    return redirect(reverse("apps:profile_detail", kwargs={"username": username}))
