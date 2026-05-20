import uuid

from django.db.models import F
from django.shortcuts import get_object_or_404, redirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import URL
from .serializers import URLCreateSerializer, URLSerializer


def generate_short_code():
    """
    Generates a unique 8-character short code using UUID.
    Collision-safe: retries until a unique code is confirmed.
    """
    while True:
        code = uuid.uuid4().hex[:8]
        if not URL.objects.filter(short_code=code).exists():
            return code


class ShortenURLView(APIView):
    """
    POST /api/shorten/

    Accepts a long URL, generates a unique short code,
    saves the mapping, and returns the short URL.
    """

    def post(self, request):

        # Reject empty request body
        if not request.data:
            return Response(
                {
                    "success": False,
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "error": "Request body cannot be empty."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = URLCreateSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {
                    "success": False,
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "error": serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        original_url = serializer.validated_data['original_url']

        # Check if this URL was already shortened — avoid duplicates
        existing = URL.objects.filter(original_url=original_url).first()
        if existing:
            short_url = request.build_absolute_uri(f'/{existing.short_code}/')
            return Response(
                {
                    "success": True,
                    "status_code": status.HTTP_200_OK,
                    "message": "This URL has already been shortened.",
                    "id": existing.id,
                    "original_url": existing.original_url,
                    "short_code": existing.short_code,
                    "short_url": short_url,
                    "created_at": existing.created_at,
                },
                status=status.HTTP_200_OK
            )

        # Generate unique short code and save
        short_code = generate_short_code()

        url_obj = URL.objects.create(
            original_url=original_url,
            short_code=short_code
        )

        short_url = request.build_absolute_uri(f'/{url_obj.short_code}/')

        return Response(
            {
                "success": True,
                "status_code": status.HTTP_201_CREATED,
                "message": "Short URL created successfully.",
                "id": url_obj.id,
                "original_url": url_obj.original_url,
                "short_code": url_obj.short_code,
                "short_url": short_url,
                "created_at": url_obj.created_at,
            },
            status=status.HTTP_201_CREATED
        )


class URLRetrieveView(APIView):
    """
    GET /api/urls/<short_code>/

    Looks up a short code and returns full record details.
    Returns 404 if the short code does not exist.
    """

    def get(self, request, short_code):

        # Validate short_code length before hitting the database
        if len(short_code) > 15:
            return Response(
                {
                    "success": False,
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "error": "Invalid short code format."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        url_obj = get_object_or_404(URL, short_code=short_code)
        serializer = URLSerializer(url_obj)

        return Response(
            {
                "success": True,
                "status_code": status.HTTP_200_OK,
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )


class RedirectToOriginalView(APIView):
    """
    GET /<short_code>/

    Looks up the short code, increments click counter atomically,
    and redirects the user to the original URL.
    Returns 404 if short code does not exist.
    """

    def get(self, request, short_code):

        url_obj = get_object_or_404(URL, short_code=short_code)

        # Atomic increment — safe for concurrent requests
        URL.objects.filter(short_code=short_code).update(
            click_count=F('click_count') + 1
        )

        return redirect(url_obj.original_url)