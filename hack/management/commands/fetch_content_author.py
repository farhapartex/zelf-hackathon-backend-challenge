from django.core.management.base import BaseCommand, CommandError
from hack.models import SocialContent, Author
from hack.tasks import fetch_social_content_task, fetch_author_details


class Command(BaseCommand):

    def handle(self, *args, **options):
        fetch_social_content_task.delay()
        
        fetch_author_details.delay()