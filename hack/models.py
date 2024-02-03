from django.db import models

class SocialContent(models.Model):
    unique_id = models.CharField(max_length=255, unique=True)
    main_text = models.TextField()
    data = models.JSONField()
    author = models.ForeignKey("Author", on_delete=models.DO_NOTHING)
    platform = models.CharField(max_length=255, blank=True, null=True)
    media_type = models.CharField(max_length=100, blank=True, null=True)
    likes = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)
    created_at = models.DateTimeField(blank=True, null=True)


class Author(models.Model):
    unique_id = models.CharField(max_length=255, unique=True)
    username = models.CharField(max_length=255, blank=True, null=True)
    unique_uuid = models.CharField(max_length=255, unique=True, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    platform = models.CharField(max_length=255, blank=True, null=True)
    data = models.JSONField(blank=True, null=True)
    is_fetched = models.BooleanField(default=False)

    def __str__(self):
        return self.username
