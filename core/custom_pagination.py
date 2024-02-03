from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    page_size_query_param = 'pageSize'  # Customize the query parameter for page size
    page_size = 10  # Default page size
    max_page_size = 100  # Maximum page size