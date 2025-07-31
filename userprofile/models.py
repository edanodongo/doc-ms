from django.db import models
from django.contrib.auth.models import User

# Model for user profiles
# This model extends the User model to include additional fields
# such as maximum files allowed
# This is useful for managing user-specific limits or settings
# e.g., maximum number of files a user can upload
# This can be used to implement user quotas or limits (to store quota per user)
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    max_files = models.PositiveIntegerField(default=100)  # e.g., max 100 files

    def __str__(self):
        return self.user.username