from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

# -----------------------------------------------------------------------------
# Review Model
# -----------------------------------------------------------------------------

class Review(models.Model):
    """
    Stores a single review entry, linking a Django user to a specific 
    AniList media ID with a numerical rating and optional text comment.
    """
    # Link to the User; if the user is deleted, their reviews are removed
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    
    # Stores the external ID from the AniList API
    media_id = models.PositiveIntegerField()
    
    # Numerical rating constrained between 1 and 10
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
    )
    
    # User's optional written feedback
    comment = models.TextField(blank=True, default='')
    
    # Timestamps for creation and latest modification
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Prevents a user from submitting multiple reviews for the same anime
        unique_together = ('user', 'media_id')
        # Default ordering to show the newest reviews first
        ordering = ['-created_at']

    def __str__(self):
        """String representation for debugging and admin display."""
        return f"Review by {self.user.username} | media_id={self.media_id} | rating={self.rating}"