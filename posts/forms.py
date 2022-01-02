
from django import forms
from posts.models import Comment, Post
from ckeditor.widgets import CKEditorWidget

class CreatePostForm(forms.ModelForm):
    body = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = Post
        fields = ['title', 'body', 'image']
        widgets = {
            'body': CKEditorWidget()
        }

class addCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
    