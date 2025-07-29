# advertisements/pagination.py
from rest_framework.pagination import PageNumberPagination
from urllib.parse import urlparse, urlunparse, parse_qs, urlencode


class StrictPageNumberPagination(PageNumberPagination):
    page_size = 4
    page_query_param = 'page'

    def _clean_query_params(self, url):
        if not url:
            return url

        parsed = urlparse(url)
        query_dict = parse_qs(parsed.query, keep_blank_values=True)

        # Нормализуем все параметры (удаляем пробелы)
        clean_params = {}
        for key, value in query_dict.items():
            clean_key = key.strip()
            clean_params[clean_key] = [v.strip() if v else v for v in value]

        # Перестраиваем URL
        new_query = urlencode(clean_params, doseq=True)
        return urlunparse(parsed._replace(query=new_query))

    def get_next_link(self):
        url = super().get_next_link()
        return self._clean_query_params(url)

    def get_previous_link(self):
        url = super().get_previous_link()
        return self._clean_query_params(url)