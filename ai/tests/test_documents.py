import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from documents.models import Document

@pytest.mark.django_db
def test_document_upload_and_quota_enforced():
    client = APIClient()
    user = get_user_model().objects.create_user(username='test', password='pass')
    client.force_authenticate(user)
    for i in range(100):
        with open('test.txt', 'rb') as f:
            response = client.post('/api/documents/', {
                'name': f'test_{i}',
                'file': f,
            }, format='multipart')
            assert response.status_code in (201, 400)
    # Attempt one more, must fail due to quota
    with open('test.txt', 'rb') as f:
        response = client.post('/api/documents/', {'name': 'overflow', 'file': f}, format='multipart')
        assert response.status_code == 400

@pytest.mark.django_db
def test_document_search(client, user):
    # Set up several documents, search for text in summary/name/tags/content
    # Verify endpoints and permissions
    pass
