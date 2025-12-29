from django.db import models


class Document(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    parent = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='children'
    )
    order = models.IntegerField(default=0)  # For drag & drop reordering
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title


class AITwin(models.Model):
    """
    Stores the AI-optimized version of a document.
    This is structured markdown that LLMs can digest instantly.
    """
    document = models.OneToOneField(
        Document,
        on_delete=models.CASCADE,
        related_name='twin'
    )
    content_ai = models.TextField(blank=True)
    last_synced = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"AI Twin: {self.document.title}"
