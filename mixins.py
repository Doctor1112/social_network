from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth import get_user_model

User = get_user_model()


class OwnerRequiredMixin(UserPassesTestMixin):
    def test_func(self) -> bool | None:
        return self.request.user == self.get_object().author


class UserPrefetchRelatedrMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = (
            User.objects
            .prefetch_related("sended_requests", "received_requests", "friends")
            .filter(pk=self.request.user.pk)
            .first()
        )
        return context


class PaginateMixin:
    paginate_by = 5

    def paginate_data(self):
        page_number = self.request.GET.get("page")
        qs = self.get_paginate_queryset()
        paginator = Paginator(qs, self.paginate_by)

        try:
            page_obj = paginator.page(page_number)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)

        return page_obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page_obj = self.paginate_data()

        context["page_obj"] = page_obj
        return context

    def get_paginate_queryset(self):
        return self.get_queryset()
