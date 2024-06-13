from claims.forms import ClaimReportForm

from django.utils.translation import activate

import pytest


@pytest.mark.django_db
def test_claim_report_form_translation():
    activate("en")
    form = ClaimReportForm()
    assert form.fields["company_name"].label == "Company Name"
    assert form.fields["nip"].label == "Tax Identification Number"

    activate("pl")
    form = ClaimReportForm()
    assert form.fields["company_name"].label == "Nazwa firmy"
    assert form.fields["nip"].label == "NIP"


@pytest.mark.django_db
def test_claim_report_form_custom_validation_messages_translation():
    form_data = {
        "company_name": "",
        "nip": "",
        "name": "",
        "surname": "",
        "tel_number": 123123,
        "email": "",
        "claim_report_type": 1,
        "invoice_number": "",
        "product": "",
        "quantity": "invalid-quantity",
        "claim_report_client_number": "",
        "description": "",
    }

    activate("en")
    form = ClaimReportForm(data=form_data)
    assert not form.is_valid()
    assert form.errors["name"] == ["This field is required."]
    assert form.errors["quantity"] == ["Incorrect quantity"]

    activate("pl")
    form = ClaimReportForm(data=form_data)
    assert not form.is_valid()
    assert form.errors["name"] == ["To pole jest wymagane."]
    assert form.errors["quantity"] == ["Niepoprawna ilość"]
