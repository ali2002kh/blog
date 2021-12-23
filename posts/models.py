from django.contrib.auth.models import User
from django.db import models
from ckeditor.fields import RichTextField

class Post(models.Model):
    author = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    visited = models.IntegerField(default=0)
    promote = models.BooleanField(default=False)
    body = RichTextField()
    date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100)
    image = models.ImageField(default="default.jpg", blank=True)
    
    def __str__(self):
        return self.title
    
    def snippet(self):
        return self.body[:50] + ' ...'
    
class Comment(models.Model):
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='Parent')
    child = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='Child')
    body = models.TextField()
    author = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, default=None, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.author.username}: {self.body}"