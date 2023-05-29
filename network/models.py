from django.contrib.auth.models import AbstractUser
from django.db import models
import os

class User(AbstractUser):
    profile_picture = models.ImageField(upload_to='network/static/network', blank=True, null=True, default=None)
    bio = models.CharField(max_length=255, default=None, blank=True, null=True)
    handle = models.CharField(max_length=50, blank=True, null=True)
    
    @property
    def total_followers(self):
        return self.followers.filter(is_followed=True).count()

    @property
    def total_following(self):
        return self.following.filter(is_followed=True).count()

    @property
    def pic_filename(self):
        return os.path.basename(self.profile_picture.name)
    
    def __str__(self):
        return f"{self.handle}"
    

class Post(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')

    class Meta:
        ordering = ['-created_at']

    @property
    def total_likes(self):
        return self.likes.filter(is_like=True).count()
    
    @property
    def is_liked_by_user_ids(self):
        return self.likes.filter(is_like=True).values_list('user',flat=True)
    

class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='liked_posts')
    is_like = models.BooleanField(default=True)

    class Meta:
        unique_together = ('post', 'user')

    def __str__(self):
        return f"{self.user.handle} likes Post#{self.post.id} {self.is_like}"


class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    is_followed = models.BooleanField(default=True)

    class Meta:
        unique_together = ('follower', 'followed')

    def __str__(self):
        return f"{self.follower} is following {self.followed} = {self.is_followed}"