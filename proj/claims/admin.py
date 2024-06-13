from claims.models import ClaimReport

from django.contrib import admin


class ClaimReportAdmin(admin.ModelAdmin):
    list_display = (
        "id",
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
        "archive",
        "processed",
    )


admin.site.register(ClaimReport, ClaimReportAdmin)
