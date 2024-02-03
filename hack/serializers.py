from rest_framework import serializers
from hack.models import Author, SocialContent


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ("id", "unique_id", "username")


class SocialContentSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    
    class Meta:
        model = SocialContent
        fields = ("id", "author", "data")
