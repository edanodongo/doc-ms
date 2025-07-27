from rest_framework import generics, permissions, viewsets
from .models import Document, Folder
from .serializers import DocumentSerializer, FolderSerializer

# FolderViewSet for managing user folders
class FolderViewSet(viewsets.ModelViewSet):
    serializer_class = FolderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Folder.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Document
from .serializers import DocumentSerializer
from ai.summary import summarize_text

from rest_framework import filters

# Extend DocumentViewSet to include summarization action
# DocumentViewSet for managing user documents with summarization
class DocumentViewSet(viewsets.ModelViewSet):
    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'tags']
    ordering_fields = ['uploaded_at', 'name']


    def get_queryset(self):
        return Document.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def summarize(self, request, pk=None):
        document = self.get_object()
        if document.owner != request.user:
            return Response({'error': 'Not allowed.'}, status=403)
        with document.file.open("r") as f:
            text = f.read()  # Ensure only use on supported (text-based) formats
        summary = summarize_text(text)
        document.summary = summary
        document.save()
        return Response({'summary': summary})
