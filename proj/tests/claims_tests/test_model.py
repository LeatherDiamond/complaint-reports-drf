from claims.models import ClaimReport

from django.utils.translation import activate

import pytest


@pytest.mark.django_db
def test_create_claim_report():
    claim_report = ClaimReport.objects.create(
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
    assert claim_report.pk is not None
    assert claim_report.company_name == "TestCompany"
    assert claim_report.nip == 123456789
    assert claim_report.processed is False


@pytest.mark.django_db
def test_claim_report_string_representation():
    claim_report = ClaimReport.objects.create(
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
    assert str(claim_report) == f"ClaimReport {claim_report.pk}"


@pytest.mark.django_db
def test_create_claim_report_translation():
    activate("en")
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
    assert claim_report._meta.get_field("company_name").verbose_name == "Company Name"
    activate("pl")
    assert claim_report._meta.get_field("company_name").verbose_name == "Nazwa firmy"
