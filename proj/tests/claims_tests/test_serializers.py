from claims.models import ClaimReport
from claims.serializers import ClaimReportSerializer

import pytest


@pytest.mark.django_db
def test_claim_report_serializer():
    claim_report = ClaimReport.objects.create(
        company_name="TestCompany",
        nip="123456789",
        name="TestName",
        surname="TestSurname",
        tel_number="123456789",
        email="test@example.com",
        claim_report_type=1,
        invoice_number="12345",
        product="TestProduct",
        quantity=10,
        claim_report_client_number="123",
        description="Test description",
        processed=False,
    )
    serializer = ClaimReportSerializer(claim_report)
    data = serializer.data
    assert data["company_name"] == "TestCompany"
    assert data["nip"] == "123456789"
    assert data["processed"] is False


def test_claim_report_serializer_validation():
    data = {
        "company_name": "TestCompany",
        "nip": "123456789",
        "name": "TestName",
        "surname": "TestSurname",
        "tel_number": "123456789",
        "email": "test@example.com",
        "claim_report_type": 1,
        "invoice_number": "12345",
        "product": "TestProduct",
        "quantity": 10,
        "claim_report_client_number": "123",
        "description": "Test description",
        "processed": False,
    }
    serializer = ClaimReportSerializer(data=data)
    assert serializer.is_valid()
