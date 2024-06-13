from claims.views import (
    create_claim_report,
    download_claim_report_archive,
    handle_unprocessed_claim_reports,
)

from django.urls import resolve, reverse


def test_create_claim_report_url():
    url = reverse("create_claim_report")
    assert resolve(url).func == create_claim_report


def test_handle_unprocessed_claim_reports_url():
    url = reverse("handle_unprocessed_claim_reports")
    assert resolve(url).func == handle_unprocessed_claim_reports


def test_download_claim_report_archive_url():
    url = reverse("download_claim_report_archive", args=[1])
    assert resolve(url).func == download_claim_report_archive
