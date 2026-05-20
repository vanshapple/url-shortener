from django.db import models


class URL(models.Model):
    """
    Stores a mapping between an original long URL
    and its generated short code.
    """

    original_url = models.URLField(
        max_length=2000,
        help_text="The original long URL submitted by the user."
    )
    short_code = models.CharField(
        max_length=15,
        unique=True,
        db_index=True,
        help_text="The unique short code generated for this URL."
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when this record was created."
    )
    click_count = models.PositiveIntegerField(
        default=0,
        help_text="Tracks how many times this short URL has been visited."
    )

    class Meta:
        ordering = ['-created_at']   # newest entries appear first
        verbose_name = "URL"
        verbose_name_plural = "URLs"

    def __str__(self):
        return f"{self.short_code} → {self.original_url}"