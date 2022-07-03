from email.policy import default
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    follower = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='followings')

    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'follower': len(self.follower.all())
        }

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    description = models.CharField(max_length=200)
    likes = models.ManyToManyField(User, blank=True, default=0, related_name="posts_likes")
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post id - {self.id}, User - {self.user}, Description - {self.description}"

    def serialize(self):
        return {
            'id': self.id,
            'user': self.user.serialize(),
            'description': self.description,
            'likes': len(self.likes.all()),
            'date_posted': self.date_posted.strftime("%b %d %Y, %I:%M %p")
        }

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='commenters', on_delete=models.CASCADE)
    comment = models.CharField(max_length=200, blank=True)
    likes = models.ManyToManyField(User, blank=True, default=0, related_name="comment_likes")
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment id - {self.id} | Name - {self.user} | Comment - {self.comment}"

    def serialize(self):
        return {
            'id': self.id,
            'user': self.user.serialize(),
            'comment': self.comment,
            'likes': len(self.likes.all()),
            'date_posted': self.date_posted.strftime("%b %d %Y, %I:%M %p")
        }

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField(default='default.png', upload_to='profile_pictures')

    def __str__(self):
        return f"{self.user}"