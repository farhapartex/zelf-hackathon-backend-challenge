from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg, Count, Min, Sum
from django.db.models.functions import Length
from rest_framework import generics, views, response
from hack import models
from hack import serializers, filters
# Create your views here.

class SocialContentListAPIView(generics.ListAPIView):
    queryset = models.SocialContent.objects.select_related("author").all()
    serializer_class = serializers.SocialContentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = filters.ContentFilter


class SocialContentStatisticsAPIView(views.APIView):
    
    def get(self, request, *args, **kwargs):
        create_start = request.query_params.get("create_start")
        create_end = request.query_params.get("create_end")
        media_type = request.query_params.get("media_type")
        author_platform = request.query_params.get("author_platform")
        content_char_count = request.query_params.get("content_char_count")
        hash_tag = request.query_params.get("hash_tag")
        
        if not create_start and create_end:
            create_start = models.SocialContent.objects.earliest("created_at").created_at
            print(create_start)
        elif create_start and not create_end:
            create_end = models.SocialContent.objects.latest("created_at").created_at
        elif not create_start and not create_end:
            create_start = models.SocialContent.objects.earliest("created_at").created_at
            create_end = models.SocialContent.objects.latest("created_at").created_at
        
        queryset = models.SocialContent.objects.select_related("author").filter(created_at__range=(create_start, create_end))
        
        if media_type:
            queryset = queryset.filter(media_type=media_type)
        
        if author_platform:
            queryset = queryset.filter(author__platform=author_platform)
        
        if content_char_count:
            queryset = queryset.annotate(main_text_len=Length('main_text')).filter(main_text_len__lte=content_char_count)
        
        total_content = queryset.count()
        total_likes = queryset.aggregate(total_likes=Sum("likes"))["total_likes"]
        total_comments = queryset.aggregate(total_comments=Sum("comments"))["total_comments"]
        total_views = queryset.aggregate(total_views=Sum("views"))["total_views"]
        distinct_authors = queryset.values("author").distinct().count()
        
        avg_likes_per_content = queryset.aggregate(avg_likes_per_content=Avg("likes"))["avg_likes_per_content"]
        avg_views_per_content = queryset.aggregate(avg_views_per_content=Avg("views"))["avg_views_per_content"]
        avg_comments_per_content = queryset.aggregate(avg_comments_per_content=Avg("comments"))["avg_comments_per_content"]
        
        mentioned_username = [f"@{username}" for username in list(models.Author.objects.values_list("username", flat=True))]
        
        mention_in_text_by_author = queryset.filter(
            main_text__icontains=mentioned_username
        ).count() # not sure why not working properly
        
        
        resp_data = {
            "total_content": total_content,
            "total_likes": total_likes if total_likes else 0,
            "total_comments": total_comments if total_comments else 0,
            "total_views": total_views if total_views else 0,
            "avg_likes_per_content": avg_likes_per_content if avg_likes_per_content else 0,
            "avg_views_per_content": avg_views_per_content if avg_views_per_content else 0,
            "avg_comments_per_content": avg_comments_per_content if avg_comments_per_content else 0,
            "distinct_total_authors": distinct_authors,
            "mention_in_text_by_author": mention_in_text_by_author if mention_in_text_by_author else 0,
        }
        
        if hash_tag:
            hash_tag_count = queryset.filter(main_text__icontains=f"#{hash_tag}").count() if hash_tag else 0
            resp_data["hash_tag_count"] = hash_tag_count if hash_tag_count else 0,
        return response.Response(resp_data)


class InstagramListAPIView(generics.ListAPIView):
    queryset = models.Instagram.objects.all()
    serializer_class = serializers.InstagramSerializer