from django.db import models

from apps.core.models import TimeStampedModel


class UserBot(TimeStampedModel):
    """
    UserBot model
    """
    chat_id = models.CharField(max_length=255, unique=True)
    username = models.CharField(max_length=255, blank=True, null=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    language_code = models.CharField(max_length=255, blank=True, null=True)

    # Permissions
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        if self.username:
            return self.username
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "UserBot"
        verbose_name_plural = "UserBots"


class Note(TimeStampedModel):
    """
    Note model for UserBot
    """
    user_bot = models.ForeignKey(UserBot, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    text = models.TextField()

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "Note"
        verbose_name_plural = "Notes"
