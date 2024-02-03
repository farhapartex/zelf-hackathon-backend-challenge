from django.contrib import admin
from hack.models import SocialContent, Author
# Register your models here.

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("id", "unique_id", "username", "name", "platform")

@admin.register(SocialContent)
class SocialContentAdmin(admin.ModelAdmin):
    list_display = ("id", "unique_id", "platform", "likes", "comments", "comments", "media_type", "author", "created_at", "main_text")
