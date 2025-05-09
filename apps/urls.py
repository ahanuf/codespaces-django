from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = "app"

urlpatterns = [
    path("", views.post_list, name="post_list"),
    path("post/new/", views.post_create, name="post_create"),
    path("post/<slug:slug>/", views.post_detail, name="post_detail"),
    path("post/<slug:slug>/edit/", views.post_edit, name="post_edit"),
    path("post/<slug:slug>/delete/", views.post_delete, name="post_delete"),
    path("category/<slug:slug>/", views.post_by_category, name="posts_by_category"),
    path("tag/<slug:tag_slug>/", views.post_by_tag, name="posts_by_tag"),
    path("search/", views.search_posts, name="search_posts"),
    # path("editor/", views.editor, name="editor"),
    path(
        "accounts/profile/<str:username>/", views.profile_detail, name="profile_detail"
    ),
    path(
        "accounts/login-redirect/",
        views.custom_login_redirect,
        name="custom_login_redirect",
    ),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
