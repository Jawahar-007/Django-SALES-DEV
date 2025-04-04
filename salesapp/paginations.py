from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class CustomPagination(PageNumberPagination):
    page_size = 3
    page_query_param = 'pagenum'
    page_size_query_param = 'size'
    max_page_size = 5

    def get_paginated_response(self, data):
        return Response({
            'next': self.get_next_link(),
            'previous':self.get_previous_link(),
            'count': self.page.paginator.count,
            'size': self.page_size,
            'results': data
        })