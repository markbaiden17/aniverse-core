from django.contrib.auth.models import User
from django.db import models


class WatchlistEntry(models.Model):

    class Status(models.TextChoices):
        PLAN_TO_WATCH = 'plan_to_watch', 'Plan to Watch'
        WATCHING = 'watching', 'Watching'
        COMPLETED = 'completed', 'Completed'
        ON_HOLD = 'on_hold', 'On Hold'
        DROPPED = 'dropped', 'Dropped'

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='watchlist',
    )
    media_id = models.PositiveIntegerField()
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PLAN_TO_WATCH,
    )
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'media_id')
        ordering = ['-added_at']

    def __str__(self):
        return f"{self.user.username} | media_id={self.media_id} | {self.get_status_display()}"