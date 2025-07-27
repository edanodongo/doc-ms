from django.db import models
from django.conf import settings

# Model for user folders and documents
class Folder(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='folders')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# Model for documents
class Document(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='documents')
    folder = models.ForeignKey(Folder, on_delete=models.SET_NULL, null=True, blank=True, related_name='documents')
    file = models.FileField(upload_to='documents/')
    name = models.CharField(max_length=255)
    tags = models.CharField(max_length=255, blank=True)  # Comma-separated or use ManyToMany to a Tag model
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


