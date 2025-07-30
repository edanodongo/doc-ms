from django.db import models
from django.conf import settings

# Model for folders
# This model is used to organize documents into folders
class Folder(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='folders')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# Model for tags
# This model is used to categorize documents with tags
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

# Model for documents
# This model represents a document uploaded by a user
class Document(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='documents')
    folder = models.ForeignKey('Folder', on_delete=models.SET_NULL, null=True, blank=True, related_name='documents')
    file = models.FileField(upload_to='documents/')
    name = models.CharField(max_length=255)
    tags = models.ManyToManyField(Tag, blank=True, related_name='documents')
    shared_with = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='shared_documents')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

summary = models.TextField(blank=True)


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

# Model for audit logs
# This model is used to track user actions on documents
class AuditLog(models.Model):
    ACTIONS = [
        ('upload', 'Upload'),
        ('delete', 'Delete'),
        ('view', 'View'),
        ('download', 'Download'),
        ('preview', 'Preview'),
        # etc.
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    action = models.CharField(max_length=20, choices=ACTIONS)
    timestamp = models.DateTimeField(auto_now_add=True)
