from rest_framework import generics, permissions, viewsets
from .models import Document, Folder
from .serializers import DocumentSerializer, FolderSerializer

# FolderViewSet for managing user folders
class FolderViewSet(viewsets.ModelViewSet):
    serializer_class = FolderSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Override get_queryset to filter folders by owner
    # This method ensures that users can only access their own folders
    def get_queryset(self):
        return Folder.objects.filter(owner=self.request.user)

    # Perform create method to set the owner automatically
    # This method ensures that the folder is associated with the authenticated user
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Document
from .serializers import DocumentSerializer
from ai.summary import summarize_text

from rest_framework import filters
import PyPDF2
from docx import Document as DocxDocument

# Extend DocumentViewSet to include summarization action
# DocumentViewSet for managing user documents with summarization
class DocumentViewSet(viewsets.ModelViewSet):
    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'tags']
    ordering_fields = ['uploaded_at', 'name']

    # Override get_queryset to filter documents by owner
    # This method ensures that users can only access their own documents
    def get_queryset(self):
        return Document.objects.filter(owner=self.request.user)

    # Perform create method to set the owner automatically
    # This method ensures that the document is associated with the authenticated user
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        
    # Action to summarize document content
    # This action generates a summary of the document content using AI
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
    
    # Action to preview document content
    # This action provides a preview of the document content based on its type
    @action(detail=True, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def preview(self, request, pk=None):
        document = self.get_object()
        file = document.file
        preview_text = ""

        if file.name.endswith('.pdf'):
            file.open('rb')
            reader = PyPDF2.PdfReader(file)
            text_parts = []
            for page in reader.pages[:2]:  # Preview first 2 pages
                text_parts.append(page.extract_text() or '')
            preview_text = "\n".join(text_parts)
            file.close()
        elif file.name.endswith('.docx'):
            file.open('rb')
            doc = DocxDocument(file)
            text_parts = [p.text for p in doc.paragraphs[:10]]  # First 10 paragraphs
            preview_text = "\n".join(text_parts)
            file.close()
        elif file.name.endswith('.txt'):
            file.open('r')
            preview_text = file.read(500)  # First 500 characters
            file.close()
        else:
            preview_text = "Preview not available for this format."

        return Response({'preview': preview_text[:1000]})
    
    # Override perform_create to check user upload quota
    # This method ensures that users do not exceed their upload quota
    # This is useful for managing user-specific limits or settings
    # e.g., maximum number of files a user can upload
    def perform_create(self, serializer):
        user = self.request.user
        profile = getattr(user, 'userprofile', None)
        if profile:
            if Document.objects.filter(owner=user).count() >= profile.max_files:
                raise serializers.ValidationError("Upload quota exceeded.")
        else:
            if Document.objects.filter(owner=user).count() >= 100:
                raise serializers.ValidationError("Upload quota exceeded.")
        serializer.save(owner=user)





            
    # Example function to log user actions
    # This function can be used in views to log actions like upload, delete, view, etc. 
    def log_action(user, document, action):
        from .models import AuditLog
        AuditLog.objects.create(user=user, document=document, action=action)

    # Example usage in every relevant view:
    log_action(request.user, document, 'preview')

    # DocumentViewSet for managing user documents with sharing functionality
    # This viewset allows users to perform CRUD operations on their documents
    def get_queryset(self):
        user = self.request.user
        return Document.objects.filter(models.Q(owner=user) | models.Q(shared_with=user)).distinct()

    # Override check_object_permissions to ensure users can only access their own documents or shared documents
    # This method checks if the user is the owner or has been granted access to the document
    # This is useful for ensuring that users cannot access documents they do not own or have not been shared with
    def check_object_permissions(self, request, obj):
        if obj.owner != request.user and request.user not in obj.shared_with.all():
            self.permission_denied(request, message="You do not have access to this document.")

    # Action to share document with other users
    # This action allows the owner to share the document with other users
    # This is useful for collaborative work
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def share(self, request, pk=None):
        document = self.get_object()
        if document.owner != request.user:
            return Response({'error': 'Only owner can share.'}, status=403)
        user_ids = request.data.get('user_ids', [])
        document.shared_with.set(user_ids)
        return Response({'detail': 'Shared.'})


    # Action to search documents
    # This action allows users to search for documents by name, tags, or content
    # Useful for quickly finding documents
    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.query_params.get('q')
        if query:
            queryset = queryset.annotate(
                rank=SearchRank(SearchVector('name', 'tags__name', 'content_search'), SearchQuery(query))
            ).filter(rank__gte=0.1).order_by('-rank')
        return queryset
    
    
from ai.tasks import generate_summary

@action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
def summarize(self, request, pk=None):
    document = self.get_object()
    generate_summary.delay(document.id)
    return Response({'detail': 'Summary is being generated and will be available soon.'})
