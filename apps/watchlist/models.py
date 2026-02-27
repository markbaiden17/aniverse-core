from django.contrib.auth.models import User
from django.db import models

# -----------------------------------------------------------------------------
# Watchlist Entry Model
# -----------------------------------------------------------------------------

class WatchlistEntry(models.Model):
    """
    Represents a specific anime title added to a user's personal list.
    Tracks the user's progress or intent via a status state machine.
    """

    class Status(models.TextChoices):
        """
        Enumerated choices for tracking the viewing state of a media item.
        Used to provide a dropdown list in the admin and validation in the API.
        """
        PLAN_TO_WATCH = 'plan_to_watch', 'Plan to Watch'
        WATCHING = 'watching', 'Watching'
        COMPLETED = 'completed', 'Completed'
        ON_HOLD = 'on_hold', 'On Hold'
        DROPPED = 'dropped', 'Dropped'

    # The user who owns this list entry
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='watchlist',
    )
    
    # The external reference ID for the anime from the AniList API
    media_id = models.PositiveIntegerField()
    
    # The current progress status of the anime for this user
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PLAN_TO_WATCH,
    )
    
    # Audit timestamps for tracking when items were added or modified
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Ensures a user cannot have the same anime in their list more than once
        unique_together = ('user', 'media_id')
        # Defaults to showing the most recently added items first
        ordering = ['-added_at']

    def __str__(self):
        """Readable string representation for logs and the admin panel."""
        return f"{self.user.username} | media_id={self.media_id} | {self.get_status_display()}"