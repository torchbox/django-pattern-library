from pattern_library import register_context_modifier
from .forms import ExampleForm


@register_context_modifier
def add_common_forms(context, request):
    context['form'] = ExampleForm()

@register_context_modifier(template='patterns/molecules/field/field.html')
def add_field(context, request):
    form = ExampleForm()
    context['field'] = form['single_line_text']
