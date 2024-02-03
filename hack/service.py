import requests
from django.conf import settings
from django.db import transaction
from hack.models import SocialContent, Author
import logging

logger = logging.getLogger(__name__)

def fetch_contenet(page):
    """
    Fetch data from hack api
    Return data if status is 200
    Else return empty dict.
    If status is not 200, next page will be None
    """
    url = f"https://hackapi.hellozelf.com/backend/api/v1/contents?page={page}"
    
    try:
        response = requests.get(
                url=url, 
                headers={"x-api-key": settings.HACK_API_KEY}
            )
        
        # get json data
        if response.status_code == 200:
            data = response.json()
            page = data.get("next", None)
            return data.get("data", []), page
    except Exception as e:
        logger.critical("Fetch content exception: ", str(e))
        page = None
    
    return [], page


def get_or_create_author(data):
    """
    Get or create author
    """
    author, created = Author.objects.get_or_create(
        unique_id=data.get("id"),
        username=data.get("username")
    )
    
    return author, created


def save_content_data(data, author):
    """
    Save content data to SocialContent model
    """
    
    try:
        social_content = SocialContent.objects.filter(unique_id=data.get("unique_id")).first()
        if social_content:
            return
        
        # prepare the payload for Social Content
        digg_counts = data.get("stats", {}).get("digg_counts", {})
        payload = {
            "unique_id": data.get("unique_id"),
            "main_text": data.get("context", {}).get("main_text", ""),
            "data": data,
            "author": author,
            "platform": data.get("origin_details", {}).get("origin_platform"),
            "media_type": data.get("media", {}).get("media_type"),
            "likes": digg_counts.get("likes", {}).get("count", 0),
            "views": digg_counts.get("views", {}).get("count", 0),
            "comments": digg_counts.get("comments", {}).get("count", 0),
            "created_at": data.get("creation_info", {}).get("created_at"),
        }
        
        with transaction.atomic():
            SocialContent.objects.create(**payload)
            logger.info(f"{data.get('unique_id')} saved successfully")
    except Exception as e:
        logger.critical(f"Save content data exception: {str(e)}")
        return