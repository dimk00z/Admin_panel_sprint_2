from django.contrib.postgres.aggregates import ArrayAgg
from django.core.paginator import Paginator, Page
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic.list import BaseListView
from django.views.generic.detail import BaseDetailView
from django.db.models.query import QuerySet
from django.core import serializers

from movies.models import FilmWork


class MoviesApiMixin:
    model = FilmWork
    http_method_names = ["get"]

    def get_queryset(self):
        films: QuerySet = FilmWork.objects.prefetch_related(
            "persons", "film_genres"
        ).annotate(
            genres=ArrayAgg("film_genres__genre__name", distinct=True),
            actors=ArrayAgg(
                "persons__person__full_name",
                filter=Q(persons__role__exact="actor"),
                distinct=True,
            ),
            directors=ArrayAgg(
                "persons__person__full_name",
                filter=Q(persons__role__exact="director"),
                distinct=True,
            ),
            writers=ArrayAgg(
                "persons__person__full_name",
                filter=Q(persons__role__exact="writer"),
                distinct=True,
            ),
        )
        return films.values()

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context, safe=False)


class MoviesList(MoviesApiMixin, BaseListView):
    paginate_by = 50
    ordering = "title"

    def get_context_data(self, *, object_list=None, **kwargs):

        context = super().get_context_data()
        paginator: Paginator = context["paginator"]
        page: Page = context["page_obj"]
        paginated_films: QuerySet = context["page_obj"]
        result = {
            "count": paginator.count,
            "total_pages": paginator.num_pages,
            "prev": page.previous_page_number() if page.has_previous() else None,
            "next": page.next_page_number() if page.has_next() else None,
            "results": list(paginated_films),
        }
        return result


class MoviesDetailApi(MoviesApiMixin, BaseDetailView):
    def get_context_data(self, **kwargs):
        return  # Словарь с данными объекта
