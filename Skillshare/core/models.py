from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField()
    skills_i_have = models.TextField(blank=True, null=True)
    skills_i_need = models.TextField(blank=True, null=True)
    location = models.TextField(blank=True,null=True)
    social_account_link = models.TextField(default='Not Provided', blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_images/', default='default.jpg')
    blank = True,
    null = True

    def __str__(self):
        return self.user.username
    

# the messages one.
class Chat(models.Model):
    sender = models.ForeignKey(User, related_name=('send_messages'), on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name=('received_messages'), on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default= False)

    def __str__(self):
        return f"From {self.sender} to {self.receiver}: {self.content[:20]}"
    
class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')  # prevent duplicates

    def __str__(self):
        return f"{self.follower} follows {self.following}"