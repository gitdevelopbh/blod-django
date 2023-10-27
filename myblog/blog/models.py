from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class BlogPost(models.Model):
    title = models.CharField(max_length=100)
    published_date = models.DateTimeField(default=timezone.now)
    main_image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    content = models.TextField()
    is_published = models.BooleanField(default=False)

    # Foreign key to User model
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_posts')

class ContentImage(models.Model):
    filename = models.CharField(max_length=200)
    blog = models.ForeignKey('BlogPost', on_delete=models.CASCADE, related_name='content_images')

    def __str__(self):
        return f'ContentImage {self.id}'


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.post.title}'