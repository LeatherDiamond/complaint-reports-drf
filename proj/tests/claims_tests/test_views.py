from claims.models import ClaimReport

from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

import pytest

from rest_framework import status


@pytest.mark.django_db
@pytest.mark.usefixtures("clear_rate_limit_cache")
def test_create_claim_report(api_client):
    url = reverse("create_claim_report")
    data = {
        "company_name": "TestCompany",
        "nip": 123456789,
        "name": "TestName",
        "surname": "TestSurname",
        "tel_number": 123456789,
        "email": "test@example.com",
        "claim_report_type": 1,
        "invoice_number": "12345",
        "product": "TestProduct",
        "quantity": 10,
        "claim_report_client_number": "123",
        "description": "Test description",
    }
    response = api_client.post(url, data, format="multipart")
    assert response.status_code == status.HTTP_302_FOUND
    assert ClaimReport.objects.count() == 1


@pytest.mark.django_db
@pytest.mark.usefixtures("clear_rate_limit_cache")
def test_create_claim_report_with_files(api_client):
    url = reverse("create_claim_report")
    file = SimpleUploadedFile(
        "file1.pdf", b"file_content", content_type="application/pdf"
    )
    data = {
        "company_name": "TestCompany",
        "nip": 123456789,
        "name": "TestName",
        "surname": "TestSurname",
        "tel_number": 123456789,
        "email": "test@example.com",
        "claim_report_type": 1,
        "invoice_number": "12345",
        "product": "TestProduct",
        "quantity": 10,
        "claim_report_client_number": "123",
        "description": "Test description",
        "attachments": [file],
    }
    response = api_client.post(url, data, format="multipart")
    assert response.status_code == status.HTTP_302_FOUND
    assert ClaimReport.objects.count() == 1
    claim_report = ClaimReport.objects.first()
    assert claim_report.archive.name.endswith(".zip")


@pytest.mark.django_db
@pytest.mark.usefixtures("clear_rate_limit_cache")
def test_create_claim_report_with_invalid_file_type(api_client):
    url = reverse("create_claim_report")
    file = SimpleUploadedFile("file.txt", b"file_content", content_type="text/plain")
    data = {
        "company_name": "TestCompany",
        "nip": 123456789,
        "name": "TestName",
        "surname": "TestSurname",
        "tel_number": 123456789,
        "email": "test@example.com",
        "claim_report_type": 1,
        "invoice_number": "12345",
        "product": "TestProduct",
        "quantity": 10,
        "claim_report_client_number": "123",
        "description": "Test description",
        "attachments": [file],
    }
    response = api_client.post(url, data, format="multipart")
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
@pytest.mark.usefixtures("clear_rate_limit_cache")
def test_download_claim_report_archive(api_client, create_user, create_claim_report):
    user, token = create_user("testuser", "testpassword")
    claim_report = create_claim_report(
        company_name="TestCompany",
        nip=123456789,
        name="TestName",
        surname="TestSurname",
        tel_number=123456789,
        email="test@example.com",
        claim_report_type=1,
        invoice_number="12345",
        product="TestProduct",
        quantity=10,
        claim_report_client_number="123",
        description="Test description",
        processed=False,
    )
    url = reverse("download_claim_report_archive", args=[claim_report.pk])
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
@pytest.mark.usefixtures("clear_rate_limit_cache")
def test_handle_unprocessed_claim_reports(api_client, create_user, create_claim_report):
    user, token = create_user("testuser", "testpassword")
    claim_report = create_claim_report(
        company_name="TestCompany",
        nip=123456789,
        name="TestName",
        surname="TestSurname",
        tel_number=123456789,
        email="test@example.com",
        claim_report_type=1,
        invoice_number="12345",
        product="TestProduct",
        quantity=10,
        claim_report_client_number="123",
        description="Test description",
        processed=False,
    )
    url = reverse("handle_unprocessed_claim_reports")
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)

    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1

    response = api_client.put(url)
    assert response.status_code == status.HTTP_200_OK
    claim_report.refresh_from_db()
    assert claim_report.processed is True


@pytest.mark.django_db
@pytest.mark.usefixtures("clear_rate_limit_cache")
def test_create_claim_report_with_invalid_total_size(api_client):
    url = reverse("create_claim_report")
    large_file = SimpleUploadedFile(
        "large_file.pdf", b"0" * (25 * 1024 * 1024), content_type="application/pdf"
    )
    data = {
        "company_name": "TestCompany",
        "nip": 123456789,
        "name": "TestName",
        "surname": "TestSurname",
        "tel_number": 123456789,
        "email": "test@example.com",
        "claim_report_type": 1,
        "invoice_number": "12345",
        "product": "TestProduct",
        "quantity": 10,
        "claim_report_client_number": "123",
        "description": "Test description",
        "attachments": [large_file],
    }
    response = api_client.post(url, data, format="multipart")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert (
        "Całkowity rozmiar plików nie powinien przekraczać 24 MB."
        in response.content.decode()
    )


@pytest.mark.django_db
@pytest.mark.usefixtures("clear_rate_limit_cache")
def test_create_claim_report_with_too_many_files(api_client):
    url = reverse("create_claim_report")
    files = [
        SimpleUploadedFile(
            f"file{i}.pdf", b"file_content", content_type="application/pdf"
        )
        for i in range(11)
    ]
    data = {
        "company_name": "TestCompany",
        "nip": 123456789,
        "name": "TestName",
        "surname": "TestSurname",
        "tel_number": 123456789,
        "email": "test@example.com",
        "claim_report_type": 1,
        "invoice_number": "12345",
        "product": "TestProduct",
        "quantity": 10,
        "claim_report_client_number": "123",
        "description": "Test description",
        "attachments": files,
    }
    response = api_client.post(url, data, format="multipart")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Nie można przesłać więcej niż 10 plików." in response.content.decode()


@pytest.mark.django_db
@pytest.mark.usefixtures("clear_rate_limit_cache")
def test_download_claim_report_archive_already_processed(
    api_client, create_user, create_claim_report
):
    user, token = create_user("testuser", "testpassword")
    claim_report = create_claim_report(
        company_name="TestCompany",
        nip=123456789,
        name="TestName",
        surname="TestSurname",
        tel_number=123456789,
        email="test@example.com",
        claim_report_type=1,
        invoice_number="12345",
        product="TestProduct",
        quantity=10,
        claim_report_client_number="123",
        description="Test description",
        processed=True,
    )
    url = reverse("download_claim_report_archive", args=[claim_report.pk])
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "Nie znaleziono archiwum." in response.data["error"]


@pytest.mark.django_db
def test_download_claim_report_archive_non_existent(api_client, create_user):
    user, token = create_user("testuser", "testpassword")
    url = reverse("download_claim_report_archive", args=[999])
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "Nie znaleziono reklamacji." in response.data["error"]


@pytest.mark.django_db
def test_handle_unprocessed_claim_reports_empty(api_client, create_user):
    user, token = create_user("testuser", "testpassword")
    url = reverse("handle_unprocessed_claim_reports")
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)

    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 0

    response = api_client.put(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 0


@pytest.mark.django_db
@pytest.mark.usefixtures("clear_rate_limit_cache")
def test_download_claim_report_archive_unauthenticated(api_client, create_claim_report):
    claim_report = create_claim_report(
        company_name="TestCompany",
        nip=123456789,
        name="TestName",
        surname="TestSurname",
        tel_number=123456789,
        email="test@example.com",
        claim_report_type=1,
        invoice_number="12345",
        product="TestProduct",
        quantity=10,
        claim_report_client_number="123",
        description="Test description",
        processed=False,
    )
    url = reverse("download_claim_report_archive", args=[claim_report.pk])
    response = api_client.get(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_handle_unprocessed_claim_reports_unauthenticated(api_client):
    url = reverse("handle_unprocessed_claim_reports")
    response = api_client.get(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    response = api_client.put(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
@pytest.mark.usefixtures("clear_rate_limit_cache")
def test_create_claim_report_with_translation(api_client, activate_language):
    activate_language("en")
    url = reverse("create_claim_report")
    data = {
        "company_name": "TestCompany",
        "nip": 123456789,
        "name": "TestName",
        "surname": "TestSurname",
        "tel_number": 123456789,
        "email": "test@example.com",
        "claim_report_type": 1,
        "invoice_number": "12345",
        "product": "TestProduct",
        "quantity": 10,
        "claim_report_client_number": "123",
        "description": "Test description",
    }
    response = api_client.post(url, data, format="multipart")
    assert response.status_code == status.HTTP_302_FOUND
    assert ClaimReport.objects.count() == 1

    activate_language("pl")
    response = api_client.post(url, data, format="multipart")
    assert response.status_code == status.HTTP_302_FOUND
    assert ClaimReport.objects.count() == 2


@pytest.mark.django_db
@pytest.mark.usefixtures("clear_rate_limit_cache")
def test_create_claim_report_with_files_and_translation(api_client, activate_language):
    activate_language("en")
    url = reverse("create_claim_report")
    file = SimpleUploadedFile(
        "file1.pdf", b"file_content", content_type="application/pdf"
    )
    data = {
        "company_name": "TestCompany",
        "nip": 123456789,
        "name": "TestName",
        "surname": "TestSurname",
        "tel_number": 123456789,
        "email": "test@example.com",
        "claim_report_type": 1,
        "invoice_number": "12345",
        "product": "TestProduct",
        "quantity": 10,
        "claim_report_client_number": "123",
        "description": "Test description",
        "attachments": [file],
    }
    response = api_client.post(url, data, format="multipart")
    assert response.status_code == status.HTTP_302_FOUND
    assert ClaimReport.objects.count() == 1
    claim_report = ClaimReport.objects.first()
    assert claim_report.archive.name.endswith(".zip")

    activate_language("pl")
    response = api_client.post(url, data, format="multipart")
    assert response.status_code == status.HTTP_302_FOUND
    assert ClaimReport.objects.count() == 2
    claim_report = ClaimReport.objects.last()
    assert claim_report.archive.name.endswith(".zip")


@pytest.mark.django_db
@pytest.mark.usefixtures("clear_rate_limit_cache")
def test_create_claim_report_with_invalid_file_type_and_translation(
    api_client, activate_language
):
    activate_language("en")
    url = reverse("create_claim_report")
    file = SimpleUploadedFile("file.txt", b"file_content", content_type="text/plain")
    data = {
        "company_name": "TestCompany",
        "nip": 123456789,
        "name": "TestName",
        "surname": "TestSurname",
        "tel_number": 123456789,
        "email": "test@example.com",
        "claim_report_type": 1,
        "invoice_number": "12345",
        "product": "TestProduct",
        "quantity": 10,
        "claim_report_client_number": "123",
        "description": "Test description",
        "attachments": [file],
    }
    response = api_client.post(url, data, format="multipart")
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    activate_language("pl")
    response = api_client.post(url, data, format="multipart")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
