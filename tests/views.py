from django.shortcuts import render

from .forms import ExampleForm


def example_form(request):
    form = ExampleForm()

    return render(request, "example_form.html", {"form": form})
