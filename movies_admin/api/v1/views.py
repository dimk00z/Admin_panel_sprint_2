from typing import List
from uuid import UUID

from django.contrib.postgres.aggregates import ArrayAgg
from django.core.paginator import Page, Paginator
from django.db.models import Model, Q
from django.db.models.query import QuerySet
from django.http import Http404, JsonResponse
from django.views.generic.detail import BaseDetailView
from django.views.generic.list import BaseListView
from movies.models import FilmWork


class MoviesApiMixin:
    model: Model = FilmWork
    http_method_names: List[str] = ["get"]

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
    paginate_by: int = 50
    ordering: str = "title"

    def get_context_data(self, *, object_list=None, **kwargs):

        context: dict = super().get_context_data()
        paginator: Paginator = context["paginator"]
        page: Page = context["page_obj"]
        paginated_films: QuerySet = context["page_obj"]
        result: dict = {
            "count": paginator.count,
            "total_pages": paginator.num_pages,
            "prev": page.previous_page_number() if page.has_previous() else None,
            "next": page.next_page_number() if page.has_next() else None,
            "results": list(paginated_films),
        }
        return result


class MoviesDetailApi(MoviesApiMixin, BaseDetailView):
    def get_object(self, queryset=None):
        filmwork_id: UUID = self.kwargs["pk"]
        try:
            return self.get_queryset().filter(id=filmwork_id).get()
        except FilmWork.DoesNotExist:
            raise Http404(f"No film with id={filmwork_id} ")

    def get_context_data(self, **kwargs):
        if self.object:
            return self.object
