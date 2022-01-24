from django.core.paginator import Paginator

from pattern_library import register_context_modifier

from .forms import ExampleForm


@register_context_modifier
def add_common_forms(context, request):
    context["form"] = ExampleForm()


@register_context_modifier(template="patterns/molecules/field/field.html")
def add_field(context, request):
    form = ExampleForm()
    context["field"] = form["single_line_text"]


@register_context_modifier(template="patterns/pages/search/search.html")
def replicate_pagination(context, request):
    """
    Replace lists of items using the 'page_obj.object_list' key
    with a real Paginator page, and add a few other pagination-related
    things to the context (like Django's `ListView` does).
    """
    object_list = context.pop("search_results", None)
    if object_list is None:
        return

    original_length = len(object_list)

    # add dummy items to force pagination
    for i in range(50):
        object_list.append(None)

    # paginate and add ListView-like values
    paginator = Paginator(object_list, original_length)
    context.update(
        paginator=paginator,
        search_results=paginator.page(10),
        is_paginated=True,
        object_list=object_list,
    )
