import os
from zipfile import ZipFile

from django.conf import settings
from django.core.files.base import ContentFile
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils.translation import gettext as _

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .forms import ClaimReportForm
from .models import ClaimReport
from .serializers import ClaimReportSerializer


@api_view(["GET", "POST"])
def create_claim_report(request):
    if request.method == "GET":
        form = ClaimReportForm()
        return render(
            request, "claim_report_form.html", {"form": form}, status=status.HTTP_200_OK
        )

    files = request.FILES.getlist("attachments")

    if len(files) > 10:
        form = ClaimReportForm(request.POST)
        return render(
            request,
            "claim_report_form.html",
            {"form": form, "error": _("You cannot upload more than 10 files.")},
            status=status.HTTP_400_BAD_REQUEST,
        )

    total_size = sum(file.size for file in files)
    if total_size > 24 * 1024 * 1024:
        form = ClaimReportForm(request.POST)
        return render(
            request,
            "claim_report_form.html",
            {
                "form": form,
                "error": _("Total file size should not exceed 24 MB."),
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    allowed_extensions = ["png", "jpg", "pdf"]
    for file in files:
        extension = file.name.split(".")[-1].lower()
        if extension not in allowed_extensions:
            form = ClaimReportForm(request.POST)
            return render(
                request,
                "claim_report_form.html",
                {
                    "form": form,
                    "error": _(
                        "File {file_name} has an invalid extension. Valid extensions are: {extensions}."
                    ).format(
                        file_name=file.name, extensions=", ".join(allowed_extensions)
                    ),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

    serializer = ClaimReportSerializer(data=request.data)
    if serializer.is_valid():
        claim_report = serializer.save()

        if files:
            zip_filename = f"claim_report_{claim_report.id}.zip"
            zip_file_path = os.path.join(settings.MEDIA_ROOT, "archives", zip_filename)
            os.makedirs(os.path.dirname(zip_file_path), exist_ok=True)

            upload_dir = os.path.join(settings.MEDIA_ROOT, "uploads")
            os.makedirs(upload_dir, exist_ok=True)

            with ZipFile(zip_file_path, "w") as zip_file:
                for file in files:
                    file_path = os.path.join(upload_dir, file.name)
                    with open(file_path, "wb") as f:
                        for chunk in file.chunks():
                            f.write(chunk)
                    zip_file.write(file_path, file.name)
                    os.remove(file_path)

            with open(zip_file_path, "rb") as f:
                claim_report.archive.save(
                    zip_filename, ContentFile(f.read()), save=True
                )
            os.remove(zip_file_path)

        return redirect("success_claim_report")

    form = ClaimReportForm(request.POST)
    return render(
        request,
        "claim_report_form.html",
        {"form": form, "errors": serializer.errors},
        status=status.HTTP_400_BAD_REQUEST,
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def download_claim_report_archive(request, pk):
    try:
        claim_report = ClaimReport.objects.get(pk=pk)
    except ClaimReport.DoesNotExist:
        return Response(
            {"error": "Nie znaleziono reklamacji."}, status=status.HTTP_404_NOT_FOUND
        )

    if not claim_report.archive:
        return Response(
            {"error": "Nie znaleziono archiwum."}, status=status.HTTP_404_NOT_FOUND
        )

    archive_path = claim_report.archive.path
    if not os.path.exists(archive_path):
        return Response(
            {"error": "Nie znaleziono pliku archiwum."},
            status=status.HTTP_404_NOT_FOUND,
        )

    with open(archive_path, "rb") as f:
        response = HttpResponse(f.read(), content_type="application/zip")
        response[
            "Content-Disposition"
        ] = f'attachment; filename="{os.path.basename(archive_path)}"'
        return response


@api_view(["GET", "PUT"])
@permission_classes([IsAuthenticated])
def handle_unprocessed_claim_reports(request):
    if request.method == "GET":
        unprocessed_claim_reports = ClaimReport.objects.filter(processed=False)
        serializer = ClaimReportSerializer(unprocessed_claim_reports, many=True)
        return Response(serializer.data)

    elif request.method == "PUT":
        unprocessed_claim_reports = ClaimReport.objects.filter(processed=False)
        for claim_report in unprocessed_claim_reports:
            claim_report.processed = True
            claim_report.save()

        serializer = ClaimReportSerializer(unprocessed_claim_reports, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
