from django import forms
from .models import Post, Comment#, Editor
from taggit.forms import TagWidget
from django_ckeditor_5.widgets import CKEditor5Widget

# from tinymce.widgets import TinyMCE

class PostForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditor5Widget())

    class Meta:
        model = Post
        fields = ["title", "category", "tags", "content", "image", "published"]
        widgets = {
            "tags": TagWidget(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-control"}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }


# class EditorForm(forms.ModelForm):
#     content = forms.CharField(widget=TinyMCE(attrs={"cols": 80, "rows": 30}))
#     class Meta:
#         model = Editor
#         fields = '__all__'