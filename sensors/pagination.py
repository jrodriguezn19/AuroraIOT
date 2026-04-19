from rest_framework.pagination import CursorPagination


class SensorDataCursorPagination(CursorPagination):
    ordering = '-time'
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000
