from rest_framework import serializers
from .models import Document, Folder

# Serializer for Document model
class FolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Folder
        fields = ['id', 'name', 'created_at']

class DocumentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Document
        fields = ['id', 'owner', 'folder', 'file', 'name', 'tags', 'uploaded_at']
        read_only_fields = ['owner', 'uploaded_at']
