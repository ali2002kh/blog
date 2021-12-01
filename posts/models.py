from django.db import models

class Post(models.Model):
    title = models.CharField(max_length = 100)
    slug = models.SlugField()
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length = 100, null=True, blank=True)
    image = models.ImageField(default="default.jpg", blank=True)
    
    def __str__(self):
        return self.title
    
    def snippet(self):
        return self.body[:50] + ' ...'