from django.contrib.auth.models import User
from django.db import models
from ckeditor.fields import RichTextField
from django.urls import reverse

class Post(models.Model):
    author = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    visited = models.IntegerField(default=0)
    promote = models.BooleanField(default=False)
    body = RichTextField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100)
    image = models.ImageField(default=False)
    noc = models.IntegerField(default=0)
    
    def __str__(self):
        return self.title
    
    def snippet(self):
        return self.body[:140] + ' ...'
    
    def get_absolute_url(self):
        return reverse('management:index')
    
class Comment(models.Model):
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='subcomments')
    body = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    date = models.DateTimeField(auto_now_add=True)
    is_confirmed = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.author.username}: {self.body}"