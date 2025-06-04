from django.core.cache import cache

class CacheMixin:
    def set_get_cache(self, query, cache_name, cache_time):
        data = cache.get(cache_name)

        if data is None:
            data = list(query)  # Выполняем запрос и кэшируем результат
            cache.set(cache_name, data, cache_time)

        return data
