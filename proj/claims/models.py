from django.db import models
from django.utils.translation import gettext_lazy as _


class ClaimReport(models.Model):
    company_name = models.CharField(
        max_length=15,
        blank=True,
        verbose_name=_("Company Name"),
    )
    nip = models.CharField(
        max_length=13,
        blank=True,
        verbose_name=_("Tax Identification Number"),
    )
    name = models.CharField(
        max_length=15,
        verbose_name=_("Name"),
    )
    surname = models.CharField(
        max_length=35,
        verbose_name=_("Last Name"),
    )
    tel_number = models.CharField(
        max_length=30,
        verbose_name=_("Phone Number"),
    )
    email = models.EmailField(
        max_length=50,
        verbose_name=_("E-mail Address"),
    )
    TYPE_CHOICES = [
        (1, _("Qualitative")),
        (2, _("Quantitative")),
        (3, _("Financial")),
        (4, _("Other")),
    ]
    claim_report_type = models.PositiveSmallIntegerField(
        choices=TYPE_CHOICES,
        verbose_name=_("Type of Complaint"),
    )
    invoice_number = models.CharField(
        max_length=15,
        verbose_name=_("Invoice Number"),
    )
    product = models.CharField(
        max_length=15,
        verbose_name=_("Goods (symbol from the invoice)"),
    )
    quantity = models.DecimalField(
        decimal_places=2,
        max_digits=10,
        verbose_name=_("Quantity"),
    )
    claim_report_client_number = models.CharField(
        max_length=50,
        blank=True,
        verbose_name=_("Customer Complaint Number"),
    )
    description = models.TextField(
        max_length=2048,
        blank=True,
        verbose_name=_("Description"),
    )
    archive = models.FileField(
        upload_to="archives/",
        blank=True,
        null=True,
        verbose_name=_("zipped attachments"),
    )
    processed = models.BooleanField(
        default=False,
        verbose_name=_("Processed"),
    )

    def __str__(self):
        return f"ClaimReport {self.pk}"
