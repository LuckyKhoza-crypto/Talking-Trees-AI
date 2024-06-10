import django_filters
from django_filters import ChoiceFilter
from .models import *
from django import forms

# this is the filter class that will be used to filter the trees in the database for the advanced search


class TreeFilter(django_filters.FilterSet):
    # common_name = django_filters.CharFilter(required=True)

    LEAF_FALL_CHOICES = [
    ('Deciduous', 'Deciduous'),
    ('Evergreen', 'Evergreen'),
    ('Coniferous', 'Coniferous'),
    ('Broadleaf', 'Broadleaf')

    ]

    FAMILY_CHOICES = [
    ('Magnoliaceae', 'Magnoliaceae'),
    ('Betulaceae', 'Betulaceae'),
    ('Fagaceae', 'Fagaceae'),
    ('Sapindaceae', 'Sapindaceae'),
    ('Pinaceae', 'Pinaceae'),
    ('Ulmaceae', 'Ulmaceae'),
    ('Cupressaceae', 'Cupressaceae'),
    ('Platanaceae', 'Platanaceae'),
    ('Fabaceae', 'Fabaceae'),
    ('Salicaceae', 'Salicaceae'),
    ('Oleaceae', 'Oleaceae'),
    ('Tiliaceae', 'Tiliaceae'),
    ('Altingiaceae', 'Altingiaceae'),
    ('Simaroubaceae', 'Simaroubaceae'),
    ('Juglandaceae', 'Juglandaceae'),
    ('Moraceae', 'Moraceae'),
    ('Bignoniaceae', 'Bignoniaceae'),
    ('Ginkgoaceae', 'Ginkgoaceae'),
    ('Cannabaceae', 'Cannabaceae'),
    ('Rosaceae', 'Rosaceae'),
    ('Hamamelidaceae', 'Hamamelidaceae'),
    ('Cornaceae', 'Cornaceae'),
    ('Taxaceae', 'Taxaceae'),
    ('Aquifoliaceae', 'Aquifoliaceae'),
    ('Araliaceae', 'Araliaceae'),
    ('Paulowniaceae', 'Paulowniaceae'),
    ('Caprifoliaceae', 'Caprifoliaceae'),
    ('Anacardiaceae', 'Anacardiaceae'),
    ('Cercidiphyllaceae', 'Cercidiphyllaceae')]


    leaf_fall = django_filters.ChoiceFilter(choices = LEAF_FALL_CHOICES, required=False, label='Leaf Fall')
    family_name = django_filters.ChoiceFilter(choices = FAMILY_CHOICES, required=False, label='Family Name')
    
    class Meta:
        # we are building for the trees_Database model
        
        model = trees_Database
        fields = ['tree_id', 'group_name', 'leaf_fall',
                  'common_name', 'species_name', 'genus', 'family_name']
