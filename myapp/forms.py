from .models import *
from django import forms


# this class is for basic search

class TreeSearchForm(forms.Form):
    tree_id = forms.CharField(label='Tree ID', max_length=5)


class CommentForm(forms.ModelForm):

    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    content = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Comment
        fields = ['name', 'email', 'content']
