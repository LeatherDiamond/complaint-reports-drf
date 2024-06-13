from django import forms
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .models import ClaimReport


class ClaimReportForm(forms.ModelForm):
    class Meta:
        model = ClaimReport
        fields = [
            "company_name",
            "nip",
            "name",
            "surname",
            "tel_number",
            "email",
            "claim_report_type",
            "invoice_number",
            "product",
            "quantity",
            "claim_report_client_number",
            "description",
        ]
        error_messages = {
            "name": {
                "invalid": _("Incorrect name"),
            },
            "surname": {
                "invalid": _("Incorrect last name"),
            },
            "tel_number": {
                "invalid": _("Incorrect phone number"),
            },
            "email": {
                "invalid": _("Incorrect email address"),
            },
            "claim_report_type": {
                "required": _("The type of complaint has not been selected"),
            },
            "invoice_number": {
                "invalid": _("Incorrect invoice number"),
            },
            "product": {
                "invalid": _("Incorrect product symbol"),
            },
            "quantity": {
                "invalid": _("Incorrect quantity"),
            },
        }
        widgets = {
            "company_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": _("Enter company name")},
            ),
            "nip": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": _("Enter Tax Identification Number"),
                },
            ),
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": _("Enter Name")},
            ),
            "surname": forms.TextInput(
                attrs={"class": "form-control", "placeholder": _("Enter Last Name")},
            ),
            "tel_number": forms.TextInput(
                attrs={"class": "form-control", "placeholder": _("Enter Phone Number")},
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": _("Enter E-mail Address"),
                },
            ),
            "claim_report_type": forms.Select(attrs={"class": "form-control"}),
            "invoice_number": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": _("Enter Invoice Number"),
                },
            ),
            "product": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": _("Enter Product Symbol"),
                },
            ),
            "quantity": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": _("Enter Quantity"),
                    "min": "0",
                },
            ),
            "claim_report_client_number": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": _("Enter Customer Complaint Number"),
                },
            ),
            "description": forms.Textarea(
                attrs={"class": "form-control", "placeholder": _("Enter Description")},
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""
        for field in self.fields.values():
            if field.required:
                field.label = format_html(f"{field.label} <span>*</span>")
