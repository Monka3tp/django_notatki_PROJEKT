from django import forms
from django.forms.utils import ErrorList

from notatki.models import Comment, Post


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('priority', 'title', 'slug', 'body',)
