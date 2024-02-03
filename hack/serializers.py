from rest_framework import serializers
import random
from hack.models import Author, SocialContent, Instagram


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ("id", "unique_id", "username", "platform")


class SocialContentSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    
    class Meta:
        model = SocialContent
        fields = ("id", "author", "data")


class InstagramSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    context = serializers.SerializerMethodField()
    
    def get_author(self, obj):
        return {
            "id": random.randint(100,2000),
            "unique_id": f"{random.randint(23900,99999)}",
            "username": obj.username,
            "platform": "instagram"
        }
    
    
    def get_context(self, obj):
        return {
            "main_text": "@pizzahuteg",
            "tag_count": 1,
            "char_count": 11,
            "token_count": 1
        }
    
    class Meta:
        model = Instagram
        fields = ("id", "author", "context", "uploaded_at", "user_profile_url", "image_link")