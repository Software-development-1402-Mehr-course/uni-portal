from django import forms

from .models import Author, Subject


class BookSearchForm(forms.Form):
    search_phrase = forms.CharField(required=False, widget=forms.HiddenInput)
    name = forms.CharField(required=False)
    authors = forms.CharField(required=False)
    publish_year_from = forms.IntegerField(required=False)
    publish_year_to = forms.IntegerField(required=False)
    subjects = forms.ModelMultipleChoiceField(Subject.objects.all())

    def author_names(self):
        return Author.objects.all().values_list("name", flat=True)
