from rest_framework import serializers
from .models import Document, Folder

# FolderSerializer for Folder model
class FolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Folder
        fields = ['id', 'name', 'created_at']

from rest_framework import serializers
from .models import Document, Tag

# TagSerializer for Tag model
# This serializer is used to handle tags in DocumentSerializer
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']
        
# DocumentSerializer for Document model
# This serializer includes nested TagSerializer for tags
class DocumentSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, required=False)

    class Meta:
        model = Document
        fields = ['id', 'owner', 'folder', 'file', 'name', 'tags', 'uploaded_at']

    # Create method to handle tags
    # This method allows creating a document with associated tags
    def create(self, validated_data):
        tags_data = validated_data.pop('tags', [])
        document = Document.objects.create(**validated_data)
        for tag_data in tags_data:
            tag_obj, created = Tag.objects.get_or_create(name=tag_data['name'])
            document.tags.add(tag_obj)
        return document

    # Update method to handle tags
    # This method allows updating the document and its associated tags
    def update(self, instance, validated_data):
        tags_data = validated_data.pop('tags', [])
        instance = super().update(instance, validated_data)
        if tags_data:
            tag_objs = []
            for tag_data in tags_data:
                tag_obj, created = Tag.objects.get_or_create(name=tag_data['name'])
                tag_objs.append(tag_obj)
            instance.tags.set(tag_objs)
        return instance
    
    # Validate file type and size
    # This method ensures that only allowed file types are uploaded and checks the file size
    def validate_file(self, value):
        allowed_types = ('.pdf', '.docx', '.txt')
        if not value.name.lower().endswith(allowed_types):
            raise serializers.ValidationError("Only PDF, DOCX, or TXT files are allowed.")
        # Example file size limit (10MB):
        if value.size > 10 * 1024 * 1024:
            raise serializers.ValidationError("File too large (10MB max).")
        return value