from claims.views import (
    create_claim_report,
    download_claim_report_archive,
    handle_unprocessed_claim_reports,
)

from django.urls import path
from django.views.generic import TemplateView


urlpatterns = [
    path("create/", create_claim_report, name="create_claim_report"),
    path(
        "unprocessed_reports/",
        handle_unprocessed_claim_reports,
        name="handle_unprocessed_claim_reports",
    ),
    path(
        "download_archive/<int:pk>/",
        download_claim_report_archive,
        name="download_claim_report_archive",
    ),
    path(
        "success/",
        TemplateView.as_view(template_name="success_claim_report.html"),
        name="success_claim_report",
    ),
    path(
        "error/",
        TemplateView.as_view(template_name="rate_limit_exceeded.html"),
        name="error_claim_report",
    ),
]
