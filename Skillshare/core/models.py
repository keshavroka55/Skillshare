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

    def average_rating(self):
        ratings = self.ratings_received.all()
        if ratings.exists():
            return round(sum(r.rating for r in ratings) / ratings.count(), 2)
        return 0

class Rating(models.Model):
    rated_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='ratings_received')
    rated_by = models.ForeignKey(User, on_delete=models.CASCADE)  # The one giving rating
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    feedback = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('rated_user', 'rated_by')  # Prevent duplicate ratings

    def __str__(self):
        return f'{self.rated_by} rated {self.rated_user.user.username} {self.rating}/5'
    

# the messages one.
class Chat(models.Model):
    sender = models.ForeignKey(User, related_name=('send_messages'), on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name=('received_messages'), on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default= False)

    def __str__(self):
        return f"From {self.sender} to {self.receiver}: {self.content[:20]}"
    