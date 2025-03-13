
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookmarks')
    url = models.URLField()
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=500, blank=True)
    image_url = models.URLField(blank=True, null=True)
    is_favorite = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tag, related_name='bookmarks', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('bookmark_detail', args=[self.id])
