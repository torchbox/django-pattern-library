from django import forms


class ExampleForm(forms.Form):
    single_line_text = forms.CharField(
        max_length=255, help_text="This is some help text"
    )
    choices = (("one", "One"), ("two", "Two"), ("three", "Three"), ("four", "Four"))
    select = forms.ChoiceField(choices=choices)
