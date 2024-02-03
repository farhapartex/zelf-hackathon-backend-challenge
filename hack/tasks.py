from time import sleep
import requests
import logging
from django.conf import settings
from django.db import transaction
from celery import shared_task
from hack.models import SocialContent, Author
from hack.service import fetch_contenet, get_or_create_author, save_content_data

logger = logging.getLogger(__name__)

# celery -A core worker -l info

    
    
@shared_task
def fetch_social_content_task():
    page = 1
    
    while page:
        logger.info(f"Fetching page: {page}")
        data_list, next_page = fetch_contenet(page)
        
        for data in data_list:
            author, _ = get_or_create_author(data.get("author")) # get author object
            save_content_data(data, author) # save social content data
        
        if next_page is None:
            next_page = 1
            logger.info("Sleeping for 5 seconds")
            sleep(5)
            
        page = next_page
        sleep(1)


@shared_task
def fetch_author_details():
    """
    Take first 20 un fetched author details.
    Fetch one by one.
    Take a sleep
    Start again
    """
    
    while True:
        authors = Author.objects.filter(is_fetched=False)[:20]
        if len(authors) == 0:
            logger.info(" No author found, wait 5 seconds for new unfetched author")
            sleep(5)
            continue
        
        for author in authors:
            url = f"https://hackapi.hellozelf.com/backend/api/v1/authors/{author.unique_id}"
        
            try:
                response = requests.get(
                        url=url, 
                        headers={"x-api-key": settings.HACK_API_KEY}
                    )
                
                # get json data
                if response.status_code == 200:
                    res_data = response.json()
                    if len(res_data["data"]) == 0:
                        continue
                    
                    data = res_data["data"][0]
                    logger.info(f"Fetching author: {author.unique_id}")
                    
                    author.unique_uuid = data["unique_uuid"]
                    author.name = data["info"]["name"]
                    author.platform = data["info"]["platform"]
                    author.is_fetched = True
                    author.data = data
                    author.save()
            except Exception as e:
                logger.critical("Fetch author exception: ", str(e))
            
        