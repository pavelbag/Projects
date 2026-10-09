from .models import (
    Author,
    Post,
)
from django import forms
from django_filters import (
    CharFilter,
    ChoiceFilter,
    DateFilter,
    FilterSet,
)

class PostsFilterForm(forms.ModelForm):
    class Meta:
        model = Post

        fields = [
            'title',
            'author',
            'date',
        ]

        labels = {
            'title': 'Заголовок',
            'author': 'Автор',
            'date': 'Дата',
        }

        querysets = {
            'author': Author.objects.all(),
        }

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'author': forms.Select(attrs={
                'class': 'form-select',
            }),
            'date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.Meta.fields:
            if field not in self.Meta.querysets:
                self.fields[field].label = self.Meta.labels[field]
                self.fields[field].widget = self.Meta.widgets[field]
            else:
                self.fields[field] = forms.ModelChoiceField(
                    empty_label=' ',
                    queryset=self.Meta.querysets[field],
                    label=self.Meta.labels[field],
                    required=False,
                    widget=self.Meta.widgets[field],
                )


class PostsFilter(FilterSet):
    author = ChoiceFilter(lookup_expr='exact')
    date = DateFilter(lookup_expr='gt')
    title = CharFilter(lookup_expr='icontains')

    class Meta:
        model = Post

        fields = [
            'author',
            'date',
            'title',
        ]

        form = PostsFilterForm