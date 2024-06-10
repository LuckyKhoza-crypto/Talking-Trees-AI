from django.contrib import admin
from .models import trees_Database as Tree
from .models import Comment
# Register your models here.
admin.site.register(Tree)
admin.site.register(Comment)
